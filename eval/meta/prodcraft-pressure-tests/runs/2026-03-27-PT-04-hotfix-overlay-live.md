# Live Pressure-Test Record

## Metadata

- `run_id`: `2026-03-27-PT-04-hotfix-overlay-live`
- `scenario_id`: `PT-04-hotfix-incident`
- `evidence_class`: `live`
- `operator`: `codex`
- `date`: `2026-03-27`

## Request

- `request_text`: |
    Production is degrading right now after the latest deploy.

    Users are seeing intermittent 500s on a critical checkout path. We need immediate containment first, but I also need to know whether this should route through operations, implementation, or both.

    Do not assume the answer is only "ship a patch" until the route is clear.
- `hidden_context_used`: `repo-local Prodcraft contracts only`

## Routing Outcome

- `first_route_correct`: `yes`
- `clarification_rounds`: `0`
- `work_type`: `Hotfix`
- `entry_phase`: `07-operations`
- `workflow_primary`: `agile-sprint`
- `workflow_overlays`: `[hotfix]`
- `next_skill`: `incident-response`

## Preserved Intake Brief

```markdown
## Intake Brief

**Work type**: Hotfix
**Entry phase**: 07-operations
**Intake mode**: fast-track
**workflow_primary**: agile-sprint
**workflow_overlays**: [hotfix]
**Key skills needed**: incident-response, tdd, feature-development, code-review, deployment-strategy
**Scope assessment**: medium
**routing_rationale**: Live checkout degradation requires containment and severity triage before any code path is changed. The hotfix overlay keeps the path compressed, but the first move is operational control so rollback, feature-flag containment, or a minimal patch can be chosen deliberately instead of assuming implementation first.
**Key risks**: Treating this as implementation-only could widen blast radius if containment options are missed; treating it as operations-only could delay the minimal fix if rollback is insufficient.

### Proposed Path
1. incident-response -- triage severity, contain user impact, and decide whether rollback or a surgical patch is the fastest safe move
2. tdd -- capture the failing checkout path before editing behavior if code change is required
3. feature-development -- apply the smallest safe fix
4. code-review -- fast-track review focused on correctness and blast radius
5. deployment-strategy -- deploy and verify production stability
```

## Evidence

- `cross_cutting_triggered`: `documentation`
- `artifacts_produced`: `intake-brief`
- `unused_artifacts`: `none observed at intake stage`
- `course_corrections`: `none`
- `low_value_friction`:
  - `none observed at intake stage`
- `subtraction_candidate`: `none`

## Judgment

- `essential_or_accidental`: `essential`
- `follow_up`: `if containment reveals a deeper structural mismatch, verify that the later `course-correction-note` path to architecture remains sufficient`
- `notes`: |
    This run confirms that explicit workflow metadata is still valuable on urgent
    overlay-bearing routes. The `hotfix` overlay is not bookkeeping; it changes
    the route by compressing the normal lifecycle and preserving incident-first
    handling. The explicit primary workflow also matters because the overlay does
    not replace governance on its own.
