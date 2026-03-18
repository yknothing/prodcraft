# Testing Strategy Isolated Benchmark Plan

This benchmark tests whether `testing-strategy` produces a sharper, more risk-aligned test plan than baseline when invoked after reviewed implementation work.

## Validity Rules

- run both branches in isolated temp workspaces outside the repo
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- prompts must provide the same task, code, and contract context
- review must compare layer selection, edge-case coverage, and CI fit

## Scenario 1: API Feature Slice

Prompt:

`Create the testing strategy for this reviewed API feature slice across unit, integration, contract, and E2E levels.`

Assertions:

- defines an intentional test pyramid
- maps critical user or API paths to the right layer
- includes CI stage expectations
- avoids over-indexing on brittle E2E coverage

## Scenario 2: Brownfield Compatibility Slice

Prompt:

`Create the testing strategy for a brownfield increment that preserves old behavior behind a new facade.`

Assertions:

- includes characterization or regression coverage where legacy behavior matters
- covers coexistence and compatibility boundaries explicitly
- treats unsupported or deferred behavior as something to fail closed, not ignore
- leaves a clearly reviewable strategy artifact

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is more risk-ordered and boundary-aware than baseline
