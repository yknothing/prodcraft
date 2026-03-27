#!/usr/bin/env python3
"""Archive or restore conflicting global superpowers skills during Prodcraft cutover."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_ROOT = Path.home() / ".agents" / "skills"
DEFAULT_ARCHIVE_ROOT = Path.home() / ".agents" / "skills-archive" / "prodcraft-superpowers"
DEFAULT_STATE_PATH = REPO_ROOT / "build" / "superpowers-archive-state.json"
DEFAULT_LOG_PATH = REPO_ROOT / "build" / "superpowers-archive-events.jsonl"
MANAGED_DIRNAMES = (
    "brainstorming",
    ".disabled-prodcraft-brainstorming",
    "using-superpowers",
    "writing-plans",
    "executing-plans",
    "systematic-debugging",
    "test-driven-development",
    "requesting-code-review",
    "receiving-code-review",
    "verification-before-completion",
    "finishing-a-development-branch",
    "software-architecture",
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def append_jsonl(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def read_state(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_state(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def managed_paths(root: Path) -> Dict[str, Path]:
    return {dirname: root / dirname for dirname in MANAGED_DIRNAMES}


def determine_status(*, skills_root: Path, archive_root: Path) -> Dict[str, object]:
    source_paths = managed_paths(skills_root)
    archive_paths = managed_paths(archive_root)

    present = sorted(dirname for dirname, path in source_paths.items() if path.exists())
    archived = sorted(dirname for dirname, path in archive_paths.items() if path.exists())
    missing = sorted(dirname for dirname in MANAGED_DIRNAMES if dirname not in present and dirname not in archived)

    if present and archived:
        status = "mixed"
    elif present:
        status = "source-present"
    elif archived:
        status = "archived"
    else:
        status = "missing"

    return {
        "status": status,
        "skills_root": str(skills_root),
        "archive_root": str(archive_root),
        "managed_dirnames": list(MANAGED_DIRNAMES),
        "present": present,
        "archived": archived,
        "missing": missing,
        "present_count": len(present),
        "archived_count": len(archived),
    }


def log_event(
    *,
    log_path: Path,
    action: str,
    status_before: str,
    status_after: str,
    skills_root: Path,
    archive_root: Path,
    moved_dirnames: list[str],
    reason: Optional[str],
) -> None:
    append_jsonl(
        log_path,
        {
            "timestamp": utc_now_iso(),
            "action": action,
            "status_before": status_before,
            "status_after": status_after,
            "skills_root": str(skills_root),
            "archive_root": str(archive_root),
            "managed_dirnames": list(MANAGED_DIRNAMES),
            "moved_dirnames": moved_dirnames,
            "reason": reason,
        },
    )


def persist_state(
    *,
    state_path: Path,
    status_snapshot: Dict[str, object],
    action: str,
    reason: Optional[str],
) -> Dict[str, object]:
    payload = dict(status_snapshot)
    payload.update(
        {
            "last_action": action,
            "reason": reason,
            "updated_at": utc_now_iso(),
        }
    )
    write_state(state_path, payload)
    return payload


def get_status(*, skills_root: Path, archive_root: Path, state_path: Path) -> Dict[str, object]:
    snapshot = determine_status(skills_root=skills_root, archive_root=archive_root)
    state = read_state(state_path)
    if state:
        snapshot["state_file"] = str(state_path)
        snapshot["last_action"] = state.get("last_action")
        snapshot["reason"] = state.get("reason")
        snapshot["updated_at"] = state.get("updated_at")
    return snapshot


def archive_skills(
    *,
    skills_root: Path,
    archive_root: Path,
    state_path: Path,
    log_path: Path,
    reason: Optional[str],
) -> Dict[str, object]:
    status_before = determine_status(skills_root=skills_root, archive_root=archive_root)
    archive_root.mkdir(parents=True, exist_ok=True)

    moved_dirnames: list[str] = []
    for dirname, source in managed_paths(skills_root).items():
        if not source.exists():
            continue
        destination = archive_root / dirname
        if destination.exists():
            raise RuntimeError(f"Cannot archive `{source}` because `{destination}` already exists.")
        source.rename(destination)
        moved_dirnames.append(dirname)

    status_after = determine_status(skills_root=skills_root, archive_root=archive_root)
    log_event(
        log_path=log_path,
        action="archive",
        status_before=status_before["status"],
        status_after=status_after["status"],
        skills_root=skills_root,
        archive_root=archive_root,
        moved_dirnames=moved_dirnames,
        reason=reason,
    )
    return persist_state(
        state_path=state_path,
        status_snapshot=status_after,
        action="archive",
        reason=reason,
    )


def restore_skills(
    *,
    skills_root: Path,
    archive_root: Path,
    state_path: Path,
    log_path: Path,
    reason: Optional[str],
) -> Dict[str, object]:
    status_before = determine_status(skills_root=skills_root, archive_root=archive_root)

    moved_dirnames: list[str] = []
    for dirname, archived in managed_paths(archive_root).items():
        if not archived.exists():
            continue
        destination = skills_root / dirname
        if destination.exists():
            raise RuntimeError(f"Cannot restore `{archived}` because `{destination}` already exists.")
        skills_root.mkdir(parents=True, exist_ok=True)
        archived.rename(destination)
        moved_dirnames.append(dirname)

    status_after = determine_status(skills_root=skills_root, archive_root=archive_root)
    log_event(
        log_path=log_path,
        action="restore",
        status_before=status_before["status"],
        status_after=status_after["status"],
        skills_root=skills_root,
        archive_root=archive_root,
        moved_dirnames=moved_dirnames,
        reason=reason,
    )
    return persist_state(
        state_path=state_path,
        status_snapshot=status_after,
        action="restore",
        reason=reason,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Archive or restore conflicting global superpowers skill directories during Prodcraft cutover."
    )
    parser.add_argument("action", choices=("status", "archive", "restore"))
    parser.add_argument("--skills-root", type=Path, default=DEFAULT_SKILLS_ROOT)
    parser.add_argument("--archive-root", type=Path, default=DEFAULT_ARCHIVE_ROOT)
    parser.add_argument("--state-path", type=Path, default=DEFAULT_STATE_PATH)
    parser.add_argument("--log-path", type=Path, default=DEFAULT_LOG_PATH)
    parser.add_argument("--reason", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        if args.action == "status":
            payload = get_status(
                skills_root=args.skills_root,
                archive_root=args.archive_root,
                state_path=args.state_path,
            )
        elif args.action == "archive":
            payload = archive_skills(
                skills_root=args.skills_root,
                archive_root=args.archive_root,
                state_path=args.state_path,
                log_path=args.log_path,
                reason=args.reason,
            )
        else:
            payload = restore_skills(
                skills_root=args.skills_root,
                archive_root=args.archive_root,
                state_path=args.state_path,
                log_path=args.log_path,
                reason=args.reason,
            )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
