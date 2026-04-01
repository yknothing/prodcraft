# Feature Development QA Strategy

## Goal

Evaluate whether `feature-development` turns a reviewed, test-backed task slice into a small implementation increment without expanding scope, breaking contracts, or hiding release-boundary risk.

## Why Start with Routed Handoff

`feature-development` sits on the core implementation spine:

- `task-breakdown` chooses the slice
- `tdd` defines the test boundary
- `feature-development` turns that boundary into code that is actually reviewable

The first QA question is therefore whether the skill:

- chooses the smallest useful slice instead of broad implementation scope
- stays inside the existing test and contract boundary
- preserves unsupported-flow, compatibility, and rollout hooks
- prepares a clean handoff to `code-review`

## Initial Evaluation Mode

The first evaluation is a **manual TDD-to-implementation handoff review** using the brownfield access-review modernization scenario.

This is review-stage evidence only. It does not replace future isolated automated benchmarks.

## Scenario

- `access-review-modernization-feature-slice`

Inputs:

- reviewed task slice
- failing-test plan or test summary
- supporting contract context when the slice changes a visible boundary

## Assertions

1. **picks-smallest-reviewable-slice**
   - output narrows to one concrete increment rather than bundling adjacent work

2. **implements-behind-tests**
   - implementation is explicitly anchored to the reviewed tests or acceptance target

3. **preserves-scope-and-contract**
   - unsupported behavior, compatibility seams, and contract boundaries remain visible

4. **stays-implementation-focused**
   - output remains an implementation increment, not a new planning or architecture exercise

5. **prepares-review-handoff**
   - output leaves a clean, understandable diff shape for `code-review`

## Pass Standard

Treat a run as strong review-stage evidence if it clearly outperforms a generic baseline on:

- slice containment
- test-bound implementation discipline
- contract and compatibility safety
- reviewable diff quality

## Next QA Step

After this manual review:

- add an isolated benchmark for the same brownfield scenario
- add a forward feature slice to verify the skill does not overfit legacy-modernization work
