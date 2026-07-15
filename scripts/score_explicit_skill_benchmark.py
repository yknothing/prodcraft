#!/usr/bin/env python3
"""Deterministically score structured explicit-benchmark responses.

The machine lane evaluates JSON assertions and exact manifest skill names. The
judge lane is supplied as a separate, content-hash-bound JSON artifact so a
successful runner process is never mistaken for an evaluation verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml


MISSING = object()
JSON_FENCE_RE = re.compile(r"\A\s*```json\s*(\{.*\})\s*```\s*\Z", re.DOTALL)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract_json_payload(response_text: str) -> dict[str, Any]:
    text = response_text.strip()
    match = JSON_FENCE_RE.fullmatch(text)
    if match:
        text = match.group(1)
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("response must be exactly one JSON object")
    return payload


def get_path(payload: dict[str, Any], dotted_path: str) -> Any:
    current: Any = payload
    for component in dotted_path.split("."):
        if not isinstance(current, dict) or component not in current:
            return MISSING
        current = current[component]
    return current


def is_non_empty(value: Any) -> bool:
    if value is MISSING or value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return True


def evaluate_assertion(
    payload: dict[str, Any],
    assertion: dict[str, Any],
    manifest_skill_names: set[str],
) -> dict[str, Any]:
    name = assertion["name"]
    path = assertion["path"]
    operator = assertion["operator"]
    actual = get_path(payload, path)
    expected = assertion.get("expected")

    if operator == "equals":
        passed = actual is not MISSING and type(actual) is type(expected) and actual == expected
        detail = f"expected {expected!r}; got {'<missing>' if actual is MISSING else repr(actual)}"
    elif operator == "non_empty":
        passed = is_non_empty(actual)
        detail = "value is non-empty" if passed else "value is missing or empty"
    elif operator == "not_present":
        passed = actual is MISSING
        detail = "path is absent" if passed else f"unexpected value {actual!r}"
    elif operator == "min_items":
        passed = isinstance(actual, list) and len(actual) >= int(expected)
        detail = f"expected at least {expected} items; got {len(actual) if isinstance(actual, list) else '<non-list>'}"
    elif operator == "manifest_skill":
        passed = isinstance(actual, str) and actual in manifest_skill_names
        detail = (
            f"resolved exact manifest skill {actual}"
            if passed
            else f"unresolved manifest skill: {'<missing>' if actual is MISSING else actual}"
        )
    elif operator == "manifest_skill_list":
        if not isinstance(actual, list) or not actual or not all(isinstance(item, str) for item in actual):
            passed = False
            detail = "expected a non-empty list of canonical skill names"
        else:
            unresolved = sorted(set(actual) - manifest_skill_names)
            duplicates = sorted({item for item in actual if actual.count(item) > 1})
            passed = not unresolved and not duplicates
            detail_parts = []
            if unresolved:
                detail_parts.append(f"unresolved={unresolved}")
            if duplicates:
                detail_parts.append(f"duplicates={duplicates}")
            detail = "; ".join(detail_parts) if detail_parts else "all names resolve exactly"
    else:
        passed = False
        detail = f"unsupported operator {operator!r}"

    return {
        "name": name,
        "path": path,
        "operator": operator,
        "passed": passed,
        "detail": detail,
    }


def score_case_response(
    response_text: str,
    scenario: dict[str, Any],
    manifest_skill_names: set[str],
) -> dict[str, Any]:
    try:
        payload = extract_json_payload(response_text)
    except (json.JSONDecodeError, ValueError) as exc:
        return {
            "passed": False,
            "payload": None,
            "assertions": [
                {
                    "name": "structured-json-response",
                    "path": "$",
                    "operator": "json-object",
                    "passed": False,
                    "detail": str(exc),
                }
            ],
        }

    assertions = [
        {
            "name": "scenario-id",
            "path": "scenario_id",
            "operator": "equals",
            "expected": scenario["id"],
        },
        *scenario.get("machine_assertions", []),
    ]
    results = [
        evaluate_assertion(payload, assertion, manifest_skill_names)
        for assertion in assertions
    ]
    return {
        "passed": all(item["passed"] for item in results),
        "payload": payload,
        "assertions": results,
    }


def load_manifest_skill_names(path: Path) -> set[str]:
    manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
    return {
        entry["name"]
        for entry in manifest.get("skills", [])
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }


def score_execution(
    run_dir: Path,
    benchmark_path: Path,
    manifest_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    scenarios = {
        item["id"]: item
        for item in json.loads(benchmark_path.read_text(encoding="utf-8"))
    }
    execution = json.loads((run_dir / "execution_summary.json").read_text(encoding="utf-8"))
    if execution.get("schema_version") != "explicit-benchmark-execution-summary.v1":
        raise ValueError("execution summary schema must be explicit-benchmark-execution-summary.v1")
    actual_benchmark_sha256 = sha256_file(benchmark_path)
    if execution.get("benchmark_sha256") != actual_benchmark_sha256:
        raise ValueError(
            "benchmark hash mismatch: "
            f"execution={execution.get('benchmark_sha256')} current={actual_benchmark_sha256}"
        )
    manifest_skills = load_manifest_skill_names(manifest_path)
    scored_cases = []

    for case in execution.get("cases", []):
        scenario_id = case["scenario_id"]
        scenario = scenarios.get(scenario_id)
        base = {
            "scenario_id": scenario_id,
            "run_number": case["run_number"],
            "arm": case.get("arm") or case.get("branch"),
            "judge_assertion_names": [
                item["name"] for item in (scenario or {}).get("judge_assertions", [])
            ],
        }
        if scenario is None:
            scored_cases.append(
                {
                    **base,
                    "response_sha256": case.get("artifact_sha256"),
                    "passed": False,
                    "assertions": [
                        {
                            "name": "scenario-definition",
                            "passed": False,
                            "detail": f"scenario {scenario_id!r} is missing from benchmark",
                        }
                    ],
                }
            )
            continue

        if case.get("status") != "completed":
            scored_cases.append(
                {
                    **base,
                    "response_sha256": case.get("artifact_sha256"),
                    "passed": False,
                    "assertions": [
                        {
                            "name": "runner-completed",
                            "passed": False,
                            "detail": f"runner status={case.get('status')} error_type={case.get('error_type')}",
                        }
                    ],
                }
            )
            continue

        artifact_path = run_dir / case["artifact_path"]
        if not artifact_path.is_file():
            scored_cases.append(
                {
                    **base,
                    "response_sha256": None,
                    "passed": False,
                    "assertions": [
                        {
                            "name": "response-artifact-exists",
                            "passed": False,
                            "detail": f"missing response artifact: {artifact_path}",
                        }
                    ],
                }
            )
            continue

        actual_sha256 = sha256_file(artifact_path)
        if actual_sha256 != case.get("artifact_sha256"):
            scored_cases.append(
                {
                    **base,
                    "response_sha256": actual_sha256,
                    "passed": False,
                    "assertions": [
                        {
                            "name": "response-hash-integrity",
                            "passed": False,
                            "detail": f"summary={case.get('artifact_sha256')}, actual={actual_sha256}",
                        }
                    ],
                }
            )
            continue

        result = score_case_response(
            artifact_path.read_text(encoding="utf-8"),
            scenario,
            manifest_skills,
        )
        scored_cases.append(
            {
                **base,
                "response_sha256": actual_sha256,
                "passed": result["passed"],
                "assertions": result["assertions"],
            }
        )

    return scored_cases, execution


def case_key(case: dict[str, Any]) -> tuple[Any, Any, Any]:
    return case.get("scenario_id"), case.get("run_number"), case.get("arm")


def cross_validate_judge(
    machine_cases: list[dict[str, Any]],
    judge_payload: dict[str, Any],
) -> dict[str, Any]:
    contradictions: list[dict[str, Any]] = []
    judge_cases = judge_payload.get("cases") if isinstance(judge_payload, dict) else None
    if judge_payload.get("schema_version") != "explicit-benchmark-judge-results.v1" or not isinstance(judge_cases, list):
        return {
            "acceptance_ready": False,
            "judge_status": "invalid",
            "contradictions": [
                {
                    "type": "invalid-judge-results",
                    "detail": "judge results must use explicit-benchmark-judge-results.v1",
                }
            ],
        }

    judge_index: dict[tuple[Any, Any, Any], dict[str, Any]] = {}
    for judge_case in judge_cases:
        key = case_key(judge_case)
        if key in judge_index:
            contradictions.append(
                {"type": "duplicate-judge-result", "case": list(key)}
            )
        judge_index[key] = judge_case

    machine_keys = {case_key(case) for case in machine_cases}
    for machine_case in machine_cases:
        key = case_key(machine_case)
        judge_case = judge_index.get(key)
        if judge_case is None:
            contradictions.append({"type": "missing-judge-result", "case": list(key)})
            continue
        if judge_case.get("response_sha256") != machine_case.get("response_sha256"):
            contradictions.append(
                {
                    "type": "response-hash-mismatch",
                    "case": list(key),
                    "machine": machine_case.get("response_sha256"),
                    "judge": judge_case.get("response_sha256"),
                }
            )
            continue
        verdict = judge_case.get("verdict")
        if verdict not in {"pass", "fail"}:
            contradictions.append(
                {"type": "invalid-judge-verdict", "case": list(key), "verdict": verdict}
            )
            continue
        judge_assertions = judge_case.get("assertions")
        if not isinstance(judge_assertions, list) or not judge_assertions:
            contradictions.append(
                {"type": "missing-judge-assertions", "case": list(key)}
            )
            continue
        expected_assertion_names = machine_case.get("judge_assertion_names") or []
        actual_assertion_names = [
            item.get("name") for item in judge_assertions if isinstance(item, dict)
        ]
        if expected_assertion_names and (
            len(actual_assertion_names) != len(set(actual_assertion_names))
            or set(actual_assertion_names) != set(expected_assertion_names)
        ):
            contradictions.append(
                {
                    "type": "judge-assertion-set-mismatch",
                    "case": list(key),
                    "expected": sorted(expected_assertion_names),
                    "actual": sorted(name for name in actual_assertion_names if isinstance(name, str)),
                }
            )
        assertion_passed = all(item.get("passed") is True for item in judge_assertions)
        if (verdict == "pass") != assertion_passed:
            contradictions.append(
                {"type": "judge-verdict-assertion-mismatch", "case": list(key)}
            )
        machine_passed = machine_case.get("passed") is True
        judge_passed = verdict == "pass"
        if machine_passed and not judge_passed:
            contradictions.append(
                {"type": "machine-pass-judge-fail", "case": list(key)}
            )
        elif not machine_passed and judge_passed:
            contradictions.append(
                {"type": "machine-fail-judge-pass", "case": list(key)}
            )

    for extra_key in sorted(set(judge_index) - machine_keys):
        contradictions.append({"type": "extra-judge-result", "case": list(extra_key)})

    all_machine_pass = bool(machine_cases) and all(case.get("passed") is True for case in machine_cases)
    all_judge_pass = bool(machine_cases) and all(
        judge_index.get(case_key(case), {}).get("verdict") == "pass"
        for case in machine_cases
    )
    acceptance_ready = all_machine_pass and all_judge_pass and not contradictions
    if contradictions:
        judge_status = "contradiction"
    elif acceptance_ready:
        judge_status = "pass"
    else:
        judge_status = "aligned-fail"
    return {
        "acceptance_ready": acceptance_ready,
        "judge_status": judge_status,
        "contradictions": contradictions,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Score explicit benchmark responses with deterministic assertions."
    )
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--benchmark", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--acceptance-arm", default="with_skill")
    lane = parser.add_mutually_exclusive_group(required=True)
    lane.add_argument(
        "--machine-only",
        action="store_true",
        help="Run deterministic checks only; output is explicitly non-authoritative for final acceptance.",
    )
    lane.add_argument("--judge-results", help="Path to explicit-benchmark-judge-results.v1 JSON.")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).resolve()
    benchmark_path = Path(args.benchmark).resolve()
    manifest_path = Path(args.manifest).resolve()
    output_path = Path(args.output).resolve()

    try:
        machine_cases, execution_summary = score_execution(
            run_dir, benchmark_path, manifest_path
        )
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        write_json(
            output_path,
            {
                "schema_version": "explicit-benchmark-score-summary.v1",
                "machine_passed": False,
                "judge_status": "not-run" if args.machine_only else "invalid",
                "acceptance_ready": False,
                "error": f"{type(exc).__name__}: {exc}",
            },
        )
        return 2

    acceptance_cases = [
        case for case in machine_cases if case.get("arm") == args.acceptance_arm
    ]
    expected_acceptance_count = (
        execution_summary.get("scenario_count", 0)
        * execution_summary.get("runs_per_scenario", 0)
    )
    count_matches = expected_acceptance_count in {0, len(acceptance_cases)}
    machine_passed = (
        bool(acceptance_cases)
        and count_matches
        and all(case.get("passed") is True for case in acceptance_cases)
    )

    summary: dict[str, Any] = {
        "schema_version": "explicit-benchmark-score-summary.v1",
        "run_dir": str(run_dir),
        "benchmark_sha256": sha256_file(benchmark_path),
        "manifest_sha256": sha256_file(manifest_path),
        "skill_file_sha256": execution_summary.get("skill_file_sha256"),
        "acceptance_arm": args.acceptance_arm,
        "expected_acceptance_case_count": expected_acceptance_count,
        "scored_acceptance_case_count": len(acceptance_cases),
        "machine_passed": machine_passed,
        "machine_cases": machine_cases,
        "judge_status": "not-run",
        "contradictions": [],
        "acceptance_ready": False,
    }

    if args.machine_only:
        write_json(output_path, summary)
        return 0 if machine_passed else 1

    try:
        judge_payload = json.loads(Path(args.judge_results).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        summary["judge_status"] = "invalid"
        summary["error"] = f"{type(exc).__name__}: {exc}"
        write_json(output_path, summary)
        return 2

    judge_result = cross_validate_judge(machine_cases, judge_payload)
    summary.update(judge_result)
    summary["acceptance_ready"] = machine_passed and judge_result["acceptance_ready"]
    write_json(output_path, summary)
    return 0 if summary["acceptance_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
