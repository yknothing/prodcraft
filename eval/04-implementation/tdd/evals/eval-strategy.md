# TDD QA Strategy

## Goal

Evaluate whether `tdd` turns a reviewed implementation slice into a test-first execution plan that protects contracts and brownfield regressions before code changes begin.

## Why Start with Routed Handoff

`tdd` is the first implementation discipline on the core spine:

- `task-breakdown` decides the slice
- `api-design` defines the contract
- `tdd` decides whether implementation starts with safety and evidence or with guesswork

The first QA question is therefore whether the skill:

- starts from the next planned slice rather than generic coding advice
- preserves coexistence and unsupported-flow safety
- sequences RED -> GREEN -> REFACTOR credibly
- prepares clean handoff for `feature-development` and `testing-strategy`

## Initial Evaluation Mode

The first evaluation is a **manual task-to-TDD handoff review** using the brownfield access-review modernization scenario.

This is review-stage evidence only. It does not replace future isolated automated benchmarks.

## Scenario

- `access-review-modernization-tdd-handoff`

Inputs:

- a reviewed task slice
- supporting API contract summary

## Assertions

1. **starts-with-tests**
   - output begins with failing tests or explicit RED-phase ordering rather than implementation-first steps

2. **preserves-brownfield-safety**
   - coexistence, unsupported-flow, or characterization protection remains explicit

3. **uses-contract-aware-tests**
   - tests are grounded in the reviewed contract or planned task boundary

4. **stays-in-implementation-discipline**
   - output is a test-first implementation plan, not a broad planning or architecture redesign

5. **prepares-downstream-handoff**
   - output sets up `feature-development` and `testing-strategy` cleanly

## Pass Standard

Treat a run as strong review-stage evidence if it clearly outperforms a generic baseline on:

- explicit RED/GREEN/REFACTOR ordering
- coexistence/unsupported-flow safety
- contract-aware test coverage
- implementation readiness

## Next QA Step

After this manual review:

- add an isolated benchmark for the same brownfield scenario
- add a non-brownfield feature slice to verify the skill does not overfit to compatibility work
