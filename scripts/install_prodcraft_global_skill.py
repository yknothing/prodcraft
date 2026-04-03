#!/usr/bin/env python3
"""Install or remove a global `prodcraft` gateway skill for this repository."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

import shutil

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from prodcraft_gateway_skill import render_prodcraft_skill


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET_ROOT = Path.home() / ".agents" / "skills"
DEFAULT_STATE_PATH = REPO_ROOT / "build" / "prodcraft-global-skill-state.json"
DEFAULT_LOG_PATH = REPO_ROOT / "build" / "prodcraft-global-skill-events.jsonl"
SKILL_NAME = "prodcraft"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def append_jsonl(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def write_state(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_state(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def skill_dir(target_root: Path) -> Path:
    return target_root / SKILL_NAME


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
    write_state(state_path, payload)
    return payload


def get_status(*, target_root: Path, state_path: Path) -> Dict[str, object]:
    skill_path = skill_dir(target_root)
    snapshot = {
        "status": "installed" if skill_path.exists() else "missing",
        "skill_exists": skill_path.exists(),
        "skill_path": str(skill_path),
    }
    state = read_state(state_path)
    if state:
        snapshot["state_file"] = str(state_path)
        snapshot["last_action"] = state.get("last_action")
        snapshot["reason"] = state.get("reason")
        snapshot["updated_at"] = state.get("updated_at")
    return snapshot


def install_skill(
    *,
    target_root: Path,
    repo_root: Path,
    state_path: Path,
    log_path: Path,
    reason: Optional[str],
) -> Dict[str, object]:
    status_before = get_status(target_root=target_root, state_path=state_path)
    target = skill_dir(target_root)
    target.mkdir(parents=True, exist_ok=True)
    (target / "SKILL.md").write_text(
        render_prodcraft_skill(
            repo_root,
            install_surface="global",
            public_stability="beta",
            public_readiness="core",
        ),
        encoding="utf-8",
    )

    status_after = get_status(target_root=target_root, state_path=state_path)
    log_event(
        log_path=log_path,
        action="install",
        status_before=status_before["status"],
        status_after=status_after["status"],
        target_root=target_root,
        reason=reason,
    )
    return persist_state(
        state_path=state_path,
        status_snapshot=status_after,
        action="install",
        reason=reason,
    )


def remove_skill(
    *,
    target_root: Path,
    state_path: Path,
    log_path: Path,
    reason: Optional[str],
) -> Dict[str, object]:
    status_before = get_status(target_root=target_root, state_path=state_path)
    target = skill_dir(target_root)
    if target.exists():
        shutil.rmtree(target)

    status_after = get_status(target_root=target_root, state_path=state_path)
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install or remove the global prodcraft gateway skill.")
    parser.add_argument("action", choices=("status", "install", "remove"))
    parser.add_argument("--target-root", type=Path, default=DEFAULT_TARGET_ROOT)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--state-path", type=Path, default=DEFAULT_STATE_PATH)
    parser.add_argument("--log-path", type=Path, default=DEFAULT_LOG_PATH)
    parser.add_argument("--reason", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.action == "status":
        payload = get_status(target_root=args.target_root, state_path=args.state_path)
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
        )

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
