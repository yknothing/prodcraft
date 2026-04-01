# Deployment Strategy Isolated Benchmark Plan

This benchmark tests whether `deployment-strategy` produces safer rollout and rollback decisions than baseline when explicitly invoked.

## Validity Rules

- baseline and with-skill branches must run in isolated temp workspaces outside the repo
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- both branches receive the same release, pipeline, and verification context
- review must compare rollout choice, stop conditions, and rollback readiness

## Scenario 1: Standard Low-Risk Service Release

Prompt:

`Choose the deployment strategy for this reviewed service release, including rollout pattern, verification checks, and rollback steps.`

Assertions:

- chooses a proportionate rollout pattern for a low-risk release
- defines basic smoke and health checks before full traffic
- keeps rollback steps concrete
- avoids unnecessary high-friction rollout theater

## Scenario 2: Brownfield Staged Rollout

Prompt:

`Choose the deployment strategy for a brownfield release that shifts a percentage of traffic to a new implementation while preserving rollback speed.`

Assertions:

- treats staged rollout or canary expansion as the default shape
- includes observability-based stop/continue gates
- preserves rollback readiness and ownership
- does not present direct full cutover as the default

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is more risk-matched and rollback-ready than baseline
- higher-risk scenario keeps verification gates and ownership explicit
