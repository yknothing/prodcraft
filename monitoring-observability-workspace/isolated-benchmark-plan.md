# Monitoring and Observability Isolated Benchmark Plan

This benchmark tests whether `monitoring-observability` produces a more actionable observability plan than baseline when invoked after delivery work.

## Validity Rules

- baseline and with-skill runs execute in isolated temp workspaces outside the repo
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- both branches receive the same service/release context
- review must compare user-impact visibility, alert quality, and rollback observability

## Scenario 1: New Service Release

Prompt:

`Design the monitoring and observability setup for a newly released approvals service before it goes fully live.`

Assertions:

- focuses on user-impactful signals rather than metric sprawl
- includes actionable alerting and dashboard expectations
- distinguishes fast feedback from deep diagnostic signals
- covers rollback health where applicable

## Scenario 2: Brownfield Coexistence Release

Prompt:

`Design observability for a brownfield release that routes some traffic to a new implementation while legacy behavior remains active.`

Assertions:

- makes coexistence boundaries and unsupported-flow safety visible
- includes migration or queue/backfill health signals if relevant
- avoids generic dashboards that blur old/new behavior together
- leaves an artifact operations can act on quickly

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is more operationally actionable than baseline
