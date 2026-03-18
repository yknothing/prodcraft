# TDD Isolated Benchmark Plan

This benchmark evaluates whether `tdd` adds real implementation discipline when deliberately invoked.

## Validity Rules

- run baseline and with-skill cases in isolated temporary workspaces outside the repo
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- both branches receive the same reviewed task slice and acceptance context
- review must compare sequencing discipline, regression safety, and minimal-implementation behavior

## Scenario 1: Forward Feature Slice

Prompt:

`Implement the reviewed task for approval reminders using test-driven development.`

Assertions:

- starts with a failing test
- keeps implementation minimal to satisfy the test
- reruns tests to verify red/green progression
- does not jump straight into refactoring-first coding

## Scenario 2: Brownfield Regression Fix

Prompt:

`Users hit a known bug in legacy access review assignment. Apply the reviewed fix using TDD without widening scope.`

Assertions:

- writes a regression test that captures the bug
- avoids unrelated cleanup or refactor drift
- preserves backward compatibility expectations
- leaves behind a test that would catch recurrence

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output shows clearer red/green discipline than baseline
- brownfield scenario remains surgical rather than turning into broad redesign
