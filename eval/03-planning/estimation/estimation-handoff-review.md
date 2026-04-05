# Estimation to Sprint Planning Handoff Review

## Goal

Verify that `estimation` produces a planning signal that `sprint-planning` can consume without guessing at uncertainty, coordination cost, or hidden scope.

## Scenario

- `access-review-modernization-estimation`

This is a brownfield planning slice where:

- coexistence with the legacy module is required
- sync semantics are not fully resolved
- rollout and verification cost should influence the estimate set

## Artifacts Reviewed

- reviewed upstream task/risk inputs:
  - `fixtures/access-review-modernization-task-list.md`
  - `fixtures/access-review-modernization-risk-register.md`
- downstream consumer boundary:
  - `sprint-planning`

## Review Findings

## 1. Estimation must stay distinct from commitment

The reviewed inputs are enough to size work, but not enough to decide what fits into a sprint.

That means `estimation` should:

- size each task explicitly
- surface confidence and blockers
- expose the coordination cost of coexistence and rollout
- hand a clean estimate set to `sprint-planning`

It should not decide sprint scope itself.

## 2. Brownfield risk should change the estimate, not just the narrative

In this scenario, the work is not all equal:

- coexistence with legacy flows increases coordination and test cost
- unresolved sync semantics widen uncertainty
- release verification depends on downstream quality work

A correct `estimation` output should make those differences visible in the numbers or ranges, not just in prose.

## 3. The downstream handoff boundary is clear

`sprint-planning` needs a committed scope, but only after estimation has exposed what is realistic.

The handoff should therefore provide:

- per-task estimates
- confidence or uncertainty markers
- explicit assumptions and blockers
- any tasks that should stay out of commitment until risk resolves

That makes the estimate set directly usable by sprint planning instead of requiring a second interpretation pass.

## Assertion Review

| Assertion | Review result | Notes |
|---|---|---|
| consistent-estimation-unit | pass | The output should keep one unit across the planning slice instead of mixing styles. |
| estimates-task-by-task | pass | Each planned task must receive a visible estimate. |
| assumptions-and-uncertainty-explicit | pass | Brownfield uncertainty should stay visible, not implied. |
| accounts-for-risk-and-coordination-cost | pass | Coexistence and rollout cost should materially affect the estimate set. |
| prepares-downstream-handoff | pass | The output should be ready for sprint-planning without translation. |

## Conclusion

This handoff review is enough to justify the promotion scaffold for `estimation`.

It does not yet justify `tested`. The remaining step is to run the isolated benchmark and compare baseline versus explicit skill invocation on the same task and risk inputs.
