from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


VALID_USAGE_PRECISIONS = {"exact", "estimated", "unknown", "unavailable"}
TOKEN_FIELDS = ("token_input", "token_output", "token_total")
ALL_TOKEN_FIELDS = (
    "token_input",
    "token_output",
    "token_total",
    "token_cache_read_input",
    "token_cache_write_input",
)
TRUSTED_TOKEN_COUNT_METHODS = {"provider_api", "official_tokenizer", "model_tokenizer"}


@dataclass(frozen=True)
class ValidationIssue:
    path: Path
    line_number: int | None
    message: str

    def render(self) -> str:
        location = str(self.path)
        if self.line_number is not None:
            location = f"{location}:{self.line_number}"
        return f"{location}: {self.message}"


def collect_jsonl_paths(inputs: Iterable[Path]) -> tuple[list[Path], list[ValidationIssue]]:
    paths: list[Path] = []
    issues: list[ValidationIssue] = []
    seen: set[Path] = set()

    for input_path in inputs:
        resolved = input_path.resolve()
        if not resolved.exists():
            issues.append(ValidationIssue(input_path, None, "input path does not exist"))
            continue

        if resolved.is_file():
            if resolved.suffix != ".jsonl":
                issues.append(ValidationIssue(resolved, None, "input file is not a .jsonl file"))
                continue
            if resolved not in seen:
                seen.add(resolved)
                paths.append(resolved)
            continue

        if resolved.is_dir():
            for candidate in sorted(resolved.rglob("*.jsonl")):
                if candidate not in seen:
                    seen.add(candidate)
                    paths.append(candidate)
            continue

        issues.append(ValidationIssue(resolved, None, "input path is neither a file nor a directory"))

    if not paths and not issues:
        issues.append(ValidationIssue(Path("."), None, "no input paths were provided"))

    return paths, issues


