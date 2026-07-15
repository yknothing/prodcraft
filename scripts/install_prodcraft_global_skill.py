#!/usr/bin/env python3
"""Install, migrate, or remove the global `pc-prodcraft` gateway skill."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from functools import wraps
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

try:
    import fcntl
except ImportError:  # pragma: no cover - the global installer currently requires POSIX locking
    fcntl = None

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from prodcraft_gateway_skill import render_prodcraft_skill


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET_ROOT = Path.home() / ".agents" / "skills"
DEFAULT_STATE_PATH = REPO_ROOT / "build" / "prodcraft-global-skill-state.json"
DEFAULT_LOG_PATH = REPO_ROOT / "build" / "prodcraft-global-skill-events.jsonl"
LEGACY_SKILL_NAME = "prodcraft"
SKILL_NAME = "pc-prodcraft"
RUNTIME_LOCATOR_FILENAME = "prodcraft-runtime.json"
MANAGED_FILENAMES = frozenset({"SKILL.md", RUNTIME_LOCATOR_FILENAME})
LOCK_FILENAME = ".pc-prodcraft.lock"


class SkillInstallConflict(RuntimeError):
    """Raised when an install path cannot be proven safe to mutate."""


def serialized_target_mutation(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        if fcntl is None:
            raise SkillInstallConflict("global gateway mutation requires POSIX advisory file locking")
        target_root = Path(kwargs["target_root"])
        target_root.mkdir(parents=True, exist_ok=True)
        lock_path = target_root / LOCK_FILENAME
        flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
        try:
            descriptor = os.open(lock_path, flags, 0o600)
        except OSError as exc:
            raise SkillInstallConflict(f"installer lock is not a safe regular file: {lock_path}") from exc
        with os.fdopen(descriptor, "r+") as lock_handle:
            if not stat.S_ISREG(os.fstat(lock_handle.fileno()).st_mode):
                raise SkillInstallConflict(f"installer lock is not a regular file: {lock_path}")
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
            return function(*args, **kwargs)

    return wrapped


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def append_jsonl(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o600)
    with os.fdopen(descriptor, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def write_state(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def snapshot_file(path: Path) -> bytes | None:
    return path.read_bytes() if path.exists() else None


def restore_file(path: Path, snapshot: bytes | None) -> None:
    if snapshot is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.rollback-",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(snapshot)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def read_state(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def absolute_without_resolving(path: Path) -> Path:
    return Path(os.path.abspath(os.path.expanduser(str(path))))


def canonicalize_system_path_alias(path: Path) -> Path:
    """Normalize only well-known root-owned macOS aliases before symlink checks."""
    for alias in (Path("/var"), Path("/tmp"), Path("/etc")):
        if path != alias and alias not in path.parents:
            continue
        try:
            if not alias.is_symlink() or alias.lstat().st_uid != 0:
                continue
            target = alias.resolve(strict=True)
        except (OSError, RuntimeError):
            continue
        return target / path.relative_to(alias)
    return path


def assert_safe_observability_path(
    path: Path,
    *,
    label: str,
    require_writable: bool = False,
) -> Path:
    absolute = canonicalize_system_path_alias(absolute_without_resolving(path))
    if absolute.is_symlink():
        raise SkillInstallConflict(f"{label} path must not be a symlink: {absolute}")

    current = Path(absolute.anchor)
    for part in absolute.parts[1:-1]:
        current /= part
        if current.is_symlink():
            raise SkillInstallConflict(f"{label} path contains a symlink: {current}")
        if current.exists() and not current.is_dir():
            raise SkillInstallConflict(f"{label} parent is not a directory: {current}")

    if absolute.exists() and not absolute.is_file():
        raise SkillInstallConflict(f"{label} path must be a regular file: {absolute}")

    nearest_parent = absolute.parent
    while not nearest_parent.exists():
        nearest_parent = nearest_parent.parent
    if not nearest_parent.is_dir():
        raise SkillInstallConflict(f"{label} parent is not a safe directory: {nearest_parent}")
    if require_writable and not os.access(nearest_parent, os.W_OK | os.X_OK):
        raise SkillInstallConflict(f"{label} parent is not writable: {nearest_parent}")
    return absolute


def preflight_observability_paths(
    *,
    state_path: Path,
    log_path: Path,
    forbidden_roots: tuple[Path, ...] = (),
) -> tuple[Path, Path]:
    state_absolute = assert_safe_observability_path(
        state_path,
        label="state",
        require_writable=True,
    )
    log_absolute = assert_safe_observability_path(
        log_path,
        label="event log",
        require_writable=True,
    )
    if state_absolute == log_absolute:
        raise SkillInstallConflict("state and event log paths must be different")

    for output_path, label in ((state_absolute, "state"), (log_absolute, "event log")):
        for forbidden_root in forbidden_roots:
            root_absolute = absolute_without_resolving(forbidden_root).resolve(strict=False)
            if output_path == root_absolute or root_absolute in output_path.parents:
                raise SkillInstallConflict(f"{label} path must not be inside managed gateway {root_absolute}")
    return state_absolute, log_absolute


def skill_dir(target_root: Path) -> Path:
    return target_root / SKILL_NAME


def legacy_skill_dir(target_root: Path) -> Path:
    return target_root / LEGACY_SKILL_NAME


def runtime_locator_path(target_root: Path) -> Path:
    return skill_dir(target_root) / RUNTIME_LOCATOR_FILENAME


def runtime_locator_payload(*, target_root: Path, repo_root: Path) -> Dict[str, object]:
    return {
        "schema_version": "prodcraft-runtime-locator.v1",
        "skill_name": SKILL_NAME,
        "install_surface": "global",
        "global_skill_path": str(skill_dir(target_root)),
        "canonical_repo_root": str(repo_root),
        "gateway_path": str(repo_root / "skills" / "_gateway.md"),
        "source_skills_root": str(repo_root / "skills"),
        "workflow_root": str(repo_root / "workflows"),
        "curated_sibling_root_hint": str(target_root),
        "singleton_gateway_directory_is_expected": True,
    }


def _frontmatter_name(skill_path: Path) -> str | None:
    try:
        text = skill_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", text)
    return match.group(1) if match else None


def assert_managed_gateway(
    path: Path,
    *,
    expected_name: str,
    repo_root: Path,
    expected_install_path: Path | None = None,
) -> None:
    if path.is_symlink() or not path.is_dir():
        raise SkillInstallConflict(f"{path} is not a managed gateway directory")

    entries = list(path.iterdir())
    entry_names = {entry.name for entry in entries}
    unmanaged = sorted(entry_names - MANAGED_FILENAMES)
    if unmanaged:
        raise SkillInstallConflict(f"{path} contains unmanaged entries: {unmanaged}")
    if entry_names != MANAGED_FILENAMES:
        missing = sorted(MANAGED_FILENAMES - entry_names)
        raise SkillInstallConflict(f"{path} is not a managed gateway; missing files: {missing}")
    if any(entry.is_symlink() or not entry.is_file() for entry in entries):
        raise SkillInstallConflict(f"{path} is not a managed gateway; managed files must be regular files")

    skill_path = path / "SKILL.md"
    if _frontmatter_name(skill_path) != expected_name:
        raise SkillInstallConflict(f"{path} is not a managed {expected_name} gateway")

    locator_path = path / RUNTIME_LOCATOR_FILENAME
    try:
        locator = json.loads(locator_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SkillInstallConflict(f"{path} has an invalid runtime locator") from exc

    expected = {
        "schema_version": "prodcraft-runtime-locator.v1",
        "skill_name": expected_name,
        "install_surface": "global",
    }
    for field, value in expected.items():
        if locator.get(field) != value:
            raise SkillInstallConflict(f"{path} runtime locator has invalid {field}")

    try:
        locator_skill_path = Path(locator["global_skill_path"]).expanduser().resolve()
        locator_repo_root = Path(locator["canonical_repo_root"]).expanduser().resolve()
    except (KeyError, TypeError, OSError) as exc:
        raise SkillInstallConflict(f"{path} runtime locator is missing ownership fields") from exc
    owned_install_path = expected_install_path or path
    if locator_skill_path != owned_install_path.resolve():
        raise SkillInstallConflict(f"{path} runtime locator does not own this skill path")
    if locator_repo_root != repo_root.resolve():
        raise SkillInstallConflict(f"{path} runtime locator belongs to another repository")


def log_event(
    *,
    log_path: Path,
    action: str,
    status_before: str,
    status_after: str,
    target_root: Path,
    reason: Optional[str],
) -> None:
    append_jsonl(
        log_path,
        {
            "timestamp": utc_now_iso(),
            "action": action,
            "status_before": status_before,
            "status_after": status_after,
            "target_root": str(target_root),
            "skill_name": SKILL_NAME,
            "skill_path": str(skill_dir(target_root)),
            "reason": reason,
        },
    )


def persist_state(
    *,
    state_path: Path,
    status_snapshot: Dict[str, object],
    action: str,
    reason: Optional[str],
    extra_fields: Optional[Dict[str, object]] = None,
) -> Dict[str, object]:
    payload = dict(status_snapshot)
    payload.update(
        {
            "skill_name": SKILL_NAME,
            "last_action": action,
            "reason": reason,
            "updated_at": utc_now_iso(),
        }
    )
    if extra_fields:
        payload.update(extra_fields)
    write_state(state_path, payload)
    return payload


def get_status(*, target_root: Path, state_path: Path, repo_root: Path = REPO_ROOT) -> Dict[str, object]:
    state_path = assert_safe_observability_path(state_path, label="state")
    skill_path = skill_dir(target_root)
    locator_path = runtime_locator_path(target_root)
    skill_exists = skill_path.exists() or skill_path.is_symlink()
    snapshot = {
        "status": "missing",
        "skill_exists": skill_exists,
        "skill_path": str(skill_path),
        "legacy_skill_exists": legacy_skill_dir(target_root).exists() or legacy_skill_dir(target_root).is_symlink(),
    }
    if skill_exists:
        try:
            assert_managed_gateway(skill_path, expected_name=SKILL_NAME, repo_root=repo_root)
        except SkillInstallConflict as exc:
            snapshot["status"] = "conflict"
            snapshot["managed"] = False
            snapshot["conflict_reason"] = str(exc)
        else:
            snapshot["status"] = "installed"
            snapshot["managed"] = True
        snapshot["runtime_locator_path"] = str(locator_path)
        snapshot["runtime_locator_exists"] = locator_path.exists()
    state = read_state(state_path)
    if state:
        snapshot["state_file"] = str(state_path)
        snapshot["last_action"] = state.get("last_action")
        snapshot["reason"] = state.get("reason")
        snapshot["updated_at"] = state.get("updated_at")
    return snapshot


@serialized_target_mutation
def install_skill(
    *,
    target_root: Path,
    repo_root: Path,
    state_path: Path,
    log_path: Path,
    reason: Optional[str],
) -> Dict[str, object]:
    target = skill_dir(target_root)
    legacy = legacy_skill_dir(target_root)
    state_path, log_path = preflight_observability_paths(
        state_path=state_path,
        log_path=log_path,
        forbidden_roots=(target, legacy),
    )
    status_before = get_status(target_root=target_root, state_path=state_path, repo_root=repo_root)
    if target.exists() or target.is_symlink():
        assert_managed_gateway(target, expected_name=SKILL_NAME, repo_root=repo_root)
    if legacy.exists() or legacy.is_symlink():
        assert_managed_gateway(legacy, expected_name=LEGACY_SKILL_NAME, repo_root=repo_root)

    target_root.mkdir(parents=True, exist_ok=True)
    legacy_removed = legacy.exists()
    state_before = snapshot_file(state_path)
    log_before = snapshot_file(log_path)
    with tempfile.TemporaryDirectory(prefix=".pc-prodcraft-install-", dir=target_root) as tmpdir:
        transaction_root = Path(tmpdir)
        staged = transaction_root / "staged"
        staged.mkdir()
        (staged / "SKILL.md").write_text(
            render_prodcraft_skill(
                repo_root,
                install_surface="global",
                public_stability="beta",
                public_readiness="core",
            ),
            encoding="utf-8",
        )
        (staged / RUNTIME_LOCATOR_FILENAME).write_text(
            json.dumps(runtime_locator_payload(target_root=target_root, repo_root=repo_root), indent=2) + "\n",
            encoding="utf-8",
        )

        current_backup = transaction_root / "current-backup"
        legacy_backup = transaction_root / "legacy-backup"
        try:
            if target.exists() or target.is_symlink():
                target.rename(current_backup)
                assert_managed_gateway(
                    current_backup,
                    expected_name=SKILL_NAME,
                    repo_root=repo_root,
                    expected_install_path=target,
                )
            if legacy.exists() or legacy.is_symlink():
                legacy.rename(legacy_backup)
                assert_managed_gateway(
                    legacy_backup,
                    expected_name=LEGACY_SKILL_NAME,
                    repo_root=repo_root,
                    expected_install_path=legacy,
                )
            staged.rename(target)
            status_after = get_status(target_root=target_root, state_path=state_path, repo_root=repo_root)
            result = persist_state(
                state_path=state_path,
                status_snapshot=status_after,
                action="install",
                reason=reason,
                extra_fields={"legacy_skill_removed": legacy_removed},
            )
            log_event(
                log_path=log_path,
                action="install",
                status_before=status_before["status"],
                status_after=status_after["status"],
                target_root=target_root,
                reason=reason,
            )
        except BaseException:
            if target.exists() or target.is_symlink():
                failed_target = transaction_root / "failed-target"
                target.rename(failed_target)
                try:
                    assert_managed_gateway(
                        failed_target,
                        expected_name=SKILL_NAME,
                        repo_root=repo_root,
                        expected_install_path=target,
                    )
                except SkillInstallConflict:
                    if not (target.exists() or target.is_symlink()):
                        failed_target.rename(target)
            if current_backup.exists() and not target.exists():
                current_backup.rename(target)
            if legacy_backup.exists() and not legacy.exists():
                legacy_backup.rename(legacy)
            restore_file(state_path, state_before)
            restore_file(log_path, log_before)
            raise
    return result


@serialized_target_mutation
def remove_skill(
    *,
    target_root: Path,
    state_path: Path,
    log_path: Path,
    reason: Optional[str],
    repo_root: Path = REPO_ROOT,
) -> Dict[str, object]:
    target = skill_dir(target_root)
    state_path, log_path = preflight_observability_paths(
        state_path=state_path,
        log_path=log_path,
        forbidden_roots=(target, legacy_skill_dir(target_root)),
    )
    status_before = get_status(target_root=target_root, state_path=state_path, repo_root=repo_root)
    state_before = snapshot_file(state_path)
    log_before = snapshot_file(log_path)
    if not (target.exists() or target.is_symlink()):
        try:
            status_after = get_status(target_root=target_root, state_path=state_path, repo_root=repo_root)
            status_after["status"] = "removed"
            log_event(
                log_path=log_path,
                action="remove",
                status_before=status_before["status"],
                status_after=status_after["status"],
                target_root=target_root,
                reason=reason,
            )
            return persist_state(
                state_path=state_path,
                status_snapshot=status_after,
                action="remove",
                reason=reason,
            )
        except BaseException:
            restore_file(state_path, state_before)
            restore_file(log_path, log_before)
            raise

    assert_managed_gateway(target, expected_name=SKILL_NAME, repo_root=repo_root)
    with tempfile.TemporaryDirectory(prefix=".pc-prodcraft-remove-", dir=target_root) as tmpdir:
        quarantine = Path(tmpdir) / "quarantine"
        try:
            target.rename(quarantine)
            assert_managed_gateway(
                quarantine,
                expected_name=SKILL_NAME,
                repo_root=repo_root,
                expected_install_path=target,
            )
            status_after = get_status(target_root=target_root, state_path=state_path, repo_root=repo_root)
            status_after["status"] = "removed"
            log_event(
                log_path=log_path,
                action="remove",
                status_before=status_before["status"],
                status_after=status_after["status"],
                target_root=target_root,
                reason=reason,
            )
            result = persist_state(
                state_path=state_path,
                status_snapshot=status_after,
                action="remove",
                reason=reason,
            )
        except BaseException:
            if quarantine.exists() and not (target.exists() or target.is_symlink()):
                quarantine.rename(target)
            restore_file(state_path, state_before)
            restore_file(log_path, log_before)
            raise
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install or remove the global pc-prodcraft gateway skill.")
    parser.add_argument("action", choices=("status", "install", "remove"))
    parser.add_argument("--target-root", type=Path, default=DEFAULT_TARGET_ROOT)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--state-path", type=Path, default=DEFAULT_STATE_PATH)
    parser.add_argument("--log-path", type=Path, default=DEFAULT_LOG_PATH)
    parser.add_argument("--reason", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        if args.action == "status":
            payload = get_status(
                target_root=args.target_root,
                state_path=args.state_path,
                repo_root=args.repo_root,
            )
        elif args.action == "install":
            payload = install_skill(
                target_root=args.target_root,
                repo_root=args.repo_root,
                state_path=args.state_path,
                log_path=args.log_path,
                reason=args.reason,
            )
        else:
            payload = remove_skill(
                target_root=args.target_root,
                state_path=args.state_path,
                log_path=args.log_path,
                reason=args.reason,
                repo_root=args.repo_root,
            )
    except SkillInstallConflict as exc:
        print(json.dumps({"status": "conflict", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
