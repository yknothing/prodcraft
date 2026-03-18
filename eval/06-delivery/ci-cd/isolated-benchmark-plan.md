# CI/CD Isolated Benchmark Plan

This benchmark tests whether `ci-cd` produces a stronger delivery pipeline plan than baseline when invoked after reviewed implementation work.

## Validity Rules

- baseline and with-skill branches must run in isolated temp workspaces outside the repo
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- both branches receive the same implementation slice and release context
- review must compare gate sequencing, rollback readiness, and stage appropriateness

## Scenario 1: Standard Service Pipeline

Prompt:

`Design the CI/CD pipeline for this reviewed service change, including build, test, and staging deployment gates.`

Assertions:

- sequences build, test, and deployment stages coherently
- includes feedback-fast checks on commit / PR
- preserves staging verification before production release
- avoids bypassing the standard pipeline

## Scenario 2: Brownfield Staged Delivery

Prompt:

`Design the CI/CD pipeline for a brownfield increment that routes a percentage of traffic to a new implementation behind a facade.`

Assertions:

- includes staged rollout or percentage-based verification
- preserves rollback readiness and observability checks
- treats compatibility and migration safety as first-class delivery concerns
- avoids presenting direct production cutover as the default

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is more release-safe and operationally explicit than baseline
- the resulting pipeline plan is clearly consumable by delivery and operations teams
