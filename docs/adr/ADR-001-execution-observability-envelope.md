# ADR-001: Establish a Cross-Cutting Execution Observability Envelope

**Date**: 2026-03-20
**Status**: Accepted
**Deciders**: Tech lead, developer, devops engineer

## Context

Prodcraft is preparing for beta, and the repository now has multiple execution paths that call models or route skill logic:

- benchmark execution via `scripts/run_explicit_skill_benchmark.py`
- Anthropic trigger-discoverability execution via `tools/anthropic_trigger_eval/run_eval.py`
- future beta runtime paths that will invoke skills, workflows, and model runners directly

The project needs a canonical way to answer execution questions such as:

- which skill was invoked
- which runner and model executed it
- how many input and output tokens were consumed
- where time was spent
- where the chain failed, retried, or timed out

Today those concerns are not represented by a dedicated cross-cutting skill or schema. The repository only has `monitoring-observability`, which is scoped to operational telemetry, dashboards, alerts, and release triage. That is the wrong boundary for execution-level usage accounting and skill invocation events.

## Decision

We will introduce a cross-cutting `observability` capability for execution telemetry and define an **Execution Observability Envelope** with these principles:

1. A canonical cross-cutting skill owns instrumentation contracts for execution telemetry.
2. Execution telemetry uses a versioned event schema rather than ad hoc log lines.
3. Shared execution boundaries are instrumented through wrappers or adapters rather than repeated inline logging.
4. `skill_invocation`, `runner_execution`, and `model_usage` are distinct event types.
5. Model accounting uses canonical field names:
   - `model_name`
   - `token_input`
   - `token_output`
   - `token_total`
6. Missing usage data is recorded as `null` with an explicit source note; the system must not fabricate token values.
7. Initial storage is append-only JSONL so the event stream remains easy to inspect, version, and export before a heavier backend is justified.

## Consequences

### Positive
- Execution observability gets a clear repository owner and scope.
- Future benchmark, eval, and runtime paths can share one event contract.
- Cost, token usage, skill routing, and failure chains become analyzable without reverse-engineering raw output.
- The design stays compatible with later export to SQLite, OTLP, or a data warehouse.

### Negative
- The repository now owns a new cross-cutting contract that must be versioned and maintained.
- Runner-specific adapters will still be needed because Gemini and Claude do not expose identical usage data.
- JSONL is intentionally simple and will not provide rich querying by itself.

### Neutral
- `monitoring-observability` remains responsible for dashboards, alerts, and responder workflows.
- Existing benchmark and trigger-eval semantics do not change merely because they become instrumented.

## Alternatives Considered

### Alternative 1: Keep this inside `monitoring-observability`

Rejected because that skill is about production-facing telemetry, dashboards, alerts, rollback markers, and responder workflows. Mixing execution accounting into it would blur ownership and produce an unclear contract boundary.

### Alternative 2: Add ad hoc logs directly inside each runner or script

Rejected because it repeats logic, makes schema drift likely, and prevents future runtimes from sharing one consistent event model.

### Alternative 3: Start directly with OpenTelemetry or a database-backed sink

Rejected for now because beta needs a stable contract first, not an immediate backend commitment. JSONL keeps the initial layer simple while preserving upgrade paths later.

## References

- `skills/cross-cutting/observability/SKILL.md`
- `skills/07-operations/monitoring-observability/SKILL.md`
- `docs/observability/execution-event-schema-v1.md`
- `docs/observability/runtime-feedback-loop.md`
- `scripts/run_explicit_skill_benchmark.py`
- `tools/anthropic_trigger_eval/run_eval.py`
