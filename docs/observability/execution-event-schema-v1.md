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
| `usage_source` | string | `provider`, `runner`, `derived`, or `unavailable` |

Rules:

- Use these exact field names.
- If usage data cannot be obtained, all token fields MUST be `null`.
- When usage is missing, set `usage_source: "unavailable"` and prefer `event_type: "model_usage.unavailable"`.
- Do not estimate token values unless the event explicitly marks them as derived.

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
  "usage_source": "provider",
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
  "usage_source": "unavailable",
  "metadata": {
    "reason": "runner stream did not expose token usage"
  }
}
```
