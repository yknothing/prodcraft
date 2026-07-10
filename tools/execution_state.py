from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO, Iterable, Iterator


AUTHORITY_STRUCTURAL = "structurally-valid-only"
AUTHORITY_GATE = "gate-authorized"
AUTHORITY_TERMINAL = "terminal-authorized"

MAX_SAFE_JSON_INTEGER = 9_007_199_254_740_991
WORKTREE_ALGORITHM_ID = "git-worktree-content-v1"
WORKTREE_SCOPE_POLICY_ID = "repo-worktree-excluding-bound-control-v1"
GIT_COMMAND_TIMEOUT_SECONDS = 300
STRICT_JSON_MAX_BYTES = 16 * 1024 * 1024
FILE_HASH_CHUNK_BYTES = 1024 * 1024


class StrictJSONError(ValueError):
    pass


class WorktreeSnapshotError(RuntimeError):
    pass


@dataclass(frozen=True)
class AuthorityContext:
    repo_root: Path
    control_root: Path
    canonical_state_path: Path


LIFECYCLE_TRANSITIONS = {
    ("received", "routed"),
    ("routed", "gated"),
    ("gated", "executing"),
    ("executing", "blocked"),
    ("executing", "completion_claimed"),
    ("executing", "rerouted"),
    ("blocked", "executing"),
    ("blocked", "rerouted"),
    ("completion_claimed", "verified"),
    ("completion_claimed", "rejected"),
    ("rejected", "gated"),
    ("rejected", "rerouted"),
    ("verified", "completed"),
}


@dataclass(frozen=True)
class ValidationResult:
    authority: str
    errors: list[str]
    candidate_completion_digest: str | None = None


def resolve_authority_context(
    state_path: Path, state: dict[str, Any]
) -> tuple[AuthorityContext | None, list[str]]:
    """Locate the Git root and enforce the unique current-state selector."""

    errors: list[str] = []
    work_id = state.get("work_id")
    if not isinstance(work_id, str) or not work_id:
        return None, ["execution state work_id must be a non-empty string"]
    try:
        supplied = state_path.absolute()
        state_stat = supplied.lstat()
    except OSError as exc:
        return None, [f"execution state path cannot be inspected: {exc}"]
    if stat.S_ISLNK(state_stat.st_mode):
        errors.append("canonical current execution-state must not be a symlink")
    elif not stat.S_ISREG(state_stat.st_mode):
        errors.append("canonical current execution-state must be a regular file")

    try:
        declared_root = _run_git(
            supplied.parent,
            "rev-parse",
            "--show-toplevel",
        ).stdout.strip()
        repo_root = Path(os.fsdecode(declared_root)).resolve(strict=True)
    except (OSError, UnicodeError, WorktreeSnapshotError) as exc:
        return None, [*errors, f"execution state is not inside a readable Git worktree: {exc}"]

    control_root = repo_root / ".prodcraft" / "artifacts" / work_id
    canonical_state_path = control_root / "execution-state.json"
    try:
        supplied_canonical = supplied.resolve(strict=True)
    except OSError as exc:
        errors.append(f"execution state path cannot be canonicalized: {exc}")
        supplied_canonical = supplied
    if supplied_canonical != canonical_state_path:
        errors.append(
            "authority mode requires the canonical current execution-state path "
            f"{canonical_state_path}"
        )

    try:
        relative = canonical_state_path.relative_to(repo_root)
    except ValueError:
        errors.append("canonical current execution-state escapes the Git root")
    else:
        current = repo_root
        for component in relative.parts:
            current = current / component
            try:
                component_stat = current.lstat()
            except OSError as exc:
                errors.append(f"canonical control path component cannot be inspected: {current}: {exc}")
                break
            if stat.S_ISLNK(component_stat.st_mode):
                errors.append(f"canonical control path contains a symlink component: {current}")
                break

    return AuthorityContext(repo_root, control_root, canonical_state_path), errors


def _strict_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for key, value in pairs:
        if key in payload:
            raise StrictJSONError(f"duplicate JSON key: {key}")
        if not key.isascii():
            raise StrictJSONError(f"JSON object member names must be ASCII: {key!r}")
        payload[key] = value
    return payload


def _strict_json_int(value: str) -> int:
    if value == "-0":
        raise StrictJSONError("JSON negative zero is forbidden")
    parsed = int(value)
    if not -MAX_SAFE_JSON_INTEGER <= parsed <= MAX_SAFE_JSON_INTEGER:
        raise StrictJSONError(f"JSON integer is outside the supported range: {value}")
    return parsed


def _reject_json_number(value: str) -> Any:
    raise StrictJSONError(f"JSON floats and non-finite numbers are forbidden: {value}")


@contextmanager
def _open_regular_file(path: Path) -> Iterator[tuple[BinaryIO, os.stat_result]]:
    """Open one stable non-symlink regular-file descriptor."""

    descriptor = -1
    try:
        entry_stat = path.lstat()
        if stat.S_ISLNK(entry_stat.st_mode):
            raise ValueError(f"content-bound path must not be a symlink: {path}")
        if not stat.S_ISREG(entry_stat.st_mode):
            raise ValueError(f"content-bound path must be a regular file: {path}")
        flags = (
            os.O_RDONLY
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_NONBLOCK", 0)
        )
        descriptor = os.open(path, flags)
        opened_stat = os.fstat(descriptor)
        if not stat.S_ISREG(opened_stat.st_mode):
            raise ValueError(f"content-bound path must be a regular file: {path}")
        if (entry_stat.st_dev, entry_stat.st_ino) != (
            opened_stat.st_dev,
            opened_stat.st_ino,
        ):
            raise ValueError(f"content-bound path changed while being opened: {path}")
        with os.fdopen(descriptor, "rb", closefd=True) as handle:
            descriptor = -1
            yield handle, opened_stat
            final_stat = os.fstat(handle.fileno())
            opened_identity = (
                opened_stat.st_dev,
                opened_stat.st_ino,
                opened_stat.st_size,
                opened_stat.st_mtime_ns,
                opened_stat.st_ctime_ns,
            )
            final_identity = (
                final_stat.st_dev,
                final_stat.st_ino,
                final_stat.st_size,
                final_stat.st_mtime_ns,
                final_stat.st_ctime_ns,
            )
            if opened_identity != final_identity:
                raise ValueError(f"content-bound path changed while being read: {path}")
    except ValueError:
        raise
    except OSError as exc:
        raise ValueError(f"failed to read content-bound file {path}: {exc}") from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _read_regular_file_bytes(
    path: Path,
    *,
    max_bytes: int | None = None,
) -> bytes:
    """Read one bounded regular-file snapshot through a safe descriptor."""

    limit = STRICT_JSON_MAX_BYTES if max_bytes is None else max_bytes
    with _open_regular_file(path) as (handle, opened_stat):
        if opened_stat.st_size > limit:
            raise ValueError(
                f"content-bound file exceeds {limit} bytes: {path}"
            )
        content = handle.read(limit + 1)
        if len(content) > limit:
            raise ValueError(
                f"content-bound file exceeds {limit} bytes: {path}"
            )
        if len(content) != opened_stat.st_size:
            raise ValueError(f"content-bound path changed while being read: {path}")
        return content


