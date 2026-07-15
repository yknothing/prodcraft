# Context Notes

This skill covers **cross-cutting instrumentation design**, not just runtime dashboards. Use it when the system needs durable telemetry contracts for:

- application events and structured logs
- metrics and traces at important boundaries
- AI execution telemetry such as skill invocation, runner execution, model usage, and token accounting
- workflow-level observability that must survive handoff across phases

This skill is intentionally distinct from `pc-monitoring-observability`:

- `pc-observability` defines **what signals should exist and how they are structured**
- `pc-monitoring-observability` turns important production signals into **dashboards, alerts, and responder workflows**

The repository's current execution contract uses append-only `execution-observability.jsonl` artifacts plus periodic summaries from `scripts/summarize_execution_observability.py`. That keeps the runtime loop concrete without committing to a heavier backend too early.

## Related Capability Notes

- `docs/observability/runtime-feedback-loop.md` -- explains how execution JSONL evidence feeds back into the skills system
