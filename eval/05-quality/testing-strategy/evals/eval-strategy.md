# Testing Strategy QA Strategy

## Goal

Evaluate whether `testing-strategy` produces a layered, risk-driven test plan for a concrete slice rather than a generic pyramid lecture.

## Why Start with Routed Handoff

`testing-strategy` sits downstream of `tdd` and `code-review`.

The first QA question is therefore whether the skill:

- translates the current slice and contract into the right coverage layers
- preserves unsupported-flow and coexistence risks as explicit test targets
- avoids defaulting to shallow happy-path advice
- prepares clean handoff for CI and broader QA execution

## Initial Evaluation Mode

The first evaluation is a **manual slice-to-test-strategy review** using the brownfield reassignment-flow scenario.

This is review-stage evidence only. It does not replace future isolated automated benchmarks.

## Scenario

- `access-review-modernization-testing-strategy`

Inputs:

- task slice
- API contract summary
- current code-review findings

## Assertions

1. **maps-risk-to-layer**
   - assigns unsupported-flow, auth, coexistence, and happy-path coverage to appropriate test layers

2. **preserves-brownfield-safety**
   - coexistence and release-boundary behaviors remain explicit verification targets

3. **uses-contract-aware-tests**
   - contract tests are grounded in the reviewed API behavior

4. **stays-strategic**
   - output remains a test strategy, not an implementation or architecture rewrite

5. **prepares-downstream-handoff**
   - output is usable by CI, QA execution, and implementation teams

## Pass Standard

Treat a run as strong review-stage evidence if it clearly outperforms a generic baseline on:

- risk-to-layer mapping
- unsupported/coexistence coverage
- contract-aware testing priorities
- execution readiness

## Next QA Step

After this manual review:

- add an isolated benchmark for the same brownfield slice
- add a non-brownfield feature slice to verify the skill does not overfit to compatibility-heavy work
