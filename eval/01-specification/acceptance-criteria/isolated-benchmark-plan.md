# Acceptance Criteria Isolated Benchmark Plan

## Goal

Prove that `acceptance-criteria` turns reviewed requirements and spec notes into measurable behavioral criteria that QA and TDD can use directly.

## Planned Scenarios

1. `password-reset-acceptance-criteria`
   - user-facing authentication flow with happy path, negative path, and security requirements

## Comparison

1. a generic baseline prompt
2. the same prompt with explicit `acceptance-criteria` skill invocation

## Assertions

1. `covers-every-important-requirement`
   - every requirement is represented by at least one criterion
2. `covers-happy-edge-error-and-security`
   - the output covers normal, failure, and security-sensitive behavior where relevant
3. `criteria-are-measurable`
   - expected outcomes are observable and testable
4. `stays-at-behavior-level`
   - the output avoids implementation-detail criteria
5. `prepares-testing-handoff`
   - QA or TDD can derive tests directly from the artifact

## Candidate Inputs

- `fixtures/password-reset-requirements.md`
- `fixtures/password-reset-spec.md`

## Exit Criteria for Tested Promotion

- one clean benchmark run exists for the bounded password-reset slice
- one routed handoff review shows downstream test planning can consume the criteria directly
