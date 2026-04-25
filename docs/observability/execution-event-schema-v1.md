# Execution Event Schema v1

## Purpose

This document defines the canonical event schema for **execution observability** in Prodcraft.

It is intended for:

- skill invocation tracking
- runner execution tracking
- model usage and token accounting
- future cost and latency analysis across benchmark, eval, and beta runtime paths

This schema is owned by the cross-cutting `observability` capability. It is distinct from production dashboards and alerts handled by `monitoring-observability`.

## Storage Format

Initial storage format: **JSON Lines (`.jsonl`)**

- one event per line
- append-only
- stable enough for local inspection, artifact retention, and later export

## Versioning Rules

- Each event MUST include `schema_version`
- v1 events use `schema_version: "execution-event.v1"`
- Additive fields are allowed in minor revisions if old consumers can ignore them
- Renames or semantic changes require a new major schema version

## Event Types

Every event MUST declare one of these `event_type` values:

- `skill_invocation.started`
- `skill_invocation.completed`
- `skill_invocation.failed`
- `skill_context.measured`
- `runner_execution.started`
- `runner_execution.completed`
- `runner_execution.failed`
- `model_usage.completed`
- `model_usage.unavailable`

## Required Common Fields

Every event MUST contain:

| Field | Type | Description |
|---|---|---|
| `schema_version` | string | Schema identifier, e.g. `execution-event.v1` |
| `timestamp` | string | UTC ISO-8601 timestamp |
| `trace_id` | string | Correlates the full execution chain |
| `span_id` | string | Unique event or span identifier |
| `parent_span_id` | string or null | Parent span when nested |
| `event_type` | string | Canonical event type |
| `status` | string | `started`, `completed`, `failed`, or `unavailable` |
| `runner` | string or null | e.g. `gemini`, `claude`, `beta-runtime` |
| `model_name` | string or null | Exact model identifier when known |
| `skill_name` | string or null | Prodcraft skill name when relevant |
| `phase` | string or null | Lifecycle phase when relevant |
| `workflow` | string or null | Workflow or route label when known |
| `duration_ms` | integer or null | Duration for completed or failed spans |
| `artifact_path` | string or null | Related output path if any |
| `metadata` | object | Extra structured context |

## Canonical Usage Fields

These fields are the standard representation for model usage:

| Field | Type | Meaning |
|---|---|---|
| `token_input` | integer or null | Prompt / input tokens |
| `token_output` | integer or null | Completion / output tokens |
| `token_total` | integer or null | Sum of known token counts |
| `token_cache_read_input` | integer or null | Input tokens read from prompt cache when the runner exposes them |
| `token_cache_write_input` | integer or null | Input tokens written to prompt cache when the runner exposes them |
| `usage_source` | string | `provider`, `runner`, or `unavailable` |
| `usage_precision` | string or null | `exact`, `estimated`, `unknown`, or `unavailable` |

Rules:

- Use these exact field names.
- If usage data cannot be obtained, all token fields MUST be `null`.
- When usage is missing, set `usage_source: "unavailable"` and prefer `event_type: "model_usage.unavailable"`.
- Do not mix exact and estimated token values in the same aggregate.
- `model_usage.completed` should use provider usage when available and set `usage_precision: "exact"`.
- Runner-reported usage is allowed with `usage_source: "runner"`, but it MUST set `usage_precision`. If the runner labels the value as an estimate, record `usage_precision: "estimated"` and keep it out of exact totals.
- `skill_context.measured` MUST NOT populate token fields unless a model-specific tokenizer or provider token-count API was actually used. Without that, set token fields to `null`, set `usage_source: "unavailable"`, and record exact byte/character counts in `metadata`.

## Recommended Additional Fields

These fields are optional but recommended when available:

