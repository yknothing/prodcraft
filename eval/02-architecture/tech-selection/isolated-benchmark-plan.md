# Tech Selection Isolated Benchmark Plan

## Goal

Prove that `tech-selection` converts architecture drivers into explicit, minimal, and consequence-aware stack choices instead of generic tool preference.

## Planned Scenarios

1. `access-review-modernization-tech-selection`
   - brownfield coexistence-heavy architecture with explicit operational constraints
2. `team-invite-tech-selection`
   - lower-complexity service slice with a smaller operational surface

## Comparison

1. baseline generic stack recommendation prompt
2. explicit `tech-selection` skill invocation

## Assertions

1. `decision-surface-is-bounded`
   - only unresolved technology categories are debated
2. `choices-map-to-drivers`
   - selected tools are justified against architecture and operations constraints
3. `trade-offs-are-recorded`
   - rejected alternatives and revisit triggers are explicit
4. `minimum-stack-wins`
   - the result avoids overlapping tools or unnecessary platform sprawl
5. `does-not-reopen-architecture`
   - the output stays in technology selection rather than redesigning the whole system

## Candidate Inputs

- `fixtures/access-review-modernization-requirements-summary.md`
- `fixtures/access-review-modernization-architecture-summary.md`

## Exit Criteria for Tested Promotion

- one clean benchmark run exists for the bounded brownfield architecture slice
- a second scenario exists to verify broader applicability
- downstream work confirms the resulting tech-decision record is actionable