def _parse_strict_json_bytes(content: bytes, path: Path) -> dict[str, Any]:
    try:
        text = content.decode("utf-8")
    except UnicodeError as exc:
        raise StrictJSONError(f"failed to decode strict JSON {path}: {exc}") from exc
    try:
        payload = json.loads(
            text,
            object_pairs_hook=_strict_json_object,
            parse_int=_strict_json_int,
            parse_float=_reject_json_number,
            parse_constant=_reject_json_number,
        )
    except StrictJSONError:
        raise
    except (json.JSONDecodeError, UnicodeError, RecursionError, ValueError) as exc:
        raise StrictJSONError(f"failed to parse strict JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise StrictJSONError(f"strict JSON root must be an object: {path}")
    try:
        _validate_unicode_scalars(payload, error_type=StrictJSONError)
    except RecursionError as exc:
        raise StrictJSONError(f"strict JSON nesting is too deep: {path}") from exc
    return payload


def load_strict_json_with_digest(path: Path) -> tuple[dict[str, Any], str]:
    """Load and hash the exact same strict-JSON byte snapshot."""

    try:
        content = _read_regular_file_bytes(path)
    except ValueError as exc:
        raise StrictJSONError(f"failed to read strict JSON {path}: {exc}") from exc
    payload = _parse_strict_json_bytes(content, path)
    digest = "sha256:" + hashlib.sha256(content).hexdigest()
    return payload, digest


def load_strict_json(path: Path) -> dict[str, Any]:
    """Load duplicate-free, portable JSON used by strict protocol artifacts."""

    payload, _digest = load_strict_json_with_digest(path)
    return payload


def _validate_unicode_scalars(
    value: Any,
    *,
    error_type: type[ValueError] = ValueError,
    path: str = "$",
) -> None:
    if isinstance(value, str):
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise error_type(f"JSON string contains an unpaired surrogate at {path}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_unicode_scalars(item, error_type=error_type, path=f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            _validate_unicode_scalars(key, error_type=error_type, path=f"{path}.<key>")
            _validate_unicode_scalars(item, error_type=error_type, path=f"{path}.{key}")


_URI_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:")


def resolve_control_ref(control_root: Path, ref: str) -> Path:
    """Resolve one strict local ref without following any symlink component."""

    if not isinstance(ref, str) or not ref:
        raise ValueError("control reference must be a non-empty string")
    if "\x00" in ref:
        raise ValueError("control reference contains a NUL byte")
    if "\\" in ref:
        raise ValueError("control reference must use POSIX separators")
    if ref.startswith("/") or ref.startswith("//"):
        raise ValueError("control reference must be relative")
    if _WINDOWS_DRIVE_RE.match(ref):
        raise ValueError("control reference must not use a Windows drive prefix")
    if _URI_SCHEME_RE.match(ref):
        raise ValueError("control reference must not use a URI scheme")
    if any(segment in {"", ".", ".."} for segment in ref.split("/")):
        raise ValueError("control reference contains a forbidden path segment")

    pure = PurePosixPath(ref)

    root = control_root.absolute()
    try:
        root_stat = root.lstat()
    except OSError as exc:
        raise ValueError(f"control root is not readable: {exc}") from exc
    if stat.S_ISLNK(root_stat.st_mode):
        raise ValueError("control root must not be a symlink")
    if not stat.S_ISDIR(root_stat.st_mode):
        raise ValueError("control root must be a directory")

    candidate = root
    for index, part in enumerate(pure.parts):
        candidate = candidate / part
        try:
            entry_stat = candidate.lstat()
        except OSError as exc:
            raise ValueError(f"control reference does not resolve to a readable file: {ref}: {exc}") from exc
        if stat.S_ISLNK(entry_stat.st_mode):
            raise ValueError(f"control reference contains a symlink component: {ref}")
        if index < len(pure.parts) - 1 and not stat.S_ISDIR(entry_stat.st_mode):
            raise ValueError(f"control reference intermediate component is not a directory: {ref}")
    if not stat.S_ISREG(candidate.lstat().st_mode):
        raise ValueError(f"control reference target must be a regular file: {ref}")

    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"control reference escapes the control root: {ref}") from exc
    return candidate


def _run_git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith("GIT_")
    }
    environment.update(
        {
            "GIT_ATTR_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_PAGER": "cat",
            "GIT_TERMINAL_PROMPT": "0",
            "LC_ALL": "C",
        }
    )
    command = [
        "git",
        "-c",
        "core.fsmonitor=false",
        "-c",
        "core.untrackedCache=false",
        "-c",
        "core.fileMode=true",
        "-c",
        "core.ignoreStat=false",
        "-c",
        "core.ignoreCase=false",
        "-c",
        "core.precomposeUnicode=true",
        "-c",
        "core.trustctime=true",
        "-c",
        "core.checkStat=default",
        "-c",
        f"core.excludesFile={os.devnull}",
        "-c",
        "core.quotepath=false",
        *args,
    ]
    try:
        return subprocess.run(
            command,
            cwd=repo_root,
            check=check,
            capture_output=True,
            env=environment,
            timeout=GIT_COMMAND_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise WorktreeSnapshotError(
            f"Git command timed out after {GIT_COMMAND_TIMEOUT_SECONDS} seconds: "
            f"{' '.join(command)}"
        ) from exc
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = ""
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            detail = f": {exc.stderr.decode('utf-8', errors='replace').strip()}"
        raise WorktreeSnapshotError(f"Git command failed: {' '.join(command)}{detail}") from exc


def _decode_git_path(raw: bytes) -> str:
    try:
        value = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise WorktreeSnapshotError("Git worktree paths must be valid UTF-8") from exc
    if not value or value.startswith("/") or "\x00" in value:
        raise WorktreeSnapshotError(f"Git returned an invalid worktree path: {value!r}")
    return value


def _relative_control_path(repo_root: Path, control_root: Path) -> str:
    root = repo_root.absolute()
    control = control_root.absolute()
    try:
        relative = control.relative_to(root)
    except ValueError as exc:
        raise WorktreeSnapshotError("excluded control root must be inside the Git root") from exc
    if relative == Path("."):
        raise WorktreeSnapshotError("the Git root itself cannot be excluded as a control root")
    return relative.as_posix().rstrip("/")


def _is_control_path(path: str, control_relative: str) -> bool:
    return path == control_relative or path.startswith(control_relative + "/")


def _tracked_entries(repo_root: Path) -> dict[str, tuple[str, str]]:
    output = _run_git(repo_root, "ls-files", "-z", "--stage").stdout
    entries: dict[str, tuple[str, str]] = {}
    for raw_record in output.split(b"\0"):
        if not raw_record:
            continue
        try:
            metadata, raw_path = raw_record.split(b"\t", 1)
            mode_raw, oid_raw, stage_raw = metadata.split(b" ", 2)
        except ValueError as exc:
            raise WorktreeSnapshotError("Git returned malformed ls-files --stage output") from exc
        path = _decode_git_path(raw_path)
        if stage_raw != b"0":
            raise WorktreeSnapshotError(f"unmerged index entry is not snapshot-safe: {path}")
        if path in entries:
            raise WorktreeSnapshotError(f"duplicate tracked path returned by Git: {path}")
        entries[path] = (mode_raw.decode("ascii"), oid_raw.decode("ascii"))
    return entries


def _untracked_entries(repo_root: Path, *, include_ignored: bool = False) -> set[str]:
    args = ["ls-files", "-z", "--others"]
    if not include_ignored:
        args.append("--exclude-standard")
    output = _run_git(repo_root, *args).stdout
    return {_decode_git_path(raw_path) for raw_path in output.split(b"\0") if raw_path}


def _other_control_entries(repo_root: Path, control_relative: str) -> set[str]:
    """Keep other work-item roots governed even when `.prodcraft/` is ignored."""

    artifacts_root = repo_root / ".prodcraft" / "artifacts"
    if not artifacts_root.exists():
        return set()
    current_control = repo_root / PurePosixPath(control_relative)
    entries: set[str] = set()
    def raise_walk_error(exc: OSError) -> None:
        raise WorktreeSnapshotError(f"cannot enumerate reserved control roots: {exc}")

    for current, dirnames, filenames in os.walk(
        artifacts_root,
        topdown=True,
        followlinks=False,
        onerror=raise_walk_error,
    ):
        current_path = Path(current)
        if current_path == current_control or current_control in current_path.parents:
            dirnames[:] = []
            continue
        retained: list[str] = []
        for dirname in dirnames:
            candidate = current_path / dirname
            if candidate == current_control:
                continue
            try:
                candidate_stat = candidate.lstat()
            except OSError as exc:
                raise WorktreeSnapshotError(
                    f"cannot inspect reserved control path {candidate}: {exc}"
                ) from exc
            if stat.S_ISLNK(candidate_stat.st_mode):
                entries.add(candidate.relative_to(repo_root).as_posix())
            else:
                retained.append(dirname)
        dirnames[:] = retained
        entries.update(
            (current_path / filename).relative_to(repo_root).as_posix()
            for filename in filenames
        )
    return entries


def _validate_ignore_policy(
    repo_root: Path,
    tracked: dict[str, tuple[str, str]],
    control_relative: str,
) -> None:
    git_path = _run_git(repo_root, "rev-parse", "--git-path", "info/exclude").stdout.strip()
    if git_path:
        info_exclude = Path(os.fsdecode(git_path))
        if not info_exclude.is_absolute():
            info_exclude = repo_root / info_exclude
        try:
            exclude_stat = info_exclude.lstat()
        except FileNotFoundError:
            exclude_stat = None
        except OSError as exc:
            raise WorktreeSnapshotError(f"cannot inspect .git/info/exclude: {exc}") from exc
        if exclude_stat is not None:
            if stat.S_ISLNK(exclude_stat.st_mode) or not stat.S_ISREG(exclude_stat.st_mode):
                raise WorktreeSnapshotError(
                    ".git/info/exclude must be a regular non-symlink file"
                )
            try:
                lines = info_exclude.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeError) as exc:
                raise WorktreeSnapshotError(f"cannot read .git/info/exclude: {exc}") from exc
            if any(line.strip() and not line.lstrip().startswith("#") for line in lines):
                raise WorktreeSnapshotError(".git/info/exclude contains a non-comment rule")

    control_abs = repo_root / PurePosixPath(control_relative)
    def raise_walk_error(exc: OSError) -> None:
        raise WorktreeSnapshotError(f"cannot enumerate governed worktree: {exc}")

    for current, dirnames, filenames in os.walk(
        repo_root,
        topdown=True,
        followlinks=False,
        onerror=raise_walk_error,
    ):
        current_path = Path(current)
        dirnames[:] = [name for name in dirnames if name != ".git"]
        dirnames[:] = [
            name
            for name in dirnames
            if not (
                (current_path / name) == control_abs
                or control_abs in (current_path / name).parents
            )
        ]
        if ".gitignore" not in filenames:
            pass
        else:
            ignore_path = current_path / ".gitignore"
            relative = ignore_path.relative_to(repo_root).as_posix()
            if relative not in tracked:
                raise WorktreeSnapshotError(f"untracked .gitignore is not allowed: {relative}")

        for filename in filenames:
            candidate = current_path / filename
            try:
                candidate_stat = candidate.lstat()
            except OSError as exc:
                raise WorktreeSnapshotError(f"cannot inspect worktree path {candidate}: {exc}") from exc
            if stat.S_ISREG(candidate_stat.st_mode) or stat.S_ISLNK(candidate_stat.st_mode):
                continue
            relative = candidate.relative_to(repo_root).as_posix()
            ignored = _run_git(repo_root, "check-ignore", "-q", "--", relative, check=False)
            if ignored.returncode != 0:
                raise WorktreeSnapshotError(f"unsupported special file in governed worktree: {relative}")


def _validate_git_index_path(repo_root: Path) -> None:
    index_path_raw = _run_git(repo_root, "rev-parse", "--git-path", "index").stdout.strip()
    if not index_path_raw:
        return
    index_path = Path(os.fsdecode(index_path_raw))
    if not index_path.is_absolute():
        index_path = repo_root / index_path
    try:
        index_stat = index_path.lstat()
    except FileNotFoundError:
        return
    except OSError as exc:
        raise WorktreeSnapshotError(f"cannot inspect Git index: {exc}") from exc
    if stat.S_ISLNK(index_stat.st_mode) or not stat.S_ISREG(index_stat.st_mode):
        raise WorktreeSnapshotError("Git index must be a regular non-symlink file")


