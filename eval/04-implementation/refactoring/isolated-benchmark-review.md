# Refactoring Isolated Benchmark Review

## Scope

This note reviews the first isolated explicit-invocation benchmark for `refactoring`.

The benchmark uses one constrained post-review cleanup slice and compares:

1. a generic baseline prompt
2. the same prompt with explicit `refactoring` skill invocation

Runner: `copilot`
Run: `eval/04-implementation/refactoring/run-2026-04-04-copilot-minimal`

## Scenario: Supported Reassignment Handler Refactor

### Baseline

The baseline was already competent. It found the duplicated create-and-sync flow, extracted a helper, and stayed within the intended cleanup boundary.

That means this is not a dramatic benchmark. The baseline already understands the shape of a reasonable structural cleanup.

### With-Skill

The with-skill branch still did the job better on the contract that matters:

- it explicitly framed the change as constrained post-review refactoring
- it kept behavior preservation and scope control central
- it added a lightweight harness check after the change instead of treating the cleanup as obviously safe
- it stayed out of policy, API, and feature expansion

The improvement is modest, but it is visible on the skill's core safety discipline.

## Judgment

This is a narrow evidence base, but it is now stronger than routed review alone:

- routed handoff review proves the code-review-to-refactoring boundary
- one isolated benchmark shows cleaner behavior-preserving discipline than baseline

Remaining gaps:

- only one duplication case exists
- the improvement is moderate rather than dramatic
- there is no larger structural-debt or tech-debt-driven benchmark yet

Those should be addressed later, but they no longer block `tested` under the current minimal promotion bar.

## Status Recommendation

- Recommended status: `tested`