| Field | Type | Description |
|---|---|---|
| `request_id` | string or null | Provider or runner request ID |
| `invocation_reason` | string or null | Why the skill was invoked |
| `route_target` | string or null | Next skill or route target |
| `error_type` | string or null | Normalized error classification |
| `error_message` | string or null | Safe failure summary |
| `timeout_ms` | integer or null | Configured timeout |
| `cost_usd_estimate` | number or null | Optional estimated cost when pricing data is reliable |

## Skill Context Measurement

`skill_context.measured` records the static context cost of a skill activation. It is not a substitute for model-provider token usage. It answers a different question: how much skill material became part of the execution path, and how much stayed deferred by progressive disclosure.

Recommended `metadata` fields:

| Field | Type | Description |
|---|---|---|
| `load_stage` | string | e.g. `metadata`, `skill_body`, `supporting_file`, `script_output` |
| `loaded_file_count` | integer | Number of skill files loaded into context for this event |
| `loaded_context_char_count` | integer or null | Exact loaded skill-context character count |
| `deferred_context_char_count` | integer or null | Exact available-but-not-loaded character count |
| `available_context_char_count` | integer or null | Exact loaded plus deferred character count |
| `loaded_context_byte_count` | integer or null | Exact loaded UTF-8 byte count |
| `deferred_context_byte_count` | integer or null | Exact available-but-not-loaded UTF-8 byte count |
| `available_context_byte_count` | integer or null | Exact loaded plus deferred UTF-8 byte count |
| `skill_metadata_char_count` | integer or null | Exact trigger/discovery metadata character count |
| `skill_body_char_count` | integer or null | Exact skill body character count |
| `supporting_context_file_count` | integer or null | Number of supporting files available below the skill directory |
| `token_count_status` | string | `exact` only when a model-specific tokenizer/provider counter was used; otherwise `unavailable` |

Initial local measurement uses exact character and UTF-8 byte counts. Token counts remain unavailable until the runner or provider exposes exact usage for the relevant model/tokenizer.

## Example: Skill Invocation Completed

```json
{
  "schema_version": "execution-event.v1",
  "timestamp": "2026-03-20T12:00:00Z",
  "trace_id": "trc_01JQEXAMPLE",
  "span_id": "spn_01JQSKILL",
  "parent_span_id": "spn_01JQRUN",
  "event_type": "skill_invocation.completed",
  "status": "completed",
  "runner": "gemini",
  "model_name": "gemini-2.5-pro",
  "skill_name": "intake",
  "phase": "00-discovery",
  "workflow": "brownfield",
  "duration_ms": 1820,
  "artifact_path": "eval/00-discovery/intake/post-redesign-benchmark-run-2026-03-19-gemini-naming-rerun/eval-2-legacy-permissions-migration/with_skill/response.md",
  "token_input": 914,
  "token_output": 287,
  "token_total": 1201,
  "token_cache_read_input": 0,
  "token_cache_write_input": 0,
  "usage_source": "provider",
  "usage_precision": "exact",
  "metadata": {
    "invocation_reason": "migration request requires routing and path comparison",
    "route_target": "problem-framing"
  }
}
```

## Example: Usage Unavailable

```json
{
  "schema_version": "execution-event.v1",
  "timestamp": "2026-03-20T12:00:01Z",
  "trace_id": "trc_01JQEXAMPLE",
  "span_id": "spn_01JQUSAGE",
  "parent_span_id": "spn_01JQRUN",
  "event_type": "model_usage.unavailable",
  "status": "unavailable",
  "runner": "claude",
  "model_name": "claude-sonnet-4-5",
  "skill_name": "intake",
  "phase": "00-discovery",
  "workflow": "discoverability-eval",
  "duration_ms": null,
  "artifact_path": null,
  "token_input": null,
  "token_output": null,
  "token_total": null,
  "token_cache_read_input": null,
  "token_cache_write_input": null,
  "usage_source": "unavailable",
  "usage_precision": "unavailable",
  "metadata": {
    "reason": "runner stream did not expose token usage"
  }
}
```