def _head_entries(repo_root: Path, control_relative: str) -> dict[str, tuple[str, str]]:
    output = _run_git(
        repo_root,
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        "HEAD",
    ).stdout
    entries: dict[str, tuple[str, str]] = {}
    for raw_record in output.split(b"\0"):
        if not raw_record:
            continue
        try:
            metadata, raw_path = raw_record.split(b"\t", 1)
            mode_raw, _type_raw, oid_raw = metadata.split(b" ", 2)
        except ValueError as exc:
            raise WorktreeSnapshotError("Git returned malformed ls-tree output") from exc
        path = _decode_git_path(raw_path)
        if not _is_control_path(path, control_relative):
            entries[path] = (mode_raw.decode("ascii"), oid_raw.decode("ascii"))
    return entries


def _validate_index_worktree_consistency(
    index_entries: dict[str, tuple[str, str]],
    head_entries: dict[str, tuple[str, str]],
    current_entries: dict[str, tuple[str, str]],
) -> None:
    """Reject staged content that is neither HEAD nor the verified worktree bytes."""

    for path in sorted(set(index_entries) | set(head_entries)):
        index_entry = index_entries.get(path)
        head_entry = head_entries.get(path)
        if index_entry != head_entry and index_entry != current_entries.get(path):
            raise WorktreeSnapshotError(
                f"Git index entry differs from both HEAD and governed worktree content: {path}"
            )


def _blob_oid(content: bytes, object_format: str) -> str:
    if object_format not in {"sha1", "sha256"}:
        raise WorktreeSnapshotError(f"unsupported Git object format: {object_format}")
    digest = hashlib.new(object_format)
    digest.update(f"blob {len(content)}\0".encode("ascii"))
    digest.update(content)
    return digest.hexdigest()


def _update_length_delimited(digest: Any, value: bytes) -> None:
    digest.update(len(value).to_bytes(8, byteorder="big", signed=False))
    digest.update(value)


def _update_worktree_entry(
    digest: Any,
    path: str,
    entry_type: bytes,
    mode: bytes,
    content: bytes,
) -> None:
    _update_length_delimited(digest, path.encode("utf-8"))
    _update_length_delimited(digest, entry_type)
    _update_length_delimited(digest, mode)
    _update_length_delimited(digest, content)


def _snapshot_entry(
    repo_root: Path,
    path: str,
    tracked: dict[str, tuple[str, str]],
    digest: Any,
    object_format: str,
) -> tuple[str, str] | None:
    absolute = repo_root / PurePosixPath(path)
    tracked_mode, tracked_oid = tracked.get(path, (None, None))
    current = repo_root
    for component in PurePosixPath(path).parts[:-1]:
        current = current / component
        try:
            component_stat = current.lstat()
        except OSError as exc:
            raise WorktreeSnapshotError(f"cannot inspect worktree path component {current}: {exc}") from exc
        if stat.S_ISLNK(component_stat.st_mode):
            raise WorktreeSnapshotError(f"worktree path contains an intermediate symlink: {path}")
        if not stat.S_ISDIR(component_stat.st_mode):
            raise WorktreeSnapshotError(f"worktree path component is not a directory: {path}")

    try:
        entry_stat = absolute.lstat()
    except FileNotFoundError:
        if tracked_mode == "160000":
            raise WorktreeSnapshotError(f"submodule worktree is not initialized: {path}")
        if tracked_mode is not None:
            return None
        raise WorktreeSnapshotError(f"worktree entry disappeared during capture: {path}")
    except OSError as exc:
        raise WorktreeSnapshotError(f"cannot inspect worktree entry {path}: {exc}") from exc

    if tracked_mode == "160000":
        if not stat.S_ISDIR(entry_stat.st_mode):
            raise WorktreeSnapshotError(f"submodule worktree is not initialized: {path}")
        nested_snapshot = capture_git_worktree(
            absolute,
            excluded_control_root=None,
            captured_at="1970-01-01T00:00:00Z",
        )
        if nested_snapshot["head"] != tracked_oid:
            raise WorktreeSnapshotError(f"submodule HEAD does not match recorded gitlink: {path}")
        if nested_snapshot["status"] != "clean":
            raise WorktreeSnapshotError(f"submodule worktree is dirty: {path}")
        content = nested_snapshot["head"].encode("ascii")
        _update_worktree_entry(digest, path, b"submodule", b"160000", content)
        return "160000", nested_snapshot["head"]

    if stat.S_ISREG(entry_stat.st_mode):
        mode = b"100755" if bool(
            entry_stat.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        ) else b"100644"
        try:
            with _open_regular_file(absolute) as (handle, opened_stat):
                _update_length_delimited(digest, path.encode("utf-8"))
                _update_length_delimited(digest, b"file")
                _update_length_delimited(digest, mode)
                digest.update(
                    opened_stat.st_size.to_bytes(8, byteorder="big", signed=False)
                )
                blob_digest = hashlib.new(object_format)
                blob_digest.update(
                    f"blob {opened_stat.st_size}\0".encode("ascii")
                )
                bytes_read = 0
                while chunk := handle.read(FILE_HASH_CHUNK_BYTES):
                    bytes_read += len(chunk)
                    digest.update(chunk)
                    blob_digest.update(chunk)
                if bytes_read != opened_stat.st_size:
                    raise ValueError(
                        f"content-bound path changed while being read: {absolute}"
                    )
        except (OSError, ValueError) as exc:
            raise WorktreeSnapshotError(f"cannot read worktree file {path}: {exc}") from exc
        return mode.decode("ascii"), blob_digest.hexdigest()
    if stat.S_ISLNK(entry_stat.st_mode):
        try:
            target = os.readlink(absolute)
        except OSError as exc:
            raise WorktreeSnapshotError(f"cannot read worktree symlink {path}: {exc}") from exc
        content = os.fsencode(target)
        _update_worktree_entry(digest, path, b"symlink", b"120000", content)
        return "120000", _blob_oid(content, object_format)
    if stat.S_ISDIR(entry_stat.st_mode):
        raise WorktreeSnapshotError(f"unsupported directory entry outside a submodule: {path}")
    raise WorktreeSnapshotError(f"unsupported special file in governed worktree: {path}")


def capture_git_worktree(
    repo_root: Path,
    *,
    excluded_control_root: Path | None,
    captured_at: str | None = None,
) -> dict[str, Any]:
    """Capture deterministic worktree content without diff/textconv semantics."""

    try:
        root = repo_root.resolve(strict=True)
    except OSError as exc:
        raise WorktreeSnapshotError(f"Git root cannot be canonicalized: {exc}") from exc
    canonical_control_root: Path | None = None
    if excluded_control_root is not None:
        try:
            canonical_control_root = excluded_control_root.resolve(strict=True)
        except OSError as exc:
            raise WorktreeSnapshotError(f"control root cannot be canonicalized: {exc}") from exc
    declared_root = _run_git(root, "rev-parse", "--show-toplevel").stdout.strip()
    try:
        actual_root = Path(os.fsdecode(declared_root)).resolve(strict=True)
    except UnicodeError as exc:
        raise WorktreeSnapshotError("Git root path must be valid UTF-8") from exc
    if actual_root != root:
        raise WorktreeSnapshotError(f"repo_root is not the Git top level: {root}")

    control_relative = (
        _relative_control_path(root, canonical_control_root)
        if canonical_control_root is not None
        else ""
    )
    _validate_git_index_path(root)
    tracked = _tracked_entries(root)
    if canonical_control_root is not None:
        _validate_ignore_policy(root, tracked, control_relative)
    untracked = _untracked_entries(
        root,
        include_ignored=canonical_control_root is None,
    )
    forced_control_entries = (
        _other_control_entries(root, control_relative)
        if canonical_control_root is not None
        else set()
    )
    paths = sorted(
        {
            path
            for path in set(tracked) | untracked | forced_control_entries
            if not _is_control_path(path, control_relative)
        },
        key=lambda value: value.encode("utf-8"),
    )

    digest = hashlib.sha256()
    digest.update(b"git-worktree-content-v1\0")
    try:
        object_format = _run_git(root, "rev-parse", "--show-object-format").stdout.strip().decode("ascii")
    except UnicodeDecodeError as exc:
        raise WorktreeSnapshotError("Git object format must be ASCII") from exc
    if object_format not in {"sha1", "sha256"}:
        raise WorktreeSnapshotError(f"unsupported Git object format: {object_format}")
    current_entries: dict[str, tuple[str, str]] = {}
    for path in paths:
        identity = _snapshot_entry(root, path, tracked, digest, object_format)
        if identity is None:
            continue
        current_entries[path] = identity

    try:
        head = _run_git(root, "rev-parse", "HEAD").stdout.strip().decode("ascii")
    except UnicodeDecodeError as exc:
        raise WorktreeSnapshotError("Git HEAD must be ASCII") from exc
    timestamp = captured_at or datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    head_entries = _head_entries(root, control_relative)
    index_entries = {
        path: identity
        for path, identity in tracked.items()
        if not _is_control_path(path, control_relative)
    }
    _validate_index_worktree_consistency(index_entries, head_entries, current_entries)
    return {
        "algorithm_id": WORKTREE_ALGORITHM_ID,
        "scope_policy_id": WORKTREE_SCOPE_POLICY_ID,
        "head": head,
        "status": "clean" if current_entries == head_entries else "dirty",
        "content_digest": "sha256:" + digest.hexdigest(),
        "captured_at": timestamp,
    }


