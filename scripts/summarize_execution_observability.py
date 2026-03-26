#!/usr/bin/env python3
"""Summarize execution-observability JSONL artifacts into recurring signals."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def summarize_events(path: Path) -> dict[str, object]:
    events = read_jsonl(path)
    failure_counter: Counter[str] = Counter()
    high_risk_actions: set[str] = set()
    missing_usage = 0

    for event in events:
        metadata = event.get("metadata", {}) or {}
        event_type = event.get("event_type")

        if event_type in {"runner_execution.failed", "skill_invocation.failed"}:
            failure_key = metadata.get("error_type") or metadata.get("reason") or "unknown"
            failure_counter[str(failure_key)] += 1

        if event_type == "model_usage.unavailable":
            missing_usage += 1

        action = metadata.get("action") or metadata.get("command")
        if isinstance(action, str):
            lowered = action.lower()
            if any(keyword in lowered for keyword in ("force push", "rm -rf", "sudo", "delete", "drop table")):
                high_risk_actions.add(action)

    return {
        "recurring_failures": dict(failure_counter),
        "missing_usage": {"count": missing_usage},
        "high_risk_actions": sorted(high_risk_actions),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize an execution-observability JSONL artifact.")
    parser.add_argument("jsonl_path", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(json.dumps(summarize_events(args.jsonl_path), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
