#!/usr/bin/env python3
"""Claude Code PreToolUse adapter for the legacy approved-intake gate.

This adapter mirrors repository-owned artifact validation. It does not grant
ADR-003 gate or terminal authority; strict authority still requires execution
state plus external route/completion pins.
"""

from __future__ import annotations

import errno
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


BLOCKING_EXIT = 2
MAX_HOOK_INPUT_BYTES = 1_048_576
MAX_BRIEF_BYTES = 1_048_576
VALIDATOR_TIMEOUT_SECONDS = 10
WORK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


@dataclass(frozen=True)
class FileSnapshot:
    data: bytes
    identity: tuple[int, int, int, int, int]


def block(message: str) -> int:
    print(f"Prodcraft blocked this write: {message}", file=sys.stderr)
    return BLOCKING_EXIT


def read_hook_input() -> dict:
    payload = sys.stdin.buffer.read(MAX_HOOK_INPUT_BYTES + 1)
    if len(payload) > MAX_HOOK_INPUT_BYTES:
        raise ValueError("hook input exceeds 1 MiB")
    parsed = json.loads(payload.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError("hook input must be a JSON object")
    return parsed


def safe_regular_file(path: Path, label: str, max_bytes: int) -> None:
    try:
        metadata = path.lstat()
    except FileNotFoundError as exc:
        raise ValueError(f"{label} is missing at {path}") from exc
    if stat.S_ISLNK(metadata.st_mode):
        raise ValueError(f"{label} must not be a symlink: {path}")
    if not stat.S_ISREG(metadata.st_mode):
        raise ValueError(f"{label} must be a regular file: {path}")
    if metadata.st_size > max_bytes:
        raise ValueError(f"{label} exceeds {max_bytes} bytes: {path}")


def _snapshot_identity(metadata: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def read_project_file_snapshot(
    project_root: Path,
    relative_path: Path,
    label: str,
    max_bytes: int,
) -> FileSnapshot:
    """Read a regular file beneath project_root without following symlinks."""
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ValueError(f"{label} path must stay beneath the project root")

    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    cloexec = getattr(os, "O_CLOEXEC", 0)
    descriptors: list[int] = []
    try:
        current_fd = os.open(project_root, directory_flags | cloexec)
        descriptors.append(current_fd)
        for component in relative_path.parts[:-1]:
            try:
                current_fd = os.open(
                    component,
                    directory_flags | nofollow | cloexec,
                    dir_fd=current_fd,
                )
            except OSError as exc:
                if exc.errno in {errno.ELOOP, errno.ENOTDIR}:
                    raise ValueError(
                        f"{label} path component must not be a symlink: {component}"
                    ) from exc
                raise
            descriptors.append(current_fd)

        try:
            file_fd = os.open(
                relative_path.name,
                os.O_RDONLY | nofollow | cloexec,
                dir_fd=current_fd,
            )
        except OSError as exc:
            if exc.errno == errno.ELOOP:
                raise ValueError(f"{label} must not be a symlink") from exc
            raise
        descriptors.append(file_fd)

        before = os.fstat(file_fd)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError(f"{label} must be a regular file")
        if before.st_size > max_bytes:
            raise ValueError(f"{label} exceeds {max_bytes} bytes")

        chunks: list[bytes] = []
        remaining = max_bytes + 1
        while remaining:
            chunk = os.read(file_fd, min(65_536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        if len(data) > max_bytes:
            raise ValueError(f"{label} exceeds {max_bytes} bytes")

        after = os.fstat(file_fd)
        if _snapshot_identity(before) != _snapshot_identity(after):
            raise ValueError(f"{label} changed while it was being read")
        return FileSnapshot(data=data, identity=_snapshot_identity(after))
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def run_repository_validator(project_root: Path, brief_path: Path) -> None:
    validator = project_root / "scripts" / "validate_prodcraft.py"
    safe_regular_file(validator, "repository validator", MAX_BRIEF_BYTES)
    try:
        result = subprocess.run(
            [
                sys.executable,
                str(validator),
                "--artifact-instance",
                str(brief_path),
                "--output-format",
                "json",
            ],
            cwd=project_root,
            text=True,
            capture_output=True,
            timeout=VALIDATOR_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"repository validator could not complete: {exc}") from exc
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise ValueError(f"repository validator rejected the intake brief: {detail or 'no details'}")
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("repository validator returned invalid JSON") from exc
    if not isinstance(output, dict) or output.get("status") != "valid" or output.get("errors") != []:
        raise ValueError("repository validator did not return a clean `valid` result")


def main() -> int:
    try:
        hook_input = read_hook_input()
        if hook_input.get("hook_event_name") != "PreToolUse":
            return block("unexpected hook event; expected PreToolUse")
        tool_name = hook_input.get("tool_name")
        if tool_name not in {"Edit", "Write"}:
            return 0
        tool_input = hook_input.get("tool_input")
        if not isinstance(tool_input, dict) or not isinstance(tool_input.get("file_path"), str):
            return block("Edit/Write input must include string tool_input.file_path")

        project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
        if not project_dir:
            return block("CLAUDE_PROJECT_DIR is not set")
        project_root = Path(project_dir).resolve(strict=True)
        if not project_root.is_dir():
            return block(f"CLAUDE_PROJECT_DIR is not a directory: {project_root}")

        work_id = os.environ.get("PRODCRAFT_WORK_ID")
        if not work_id or not WORK_ID_RE.fullmatch(work_id):
            return block("set PRODCRAFT_WORK_ID to a safe current work identifier")

        brief_relative = Path(".prodcraft") / "artifacts" / work_id / "intake-brief.json"
        brief_path = project_root / brief_relative
        requested_path = Path(tool_input["file_path"])
        if not requested_path.is_absolute():
            return block("Claude Edit/Write file_path must be absolute")
        requested_normalized = Path(os.path.realpath(os.path.normpath(requested_path)))

        try:
            approved_snapshot = read_project_file_snapshot(
                project_root,
                brief_relative,
                "intake brief",
                MAX_BRIEF_BYTES,
            )
        except FileNotFoundError:
            if tool_name == "Write" and requested_normalized == brief_path:
                return 0
            return block(
                f"approved intake brief is missing at {brief_path}; bootstrap it with Write first"
            )

        with tempfile.TemporaryDirectory(prefix="prodcraft-intake-snapshot-") as temp_dir:
            validation_path = Path(temp_dir) / "intake-brief.json"
            validation_path.write_bytes(approved_snapshot.data)
            run_repository_validator(project_root, validation_path)

        current_snapshot = read_project_file_snapshot(
            project_root,
            brief_relative,
            "intake brief",
            MAX_BRIEF_BYTES,
        )
        if current_snapshot != approved_snapshot:
            return block("intake brief changed during validation; retry with a stable approved brief")

        brief = json.loads(approved_snapshot.data.decode("utf-8"))
        if brief.get("status") != "approved":
            return block("intake brief status must be `approved`")
        approver = brief.get("approver")
        if not isinstance(approver, str) or not approver.strip():
            return block("intake brief approver must be non-empty")
        if brief.get("intake_mode") == "micro":
            return block(
                "micro intake does not grant blocking host-adapter authority; use fast-track/full/resume"
            )
        return 0
    except Exception as exc:
        return block(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