def canonical_json_bytes(payload: Any) -> bytes:
    """Return the repository's deterministic JSON representation."""

    _validate_canonical_json_value(payload)
    return json.dumps(
        payload,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _validate_canonical_json_value(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, bool):
        return
    if isinstance(value, str):
        _validate_unicode_scalars(value, path=path)
        return
    if isinstance(value, int):
        if not -MAX_SAFE_JSON_INTEGER <= value <= MAX_SAFE_JSON_INTEGER:
            raise ValueError(f"canonical JSON integer is outside the supported range at {path}")
        return
    if isinstance(value, float):
        raise ValueError(f"canonical JSON floats are forbidden at {path}")
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_canonical_json_value(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError(f"canonical JSON object keys must be strings at {path}")
            if not key.isascii():
                raise ValueError(f"canonical JSON object keys must be ASCII at {path}.{key}")
            _validate_canonical_json_value(item, f"{path}.{key}")
        return
    raise ValueError(f"unsupported canonical JSON value at {path}: {type(value).__name__}")


def canonical_json_digest(payload: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def file_sha256(path: Path) -> str:
    try:
        digest = hashlib.sha256()
        with _open_regular_file(path) as (handle, opened_stat):
            bytes_read = 0
            while chunk := handle.read(FILE_HASH_CHUNK_BYTES):
                bytes_read += len(chunk)
                digest.update(chunk)
            if bytes_read != opened_stat.st_size:
                raise ValueError(f"content-bound path changed while being read: {path}")
    except ValueError as exc:
        raise ValueError(f"cannot read content-bound file {path}: {exc}") from exc
    return "sha256:" + digest.hexdigest()


def claim_payload_projection(attempt: dict[str, Any]) -> dict[str, Any]:
    excluded = {
        "claim_digest",
        "completion_basis_digest",
        "terminal_transitions",
        "completion_binding",
    }
    return {key: deepcopy(value) for key, value in attempt.items() if key not in excluded}


def _basis_attempt_projection(attempt: dict[str, Any]) -> dict[str, Any]:
    excluded = {"completion_basis_digest", "terminal_transitions", "completion_binding"}
    return {key: deepcopy(value) for key, value in attempt.items() if key not in excluded}


def _cursor_projection(phase_events: Iterable[dict[str, Any]], cut: int) -> dict[str, Any] | None:
    eligible = [
        event
        for event in phase_events
        if isinstance(event.get("recorded_sequence"), int) and event["recorded_sequence"] <= cut
    ]
    if not eligible:
        return None
    last = max(eligible, key=lambda event: event["recorded_sequence"])
    return {
        "phase_index": last.get("phase_index"),
        "phase": last.get("phase"),
        "checkpoint": last.get("kind"),
    }


def completion_basis_projection(
    state: dict[str, Any], attempt: dict[str, Any]
) -> dict[str, Any]:
    """Reconstruct the immutable execution meaning at one completion cut."""

    cut = attempt.get("claim_cut_sequence")
    if not isinstance(cut, int) or isinstance(cut, bool):
        raise ValueError("claim_cut_sequence must be an integer")
    attempts = state.get("completion_attempts", [])
    current_index = next(
        (
            index
            for index, candidate in enumerate(attempts)
            if candidate.get("attempt_id") == attempt.get("attempt_id")
            and candidate.get("attempt_revision") == attempt.get("attempt_revision")
        ),
        None,
    )
    if current_index is None:
        raise ValueError("completion attempt is not present in execution state")

    transitions = [
        deepcopy(record)
        for record in state.get("lifecycle_transitions", [])
        if isinstance(record.get("recorded_sequence"), int) and record["recorded_sequence"] <= cut
    ]
    phase_events = [
        deepcopy(record)
        for record in state.get("phase_events", [])
        if isinstance(record.get("recorded_sequence"), int) and record["recorded_sequence"] <= cut
    ]
    artifact_bindings = [
        deepcopy(record)
        for record in state.get("artifact_bindings", [])
        if isinstance(record.get("recorded_sequence"), int) and record["recorded_sequence"] <= cut
    ]
    lifecycle_at_cut = "received"
    if transitions:
        lifecycle_at_cut = max(
            transitions, key=lambda record: record["recorded_sequence"]
        ).get("to_state")

    projection: dict[str, Any] = {
        "artifact": state.get("artifact"),
        "schema_version": state.get("schema_version"),
        "work_id": state.get("work_id"),
        "route_binding": deepcopy(state.get("route_binding")),
        "lifecycle_state": lifecycle_at_cut,
        "lifecycle_transitions": transitions,
        "phase_events": phase_events,
        "artifact_bindings": artifact_bindings,
        "block_contexts": [
            deepcopy(context)
            for context in state.get("block_contexts", [])
            if isinstance(context.get("transition_sequence"), int)
            and context["transition_sequence"] <= cut
        ],
        "completion_attempts": [
            *deepcopy(attempts[:current_index]),
            _basis_attempt_projection(attempt),
        ],
        "current_completion_attempt_id": attempt.get("attempt_id"),
    }
    cursor = _cursor_projection(phase_events, cut)
    if cursor is not None:
        projection["workflow_cursor"] = cursor
    if "previous_execution" in state:
        projection["previous_execution"] = deepcopy(state["previous_execution"])
    return projection


def terminal_authority_projection(state: dict[str, Any]) -> dict[str, Any]:
    """Project the final authority surface pinned outside the writable bundle."""

    attempt_id = state.get("current_completion_attempt_id")
    attempt = next(
        (
            candidate
            for candidate in state.get("completion_attempts", [])
            if isinstance(candidate, dict) and candidate.get("attempt_id") == attempt_id
        ),
        None,
    )
    if not isinstance(attempt, dict):
        raise ValueError("terminal authority requires a current completion attempt")
    transition_by_sequence = _transition_by_sequence(state)
    terminal_records: list[dict[str, Any]] = []
    for reference in attempt.get("terminal_transitions", []):
        sequence = reference.get("recorded_sequence") if isinstance(reference, dict) else None
        record = transition_by_sequence.get(sequence) if isinstance(sequence, int) else None
        if not isinstance(record, dict):
            raise ValueError("terminal authority references a missing transition record")
        terminal_records.append(deepcopy(record))
    projection: dict[str, Any] = {
        "schema_version": "terminal-authority.v1",
        "work_id": state.get("work_id"),
        "state_revision": state.get("state_revision"),
        "updated_at": state.get("updated_at"),
        "route_binding": deepcopy(state.get("route_binding")),
        "lifecycle_state": state.get("lifecycle_state"),
        "current_completion_attempt_id": attempt_id,
        "completion_attempt": deepcopy(attempt),
        "terminal_transition_records": terminal_records,
    }
    if "workflow_cursor" in state:
        projection["workflow_cursor"] = deepcopy(state["workflow_cursor"])
    if "previous_execution" in state:
        projection["previous_execution"] = deepcopy(state["previous_execution"])
    return projection


def terminal_authority_digest(state: dict[str, Any]) -> str:
    return canonical_json_digest(terminal_authority_projection(state))


def _transition_by_sequence(state: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {
        transition["recorded_sequence"]: transition
        for transition in state.get("lifecycle_transitions", [])
        if isinstance(transition, dict)
        and isinstance(transition.get("recorded_sequence"), int)
        and not isinstance(transition.get("recorded_sequence"), bool)
    }


def _attempt_terminal_transitions(
    state: dict[str, Any], cut: int, next_cut: int | None
) -> list[dict[str, Any]]:
    candidates = sorted(
        (
            transition
            for transition in state.get("lifecycle_transitions", [])
            if isinstance(transition.get("recorded_sequence"), int)
            and transition["recorded_sequence"] > cut
            and (next_cut is None or transition["recorded_sequence"] < next_cut)
        ),
        key=lambda transition: transition["recorded_sequence"],
    )
    outcome: list[dict[str, Any]] = []
    for transition in candidates:
        edge = (transition.get("from_state"), transition.get("to_state"))
        if edge in {
            ("completion_claimed", "verified"),
            ("completion_claimed", "rejected"),
            ("verified", "completed"),
        }:
            outcome.append(transition)
            if edge in {
                ("completion_claimed", "rejected"),
                ("verified", "completed"),
            }:
                break
    return outcome


def validate_completion_attempts(
    state: dict[str, Any], route: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    attempts = state.get("completion_attempts", [])
    if not isinstance(attempts, list):
        return ["completion_attempts must be an array"]

    transitions = _transition_by_sequence(state)
    claim_transitions = sorted(
        sequence
        for sequence, transition in transitions.items()
        if transition.get("from_state") == "executing"
        and transition.get("to_state") == "completion_claimed"
    )
    if len(claim_transitions) != len(attempts):
        errors.append(
            "every executing -> completion_claimed transition must have exactly one completion attempt"
        )

    attempt_ids: set[str] = set()
    verification_record_digests: set[str] = set()
    verification_evidence_ids: set[str] = set()
    previous_cut = 0
    for index, attempt in enumerate(attempts):
        label = f"completion attempt {index + 1}"
        if not isinstance(attempt, dict):
            errors.append(f"{label} must be an object")
            continue
        attempt_id = attempt.get("attempt_id")
        if attempt_id in attempt_ids:
            errors.append(f"duplicate completion attempt id: {attempt_id}")
        elif isinstance(attempt_id, str):
            attempt_ids.add(attempt_id)
        if attempt.get("attempt_revision") != index + 1:
            errors.append(f"{label} attempt_revision must be {index + 1}")
        for field in ("route_id", "route_revision", "route_digest"):
            if attempt.get(field) != route.get(field):
                errors.append(f"{label} {field} does not match the approved route")

        cut = attempt.get("claim_cut_sequence")
        if isinstance(cut, int) and not isinstance(cut, bool):
            if cut <= previous_cut:
                errors.append(f"{label} claim_cut_sequence must increase across attempts")
            previous_cut = cut
        cut_transition = transitions.get(cut) if isinstance(cut, int) else None
        if not isinstance(cut_transition, dict) or (
            cut_transition.get("from_state"), cut_transition.get("to_state")
        ) != ("executing", "completion_claimed"):
            errors.append(
                f"{label} claim_cut_sequence must identify executing -> completion_claimed"
            )

        expected_claim_digest = canonical_json_digest(claim_payload_projection(attempt))
        if attempt.get("claim_digest") != expected_claim_digest:
            errors.append(f"{label} claim_digest does not match its immutable claim payload")
        try:
            expected_basis_digest = canonical_json_digest(
                completion_basis_projection(state, attempt)
            )
        except (TypeError, ValueError) as exc:
            errors.append(f"{label} completion basis cannot be reconstructed: {exc}")
        else:
            if attempt.get("completion_basis_digest") != expected_basis_digest:
                errors.append(
                    f"{label} completion_basis_digest does not match the preterminal projection"
                )

        snapshot = attempt.get("work_snapshot")
        if not isinstance(snapshot, dict):
            errors.append(f"{label} work_snapshot must be an object")
        else:
            if snapshot.get("algorithm_id") != WORKTREE_ALGORITHM_ID:
                errors.append(f"{label} uses an unsupported work snapshot algorithm")
            if snapshot.get("scope_policy_id") != WORKTREE_SCOPE_POLICY_ID:
                errors.append(f"{label} uses an unsupported work snapshot scope policy")
            snapshot_time = _parse_datetime(snapshot.get("captured_at"))
            claimed_time = _parse_datetime(attempt.get("claimed_at"))
            if snapshot_time is None or claimed_time is None:
                errors.append(f"{label} work snapshot and claimed_at must be timezone-aware")
            elif claimed_time < snapshot_time:
                errors.append(f"{label} claimed_at predates its work snapshot")

        commitment = attempt.get("verification_commitment")
        if not isinstance(commitment, dict):
            errors.append(f"{label} verification_commitment must be an object")
        else:
            if commitment.get("work_snapshot") != snapshot:
                errors.append(f"{label} verification commitment work_snapshot does not match")
            evidence_bindings = commitment.get("evidence_bindings")
            if not isinstance(evidence_bindings, list) or not evidence_bindings:
                errors.append(f"{label} verification commitment requires evidence bindings")
            else:
                evidence_ids: list[str] = []
                for evidence_binding in evidence_bindings:
                    evidence_id = (
                        evidence_binding.get("evidence_id")
                        if isinstance(evidence_binding, dict)
                        else None
                    )
                    if isinstance(evidence_id, str):
                        evidence_ids.append(evidence_id)
                if len(evidence_ids) != len(evidence_bindings) or len(evidence_ids) != len(set(evidence_ids)):
                    errors.append(f"{label} verification commitment evidence IDs must be unique")
                reused_ids = sorted(set(evidence_ids) & verification_evidence_ids)
                if reused_ids:
                    errors.append(
                        f"{label} retry reuses prior verification evidence IDs: {reused_ids}"
                    )
                verification_evidence_ids.update(evidence_ids)
            verification_digest = commitment.get("verification_record_sha256")
            if verification_digest in verification_record_digests:
                errors.append(f"{label} retry reuses a prior verification record digest")
            elif isinstance(verification_digest, str):
                verification_record_digests.add(verification_digest)

        next_cut = None
        if index + 1 < len(attempts):
            candidate = attempts[index + 1].get("claim_cut_sequence")
            if isinstance(candidate, int):
                next_cut = candidate
        terminal_records = _attempt_terminal_transitions(state, cut, next_cut) if isinstance(cut, int) else []
        expected_refs = [
            {
                "recorded_sequence": record.get("recorded_sequence"),
                "record_digest": record.get("record_digest"),
            }
            for record in terminal_records
        ]
        if attempt.get("terminal_transitions") != expected_refs:
            errors.append(f"{label} terminal transition references do not match execution history")

        rejected = bool(terminal_records) and terminal_records[-1].get("to_state") == "rejected"
        if rejected and attempt.get("completion_binding") is not None:
            errors.append(f"{label} rejected attempt must not retain a completion binding")

        if index + 1 < len(attempts):
            if not terminal_records or terminal_records[-1].get("to_state") != "rejected":
                errors.append(f"{label} must end rejected before a later completion attempt")

    lifecycle_state = state.get("lifecycle_state")
    current_attempt_id = state.get("current_completion_attempt_id")
    if lifecycle_state in {"completion_claimed", "verified", "completed"}:
        if not attempts:
            errors.append(f"lifecycle state {lifecycle_state} requires a completion attempt")
        elif current_attempt_id != attempts[-1].get("attempt_id"):
            errors.append("current_completion_attempt_id must identify the latest completion attempt")
    elif current_attempt_id is not None:
        errors.append(f"current_completion_attempt_id must be absent in lifecycle state {lifecycle_state}")
    return errors


def _parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _snapshot_identity(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        key: snapshot.get(key)
        for key in ("algorithm_id", "scope_policy_id", "head", "status", "content_digest")
    }


def validate_terminal_completion(
    state: dict[str, Any],
    route: dict[str, Any],
    *,
    control_root: Path,
    repo_root: Path,
    verification_document: dict[str, Any] | None = None,
    verification_document_digest: str | None = None,
) -> list[str]:
    """Validate content closure and live freshness for verified/completed state."""

    errors: list[str] = []
    if state.get("lifecycle_state") not in {"verified", "completed"}:
        return ["terminal completion validation requires verified or completed lifecycle state"]
    attempts = state.get("completion_attempts", [])
    attempt = next(
        (
            candidate
            for candidate in attempts
            if candidate.get("attempt_id") == state.get("current_completion_attempt_id")
        ),
        None,
    )
    if not isinstance(attempt, dict):
        return ["terminal state does not identify a valid current completion attempt"]
    binding = attempt.get("completion_binding")
    if not isinstance(binding, dict):
        return ["terminal completion attempt is missing completion_binding"]

    for field in (
        "attempt_id",
        "attempt_revision",
        "claim_digest",
        "completion_basis_digest",
        "route_id",
        "route_revision",
        "route_digest",
    ):
        if binding.get(field) != attempt.get(field):
            errors.append(f"completion binding {field} does not match the current attempt")
    if binding.get("work_snapshot") != attempt.get("work_snapshot"):
        errors.append("completion binding work_snapshot does not match the current attempt")
    commitment = attempt.get("verification_commitment")
    if not isinstance(commitment, dict):
        errors.append("terminal completion attempt is missing verification_commitment")
        commitment = {}
    for binding_field, commitment_field in (
        ("verification_record_ref", "verification_record_ref"),
        ("verification_record_sha256", "verification_record_sha256"),
        ("evidence_bindings", "evidence_bindings"),
        ("work_snapshot", "work_snapshot"),
    ):
        if binding.get(binding_field) != commitment.get(commitment_field):
            errors.append(
                f"completion binding {binding_field} does not match verification commitment"
            )

    terminal_digests = [
        record.get("record_digest") for record in attempt.get("terminal_transitions", [])
    ]
    if binding.get("terminal_transition_digests") != terminal_digests:
        errors.append("completion binding terminal transition digests do not match the attempt")

    verification_ref = binding.get("verification_record_ref")
    verification: dict[str, Any] | None = verification_document
    if isinstance(verification_ref, str):
        if verification is not None:
            actual_digest = verification_document_digest
            if not isinstance(actual_digest, str):
                errors.append("preloaded verification record is missing its content digest")
        else:
            try:
                verification_path = resolve_control_ref(control_root, verification_ref)
                verification, actual_digest = load_strict_json_with_digest(verification_path)
            except (StrictJSONError, ValueError) as exc:
                errors.append(f"verification record is invalid: {exc}")
                actual_digest = None
        if (
            isinstance(actual_digest, str)
            and binding.get("verification_record_sha256") != actual_digest
        ):
            errors.append("verification record digest does not match completion binding")
    else:
        errors.append("completion binding verification_record_ref must be a local ref")

    work_snapshot = attempt.get("work_snapshot", {})
    if verification is not None:
        if verification.get("status") != "accepted" or verification.get("claim_may_be_made") is not True:
            errors.append("verification record does not authorize a completion claim")
        if verification.get("claim") != attempt.get("claim"):
            errors.append("verification record claim does not match the completion attempt")
        if verification.get("claim_scope") != attempt.get("claim_scope"):
            errors.append("verification record claim_scope does not match the completion attempt")
        if verification.get("failed") != [] or verification.get("remaining_unverified") != []:
            errors.append("verification record retains failed or unverified scope")

        work_state = verification.get("work_state_ref")
        if not isinstance(work_state, dict):
            errors.append("verification record work_state_ref must be structured")
            work_state = {}
        if work_state.get("id") != work_snapshot.get("content_digest"):
            errors.append("verification work state id does not match the governed content digest")
        if work_state.get("ref") != work_snapshot.get("head"):
            errors.append("verification work state ref does not match the governed Git HEAD")
        if work_state.get("status") != work_snapshot.get("status"):
            errors.append("verification work state status does not match the governed snapshot")
        if work_state.get("captured_at") != work_snapshot.get("captured_at"):
            errors.append("verification work state captured_at does not match the governed snapshot")
        if work_snapshot.get("status") == "dirty":
            if work_state.get("diff_ref") != work_snapshot.get("content_digest"):
                errors.append("dirty verification work state diff_ref must equal content_digest")
        elif work_state.get("diff_ref") not in {None, work_snapshot.get("content_digest")}:
            errors.append("clean verification work state diff_ref disagrees with content_digest")

        evidence_refs = verification.get("evidence_refs")
        evidence_by_id: dict[str, dict[str, Any]] = {}
        if not isinstance(evidence_refs, list) or not evidence_refs:
            errors.append("verification record must contain evidence_refs")
        else:
            for evidence in evidence_refs:
                evidence_id = evidence.get("id") if isinstance(evidence, dict) else None
                if not isinstance(evidence_id, str) or not evidence_id:
                    errors.append("verification evidence must have a non-empty id")
                elif evidence_id in evidence_by_id:
                    errors.append(f"duplicate verification evidence id: {evidence_id}")
                else:
                    evidence_by_id[evidence_id] = evidence

        evidence_bindings = binding.get("evidence_bindings")
        binding_by_id: dict[str, dict[str, Any]] = {}
        if not isinstance(evidence_bindings, list):
            errors.append("completion binding evidence_bindings must be an array")
            evidence_bindings = []
        for evidence_binding in evidence_bindings:
            evidence_id = evidence_binding.get("evidence_id") if isinstance(evidence_binding, dict) else None
            if not isinstance(evidence_id, str) or evidence_id in binding_by_id:
                errors.append(f"duplicate or invalid evidence binding id: {evidence_id!r}")
                continue
            binding_by_id[evidence_id] = evidence_binding
            try:
                evidence_path = resolve_control_ref(control_root, evidence_binding.get("local_ref"))
                if file_sha256(evidence_path) != evidence_binding.get("sha256"):
                    errors.append(f"evidence binding {evidence_id} content digest does not match")
            except (TypeError, ValueError) as exc:
                errors.append(f"evidence binding {evidence_id} is invalid: {exc}")
        if set(evidence_by_id) != set(binding_by_id):
            errors.append("completion evidence bindings must exactly cover verification evidence IDs")

        checks = verification.get("checks_run")
        if not isinstance(checks, list) or not checks:
            errors.append("verification record must contain checks_run")
        else:
            for check in checks:
                if not isinstance(check, dict) or check.get("result") != "passed":
                    errors.append("every terminal verification check must have result passed")
                    continue
                if check.get("evidence_ref") not in evidence_by_id:
                    errors.append("verification check references unknown evidence")
                if check.get("work_state_ref") != work_snapshot.get("content_digest"):
                    errors.append("verification check references a different work state")

        work_captured = _parse_datetime(work_snapshot.get("captured_at"))
        verified_at = _parse_datetime(verification.get("verified_at"))
        if work_captured is None or verified_at is None:
            errors.append("work and verification timestamps must be timezone-aware")
        for evidence_id, evidence in evidence_by_id.items():
            evidence_captured = _parse_datetime(evidence.get("captured_at"))
            if evidence.get("work_state_ref") != work_snapshot.get("content_digest"):
                errors.append(f"verification evidence {evidence_id} references a different work state")
            if evidence_captured is None:
                errors.append(f"verification evidence {evidence_id} has an invalid captured_at")
            else:
                if work_captured is not None and evidence_captured < work_captured:
                    errors.append(f"verification evidence {evidence_id} predates the work snapshot")
                if verified_at is not None and evidence_captured > verified_at:
                    errors.append(f"verification evidence {evidence_id} postdates verification")

    try:
        first_live = capture_git_worktree(
            repo_root,
            excluded_control_root=control_root,
        )
        second_live = capture_git_worktree(
            repo_root,
            excluded_control_root=control_root,
        )
    except WorktreeSnapshotError as exc:
        errors.append(f"live work snapshot failed: {exc}")
    else:
        if _snapshot_identity(first_live) != _snapshot_identity(second_live):
            errors.append("live work snapshot changed during terminal validation")
        if _snapshot_identity(first_live) != _snapshot_identity(work_snapshot):
            errors.append("live work snapshot does not match the completion attempt")

    return errors


def validate_control_bundle(
    control_root: Path,
    *,
    state_path: Path,
    state: dict[str, Any],
    route: dict[str, Any],
    historical_states: Iterable[dict[str, Any]] = (),
    predecessor_routes: Iterable[dict[str, Any]] = (),
) -> list[str]:
    """Validate that the excluded control root is a closed content-bound set."""

    errors: list[str] = []
    root = control_root.absolute()
    allowed_paths: set[Path] = set()
    expected_digests: dict[Path, tuple[str, str]] = {}

    def allow_path(path: Path, label: str, digest: str | None = None) -> None:
        absolute = path.absolute()
        try:
            absolute.relative_to(root)
        except ValueError:
            errors.append(f"{label} escapes the control root")
            return
        allowed_paths.add(absolute)
        if digest is not None:
            previous = expected_digests.get(absolute)
            if previous is not None and previous[0] != digest:
                errors.append(
                    f"{label} conflicts with another digest binding for {absolute.relative_to(root)}"
                )
            else:
                expected_digests[absolute] = (digest, label)

    def allow_ref(ref: Any, label: str, digest: Any = None) -> None:
        if not isinstance(ref, str):
            errors.append(f"{label} must be a local reference")
            return
        try:
            resolved = resolve_control_ref(root, ref)
        except ValueError as exc:
            errors.append(f"{label} is invalid: {exc}")
            return
        allow_path(resolved, label, digest if isinstance(digest, str) else None)

    all_routes = [route, *predecessor_routes]
    all_states = [state, *historical_states]
    allow_path(state_path, "canonical execution state")

    for route_index, route_item in enumerate(all_routes):
        approval_evidence = route_item.get("approval_evidence", {})
        if isinstance(approval_evidence, dict):
            allow_ref(
                approval_evidence.get("ref"),
                f"route {route_index} approval evidence",
                approval_evidence.get("sha256"),
            )
        previous_route = route_item.get("previous_route")
        if isinstance(previous_route, dict):
            # previous_route.digest is the predecessor's canonical route digest,
            # not a raw file digest; the predecessor loader validates that value.
            allow_ref(previous_route.get("ref"), f"route {route_index} previous route")

    for state_index, state_item in enumerate(all_states):
        route_binding = state_item.get("route_binding", {})
        allow_ref(route_binding.get("ref"), f"state {state_index} route binding")
        previous_execution = state_item.get("previous_execution")
        if isinstance(previous_execution, dict):
            allow_ref(
                previous_execution.get("ref"),
                f"state {state_index} previous execution",
                previous_execution.get("sha256"),
            )

        for index, binding in enumerate(state_item.get("artifact_bindings", [])):
            if not isinstance(binding, dict):
                continue
            allow_ref(
                binding.get("ref"),
                f"state {state_index} artifact binding {index} subject",
                binding.get("subject_sha256"),
            )
            structural = binding.get("structural_evidence")
            if isinstance(structural, dict):
                evidence = structural.get("evidence")
                if isinstance(evidence, dict):
                    allow_ref(
                        evidence.get("ref"),
                        f"state {state_index} artifact binding {index} structural evidence",
                        evidence.get("sha256"),
                    )
            approval = binding.get("approval")
            if isinstance(approval, dict):
                evidence = approval.get("evidence")
                if isinstance(evidence, dict):
                    allow_ref(
                        evidence.get("ref"),
                        f"state {state_index} artifact binding {index} approval evidence",
                        evidence.get("sha256"),
                    )

        evidence_owners = [
            *(state_item.get("lifecycle_transitions", []) or []),
            *(state_item.get("phase_events", []) or []),
            *(state_item.get("block_contexts", []) or []),
        ]
        for owner_index, owner in enumerate(evidence_owners):
            if not isinstance(owner, dict):
                continue
            for evidence_index, evidence in enumerate(owner.get("evidence_refs", [])):
                if isinstance(evidence, dict):
                    allow_ref(
                        evidence.get("ref"),
                        f"state {state_index} execution evidence {owner_index}:{evidence_index}",
                        evidence.get("sha256"),
                    )

        for attempt_index, attempt in enumerate(state_item.get("completion_attempts", [])):
            if not isinstance(attempt, dict):
                continue
            verification_commitment = attempt.get("verification_commitment")
            if isinstance(verification_commitment, dict):
                allow_ref(
                    verification_commitment.get("verification_record_ref"),
                    f"state {state_index} completion attempt {attempt_index + 1} verification commitment",
                    verification_commitment.get("verification_record_sha256"),
                )
                for evidence_index, evidence in enumerate(
                    verification_commitment.get("evidence_bindings", [])
                ):
                    if isinstance(evidence, dict):
                        allow_ref(
                            evidence.get("local_ref"),
                            f"state {state_index} completion attempt {attempt_index + 1} commitment evidence {evidence_index}",
                            evidence.get("sha256"),
                        )
            completion_binding = attempt.get("completion_binding")
            if not isinstance(completion_binding, dict):
                continue
            allow_ref(
                completion_binding.get("verification_record_ref"),
                f"state {state_index} completion attempt {attempt_index + 1} verification record",
                completion_binding.get("verification_record_sha256"),
            )
            for evidence_index, evidence in enumerate(completion_binding.get("evidence_bindings", [])):
                if isinstance(evidence, dict):
                    allow_ref(
                        evidence.get("local_ref"),
                        f"state {state_index} completion attempt {attempt_index + 1} evidence binding {evidence_index}",
                        evidence.get("sha256"),
                    )

    for path, (expected_digest, label) in expected_digests.items():
        try:
            actual_digest = file_sha256(path)
        except ValueError as exc:
            errors.append(f"{label} digest cannot be checked: {exc}")
            continue
        if actual_digest != expected_digest:
            errors.append(
                f"{label} digest mismatch for {path.relative_to(root).as_posix()}"
            )

    try:
        root_stat = root.lstat()
    except OSError as exc:
        return [*errors, f"control root cannot be enumerated: {exc}"]
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        return [*errors, "control root must be a non-symlink directory"]

    def record_walk_error(exc: OSError) -> None:
        errors.append(f"control bundle cannot be fully enumerated: {exc}")

    for current, dirnames, filenames in os.walk(
        root,
        topdown=True,
        followlinks=False,
        onerror=record_walk_error,
    ):
        current_path = Path(current)
        retained_dirs: list[str] = []
        for dirname in dirnames:
            directory = current_path / dirname
            try:
                directory_stat = directory.lstat()
            except OSError as exc:
                errors.append(f"control directory cannot be inspected: {directory}: {exc}")
                continue
            if stat.S_ISLNK(directory_stat.st_mode):
                errors.append(f"control bundle contains a symlink directory: {directory.relative_to(root)}")
            elif not stat.S_ISDIR(directory_stat.st_mode):
                errors.append(f"control bundle contains an unsupported directory entry: {directory.relative_to(root)}")
            else:
                retained_dirs.append(dirname)
        dirnames[:] = retained_dirs

        for filename in filenames:
            path = (current_path / filename).absolute()
            try:
                entry_stat = path.lstat()
            except OSError as exc:
                errors.append(f"control file cannot be inspected: {path}: {exc}")
                continue
            relative = path.relative_to(root).as_posix()
            if stat.S_ISLNK(entry_stat.st_mode):
                errors.append(f"control bundle contains a symlink file: {relative}")
            elif not stat.S_ISREG(entry_stat.st_mode):
                errors.append(f"control bundle contains an unsupported file type: {relative}")
            elif path not in allowed_paths:
                errors.append(f"unbound control file is not allowed: {relative}")

    return errors


def _without_key(payload: dict[str, Any], key: str) -> dict[str, Any]:
    return {name: value for name, value in payload.items() if name != key}


def validate_route_decision_contract(
    route: dict[str, Any],
    *,
    phases: set[str],
    primary_workflows: set[str],
    overlays: set[str],
    artifact_names: set[str],
) -> list[str]:
    """Validate route semantics that JSON Schema cannot express."""

    errors: list[str] = []
    if canonical_json_digest(_without_key(route, "route_digest")) != route.get("route_digest"):
        errors.append("route_digest does not match canonical route content")
    if _parse_datetime(route.get("approved_at")) is None:
        errors.append("approved_at must be a timezone-aware date-time")

    entry_phase = route.get("entry_phase")
    if entry_phase not in phases:
        errors.append(f"entry_phase is not a registered phase: {entry_phase!r}")

    workflow = route.get("workflow")
    if not isinstance(workflow, dict):
        return [*errors, "workflow must be an object"]

    if workflow.get("primary") not in primary_workflows:
        errors.append(f"workflow.primary is not registered: {workflow.get('primary')!r}")

    route_overlays = workflow.get("overlays", [])
    if not isinstance(route_overlays, list):
        errors.append("workflow.overlays must be an array")
    else:
        unknown_overlays = sorted(set(route_overlays) - overlays)
        if unknown_overlays:
            errors.append(f"workflow.overlays contains unregistered values: {unknown_overlays}")
        if len(route_overlays) != len(set(route_overlays)):
            errors.append("workflow.overlays must not contain duplicates")

    focus_sequence = workflow.get("focus_sequence")
    if not isinstance(focus_sequence, list) or not focus_sequence:
        errors.append("workflow.focus_sequence must be a non-empty array")
    else:
        unknown_phases = [phase for phase in focus_sequence if phase not in phases]
        if unknown_phases:
            errors.append(f"workflow.focus_sequence contains unregistered phases: {unknown_phases}")
        if focus_sequence[0] != entry_phase:
            errors.append("focus_sequence[0] must equal entry_phase")

    revision = route.get("route_revision")
    previous_route = route.get("previous_route")
    if isinstance(revision, int) and not isinstance(revision, bool):
        if revision == 1 and previous_route is not None:
            errors.append("route revision 1 must not declare previous_route")
        if revision > 1:
            if not isinstance(previous_route, dict):
                errors.append("route revision greater than 1 requires previous_route")
            elif previous_route.get("revision") != revision - 1:
                errors.append("previous_route.revision must immediately precede route_revision")

    obligations = route.get("obligations")
    if not isinstance(obligations, list) or not obligations:
        return [*errors, "obligations must be a non-empty array"]

    obligation_ids: set[str] = set()
    intake_gate_count = 0
    for index, obligation in enumerate(obligations):
        label = f"obligations[{index}]"
        if not isinstance(obligation, dict):
            errors.append(f"{label} must be an object")
            continue

        obligation_id = obligation.get("id")
        if not isinstance(obligation_id, str) or not obligation_id:
            errors.append(f"{label}.id must be a non-empty string")
        elif obligation_id in obligation_ids:
            errors.append(f"duplicate obligation id: {obligation_id}")
        else:
            obligation_ids.add(obligation_id)

        artifact = obligation.get("artifact")
        if artifact not in artifact_names:
            errors.append(f"{label}.artifact is not registered: {artifact!r}")

        gate = obligation.get("gate")
        if not isinstance(gate, dict):
            errors.append(f"{label}.gate must be an object")
            continue
        if gate.get("kind") == "phase_checkpoint":
            phase_index = gate.get("phase_index")
            if not isinstance(phase_index, int) or isinstance(phase_index, bool):
                errors.append(f"{label}.gate.phase_index must be an integer")
            elif not isinstance(focus_sequence, list) or phase_index >= len(focus_sequence):
                errors.append(f"{label}.gate.phase_index is outside workflow.focus_sequence")
        elif gate.get("kind") == "lifecycle_transition":
            edge = (gate.get("from_state"), gate.get("to_state"))
            if edge not in LIFECYCLE_TRANSITIONS:
                errors.append(f"{label}.gate names an invalid lifecycle transition: {edge}")
            if (
                artifact == "intake-brief"
                and edge == ("received", "routed")
                and obligation.get("assurance") == "approval_accepted"
            ):
                intake_gate_count += 1
        else:
            errors.append(f"{label}.gate.kind is not supported")

    if intake_gate_count < 1:
        errors.append(
            "route must declare at least one approval_accepted intake-brief obligation "
            "for received -> routed"
        )

    return errors


def _record_digest_error(record: dict[str, Any], label: str) -> str | None:
    expected = canonical_json_digest(_without_key(record, "record_digest"))
    if record.get("record_digest") != expected:
        return f"{label} record_digest does not match canonical record content"
    return None


def _obligations_for_lifecycle_edge(
    obligations: Iterable[dict[str, Any]], source: str, target: str
) -> Iterable[dict[str, Any]]:
    for obligation in obligations:
        gate = obligation.get("gate", {})
        if (
            gate.get("kind") == "lifecycle_transition"
            and gate.get("from_state") == source
            and gate.get("to_state") == target
        ):
            yield obligation


def _obligations_for_phase_event(
    obligations: Iterable[dict[str, Any]], phase_index: int, checkpoint: str
) -> Iterable[dict[str, Any]]:
    for obligation in obligations:
        gate = obligation.get("gate", {})
        if (
            gate.get("kind") == "phase_checkpoint"
            and gate.get("phase_index") == phase_index
            and gate.get("checkpoint") == checkpoint
        ):
            yield obligation


def _validate_binding(binding: dict[str, Any], obligation: dict[str, Any]) -> list[str]:
    obligation_id = obligation.get("id")
    errors: list[str] = []
    if binding.get("artifact") != obligation.get("artifact"):
        errors.append(f"binding for obligation {obligation_id} names the wrong artifact")
    if binding.get("assurance") != obligation.get("assurance"):
        errors.append(f"binding for obligation {obligation_id} names the wrong assurance")

    assurance = obligation.get("assurance")
    if assurance == "structural_valid":
        structural = binding.get("structural_evidence")
        if not isinstance(structural, dict) or structural.get("result") != "passed":
            errors.append(f"binding for obligation {obligation_id} lacks passing structural evidence")
    elif assurance == "approval_accepted":
        approval = binding.get("approval")
        if not isinstance(approval, dict) or approval.get("status") != "accepted":
            errors.append(f"binding for obligation {obligation_id} lacks accepted approval evidence")
        elif approval.get("subject_sha256") != binding.get("subject_sha256"):
            errors.append(f"binding for obligation {obligation_id} approval subject digest does not match")
    return errors


def _expected_phase_event(
    cursor: tuple[int, str] | None, focus_sequence: list[str]
) -> tuple[int, str] | None:
    if cursor is None:
        return (0, "entered")
    phase_index, checkpoint = cursor
    if checkpoint == "entered":
        return (phase_index, "exited")
    if phase_index + 1 < len(focus_sequence):
        return (phase_index + 1, "entered")
    return None


def validate_execution_state_contract(
    state: dict[str, Any],
    route: dict[str, Any],
    *,
    approved_route_digest: str | None,
    is_canonical_current: bool,
    authority_mode: bool,
    terminal_validation_passed: bool = False,
    approved_completion_digest: str | None = None,
) -> ValidationResult:
    """Replay execution state and determine its bounded authority.

    Callers must perform JSON Schema and local-reference validation before this
    semantic replay. Structural validation never upgrades itself to operator
    authority: the canonical path and the independently supplied route pin are
    explicit inputs.
    """

    errors: list[str] = []
    if _parse_datetime(state.get("updated_at")) is None:
        errors.append("updated_at must be a timezone-aware date-time")
    route_digest = route.get("route_digest")
    if canonical_json_digest(_without_key(route, "route_digest")) != route_digest:
        errors.append("route_digest does not match canonical route content")

    route_binding = state.get("route_binding")
    if not isinstance(route_binding, dict):
        return ValidationResult(AUTHORITY_STRUCTURAL, [*errors, "route_binding must be an object"])
    for state_key, route_key in (
        ("route_id", "route_id"),
        ("route_revision", "route_revision"),
        ("route_digest", "route_digest"),
    ):
        if route_binding.get(state_key) != route.get(route_key):
            errors.append(f"route_binding.{state_key} does not match the route decision")
    if state.get("work_id") != route.get("work_id"):
        errors.append("execution-state work_id does not match route decision")

    if authority_mode:
        if approved_route_digest is None:
            errors.append("authority mode requires an operator pin for the approved route digest")
        elif approved_route_digest != route_digest:
            errors.append("operator pin does not match the approved route digest")
        if not is_canonical_current:
            errors.append("authority mode requires the canonical current execution-state")

    events: list[tuple[int, str, dict[str, Any]]] = []
    event_groups = (
        ("lifecycle transition", state.get("lifecycle_transitions")),
        ("phase event", state.get("phase_events")),
        ("artifact binding", state.get("artifact_bindings")),
    )
    for label, records in event_groups:
        if not isinstance(records, list):
            errors.append(f"{label} records must be an array")
            continue
        for record in records:
            if not isinstance(record, dict):
                errors.append(f"{label} record must be an object")
                continue
            sequence = record.get("recorded_sequence")
            if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 1:
                errors.append(f"{label} recorded_sequence must be a positive integer")
                continue
            events.append((sequence, label, record))
            if label in {"lifecycle transition", "phase event"} and _parse_datetime(
                record.get("occurred_at")
            ) is None:
                errors.append(f"{label} {sequence} occurred_at must be timezone-aware")
            if label in {"lifecycle transition", "phase event"}:
                digest_error = _record_digest_error(record, f"{label} {sequence}")
                if digest_error:
                    errors.append(digest_error)

    events.sort(key=lambda item: item[0])
    sequences = [sequence for sequence, _, _ in events]
    state_revision = state.get("state_revision")
    if not isinstance(state_revision, int) or isinstance(state_revision, bool):
        errors.append("state_revision must be an integer")
    elif sequences != list(range(1, state_revision + 1)):
        errors.append(
            "global recorded_sequence must be unique and contiguous from 1 through state_revision"
        )

    lifecycle_state = "received"
    cursor: tuple[int, str] | None = None
    focus_sequence = route.get("workflow", {}).get("focus_sequence", [])
    obligations = route.get("obligations", [])
    obligation_by_id = {
        obligation.get("id"): obligation
        for obligation in obligations
        if isinstance(obligation, dict) and isinstance(obligation.get("id"), str)
    }
    bound_at: dict[str, int] = {}
    block_context_by_transition: dict[int, dict[str, Any]] = {}
    active_block_sequence: int | None = None

    block_contexts = state.get("block_contexts", [])
    if isinstance(block_contexts, list):
        for context in block_contexts:
            if isinstance(context, dict) and isinstance(context.get("transition_sequence"), int):
                transition_sequence = context["transition_sequence"]
                if transition_sequence in block_context_by_transition:
                    errors.append(f"duplicate block_context for transition {transition_sequence}")
                else:
                    block_context_by_transition[transition_sequence] = context

    for sequence, label, record in events:
        if label == "artifact binding":
            if lifecycle_state in {"completion_claimed", "verified", "completed", "rerouted"}:
                errors.append(
                    f"artifact binding {sequence} is invalid while lifecycle state is "
                    f"{lifecycle_state}"
                )
            obligation_id = record.get("obligation_id")
            if not isinstance(obligation_id, str):
                errors.append(f"artifact binding {sequence} obligation_id must be a string")
                continue
            obligation = obligation_by_id.get(obligation_id)
            if obligation is None:
                errors.append(f"artifact binding {sequence} names unknown obligation {obligation_id!r}")
                continue
            if obligation_id in bound_at:
                errors.append(f"obligation {obligation_id} is bound more than once")
                continue
            errors.extend(_validate_binding(record, obligation))
            bound_at[obligation_id] = sequence
            continue

        if label == "lifecycle transition":
            source = record.get("from_state")
            target = record.get("to_state")
            if not isinstance(source, str) or not isinstance(target, str):
                errors.append(f"lifecycle transition {sequence} states must be strings")
                continue
            if source != lifecycle_state:
                errors.append(
                    f"lifecycle transition {sequence} starts at {source!r}, "
                    f"but replay state is {lifecycle_state!r}"
                )
            if (source, target) not in LIFECYCLE_TRANSITIONS:
                errors.append(f"lifecycle transition {sequence} is not allowed: {source} -> {target}")
            for obligation in _obligations_for_lifecycle_edge(obligations, source, target):
                obligation_id = obligation.get("id")
                if obligation_id not in bound_at:
                    errors.append(
                        f"obligation {obligation_id} must be bound before lifecycle transition "
                        f"{source} -> {target}"
                    )
            if target == "completion_claimed":
                final_cursor = (len(focus_sequence) - 1, "exited")
                if cursor != final_cursor:
                    errors.append(
                        f"lifecycle transition {sequence} cannot claim completion before "
                        "the final phase has exited"
                    )
            if target == "blocked":
                if sequence not in block_context_by_transition:
                    errors.append(f"blocked transition {sequence} requires a matching block_context")
                active_block_sequence = sequence
            elif source == "blocked" and target == "executing":
                context = (
                    block_context_by_transition.get(active_block_sequence)
                    if active_block_sequence is not None
                    else None
                )
                if context is None or context.get("resume_transition_sequence") != sequence:
                    errors.append(
                        f"resume transition {sequence} requires the active block_context "
                        "to name resume_transition_sequence"
                    )
                active_block_sequence = None
            lifecycle_state = target
            continue

        phase_index = record.get("phase_index")
        checkpoint = record.get("kind")
        if lifecycle_state != "executing":
            errors.append(
                f"phase event {sequence} is invalid while lifecycle state is {lifecycle_state}; "
                "phase events require executing"
            )

        expected = _expected_phase_event(cursor, focus_sequence)
        actual = (phase_index, checkpoint)
        if expected is None:
            errors.append(f"phase event {sequence} occurs after the final phase exited")
        elif actual != expected:
            errors.append(f"phase event {sequence} must be {expected}, got {actual}")

        if not isinstance(checkpoint, str):
            errors.append(f"phase event {sequence} kind must be a string")
        elif not isinstance(phase_index, int) or isinstance(phase_index, bool):
            errors.append(f"phase event {sequence} phase_index must be an integer")
        elif phase_index < 0 or phase_index >= len(focus_sequence):
            errors.append(f"phase event {sequence} phase_index is outside workflow.focus_sequence")
        else:
            expected_phase = focus_sequence[phase_index]
            if record.get("phase") != expected_phase:
                errors.append(
                    f"phase event {sequence} phase does not match focus_sequence[{phase_index}]"
                )
            for obligation in _obligations_for_phase_event(obligations, phase_index, checkpoint):
                obligation_id = obligation.get("id")
                if obligation_id not in bound_at:
                    errors.append(
                        f"obligation {obligation_id} must be bound before phase event "
                        f"{phase_index}:{checkpoint}"
                    )
            cursor = (phase_index, checkpoint)

    if lifecycle_state != state.get("lifecycle_state"):
        errors.append(
            f"declared lifecycle_state {state.get('lifecycle_state')!r} does not match "
            f"replayed state {lifecycle_state!r}"
        )

    transition_records = _transition_by_sequence(state)
    for block_sequence, context in block_context_by_transition.items():
        block_transition = transition_records.get(block_sequence)
        if not isinstance(block_transition, dict) or block_transition.get("to_state") != "blocked":
            errors.append(f"block_context {block_sequence} does not identify a blocked transition")
        resume_sequence = context.get("resume_transition_sequence")
        if resume_sequence is not None:
            resume_transition = transition_records.get(resume_sequence)
            if not isinstance(resume_transition, dict) or (
                resume_transition.get("from_state"), resume_transition.get("to_state")
            ) != ("blocked", "executing"):
                errors.append(
                    f"block_context {block_sequence} resume_transition_sequence is not blocked -> executing"
                )

    declared_cursor = state.get("workflow_cursor")
    if cursor is None:
        if declared_cursor is not None:
            errors.append("workflow_cursor must be absent before the first phase event")
    else:
        replayed_cursor = {
            "phase_index": cursor[0],
            "phase": focus_sequence[cursor[0]],
            "checkpoint": cursor[1],
        }
        if declared_cursor != replayed_cursor:
            errors.append("workflow_cursor does not match the replayed phase event cursor")

    errors.extend(validate_completion_attempts(state, route))

    if errors:
        return ValidationResult(AUTHORITY_STRUCTURAL, errors)
    if not authority_mode or approved_route_digest is None or not is_canonical_current:
        return ValidationResult(AUTHORITY_STRUCTURAL, [])
    if lifecycle_state == "rerouted":
        return ValidationResult(AUTHORITY_STRUCTURAL, [])
    if lifecycle_state in {"verified", "completed"}:
        try:
            completion_digest = terminal_authority_digest(state)
        except ValueError as exc:
            return ValidationResult(AUTHORITY_STRUCTURAL, [str(exc)])
        if not terminal_validation_passed:
            return ValidationResult(
                AUTHORITY_STRUCTURAL,
                [f"{lifecycle_state} state requires terminal completion authorization"],
            )
        if approved_completion_digest is None:
            return ValidationResult(
                AUTHORITY_STRUCTURAL,
                [
                    "terminal authority requires an operator completion pin; "
                    f"candidate completion digest is {completion_digest}"
                ],
                candidate_completion_digest=completion_digest,
            )
        if approved_completion_digest != completion_digest:
            return ValidationResult(
                AUTHORITY_STRUCTURAL,
                ["operator completion pin does not match the terminal authority digest"],
            )
        return ValidationResult(AUTHORITY_TERMINAL, [])
    return ValidationResult(AUTHORITY_GATE, [])