def validate_paths(paths: Iterable[Path]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path in paths:
        issues.extend(validate_jsonl_file(path))
    return issues


def validate_jsonl_file(path: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                issues.append(ValidationIssue(path, line_number, f"invalid JSON: {exc.msg}"))
                continue

            if not isinstance(event, dict):
                issues.append(ValidationIssue(path, line_number, "event must be a JSON object"))
                continue

            issues.extend(validate_event(event, path, line_number))
    return issues


def validate_event(event: dict, path: Path, line_number: int) -> list[ValidationIssue]:
    event_type = event.get("event_type")
    if event_type == "model_usage.completed":
        return _validate_model_usage_completed(event, path, line_number)
    if event_type == "model_usage.unavailable":
        return _validate_model_usage_unavailable(event, path, line_number)
    if event_type == "skill_context.measured":
        return _validate_skill_context_measured(event, path, line_number)
    return []


def _validate_model_usage_completed(event: dict, path: Path, line_number: int) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    precision = event.get("usage_precision")
    if precision not in VALID_USAGE_PRECISIONS:
        issues.append(
            ValidationIssue(
                path,
                line_number,
                "model_usage.completed requires usage_precision in exact, estimated, unknown, unavailable",
            )
        )
        return issues

    if precision == "exact":
        if event.get("usage_source") not in {"provider", "runner"}:
            issues.append(
                ValidationIssue(
                    path,
                    line_number,
                    "exact model_usage.completed requires usage_source provider or runner",
                )
            )

        token_issues: list[ValidationIssue] = []
        for field in TOKEN_FIELDS:
            token_issues.extend(_require_non_negative_int(event, field, path, line_number, "exact model usage"))
        issues.extend(token_issues)

        if not token_issues:
            token_input = event["token_input"]
            token_output = event["token_output"]
            token_total = event["token_total"]
            if token_total != token_input + token_output:
                issues.append(
                    ValidationIssue(
                        path,
                        line_number,
                        "exact model usage token_total must equal token_input + token_output",
                    )
                )
        return issues

    if precision == "estimated":
        if _has_any_token_value(event):
            if event.get("usage_source") != "runner":
                issues.append(
                    ValidationIssue(
                        path,
                        line_number,
                        "estimated model_usage.completed with token fields requires usage_source runner",
                    )
                )
            token_issues = []
            for field in TOKEN_FIELDS:
                token_issues.extend(_require_non_negative_int(event, field, path, line_number, "estimated model usage"))
            for field in ("token_cache_read_input", "token_cache_write_input"):
                token_issues.extend(
                    _require_optional_non_negative_int(event, field, path, line_number, "estimated model usage")
                )
            issues.extend(token_issues)
            if not token_issues:
                if event["token_total"] != event["token_input"] + event["token_output"]:
                    issues.append(
                        ValidationIssue(
                            path,
                            line_number,
                            "estimated model usage token_total must equal token_input + token_output",
                        )
                    )
        return issues

    if _has_any_token_value(event):
        issues.append(
            ValidationIssue(
                path,
                line_number,
                "model_usage.completed with unknown or unavailable precision must keep token fields null",
            )
        )

    return issues


def _validate_model_usage_unavailable(event: dict, path: Path, line_number: int) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if _has_any_token_value(event):
        issues.append(
            ValidationIssue(path, line_number, "model_usage.unavailable requires all token fields to be null")
        )

    if event.get("usage_source") != "unavailable":
        issues.append(
            ValidationIssue(path, line_number, 'model_usage.unavailable requires usage_source "unavailable"')
        )

    precision = event.get("usage_precision")
    if precision not in (None, "unavailable"):
        issues.append(
            ValidationIssue(
                path,
                line_number,
                "model_usage.unavailable requires usage_precision unavailable or null",
            )
        )

    return issues


def _validate_skill_context_measured(event: dict, path: Path, line_number: int) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    precision = event.get("usage_precision")
    if precision is not None and precision not in VALID_USAGE_PRECISIONS:
        issues.append(
            ValidationIssue(
                path,
                line_number,
                "skill_context.measured usage_precision must be exact, estimated, unknown, unavailable, or null",
            )
        )
        return issues

    token_values_present = any(event.get(field) is not None for field in TOKEN_FIELDS)
    if not token_values_present:
        return issues

    if precision != "exact":
        issues.append(
            ValidationIssue(
                path,
                line_number,
                "skill_context.measured token fields must be null unless usage_precision is exact with trusted tokenizer/provider evidence",
            )
        )
        return issues

    if not _has_trusted_token_evidence(event.get("metadata")):
        issues.append(
            ValidationIssue(
                path,
                line_number,
                "skill_context.measured exact token fields require metadata token_count_method provider_api, official_tokenizer, or model_tokenizer with provider or tokenizer evidence",
            )
        )
        return issues

    for field in TOKEN_FIELDS:
        issues.extend(_require_non_negative_int(event, field, path, line_number, "exact skill context token usage"))

    if not any(issue.line_number == line_number for issue in issues):
        if event["token_total"] != event["token_input"] + event["token_output"]:
            issues.append(
                ValidationIssue(
                    path,
                    line_number,
                    "exact skill context token_total must equal token_input + token_output",
                )
            )

    return issues


def _require_non_negative_int(
    event: dict,
    field: str,
    path: Path,
    line_number: int,
    label: str,
) -> list[ValidationIssue]:
    value = event.get(field)
    if isinstance(value, bool) or not isinstance(value, int):
        return [ValidationIssue(path, line_number, f"{label} {field} must be a non-negative integer")]
    if value < 0:
        return [ValidationIssue(path, line_number, f"{label} {field} must be a non-negative integer")]
    return []


def _require_optional_non_negative_int(
    event: dict,
    field: str,
    path: Path,
    line_number: int,
    label: str,
) -> list[ValidationIssue]:
    if event.get(field) is None:
        return []
    return _require_non_negative_int(event, field, path, line_number, label)


def _has_any_token_value(event: dict) -> bool:
    return any(event.get(field) is not None for field in ALL_TOKEN_FIELDS)


def _has_trusted_token_evidence(metadata: object) -> bool:
    if not isinstance(metadata, dict):
        return False

    method = metadata.get("token_count_method")
    if method not in TRUSTED_TOKEN_COUNT_METHODS:
        return False

    provider = metadata.get("token_provider") or metadata.get("provider")
    tokenizer = metadata.get("tokenizer") or metadata.get("tokenizer_name")
    model = metadata.get("model") or metadata.get("model_name")

    if method == "provider_api":
        return isinstance(provider, str) and bool(provider.strip())

    return isinstance(tokenizer, str) and bool(tokenizer.strip()) and isinstance(model, str) and bool(model.strip())
