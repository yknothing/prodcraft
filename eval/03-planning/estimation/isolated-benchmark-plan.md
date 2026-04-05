# Estimation Isolated Benchmark Plan

This benchmark tests whether `estimation` turns reviewed task and risk context into a more honest, planning-usable estimate set than baseline.

## Validity Rules

- baseline and with-skill runs execute in isolated temp workspaces outside the repo
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- both branches receive the same task list and risk register
- review must compare uncertainty handling, unit discipline, and downstream planning usability

## Scenario 1: Brownfield Access Review Estimate Set

Prompt:

`Estimate a brownfield access-review task set where coexistence and rollback work increase delivery uncertainty.`

Assertions:

- chooses and keeps a consistent estimation unit
- sizes work task by task
- records assumptions, blockers, or confidence explicitly
- lets risk and coordination cost widen estimates where appropriate
- produces an artifact that downstream sprint planning can consume directly

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is materially stronger than baseline on uncertainty honesty and planning readiness
- no scenario collapses into backlog prioritization or architecture redesign
