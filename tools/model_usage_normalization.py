"""Normalize model usage payloads without mixing exact and estimated counts."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any


NormalizedUsage = dict[str, int | str]

COPILOT_FOOTER_RE = re.compile(r"(?:^|\n+)Total usage est:.*\Z", re.DOTALL)
COPILOT_MODEL_USAGE_LINE_RE = re.compile(
    r"^\s*(?P<model>.+?)\s+"
    r"(?P<input>[0-9]+(?:\.[0-9]+)?[kKmM]?)\s+input,\s+"
    r"(?P<output>[0-9]+(?:\.[0-9]+)?[kKmM]?)\s+output,\s+"
    r"(?P<cache_read>[0-9]+(?:\.[0-9]+)?[kKmM]?)\s+cache read,\s+"
    r"(?P<cache_write>[0-9]+(?:\.[0-9]+)?[kKmM]?)\s+cache write"
)


def _non_negative_int(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    return {}


def _int_field(payload: Mapping[str, Any], field: str, *, required: bool = True) -> int | None:
    if field not in payload:
        return None if required else 0
    return _non_negative_int(payload.get(field))


def _normalized(
    *,
    usage_source: str,
    usage_precision: str,
    token_input: int,
    token_output: int,
    token_cache_read_input: int = 0,
    token_cache_write_input: int = 0,
    model_name: str | None = None,
    extras: Mapping[str, int] | None = None,
) -> NormalizedUsage:
    usage: NormalizedUsage = {
        "usage_source": usage_source,
        "usage_precision": usage_precision,
        "token_input": token_input,
        "token_output": token_output,
        "token_total": token_input + token_output,
        "token_cache_read_input": token_cache_read_input,
        "token_cache_write_input": token_cache_write_input,
    }
    if model_name:
        usage["model_name"] = model_name
    if extras:
        usage.update(extras)
    return usage


def normalize_openai_usage(payload: Mapping[str, Any]) -> NormalizedUsage | None:
    """Normalize exact OpenAI Responses or Chat Completions usage payloads."""
    input_tokens = _int_field(payload, "input_tokens")
    output_tokens = _int_field(payload, "output_tokens")
    total_tokens = _int_field(payload, "total_tokens")
    input_details = _mapping(payload.get("input_tokens_details"))
    output_details = _mapping(payload.get("output_tokens_details"))

    if input_tokens is None or output_tokens is None or total_tokens is None:
        input_tokens = _int_field(payload, "prompt_tokens")
        output_tokens = _int_field(payload, "completion_tokens")
        total_tokens = _int_field(payload, "total_tokens")
        input_details = _mapping(payload.get("prompt_tokens_details"))
        output_details = _mapping(payload.get("completion_tokens_details"))

    if input_tokens is None or output_tokens is None or total_tokens is None:
        return None
    if total_tokens != input_tokens + output_tokens:
        return None

    cache_read = _int_field(input_details, "cached_tokens", required=False)
    reasoning_tokens = _int_field(output_details, "reasoning_tokens", required=False)
    if cache_read is None or reasoning_tokens is None:
        return None

    extras = {}
    if reasoning_tokens:
        extras["token_reasoning_output"] = reasoning_tokens

    return _normalized(
        usage_source="provider",
        usage_precision="exact",
        token_input=input_tokens,
        token_output=output_tokens,
        token_cache_read_input=cache_read,
        extras=extras,
    )


def normalize_anthropic_usage(payload: Mapping[str, Any]) -> NormalizedUsage | None:
    """Normalize exact Anthropic Messages usage payloads."""
    input_tokens = _int_field(payload, "input_tokens")
    output_tokens = _int_field(payload, "output_tokens")
    cache_read = _int_field(payload, "cache_read_input_tokens", required=False)
    cache_write = _int_field(payload, "cache_creation_input_tokens", required=False)

    if input_tokens is None or output_tokens is None or cache_read is None or cache_write is None:
        return None

    for total_field in ("total_tokens", "totalTokenCount"):
        if total_field in payload:
            total_tokens = _int_field(payload, total_field)
            if total_tokens is None or total_tokens != input_tokens + output_tokens:
                return None

    return _normalized(
        usage_source="provider",
        usage_precision="exact",
        token_input=input_tokens,
        token_output=output_tokens,
        token_cache_read_input=cache_read,
        token_cache_write_input=cache_write,
    )


def normalize_gemini_usage(payload: Mapping[str, Any]) -> NormalizedUsage | None:
    """Normalize exact Gemini usageMetadata payloads."""
    usage_payload = _mapping(payload.get("usageMetadata")) or payload
    prompt_tokens = _int_field(usage_payload, "promptTokenCount")
    candidate_tokens = _int_field(usage_payload, "candidatesTokenCount")
    total_tokens = _int_field(usage_payload, "totalTokenCount")
    cache_read = _int_field(usage_payload, "cachedContentTokenCount", required=False)
    thoughts_tokens = _int_field(usage_payload, "thoughtsTokenCount", required=False)

    if (
        prompt_tokens is None
        or candidate_tokens is None
        or total_tokens is None
        or cache_read is None
        or thoughts_tokens is None
    ):
        return None

    output_tokens = candidate_tokens + thoughts_tokens
    if total_tokens != prompt_tokens + output_tokens:
        return None

    extras = {}
    if thoughts_tokens:
        extras["token_reasoning_output"] = thoughts_tokens

    return _normalized(
        usage_source="provider",
        usage_precision="exact",
        token_input=prompt_tokens,
        token_output=output_tokens,
        token_cache_read_input=cache_read,
        extras=extras,
    )


def normalize_provider_usage(provider: str, payload: Mapping[str, Any]) -> NormalizedUsage | None:
    """Route a provider usage payload through the provider-specific exact parser."""
    normalized_provider = provider.strip().lower()
    if normalized_provider == "openai":
        return normalize_openai_usage(payload)
    if normalized_provider == "anthropic":
        return normalize_anthropic_usage(payload)
    if normalized_provider == "gemini":
        return normalize_gemini_usage(payload)
    return None


def parse_compact_token_count(raw_value: str) -> int:
    value = raw_value.strip().lower().replace(",", "")
    multiplier = 1
    if value.endswith("k"):
        multiplier = 1_000
        value = value[:-1]
    elif value.endswith("m"):
        multiplier = 1_000_000
        value = value[:-1]
    return int(float(value) * multiplier)


def normalize_copilot_footer_usage(output: str) -> NormalizedUsage | None:
    """Normalize Copilot footer usage as runner-reported estimated counts."""
    footer_match = COPILOT_FOOTER_RE.search(output)
    if not footer_match:
        return None

    totals = {
        "token_input": 0,
        "token_output": 0,
        "token_cache_read_input": 0,
        "token_cache_write_input": 0,
    }
    model_names: list[str] = []
    for line in footer_match.group(0).splitlines():
        match = COPILOT_MODEL_USAGE_LINE_RE.match(line)
        if not match:
            continue
        model_names.append(match.group("model").strip())
        totals["token_input"] += parse_compact_token_count(match.group("input"))
        totals["token_output"] += parse_compact_token_count(match.group("output"))
        totals["token_cache_read_input"] += parse_compact_token_count(match.group("cache_read"))
        totals["token_cache_write_input"] += parse_compact_token_count(match.group("cache_write"))

    if not model_names:
        return None

    return _normalized(
        usage_source="runner",
        usage_precision="estimated",
        model_name=", ".join(model_names),
        token_input=totals["token_input"],
        token_output=totals["token_output"],
        token_cache_read_input=totals["token_cache_read_input"],
        token_cache_write_input=totals["token_cache_write_input"],
    )


def normalize_runner_usage(runner: str, output: str) -> NormalizedUsage | None:
    """Route runner usage through runner-specific parsers."""
    normalized_runner = runner.strip().lower()
    if normalized_runner == "copilot":
        return normalize_copilot_footer_usage(output)
    return None
