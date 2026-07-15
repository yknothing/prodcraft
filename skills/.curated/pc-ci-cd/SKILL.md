---
name: pc-ci-cd
description: Use when a reviewed implementation slice needs an automated build, test, and deployment pipeline, especially when brownfield rollback, release-boundary checks, contract/integration gates, and staged delivery must be explicit before shipping.
metadata:
  phase: 06-delivery
  inputs:
  - source-code
  - test-strategy-doc
  - architecture-doc
  - task-list
  outputs:
  - ci-cd-pipeline
  - build-artifacts
  prerequisites:
  - pc-testing-strategy
  quality_gate: Pipeline runs end-to-end, all stages pass, deployment to staging automated
  roles:
  - devops-engineer
  - developer
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/06-delivery/pc-ci-cd/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# CI/CD

> Automate everything between code commit and production deployment. Manual steps are bugs waiting to happen.

## Context

CI/CD is the backbone of reliable delivery.

See [context notes](references/context.md).

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Design Pipeline Stages

A typical pipeline:
```
Commit -> Lint -> Build -> Unit Test -> Integration Test -> Security Scan -> Deploy Staging -> Deploy Production
```

Each stage should:
- Fail fast (cheapest checks first)
- Run in isolation (no shared state between stages)
- Produce artifacts usable by downstream stages

For brownfield or compatibility-sensitive delivery, include explicit gates for:
- contract/integration behavior that protects release boundaries
- coexistence or rollback verification
- staged rollout readiness rather than a single blind production hop

### Step 2: Configure Build Environment

- Use containerized builds for reproducibility (same result locally and in CI)
- Pin dependency versions (lockfile committed)
- Cache dependencies between runs for speed
- Matrix builds for multi-platform support

### Step 3: Automate Testing

- Unit tests run on every commit (< 5 min)
- Integration tests run on every PR (< 15 min)
- E2E tests run before deployment (< 30 min)
- Parallelize test suites where possible

Match stages to the reviewed test strategy rather than assuming a generic default. Unsupported-flow or coexistence tests should run where they can actually stop an unsafe deploy.

### Step 4: Automate Deployment

- Staging: auto-deploy on merge to main
- Production: one-click (or auto) deploy with approval gate
- Use infrastructure-as-code for environment consistency
- Implement rollback automation

If release boundaries or sync semantics remain constrained, use staging and gated rollout steps that fail closed rather than pipelines that assume instant full production rollout.

### Step 5: Configure Notifications

- Notify on failure (but not on success -- reduce noise)
- Link to logs and artifacts for quick debugging
- Alert on deployment completion

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Pipeline runs on every PR and merge to main
- [ ] Build time < 15 minutes for fast feedback
- [ ] All test types automated (unit, integration, security scan)
- [ ] Staging deployment automated
- [ ] Rollback mechanism tested
- [ ] Brownfield coexistence or release-boundary checks are enforced where applicable

## Anti-Patterns

1. **"It works on my machine"** -- Containerize builds. Environment differences are bugs.
2. **Slow pipelines** -- If CI takes 30+ minutes, developers skip it. Optimize relentlessly.
3. **Flaky tests in CI** -- Quarantine or fix immediately. A flaky pipeline is a useless pipeline.
4. **Manual deployment steps** -- "SSH into the server and run this script" is not CI/CD.
5. **No rollback plan** -- Every deployment must have a tested rollback path.
6. **Pipeline that ignores release boundaries** -- Shipping a generic pipeline that never verifies unsupported-flow behavior, coexistence, or rollback readiness for the current slice.

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/06-delivery/pc-ci-cd/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
