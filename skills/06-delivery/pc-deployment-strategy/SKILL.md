---
name: pc-deployment-strategy
description: Use when a release candidate is ready and the team must choose the safest rollout pattern, verification checkpoints, and rollback path for the current risk, blast radius, and operational constraints.
metadata:
  phase: 06-delivery
  inputs:
  - ci-cd-pipeline
  - build-artifacts
  - release-plan
  outputs:
  - deployment-runbook
  prerequisites:
  - pc-ci-cd
  quality_gate: Rollout pattern, rollback path, verification checkpoints, and ownership are explicit and rehearsable for the current release
  roles:
  - devops-engineer
  - tech-lead
  methodologies:
  - all
  effort: medium
---

# Deployment Strategy

> Decide how the release reaches production, how it is verified, and how it is reversed if reality disagrees with the plan.

## Context

CI/CD automates the path to deployment; deployment strategy decides how much risk to take on each step of that path.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Classify Release Risk

Assess user impact, data migration risk, trust-boundary change, reversibility, and observability quality. Decide whether the release is low risk, staged-risk, or high risk.

### Step 2: Choose the Rollout Pattern

Match the pattern to the risk:

- **rolling** for low-risk stateless changes
- **canary** for user-facing or behavior-sensitive changes
- **blue-green** when instant rollback matters more than infrastructure cost
- **big-bang** only when the system or migration constraints truly require it

If the release cannot be observed or rolled back safely, the strategy is wrong.

### Step 3: Define Verification and Expansion Gates

Specify what must be checked before traffic increases:

- smoke tests
- error rate and latency thresholds
- dependency health
- data validation
- business event sanity checks for the changed flow

Tie each checkpoint to an owner and a stop/continue decision.

### Step 4: Write the Rollback-First Runbook

Document the exact release sequence, rollback trigger conditions, rollback commands, communication path, and post-deploy observation window. A rollout plan without a concrete rollback path is incomplete.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Rollout pattern matches the release risk and blast radius
- [ ] Verification checkpoints and stop conditions are explicit
- [ ] Rollback path is concrete, fast, and tested or rehearsed
- [ ] Release ownership and communication path are documented
- [ ] The runbook is specific to this release, not a generic template
