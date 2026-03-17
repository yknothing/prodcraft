---
name: ci-cd
description: Use when setting up or improving continuous integration and continuous delivery pipelines
metadata:
  phase: 06-delivery
  inputs:
  - source-code
  - test-suite
  - architecture-doc
  outputs:
  - ci-cd-pipeline
  - build-artifacts
  prerequisites:
  - testing-strategy
  quality_gate: Pipeline runs end-to-end, all stages pass, deployment to staging automated
  roles:
  - devops-engineer
  - developer
  methodologies:
  - all
  effort: medium
---

# CI/CD

> Automate everything between code commit and production deployment. Manual steps are bugs waiting to happen.

## Context

CI/CD is the backbone of reliable delivery. Continuous Integration ensures every code change is validated automatically. Continuous Delivery ensures validated code can be deployed to production at any time. Together, they reduce the risk of releases from "big scary event" to "routine operation."

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

### Step 4: Automate Deployment

- Staging: auto-deploy on merge to main
- Production: one-click (or auto) deploy with approval gate
- Use infrastructure-as-code for environment consistency
- Implement rollback automation

### Step 5: Configure Notifications

- Notify on failure (but not on success -- reduce noise)
- Link to logs and artifacts for quick debugging
- Alert on deployment completion

## Quality Gate

- [ ] Pipeline runs on every PR and merge to main
- [ ] Build time < 15 minutes for fast feedback
- [ ] All test types automated (unit, integration, security scan)
- [ ] Staging deployment automated
- [ ] Rollback mechanism tested

## Anti-Patterns

1. **"It works on my machine"** -- Containerize builds. Environment differences are bugs.
2. **Slow pipelines** -- If CI takes 30+ minutes, developers skip it. Optimize relentlessly.
3. **Flaky tests in CI** -- Quarantine or fix immediately. A flaky pipeline is a useless pipeline.
4. **Manual deployment steps** -- "SSH into the server and run this script" is not CI/CD.
5. **No rollback plan** -- Every deployment must have a tested rollback path.

## Related Skills

- [testing-strategy](../../05-quality/testing-strategy/SKILL.md) -- defines what tests to run in the pipeline
- [deployment-strategy](../deployment-strategy/SKILL.md) -- defines deployment patterns (blue-green, canary)
- [release-management](../release-management/SKILL.md) -- coordinates release process
- [monitoring-observability](../../07-operations/monitoring-observability/SKILL.md) -- post-deployment validation
