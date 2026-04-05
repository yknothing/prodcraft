# Acceptance Criteria Eval Strategy

## Goal

Evaluate whether `acceptance-criteria` turns reviewed requirements and specs into measurable, testable criteria that QA and implementation can use directly.

## Why Routed Review First

This skill is a verification bridge, not a writing exercise. Review should confirm that it produces criteria strong enough to drive TDD and QA while staying away from implementation detail.

## Scenarios

Use two review scenarios:

1. A user-facing requirement with a clear happy path and obvious negative cases.
2. A requirement set with security, boundary, or error-path behavior that must not be left vague.

## Assertions

1. Every important requirement has at least one acceptance criterion.
2. Happy path, edge cases, error paths, and security paths are covered where relevant.
3. The criteria are measurable and testable.
4. QA can derive test cases directly from the output without guessing.
5. The criteria stay at behavior level rather than implementation detail.
6. The output makes downstream `tdd` and `testing-strategy` work easier, not harder.

## Method

Compare a rough requirements note with and without `acceptance-criteria` applied. Review the two outputs for:

- completeness of behavioral coverage
- measurability
- clarity of negative cases
- whether the criteria are ready to become tests

## Exit Criteria

Promote the skill to `review` when the criteria are specific enough that QA can turn them into test cases and engineers can use them to drive implementation. If the output is still vague or prose-only, it is not ready.
