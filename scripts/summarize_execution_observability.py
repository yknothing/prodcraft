#!/usr/bin/env python3
"""Summarize execution-observability JSONL artifacts into recurring signals."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
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


def _new_usage_bucket() -> dict[str, int]:
    return {
        "event_count": 0,
        "token_input": 0,
        "token_output": 0,
        "token_total": 0,
        "token_cache_read_input": 0,
        "token_cache_write_input": 0,
    }


def _add_token_usage(bucket: dict[str, int], event: dict) -> None:
    bucket["event_count"] += 1
    for field in (
        "token_input",
        "token_output",
        "token_total",
        "token_cache_read_input",
        "token_cache_write_input",
    ):
        value = event.get(field)
        if isinstance(value, int):
            bucket[field] += value


def _usage_precision(event: dict) -> str:
    precision = event.get("usage_precision")
    if isinstance(precision, str):
        return precision.strip().lower()
    return "unknown"


def _is_non_bool_non_negative_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _invalid_exact_usage_reason(event: dict) -> str | None:
    if _usage_precision(event) != "exact":
        return None

    if event.get("usage_source") not in {"provider", "runner"}:
        return "exact_usage_untrusted_source"

    required_fields = ("token_input", "token_output", "token_total")
    if any(isinstance(event.get(field), bool) for field in required_fields):
        return "exact_usage_bool_token_fields"

    if not all(isinstance(event.get(field), int) for field in required_fields):
        return "exact_usage_missing_integer_token_fields"

    if not all(_is_non_bool_non_negative_int(event.get(field)) for field in required_fields):
        return "exact_usage_negative_token_fields"

    if event["token_total"] != event["token_input"] + event["token_output"]:
        return "exact_usage_total_mismatch"

    return None


def _branch_key(event: dict) -> tuple[str, str] | None:
    metadata = event.get("metadata", {}) or {}
    scenario_id = metadata.get("scenario_id")
    branch = metadata.get("branch")
    if isinstance(scenario_id, str) and isinstance(branch, str):
        return scenario_id, branch
    return None


def _context_ratio(loaded: int, available: int) -> float | None:
    if available <= 0:
        return None
    return round(loaded / available, 4)


def _stable_invocation_key(event: dict) -> str | None:
    metadata = event.get("metadata", {}) or {}
    trace_id = event.get("trace_id") or metadata.get("trace_id")
    span_id = event.get("span_id") or metadata.get("span_id")
    if isinstance(trace_id, str) and trace_id and isinstance(span_id, str) and span_id:
        return f"trace_span:{trace_id}:{span_id}"

    for field in ("invocation_id", "skill_invocation_id", "span_id"):
        value = event.get(field)
        if isinstance(value, str) and value:
            return f"{field}:{value}"
        value = metadata.get(field)
        if isinstance(value, str) and value:
            return f"{field}:{value}"

    return None


def _is_terminal_invocation_event(event_type: str) -> bool:
    return event_type in {"skill_invocation.completed", "skill_invocation.failed", "skill_invocation.cancelled"}


def _context_bucket_with_ratios(bucket: dict[str, int]) -> dict[str, int | float | None]:
    return {
        **bucket,
        "loaded_context_char_ratio": _context_ratio(
            bucket["loaded_context_char_count"],
            bucket["available_context_char_count"],
        ),
        "deferred_context_char_ratio": _context_ratio(
            bucket["deferred_context_char_count"],
            bucket["available_context_char_count"],
        ),
        "loaded_context_byte_ratio": _context_ratio(
            bucket["loaded_context_byte_count"],
            bucket["available_context_byte_count"],
        ),
        "deferred_context_byte_ratio": _context_ratio(
            bucket["deferred_context_byte_count"],
            bucket["available_context_byte_count"],
        ),
    }


def summarize_events(paths: Path | list[Path]) -> dict[str, object]:
    if isinstance(paths, Path):
        paths = [paths]

    failure_counter: Counter[str] = Counter()
    invalid_usage_counter: Counter[str] = Counter()
    high_risk_actions: set[str] = set()
    missing_usage = 0
    skill_invocation_keys: set[str] = set()
    skill_invocation_without_key_count = 0
    skill_context_invocation_keys: set[str] = set()
    skill_context_without_key_count = 0
    token_usage_totals = _new_usage_bucket()
    token_usage_by_skill: dict[str, dict[str, int]] = defaultdict(_new_usage_bucket)
    token_usage_by_runner: dict[str, dict[str, int]] = defaultdict(_new_usage_bucket)
    estimated_token_usage_totals = _new_usage_bucket()
    estimated_token_usage_by_skill: dict[str, dict[str, int]] = defaultdict(_new_usage_bucket)
    estimated_token_usage_by_runner: dict[str, dict[str, int]] = defaultdict(_new_usage_bucket)
    unknown_token_usage_totals = _new_usage_bucket()
    unknown_token_usage_by_skill: dict[str, dict[str, int]] = defaultdict(_new_usage_bucket)
    unknown_token_usage_by_runner: dict[str, dict[str, int]] = defaultdict(_new_usage_bucket)
    invalid_token_usage_totals = _new_usage_bucket()
    branch_usage: dict[str, dict[str, dict[str, int]]] = defaultdict(dict)
    estimated_branch_usage: dict[str, dict[str, dict[str, int]]] = defaultdict(dict)
    skill_context_totals = {
        "measured_count": 0,
        "loaded_context_char_count": 0,
        "deferred_context_char_count": 0,
        "available_context_char_count": 0,
        "loaded_context_byte_count": 0,
        "deferred_context_byte_count": 0,
        "available_context_byte_count": 0,
    }
    skill_context_by_skill: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "measured_count": 0,
            "loaded_context_char_count": 0,
            "deferred_context_char_count": 0,
            "available_context_char_count": 0,
            "loaded_context_byte_count": 0,
            "deferred_context_byte_count": 0,
            "available_context_byte_count": 0,
        }
    )

    for path in paths:
        for event in read_jsonl(path):
            metadata = event.get("metadata", {}) or {}
            event_type = event.get("event_type")

            if isinstance(event_type, str) and event_type.startswith("skill_invocation."):
                invocation_key = _stable_invocation_key(event)
                if invocation_key is not None:
                    skill_invocation_keys.add(invocation_key)
                elif _is_terminal_invocation_event(event_type):
                    skill_invocation_without_key_count += 1

            if event_type in {"runner_execution.failed", "skill_invocation.failed"}:
                failure_key = metadata.get("error_type") or metadata.get("reason") or "unknown"
                failure_counter[str(failure_key)] += 1

            if event_type == "model_usage.unavailable":
                missing_usage += 1
            elif event_type == "model_usage.completed":
                skill_key = str(event.get("skill_name") or "__no_skill__")
                runner_key = str(event.get("runner") or "__unknown_runner__")
                precision = _usage_precision(event)
                invalid_reason = _invalid_exact_usage_reason(event)

                if invalid_reason is not None:
                    invalid_token_usage_totals["event_count"] += 1
                    invalid_usage_counter[invalid_reason] += 1
                    continue

                if precision == "exact":
                    totals = token_usage_totals
                    by_skill = token_usage_by_skill
                    by_runner = token_usage_by_runner
                    branch_map = branch_usage
                elif precision == "estimated":
                    totals = estimated_token_usage_totals
                    by_skill = estimated_token_usage_by_skill
                    by_runner = estimated_token_usage_by_runner
                    branch_map = estimated_branch_usage
                else:
                    totals = unknown_token_usage_totals
                    by_skill = unknown_token_usage_by_skill
                    by_runner = unknown_token_usage_by_runner
                    branch_map = None

                _add_token_usage(totals, event)
                _add_token_usage(by_skill[skill_key], event)
                _add_token_usage(by_runner[runner_key], event)

                branch_key = _branch_key(event)
                if branch_key is not None and branch_map is not None:
                    scenario_id, branch = branch_key
                    branch_map[scenario_id][branch] = {
                        "token_input": int(event.get("token_input") or 0),
                        "token_output": int(event.get("token_output") or 0),
                        "token_total": int(event.get("token_total") or 0),
                        "token_cache_read_input": int(event.get("token_cache_read_input") or 0),
                        "token_cache_write_input": int(event.get("token_cache_write_input") or 0),
                    }

            elif event_type == "skill_context.measured":
                invocation_key = _stable_invocation_key(event)
                if invocation_key is not None:
                    skill_context_invocation_keys.add(invocation_key)
                else:
                    skill_context_without_key_count += 1

                loaded_chars = int(metadata.get("loaded_context_char_count") or 0)
                deferred_chars = int(metadata.get("deferred_context_char_count") or 0)
                available_chars = int(metadata.get("available_context_char_count") or 0)
                loaded_bytes = int(metadata.get("loaded_context_byte_count") or 0)
                deferred_bytes = int(metadata.get("deferred_context_byte_count") or 0)
                available_bytes = int(metadata.get("available_context_byte_count") or 0)
                skill_key = str(event.get("skill_name") or "__unknown_skill__")

                skill_context_totals["measured_count"] += 1
                skill_context_totals["loaded_context_char_count"] += loaded_chars
                skill_context_totals["deferred_context_char_count"] += deferred_chars
                skill_context_totals["available_context_char_count"] += available_chars
                skill_context_totals["loaded_context_byte_count"] += loaded_bytes
                skill_context_totals["deferred_context_byte_count"] += deferred_bytes
                skill_context_totals["available_context_byte_count"] += available_bytes

                skill_context_by_skill[skill_key]["measured_count"] += 1
                skill_context_by_skill[skill_key]["loaded_context_char_count"] += loaded_chars
                skill_context_by_skill[skill_key]["deferred_context_char_count"] += deferred_chars
                skill_context_by_skill[skill_key]["available_context_char_count"] += available_chars
                skill_context_by_skill[skill_key]["loaded_context_byte_count"] += loaded_bytes
                skill_context_by_skill[skill_key]["deferred_context_byte_count"] += deferred_bytes
                skill_context_by_skill[skill_key]["available_context_byte_count"] += available_bytes

            action = metadata.get("action") or metadata.get("command")
            if isinstance(action, str):
                lowered = action.lower()
                if any(keyword in lowered for keyword in ("force push", "rm -rf", "sudo", "delete", "drop table")):
                    high_risk_actions.add(action)

    def build_branch_deltas(source: dict[str, dict[str, dict[str, int]]]) -> dict[str, dict[str, int]]:
        deltas: dict[str, dict[str, int]] = {}
        for scenario_id, branches in source.items():
            baseline = branches.get("without_skill")
            with_skill = branches.get("with_skill")
            if baseline is None or with_skill is None:
                continue
            deltas[scenario_id] = {
                "token_input_delta": with_skill["token_input"] - baseline["token_input"],
                "token_output_delta": with_skill["token_output"] - baseline["token_output"],
                "token_total_delta": with_skill["token_total"] - baseline["token_total"],
                "cache_read_input_delta": with_skill["token_cache_read_input"] - baseline["token_cache_read_input"],
                "cache_write_input_delta": with_skill["token_cache_write_input"] - baseline["token_cache_write_input"],
            }
        return deltas

    branch_deltas = build_branch_deltas(branch_usage)
    estimated_branch_deltas = build_branch_deltas(estimated_branch_usage)
    exact_usage_count = token_usage_totals["event_count"]
    estimated_usage_count = estimated_token_usage_totals["event_count"]
    unknown_usage_count = unknown_token_usage_totals["event_count"]
    invalid_usage_count = invalid_token_usage_totals["event_count"]
    model_usage_event_count = exact_usage_count + estimated_usage_count + unknown_usage_count + invalid_usage_count + missing_usage
    skill_invocation_count = len(skill_invocation_keys) + skill_invocation_without_key_count
    measured_invocation_count = len(skill_context_invocation_keys) + skill_context_without_key_count

    return {
        "inputs": [str(path) for path in paths],
        "input_count": len(paths),
        "recurring_failures": dict(failure_counter),
        "missing_usage": {"count": missing_usage},
        "usage_quality": {
            "model_usage_event_count": model_usage_event_count,
            "exact_usage_event_count": exact_usage_count,
            "estimated_usage_event_count": estimated_usage_count,
            "unknown_usage_event_count": unknown_usage_count,
            "invalid_usage_event_count": invalid_usage_count,
            "missing_usage_event_count": missing_usage,
            "exact_usage_coverage_ratio": _context_ratio(exact_usage_count, model_usage_event_count),
            "estimated_usage_ratio": _context_ratio(estimated_usage_count, model_usage_event_count),
            "unknown_usage_ratio": _context_ratio(unknown_usage_count, model_usage_event_count),
            "invalid_usage_ratio": _context_ratio(invalid_usage_count, model_usage_event_count),
            "missing_usage_ratio": _context_ratio(missing_usage, model_usage_event_count),
        },
        "token_usage": {
            **token_usage_totals,
            "precision": "exact",
            "by_skill": dict(sorted(token_usage_by_skill.items())),
            "by_runner": dict(sorted(token_usage_by_runner.items())),
        },
        "estimated_token_usage": {
            **estimated_token_usage_totals,
            "precision": "estimated",
            "advisory": True,
            "by_skill": dict(sorted(estimated_token_usage_by_skill.items())),
            "by_runner": dict(sorted(estimated_token_usage_by_runner.items())),
        },
        "unknown_token_usage": {
            **unknown_token_usage_totals,
            "precision": "unknown",
            "by_skill": dict(sorted(unknown_token_usage_by_skill.items())),
            "by_runner": dict(sorted(unknown_token_usage_by_runner.items())),
        },
        "invalid_token_usage": {
            **invalid_token_usage_totals,
            "by_reason": dict(sorted(invalid_usage_counter.items())),
        },
        "skill_context": {
            **_context_bucket_with_ratios(skill_context_totals),
            "measurement_precision": "exact_char_and_byte",
            "token_count_status": "unavailable",
            "skill_invocation_event_count": skill_invocation_count,
            "measured_invocation_count": measured_invocation_count,
            "sampling_ratio": _context_ratio(measured_invocation_count, skill_invocation_count),
            "by_skill": {
                skill: _context_bucket_with_ratios(bucket)
                for skill, bucket in sorted(skill_context_by_skill.items())
            },
        },
        "context_efficiency": {
            "exact_token_branch_deltas": {
                "source_precision": "exact",
                "deltas": dict(sorted(branch_deltas.items())),
            },
            "estimated_token_branch_deltas_advisory": {
                "source_precision": "estimated",
                "advisory": True,
                "deltas": dict(sorted(estimated_branch_deltas.items())),
            },
            "branch_deltas": dict(sorted(branch_deltas.items())),
            "estimated_branch_deltas": dict(sorted(estimated_branch_deltas.items())),
        },
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

    token_usage_config = thresholds.get("token_usage", {}) or {}
    if "min_completed_count" in token_usage_config:
        min_completed = int(token_usage_config.get("min_completed_count", 0))
        completed_count = int(((summary.get("token_usage") or {}).get("event_count", 0)))
        if completed_count < min_completed:
            breaches.append(f"exact model usage completed count {completed_count} below min {min_completed}")
    if "min_exact_coverage_ratio" in token_usage_config:
        min_coverage = float(token_usage_config.get("min_exact_coverage_ratio", 0))
        usage_quality = summary.get("usage_quality") or {}
        exact_coverage = usage_quality.get("exact_usage_coverage_ratio")
        if exact_coverage is None:
            exact_coverage = 0.0
        exact_coverage = float(exact_coverage)
        if exact_coverage < min_coverage:
            breaches.append(f"exact model usage coverage {exact_coverage:.4f} below min {min_coverage:.4f}")

    estimated_usage_config = thresholds.get("estimated_token_usage", {}) or {}
    if "max_count" in estimated_usage_config:
        max_estimated = int(estimated_usage_config.get("max_count", 0))
        estimated_count = int(((summary.get("estimated_token_usage") or {}).get("event_count", 0)))
        if estimated_count > max_estimated:
            breaches.append(f"estimated model usage count {estimated_count} exceeds max {max_estimated}")

    unknown_usage_config = thresholds.get("unknown_token_usage", {}) or {}
    if "max_count" in unknown_usage_config:
        max_unknown = int(unknown_usage_config.get("max_count", 0))
        unknown_count = int(((summary.get("unknown_token_usage") or {}).get("event_count", 0)))
        if unknown_count > max_unknown:
            breaches.append(f"unknown model usage count {unknown_count} exceeds max {max_unknown}")

    invalid_usage_config = thresholds.get("invalid_token_usage", {}) or {}
    if "max_count" in invalid_usage_config:
        max_invalid = int(invalid_usage_config.get("max_count", 0))
        invalid_count = int(((summary.get("invalid_token_usage") or {}).get("event_count", 0)))
        if invalid_count > max_invalid:
            breaches.append(f"invalid model usage count {invalid_count} exceeds max {max_invalid}")

    skill_context_config = thresholds.get("skill_context", {}) or {}
    if "min_measured_count" in skill_context_config:
        min_measured = int(skill_context_config.get("min_measured_count", 0))
        measured_count = int(((summary.get("skill_context") or {}).get("measured_count", 0)))
        if measured_count < min_measured:
            breaches.append(f"skill context measured count {measured_count} below min {min_measured}")
    if "min_sampling_ratio" in skill_context_config:
        min_sampling = float(skill_context_config.get("min_sampling_ratio", 0))
        sampling_ratio = (summary.get("skill_context") or {}).get("sampling_ratio")
        if sampling_ratio is None:
            sampling_ratio = 0.0
        sampling_ratio = float(sampling_ratio)
        if sampling_ratio < min_sampling:
            breaches.append(f"skill context sampling ratio {sampling_ratio:.4f} below min {min_sampling:.4f}")

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
