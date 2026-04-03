# Risk Assessment Isolated Benchmark Plan

## Goal

Prove that `risk-assessment` converts a task plan into a useful risk register that changes sequencing and mitigation instead of producing generic concern lists.

## Planned Scenarios

1. `access-review-modernization-risk-register`
   - brownfield coexistence-heavy planning slice
2. `team-invite-risk-register`
   - lower-coordination planning slice without migration burden

## Comparison

1. baseline generic project risk prompt
2. explicit `risk-assessment` skill invocation

## Assertions

1. `risks-are-material`
   - the output filters out trivial noise
2. `mitigation-is-explicit`
   - major risks have owner, mitigation, or contingency
3. `plan-changes-when-risk-matters`
   - sequencing, gating, or scope changes in response to risk
4. `brownfield-risks-stay-visible`
   - coexistence, rollback, and dependency risks remain concrete
5. `does-not-turn-into-sizing`
   - the output stays distinct from estimation

## Candidate Inputs

- `fixtures/access-review-modernization-task-list.md`
- `fixtures/access-review-modernization-dependency-graph.md`
- `fixtures/access-review-modernization-architecture-risk-context.md`

## Exit Criteria for Tested Promotion

- one clean benchmark run exists for the bounded brownfield planning slice
- one lower-risk scenario exists for comparison
- downstream planning or delivery work consumes the resulting risk register cleanly
