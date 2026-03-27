# Live Pressure-Test Record

## Metadata

- `run_id`: `2026-03-27-PT-04-hotfix-execution-discipline-live`
- `scenario_id`: `PT-04-hotfix-incident`
- `evidence_class`: `live`
- `operator`: `codex`
- `date`: `2026-03-27`

## Request

- `request_text`: |
    Production is degrading right now after the latest deploy.

    Users are seeing intermittent 500s on a critical checkout path. We need immediate containment first, but I also need to know whether this should route through operations, implementation, or both.

    Do not assume the answer is only "ship a patch" until the route is clear.
- `hidden_context_used`: `current machine-installed prodcraft gateway plus repo-local Prodcraft contracts`

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
**Key skills needed**: incident-response, systematic-debugging, tdd, feature-development, code-review, verification-before-completion, delivery-completion, deployment-strategy
**Scope assessment**: medium
**routing_rationale**: Live checkout degradation still requires containment first, but the route now preserves the full post-containment execution chain explicitly: root-cause-first debugging, test-first fix, honest completion verification, explicit branch outcome, then rollout planning.
**Key risks**: Treating this as implementation-only could widen blast radius before containment. Treating it as operations-only could hide the required follow-on debugging and verification discipline after the service is stabilized.

### Proposed Path
1. incident-response -- triage severity, contain user impact, and decide whether rollback or a surgical patch is the fastest safe move
2. systematic-debugging -- establish the evidenced root cause after containment
3. tdd -- capture the failing checkout path before editing behavior
4. feature-development -- apply the smallest safe fix
5. code-review -- fast-track review focused on correctness and blast radius
6. verification-before-completion -- confirm the fix and handoff claim with fresh evidence
7. delivery-completion -- make the completion and integration outcome explicit
8. deployment-strategy -- deploy and verify production stability
```

## Evidence

- `cross_cutting_triggered`: `none observed at intake stage; the routed path now explicitly names verification-before-completion later in the flow`
- `artifacts_produced`: `intake-brief`
- `unused_artifacts`: `none observed at intake stage`
- `course_corrections`: `none`
- `low_value_friction`:
  - `none observed at intake stage`
- `subtraction_candidate`: `none`

## Judgment

- `essential_or_accidental`: `essential`
- `follow_up`: `run a downstream hotfix execution review to confirm that the incident-to-debugging handoff produces the expected bug-fix-report, verification-record, and delivery-decision-record`
- `notes`: |
    This run confirms that the hotfix route still starts in operations, but the
    post-containment execution chain is now materially clearer than in earlier
    runs. The route no longer compresses directly from incident handling into
    code/test/release steps; it preserves the new debugging, completion-verification,
    and delivery-completion gates explicitly. The machine-installed prodcraft
    gateway and the repo-local gateway are aligned on this behavior.
