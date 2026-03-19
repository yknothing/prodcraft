# Cross-Cutting Concerns

## Purpose

Skills that span the entire lifecycle and apply at every phase. These are not sequential -- they are continuous practices woven into all work.

## When to Apply

Cross-cutting skills are triggered by context, not by phase transitions:
- Building UI? Apply accessibility.
- User-facing text? Apply internationalization.
- Any code, workflow, or AI execution path? Apply observability (structured events, usage accounting, logs, metrics).
- Any project? Apply documentation.
- Any recurring bug, regression, or incident symptom that may already be known? Apply bug-history-retrieval.
- Regulated industry? Apply compliance.

## Key Skills

| Skill | Applies When | Effort |
|---|---|---|
| documentation | Any phase produces artifacts worth documenting | small-medium |
| observability | Any code, workflow, or AI execution boundary needs structured telemetry and stable signal contracts | medium |
| bug-history-retrieval | A current failure may match known defects in canonical trackers, monitoring, release, or git history | small |
| accessibility | Any user interface is built or modified | small-medium |
| internationalization | Any user-facing text is created | medium |
| compliance | Regulatory or legal requirements apply | large |

## Integration Pattern

Cross-cutting skills are incorporated into the Definition of Done for each phase:
- Code review checks for observability (structured events, logs, metrics, usage accounting where relevant)
- PR checklists include accessibility verification
- Sprint definition of done includes documentation updates
- Release checklists include compliance verification

Important distinction:

- `observability` is the cross-cutting instrumentation contract
- `monitoring-observability` in `07-operations` consumes those signals for dashboards, alerts, and release/incident triage
