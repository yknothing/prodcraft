# Sprint Planning Isolated Benchmark Review

## Scope

This note reviews the first isolated explicit-invocation benchmark for `sprint-planning`.

The benchmark uses one brownfield, capacity-constrained planning slice and compares:

1. a generic baseline prompt
2. the same prompt with explicit `sprint-planning` skill invocation

Runner: `copilot`
Run: `eval/03-planning/sprint-planning/run-2026-04-03-copilot-brownfield-minimal`

## Scenario: Brownfield Capacity-Constrained Sprint Plan

### Baseline

The baseline stayed close to the requested planning layer and did keep dependency order visible. Its main weakness was commitment discipline: it explicitly committed contract tests, coexistence checks, and the full bounded reassignment path while also admitting that this slightly exceeded the stated 4-day capacity.

That is a meaningful miss for this skill. `sprint-planning` should turn sized work into a bounded iteration commitment, not rationalize mild overcommitment.

### With-Skill

The skill-applied branch made the stronger planning decision:

- it started from the 4-day capacity directly
- it kept the risky dependency chain visible
- it split the 2-day implementation task so committed scope stayed at 3.5 days
- it kept the sync-semantics gate and the remainder of implementation in stretch instead of silently overcommitting

This is the exact behavior the skill is meant to teach: protect the commitment boundary first, then make stretch explicit.

## Judgment

This is a narrow benchmark, but it is a clean isolated run and the with-skill branch shows an observable quality improvement over baseline on the central contract of the skill.

The evidence now covers:

- routed handoff review proving the skill boundary
- one isolated benchmark proving better capacity discipline on the same bounded planning slice

Remaining gaps are real but no longer block `tested` under the current minimal promotion bar:

- only one benchmark scenario exists
- no later replanning or execution evidence exists yet

Those should be expanded in later iterations before stronger status claims.

## Status Recommendation

- Recommended status: `tested`
