# Incident Response Isolated Benchmark Plan

This benchmark tests whether `incident-response` produces a safer and more coordinated incident artifact than baseline under deliberate invocation.

## Validity Rules

- use isolated temp workspaces outside the repo for both branches
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- both branches receive the same alert or outage fixture
- review must compare containment quality, communication discipline, and scope control

## Scenario 1: Release Regression

Prompt:

`A recent release caused production checkout failures. Produce the incident response plan for the next 2 hours.`

Assertions:

- prioritizes containment before deep redesign
- defines severity, owner, and stakeholder communication
- preserves rollback and evidence capture discipline
- avoids broadening the incident into root-cause redesign work too early

## Scenario 2: Brownfield Data Integrity Risk

Prompt:

`A brownfield modernization increment is causing inconsistent access-review data. Produce the incident response plan.`

Assertions:

- favors fail-closed or containment-safe actions
- protects data integrity and coexistence boundaries
- records timeline/evidence expectations
- leaves behind a cleaner artifact for postmortem and follow-up work

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is materially safer and more coordinated than baseline
