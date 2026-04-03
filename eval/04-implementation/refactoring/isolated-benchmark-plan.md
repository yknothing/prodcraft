# Refactoring Isolated Benchmark Plan

## Goal

Prove that `refactoring` keeps structural cleanup narrow, behavior-preserving, and reviewable under explicit execution pressure.

## Planned Scenario

- `supported-reassignment-handler-refactor`

This scenario should use a small handler that is already correct under tests but contains obvious supported-path duplication and an awkward extension seam.

## Comparison

1. baseline generic cleanup prompt
2. explicit `refactoring` skill invocation

## Assertions

1. `behavior-does-not-change`
   - the output preserves the supported and unsupported response contract
2. `duplication-targeted`
   - the output attacks the duplicated supported-path logic directly
3. `test-safety-net-used`
   - the output treats current tests as a prerequisite and adds characterization coverage only when needed
4. `scope-stays-small`
   - the output does not expand into policy changes, broader API redesign, or unrelated cleanup
5. `reviewable-step-shape`
   - the resulting plan or diff remains small enough for confident review

## Candidate Inputs

- `fixtures/reassignment_handlers.py`
- `fixtures/test_reassignment_handlers.py`
- `fixtures/reassignment-structural-review-report.md`
- `fixtures/reassignment-tech-debt-note.md`

## Exit Criteria for Tested Promotion

- one clean benchmark run exists for the constrained refactor slice
- the with-skill path stays narrower and more behavior-preserving than baseline
- findings and follow-up review agree that the skill improves structural cleanup discipline without disguising behavior change
