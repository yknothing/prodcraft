#!/usr/bin/env python3
"""Temporarily disable or restore the global brainstorming skill for Prodcraft experiments."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_ROOT = Path.home() / ".agents" / "skills"
DEFAULT_STATE_PATH = REPO_ROOT / "build" / "brainstorming-gate-state.json"
DEFAULT_LOG_PATH = REPO_ROOT / "build" / "brainstorming-gate-events.jsonl"
SKILL_NAME = "brainstorming"
DISABLED_DIRNAME = ".disabled-prodcraft-brainstorming"


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


def current_paths(skills_root: Path) -> Dict[str, Path]:
    return {
        "original": skills_root / SKILL_NAME,
        "disabled": skills_root / DISABLED_DIRNAME,
    }


def determine_status(skills_root: Path) -> Dict[str, object]:
    paths = current_paths(skills_root)
    original_exists = paths["original"].exists()
    disabled_exists = paths["disabled"].exists()

    if original_exists and disabled_exists:
        raise RuntimeError(
            "Inconsistent brainstorming gate state: both the original and disabled directories exist."
        )
    if original_exists:
        status = "enabled"
    elif disabled_exists:
        status = "disabled"
    else:
        status = "missing"

    return {
        "status": status,
        "brainstorming_exists": original_exists,
        "disabled_dir_exists": disabled_exists,
        "original_path": str(paths["original"]),
        "disabled_path": str(paths["disabled"]),
    }


def log_event(
    *,
    log_path: Path,
    action: str,
    status_before: str,
    status_after: str,
    skills_root: Path,
    reason: Optional[str],
) -> None:
    paths = current_paths(skills_root)
    append_jsonl(
        log_path,
        {
            "timestamp": utc_now_iso(),
            "action": action,
            "status_before": status_before,
            "status_after": status_after,
            "skills_root": str(skills_root),
            "skill_name": SKILL_NAME,
            "original_path": str(paths["original"]),
            "disabled_path": str(paths["disabled"]),
            "reason": reason,
        },
    )


def persist_state(
    *,
    state_path: Path,
    status_snapshot: Dict[str, object],
    action: str,
    reason: Optional[str],
) -> None:
    payload = dict(status_snapshot)
    payload.update(
        {
            "skill_name": SKILL_NAME,
            "disabled_dirname": DISABLED_DIRNAME,
            "last_action": action,
            "reason": reason,
            "updated_at": utc_now_iso(),
        }
    )
    write_state(state_path, payload)


def get_status(*, skills_root: Path, state_path: Path) -> Dict[str, object]:
    status_snapshot = determine_status(skills_root)
    state = read_state(state_path)
    if state:
        status_snapshot["state_file"] = str(state_path)
        status_snapshot["last_action"] = state.get("last_action")
        status_snapshot["reason"] = state.get("reason")
        status_snapshot["updated_at"] = state.get("updated_at")
    return status_snapshot


def disable_brainstorming(
    *,
    skills_root: Path,
    state_path: Path,
    log_path: Path,
    reason: Optional[str],
) -> Dict[str, object]:
    status_before = determine_status(skills_root)
    paths = current_paths(skills_root)

    if status_before["status"] == "enabled":
        paths["original"].rename(paths["disabled"])
    elif status_before["status"] == "missing":
        raise RuntimeError(f"Cannot disable brainstorming because `{paths['original']}` does not exist.")

    status_after = determine_status(skills_root)
    log_event(
        log_path=log_path,
        action="disable",
        status_before=status_before["status"],
        status_after=status_after["status"],
        skills_root=skills_root,
        reason=reason,
    )
    persist_state(
        state_path=state_path,
        status_snapshot=status_after,
        action="disable",
        reason=reason,
    )
    return status_after


def enable_brainstorming(
    *,
    skills_root: Path,
    state_path: Path,
    log_path: Path,
    reason: Optional[str],
) -> Dict[str, object]:
    status_before = determine_status(skills_root)
    paths = current_paths(skills_root)

    if status_before["status"] == "disabled":
        paths["disabled"].rename(paths["original"])
    elif status_before["status"] == "missing":
        raise RuntimeError(f"Cannot enable brainstorming because `{paths['disabled']}` does not exist.")

    status_after = determine_status(skills_root)
    log_event(
        log_path=log_path,
        action="enable",
        status_before=status_before["status"],
        status_after=status_after["status"],
        skills_root=skills_root,
        reason=reason,
    )
    persist_state(
        state_path=state_path,
        status_snapshot=status_after,
        action="enable",
        reason=reason,
    )
    return status_after


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Temporarily disable or restore the global brainstorming skill for Prodcraft experiments."
    )
    parser.add_argument("action", choices=("status", "disable", "enable"))
    parser.add_argument("--skills-root", type=Path, default=DEFAULT_SKILLS_ROOT)
    parser.add_argument("--state-path", type=Path, default=DEFAULT_STATE_PATH)
    parser.add_argument("--log-path", type=Path, default=DEFAULT_LOG_PATH)
    parser.add_argument("--reason", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        if args.action == "status":
            payload = get_status(skills_root=args.skills_root, state_path=args.state_path)
        elif args.action == "disable":
            payload = disable_brainstorming(
                skills_root=args.skills_root,
                state_path=args.state_path,
                log_path=args.log_path,
                reason=args.reason,
            )
        else:
            payload = enable_brainstorming(
                skills_root=args.skills_root,
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
