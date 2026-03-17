#!/usr/bin/env python3
"""Analyze trigger-eval results with optional bucketed eval metadata."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_eval_buckets(paths: list[Path]) -> dict[str, dict]:
    items: dict[str, dict] = {}
    for path in paths:
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        for item in data:
            items[item["query"]] = item
    return items


def summarize(results: list[dict]) -> dict[str, object]:
    total = len(results)
    passed = sum(1 for r in results if r["pass"])
    positives = [r for r in results if r["should_trigger"]]
    negatives = [r for r in results if not r["should_trigger"]]
    tp = sum(1 for r in positives if r["pass"])
    tn = sum(1 for r in negatives if r["pass"])
    fn = len(positives) - tp
    fp = len(negatives) - tn
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "tp": tp,
        "fn": fn,
        "tn": tn,
        "fp": fp,
        "recall": None if not positives else tp / len(positives),
        "precision": None if tp + fp == 0 else tp / (tp + fp),
        "accuracy": None if total == 0 else passed / total,
    }


def fmt_ratio(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.0%}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze intake trigger-eval results.")
    parser.add_argument("results_json", help="Path to run_eval results.json")
    parser.add_argument(
        "--eval-set",
        action="append",
        default=[],
        help="Optional eval-set JSON with bucket metadata; may be repeated",
    )
    args = parser.parse_args()

    results_path = Path(args.results_json)
    results_data = json.loads(results_path.read_text())
    results = results_data["results"]

    bucket_map = load_eval_buckets([Path(p) for p in args.eval_set])
    bucketed: dict[str, list[dict]] = defaultdict(list)

    for result in results:
        bucket = bucket_map.get(result["query"], {}).get("bucket", "unbucketed")
        bucketed[bucket].append(result)

    overall = summarize(results)
    print("OVERALL")
    print(json.dumps(overall, ensure_ascii=False, indent=2))

    for bucket in sorted(bucketed):
        print()
        print(f"BUCKET: {bucket}")
        summary = summarize(bucketed[bucket])
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        failed = [r["query"] for r in bucketed[bucket] if not r["pass"]]
        if failed:
            print("FAILED:")
            for query in failed:
                print(f"- {query}")

    print()
    print(
        "HUMAN_SUMMARY",
        json.dumps(
            {
                "overall_accuracy": fmt_ratio(overall["accuracy"]),
                "overall_recall": fmt_ratio(overall["recall"]),
                "overall_precision": fmt_ratio(overall["precision"]),
            },
            ensure_ascii=False,
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
