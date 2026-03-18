# Task Breakdown Isolated Benchmark Plan

This benchmark tests whether `task-breakdown` produces a more implementation-ready and safer plan than baseline when invoked after reviewed design work.

## Validity Rules

- use isolated temp workspaces outside the repo for both branches
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- both branches receive the same architecture and contract inputs
- review must check sequencing quality, slice size, and dependency clarity

## Scenario 1: Greenfield Vertical Slices

Prompt:

`Break this reviewed architecture and API contract into implementation-ready tasks for a first-release approvals workflow.`

Assertions:

- tasks are small enough to complete in 1-3 days
- slices remain vertical rather than backend-first chunks
- dependencies are explicit
- no orphan tasks appear without upstream rationale

## Scenario 2: Brownfield Increment Plan

Prompt:

`Break this brownfield modernization design into reversible increments that preserve release boundaries and rollback safety.`

Assertions:

- tasks preserve coexistence and rollback constraints
- sequencing favors low-risk, high-signal increments
- characterization / regression safety work appears before behavioral changes
- migration tasks do not imply a big-bang cutover

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is more executable and lower-risk than baseline
- the task list is clearly consumable by `tdd` and implementation work without re-planning
