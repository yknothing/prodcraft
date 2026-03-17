# Code Review QA Strategy

## Goal

Evaluate whether `code-review` identifies correctness, contract, and brownfield-boundary issues in a concrete changeset instead of drifting into generic style commentary.

## Why Start with Changeset Review

`code-review` is the first quality gate on the core spine:

- `tdd` should have forced behavior-first implementation
- `code-review` should stop unsafe or scope-breaking code from merging

The first QA question is therefore whether the skill:

- finds blockers that matter to the current task slice and contract
- preserves unsupported-flow and coexistence boundaries
- distinguishes blocking issues from weaker suggestions
- prepares clean handoff for broader quality/testing work

## Initial Evaluation Mode

The first evaluation is a **manual changeset review** using a brownfield reassignment-flow slice.

This is review-stage evidence only. It does not replace future isolated benchmark runs against real diffs.

## Scenario

- `access-review-modernization-code-review`

Inputs:

- implementation task slice
- API contract summary
- representative code and tests for the slice

## Assertions

1. **finds-blocking-contract-violations**
   - identifies when code violates the reviewed API contract or release boundary

2. **preserves-brownfield-safety**
   - identifies coexistence or unsupported-flow regressions as review concerns

3. **checks-test-adequacy**
   - calls out missing tests for unsupported or contract-sensitive behavior

4. **prioritizes-findings**
   - distinguishes blocking issues from weaker concerns

5. **stays-within-review-scope**
   - focuses on the changeset and current slice rather than demanding unrelated redesign

## Pass Standard

Treat a run as strong review-stage evidence if it clearly outperforms a generic baseline on:

- finding real blockers
- preserving contract and coexistence boundaries
- highlighting missing tests with proper severity
- keeping review scope disciplined

## Next QA Step

After this manual review:

- add an isolated benchmark against the same changeset
- add a non-brownfield feature slice to ensure the skill does not overfit to compatibility-heavy cases
