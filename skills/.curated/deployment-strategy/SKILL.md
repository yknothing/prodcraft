---
name: deployment-strategy
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
  - ci-cd
  quality_gate: Rollout pattern, rollback path, verification checkpoints, and ownership are explicit and rehearsable for the current release
  roles:
  - devops-engineer
  - tech-lead
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/06-delivery/deployment-strategy/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Deployment Strategy

> Decide how the release reaches production, how it is verified, and how it is reversed if reality disagrees with the plan.

## Context

CI/CD automates the path to deployment; deployment strategy decides how much risk to take on each step of that path. It selects the rollout pattern that matches the change's blast radius, reversibility, and operational visibility.

Use this skill when "deploy" is no longer a binary action. The questions are: canary or blue-green, full rollout or staged activation, what to verify before expanding traffic, and what exact action restores service if the release misbehaves.

## Inputs

- **ci-cd-pipeline** -- The automated delivery path and available gates.
- **build-artifacts** -- The exact release package that will be deployed.
- **release-plan** -- The intended scope, release window, and stakeholder expectations when one exists.

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

- **deployment-runbook** -- The chosen rollout pattern, verification sequence, rollback path, communications, and ownership for the release.

## Quality Gate

- [ ] Rollout pattern matches the release risk and blast radius
- [ ] Verification checkpoints and stop conditions are explicit
- [ ] Rollback path is concrete, fast, and tested or rehearsed
- [ ] Release ownership and communication path are documented
- [ ] The runbook is specific to this release, not a generic template

## Anti-Patterns

1. **Default full rollout** -- treating every release as equally safe.
2. **Monitoring after the fact** -- deploying first and deciding what to watch later.
3. **Rollback in theory only** -- naming rollback without documenting or rehearsing the actual path.
4. **Pipeline equals strategy** -- assuming automation alone decides rollout risk.

## Related Skills

- [ci-cd](../ci-cd/SKILL.md) -- provides the automated delivery path
- [monitoring-observability](../../07-operations/monitoring-observability/SKILL.md) -- supplies the signals used for rollout verification
- [runbooks](../../07-operations/runbooks/SKILL.md) -- operationalizes the deployment procedure after release
- [release-management](../release-management/SKILL.md) -- coordinates the broader human release process

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/06-delivery/deployment-strategy/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
