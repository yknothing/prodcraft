# Code Review Isolated Benchmark Plan

This benchmark tests whether `code-review` produces sharper, better-prioritized review feedback than baseline when explicitly invoked.

## Validity Rules

- baseline and with-skill runs execute in isolated temporary workspaces outside the repo
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- both branches receive the same changeset, task context, and test evidence
- review must compare issue severity, contract awareness, and noise ratio

## Scenario 1: Authorization Boundary Change

Prompt:

`Review this changeset that modifies tenant-scoped authorization for admin actions.`

Assertions:

- surfaces security and tenant-boundary risks explicitly
- distinguishes blocking issues from suggestions
- checks tests for negative and unauthorized paths
- avoids nit-heavy feedback dominating substantive risks

## Scenario 2: Brownfield Compatibility Change

Prompt:

`Review this migration-related changeset that adds a facade while preserving an old API contract.`

Assertions:

- checks backward compatibility and coexistence risks
- calls out unresolved release-boundary assumptions
- verifies rollback or failure handling concerns where relevant
- leaves a review artifact that is actionable for the author

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is more risk-ordered and less noisy than baseline
- no scenario receives approval-style feedback while blocking issues remain visible
