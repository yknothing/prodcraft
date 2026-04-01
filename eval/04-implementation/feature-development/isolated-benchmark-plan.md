# Feature Development Isolated Benchmark Plan

This benchmark tests whether `feature-development` keeps implementation smaller, more test-bound, and more reviewable than baseline when explicitly invoked.

## Validity Rules

- baseline and with-skill branches must run in isolated temp workspaces outside the repo
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- both branches receive the same reviewed slice and test/contract context
- review must compare scope control, contract safety, and mergeability

## Scenario 1: Forward Feature Slice

Prompt:

`Implement the next reviewed reminder-delivery slice as a small mergeable increment that satisfies the agreed tests.`

Assertions:

- lands one concrete vertical slice instead of multiple adjacent improvements
- keeps implementation behind the stated tests
- leaves a diff small enough for effective review
- does not silently widen product scope

## Scenario 2: Brownfield Compatibility Slice

Prompt:

`Implement the reviewed access-review modernization slice behind the existing contract without widening scope or hiding compatibility risk.`

Assertions:

- preserves compatibility or coexistence seams explicitly
- avoids broad cleanup or architecture drift
- keeps rollout and unsupported-flow notes visible where relevant
- produces a code increment that is ready for code review

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output stays smaller and more reviewable than baseline
- brownfield scenario remains surgical rather than expanding into redesign
