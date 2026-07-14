# Cross-Cutting Concerns

## Purpose

Skills that span the entire lifecycle and apply at every phase. These are not sequential -- they are continuous practices woven into all work.

## When to Apply

Cross-cutting skills are triggered by context, not by phase transitions:
- Building UI? Apply `pc-accessibility`.
- User-facing text? Apply `pc-internationalization`.
- Any code, workflow, or AI execution path? Apply `pc-observability` (structured events, usage accounting, logs, metrics).
- Any project? Apply `pc-documentation`.
- Any recurring bug, regression, or incident symptom that may already be known? Apply `pc-bug-history-retrieval`.
- Regulated industry? Apply `pc-compliance`.

## Key Skills

| Skill | Applies When | Effort |
|---|---|---|
| pc-documentation | Any phase produces artifacts worth documenting | small-medium |
| pc-observability | Any code, workflow, or AI execution boundary needs structured telemetry and stable signal contracts | medium |
| pc-bug-history-retrieval | A current failure may match known defects in canonical trackers, monitoring, release, or git history | small |
| pc-accessibility | Any user interface is built or modified | small-medium |
| pc-internationalization | Any user-facing text is created | medium |
| pc-compliance | Regulatory or legal requirements apply | large |

## Integration Pattern

Cross-cutting skills are incorporated into the lifecycle through four obligation types:
- `must_consider` means the phase owner must explicitly decide whether the concern changes the work
- `must_produce` means durable output is required when the stated condition is met
- `skip_when_fast_track` documents which otherwise-expected durable outputs may be waived on approved `intake_mode=fast-track` routes
- `conditional` means the skill activates only when the listed trigger is true

The authoritative phase-by-phase injection contract lives in `rules/cross-cutting-matrix.yml`.

Important distinction:

- `pc-observability` is the cross-cutting instrumentation contract
- `pc-monitoring-observability` in `07-operations` consumes those signals for dashboards, alerts, and release/incident triage
