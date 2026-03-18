# Tech Debt Management Isolated Benchmark Plan

This benchmark tests whether `tech-debt-management` produces a more disciplined debt registry and remediation route than baseline.

## Validity Rules

- run both branches in isolated temp workspaces outside the repo
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- both branches receive the same review, incident, or retrospective inputs
- review must compare evidence quality, prioritization logic, and remediation routing

## Scenario 1: Review-Finding Accumulation

Prompt:

`Turn these repeated code-review and testing findings into a prioritized technical-debt registry and remediation plan.`

Assertions:

- groups repeated structural debt rather than listing every complaint separately
- prioritizes by impact and recurrence risk
- assigns owners or next routes
- avoids dumping low-signal annoyances into the debt register

## Scenario 2: Brownfield Operational Workarounds

Prompt:

`Turn these brownfield incidents, rollback notes, and coexistence workarounds into a technical-debt remediation plan.`

Assertions:

- captures release-boundary and coexistence debt explicitly
- distinguishes immediate fixes from longer-term structural work
- keeps the plan grounded in repeated evidence
- leaves a clearer artifact for planning and follow-up intake

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is more evidence-based and more actionable than baseline
