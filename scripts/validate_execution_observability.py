#!/usr/bin/env python3
"""Validate execution-observability JSONL precision contracts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.execution_observability_validator import collect_jsonl_paths, validate_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate execution-observability JSONL files or directories."
    )
    parser.add_argument(
        "input_paths",
        nargs="+",
        type=Path,
        help="JSONL file(s) or directories containing JSONL files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths, input_issues = collect_jsonl_paths(args.input_paths)
    issues = [*input_issues, *validate_paths(paths)]

    if issues:
        print("Execution observability validation failed:", file=sys.stderr)
        for issue in issues:
            print(f"- {issue.render()}", file=sys.stderr)
        return 1

    print(f"Execution observability validation passed for {len(paths)} JSONL file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
