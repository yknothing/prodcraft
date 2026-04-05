# Feature Development Isolated Benchmark Review

## Scope

This note records the current isolated benchmark state for `feature-development`.

It now counts as a valid fixture-backed benchmark result artifact for review-stage evaluation.

Under the current minimal promotion bar, it now counts as a narrow tested-grade promotion artifact, but the evidence should still be treated as limited because the quality delta over baseline is modest.

The purpose of this note is to record the first fair implementation benchmark for the current brownfield slice and make the remaining blocker auditable.

The current primary artifact is:

- `eval/04-implementation/feature-development/run-2026-04-03-copilot-brownfield-only-fixture-rerun`

## Runtime Notes

- The benchmark asset now exists at `isolated-benchmark.json`.
- The current scenario now uses:
  - `access-review-modernization-task-slice.md`
  - `access-review-modernization-api-contract.md`
  - `fixtures/reassignments.py`
  - `fixtures/test_reassignments.py`
- A fresh `copilot` rerun completed both baseline and with-skill branches cleanly.
- The old fixture-thin and connection-failure artifacts remain useful history, but they are no longer the primary evidence.

## Scenario 1: Brownfield Compatibility Slice

### Baseline

The isolated baseline completed successfully.

Observed behavior:

- made a focused patch to the supplied module and tests
- fixed unsupported-flow handling to return `UNSUPPORTED_RELEASE1_FLOW`
- added coverage for unsupported-flow behavior and `backup_delegate`
- stayed within the supplied fixture instead of inventing a larger project structure

Why this matters:

- the baseline is now a fair control artifact for the implementation skill
- any skill lift must come from smaller diff shape, stronger contract discipline, or clearer reviewability, not from merely having enough code context

### With-Skill

The with-skill branch also completed successfully.

Observed behavior:

- read the fixture and skill body, then edited only the supplied module and tests
- fixed unsupported-flow handling to return `UNSUPPORTED_RELEASE1_FLOW`
- added explicit unsupported-flow and `backup_delegate` coverage
- kept the change reviewable and bounded to the supplied files
- but did not show a clearly stronger implementation shape than baseline
- and preserved an unresolved TODO comment instead of making the diff materially cleaner than the control case

Why this matters:

- the fairness blocker is closed, so the current question is real skill lift rather than benchmark validity
- the with-skill branch is usable, but `tested` should require clearer evidence that the skill produces a more constrained or higher-quality increment than a generic baseline

## Current Judgment

`feature-development` now qualifies for a narrow `tested` posture.

Why:

- the routed handoff review remains valid
- the benchmark is fair and both branches complete cleanly
- the current isolated result is enough to prove repository-local basic tested coverage even though the with-skill advantage over baseline is modest

## Status Recommendation

- recommended status now: `tested`

## Next Smallest Honest Step

- keep this rerun as the current primary evidence
- decide whether one more contract tightening is warranted to force smaller, cleaner implementation diffs on the same fixture
- if not, add the second forward slice promised in the QA strategy so the skill can be judged on a broader implementation surface
