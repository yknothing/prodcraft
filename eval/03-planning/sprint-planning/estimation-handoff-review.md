# Estimation to Sprint Planning Handoff Review

## Goal

Verify that `sprint-planning` is the correct routed follow-up after the team has tasks, estimates, and risks but still needs a realistic iteration commitment.

## Scenario

- `access-review-modernization-sprint-plan`

This scenario is a brownfield planning slice where:

- coexistence and rollback work still matter
- some tasks carry explicit uncertainty and should not all be committed at once
- team capacity is limited enough that not everything fits in the next iteration

## Artifacts Reviewed

- planning inputs:
  - `fixtures/access-review-modernization-task-list.md`
  - `fixtures/access-review-modernization-estimate-set.md`
  - `fixtures/access-review-modernization-risk-register.md`
  - `fixtures/access-review-modernization-capacity-note.md`

## Review Findings

## 1. The missing output is a commitment boundary

The upstream inputs already provide:

- decomposed tasks
- sizing and confidence
- major risks and mitigations

What they do not provide is a concrete answer to:

- what fits in the next sprint
- what should wait
- what is stretch rather than commitment

That is exactly the boundary `sprint-planning` should fill.

## 2. Capacity must win over desire

For this scenario, a correct sprint-planning output should:

- start from the real team capacity and carry-over constraints
- keep risky or dependency-heavy work from all landing in the same sprint
- commit only the smallest set of tasks that advances the release boundary safely

## 3. The route stays distinct from neighboring skills

This scenario should not go back to `estimation`, because the work is already sized.

It also should not remain inside `task-breakdown`, because task decomposition alone does not decide what is achievable this iteration.

The clean route is:

- `task-breakdown` produces the candidate task set
- `estimation` sizes the work
- `risk-assessment` exposes uncertainty and sequencing pressure
- `sprint-planning` chooses the actual iteration commitment

## Assertion Review

| Assertion | Review result | Notes |
|---|---|---|
| capacity-first | pass | The scenario only works if capacity constrains scope. |
| scope-is-defensible | pass | Not every task should fit into the next sprint. |
| sequence-respects-dependencies | pass | Coexistence and rollback tasks shape ordering. |
| stretch-and-defer-are-explicit | pass | The output boundary requires committed vs stretch separation. |
| does-not-collapse-into-backlog-prioritization | pass | The downstream need is an iteration plan, not a general roadmap. |

## Conclusion

This first routed handoff review is enough to justify moving `sprint-planning` from `draft` to `review`.

It does not justify `tested`. The next step is an isolated benchmark on the same bounded planning slice plus a second scenario with different capacity and lower modernization pressure.
