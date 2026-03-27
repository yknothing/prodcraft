#!/usr/bin/env python3
"""Summarize execution-observability JSONL artifacts into recurring signals."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import yaml


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def collect_jsonl_paths(inputs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()

    for input_path in inputs:
        resolved = input_path.resolve()
        if resolved.is_file():
            if resolved.suffix == ".jsonl" and resolved not in seen:
                seen.add(resolved)
                paths.append(resolved)
            continue

        if resolved.is_dir():
            for candidate in sorted(resolved.rglob("*.jsonl")):
                if candidate not in seen:
                    seen.add(candidate)
                    paths.append(candidate)

    return paths


def summarize_events(paths: Path | list[Path]) -> dict[str, object]:
    if isinstance(paths, Path):
        paths = [paths]

    failure_counter: Counter[str] = Counter()
    high_risk_actions: set[str] = set()
    missing_usage = 0

    for path in paths:
        for event in read_jsonl(path):
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
        "inputs": [str(path) for path in paths],
        "input_count": len(paths),
        "recurring_failures": dict(failure_counter),
        "missing_usage": {"count": missing_usage},
        "high_risk_actions": sorted(high_risk_actions),
    }


def load_thresholds(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def evaluate_thresholds(summary: dict[str, object], thresholds: dict[str, object]) -> list[str]:
    breaches: list[str] = []

    failure_config = thresholds.get("recurring_failures", {}) or {}
    min_occurrences = int(failure_config.get("min_occurrences", 1))
    for failure_key, count in (summary.get("recurring_failures") or {}).items():
        if int(count) >= min_occurrences:
            breaches.append(f"recurring failure '{failure_key}' seen {count} times")

    missing_usage_config = thresholds.get("missing_usage", {}) or {}
    max_missing = int(missing_usage_config.get("max_count", 0))
    missing_count = int(((summary.get("missing_usage") or {}).get("count", 0)))
    if missing_count > max_missing:
        breaches.append(f"missing usage count {missing_count} exceeds max {max_missing}")

    risk_config = thresholds.get("high_risk_actions", {}) or {}
    max_high_risk = int(risk_config.get("max_count", 0))
    high_risk_count = len(summary.get("high_risk_actions") or [])
    if high_risk_count > max_high_risk:
        breaches.append(f"high-risk action count {high_risk_count} exceeds max {max_high_risk}")

    return breaches


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize an execution-observability JSONL artifact.")
    parser.add_argument("input_paths", nargs="+", type=Path, help="JSONL file(s) or directories containing JSONL files.")
    parser.add_argument("--thresholds", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--fail-on-breach", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    jsonl_paths = collect_jsonl_paths(args.input_paths)
    summary = summarize_events(jsonl_paths)

    if args.thresholds is not None:
        summary["threshold_breaches"] = evaluate_thresholds(summary, load_thresholds(args.thresholds))

    rendered = json.dumps(summary, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)

    if args.fail_on_breach and summary.get("threshold_breaches"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
