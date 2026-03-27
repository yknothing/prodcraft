# Live Pressure-Test Record

## Metadata

- `run_id`: `2026-03-26-PT-05-docs-only-live`
- `scenario_id`: `PT-05-docs-only-change`
- `evidence_class`: `live`
- `operator`: `codex`
- `date`: `2026-03-26`

## Request

- `request_text`: |
    I only need to update technical documentation.

    There is no product behavior change, no code change, and no deployment.
    The work is to rewrite a stale runbook so another engineer can follow it without tribal knowledge.
- `hidden_context_used`: `repo-local Prodcraft contracts only`

## Routing Outcome

- `first_route_correct`: `yes`
- `clarification_rounds`: `0`
- `work_type`: `Documentation`
- `entry_phase`: `cross-cutting`
- `workflow_primary`: `agile-sprint`
- `workflow_overlays`: `[]`
- `next_skill`: `documentation`

## Preserved Intake Brief

```markdown
## Intake Brief

**Work type**: Documentation
**Entry phase**: cross-cutting
**Intake mode**: fast-track
**workflow_primary**: agile-sprint
**workflow_overlays**: []
**Key skills needed**: documentation
**Scope assessment**: small
**routing_rationale**: This request changes only durable technical docs. No product behavior, code path, or deployment boundary changes, so the clean route is direct handoff to the cross-cutting documentation skill.
**Key risks**: Existing runbook may hide stale operational assumptions if the rewrite does not preserve current operational constraints.

### Proposed Path
1. documentation -- rewrite the runbook as durable operator guidance
```

## Evidence

- `cross_cutting_triggered`: `documentation`
- `artifacts_produced`: `intake-brief`
- `unused_artifacts`: `none observed at intake stage`
- `course_corrections`: `none`
- `low_value_friction`:
  - `workflow_primary=agile-sprint` does not materially affect the route once `entry_phase=cross-cutting`
  - `workflow_overlays=[]` adds bookkeeping but no routing value
- `subtraction_candidate`: `evaluate whether docs-only intake routes can omit explicit workflow metadata from the user-facing brief or from the artifact schema`

## Judgment

- `essential_or_accidental`: `accidental`
- `follow_up`: `compare against at least one non-documentation fast-track route before narrowing the intake contract`
- `notes`: |
    This run confirms that intake can hide most of the lifecycle cleanly for a
    docs-only request. The route itself is not confusing.

    The friction appears in the structured metadata: the artifact still requires
    `workflow_primary` and `workflow_overlays` even though the route bypasses
    primary workflow composition in practice. That looks like accidental control
    plane verbosity rather than essential problem complexity.
