# Runbooks Isolated Benchmark Plan

This benchmark tests whether `runbooks` produces a clearer executable procedure than baseline for operational tasks and incidents.

## Validity Rules

- both branches run in isolated temp workspaces outside the repo
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- prompts must provide the same operational context
- review must compare trigger clarity, step safety, and rollback coverage

## Scenario 1: Standard Operational Procedure

Prompt:

`Write the runbook for rotating service credentials without downtime.`

Assertions:

- defines trigger, owner, and prerequisites
- gives step-by-step execution guidance
- includes verification and rollback steps
- avoids mixing theory with operational procedure

## Scenario 2: Brownfield Fallback Procedure

Prompt:

`Write the runbook for rolling traffic back from a new brownfield facade to the legacy path if alerts fire.`

Assertions:

- includes explicit fallback and fail-closed behavior
- preserves coexistence-safe steps
- includes communication cadence and evidence capture
- leaves a procedure another responder can actually execute under stress

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is materially more executable and safer than baseline
