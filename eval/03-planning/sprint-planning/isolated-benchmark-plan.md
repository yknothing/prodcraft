# Sprint Planning Isolated Benchmark Plan

## Goal

Prove that `sprint-planning` converts a sized task set into a realistic sprint commitment rather than a backlog-stuffing exercise.

## Planned Scenarios

1. `access-review-modernization-sprint-plan`
   - brownfield slice with coexistence and rollback risk
2. `team-invite-sprint-plan`
   - lower-risk service slice with simpler capacity trade-offs

## Comparison

1. baseline generic sprint-planning prompt
2. explicit `sprint-planning` skill invocation

## Assertions

1. `capacity-first`
   - actual team capacity constrains scope
2. `commitment-is-bounded`
   - committed scope is smaller than the full candidate backlog
3. `dependencies-shape-sequence`
   - task and risk order affect the sprint layout
4. `stretch-is-explicit`
   - optional work is kept out of committed scope
5. `does-not-turn-into-roadmap`
   - the result stays at iteration level rather than long-range prioritization

## Candidate Inputs

- `fixtures/access-review-modernization-task-list.md`
- `fixtures/access-review-modernization-estimate-set.md`
- `fixtures/access-review-modernization-risk-register.md`
- `fixtures/access-review-modernization-capacity-note.md`

## Exit Criteria for Tested Promotion

- one clean benchmark run exists for the bounded sprint-planning slice
- a second scenario exists with a different capacity/risk profile
- downstream execution shows the resulting sprint plan is usable and resilient to replanning
