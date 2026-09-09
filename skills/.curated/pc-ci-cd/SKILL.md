---
name: pc-ci-cd
description: Use when a repository needs automated validation, builds, packaging, or deployment, or when an existing pipeline must enforce changed test, compatibility, or release requirements.
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
  prerequisites: []
  quality_gate: Pipeline enforces applicable checks and release policy, with execution evidence and any unverified stages explicit
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

> Automate repeatable validation and delivery while preserving required approvals.

## Context

CI/CD is the backbone of reliable delivery.

See [context notes](references/context.md).

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Design Pipeline Stages

Select stages from the artifact and delivery target. A service may use:
```
Commit -> Lint -> Build -> Unit Test -> Integration Test -> Security Scan -> Deploy Staging -> Deploy Production
```

Documentation repositories may need only schema/link checks; a library or CLI may add packaging without a staging service. Each selected stage should:
- Fail fast (cheapest checks first)
- Use isolated workspaces and explicit artifact inputs
- Produce artifacts usable by downstream stages

For brownfield or compatibility-sensitive delivery, include explicit gates for:
- contract/integration behavior that protects release boundaries
- coexistence or rollback verification
- staged rollout readiness rather than a single blind production hop

### Step 2: Configure Build Environment

- Use a reproducible environment compatible with the target platform: pinned native runners or containers as appropriate
- Pin dependency versions (lockfile committed)
- Cache dependencies between runs for speed
- Matrix builds for supported platforms only

### Step 3: Automate Testing

- Place required checks at the PR, merge, or release boundary they protect
- Agree feedback-time targets from actual workload and risk; measure slow stages
- Parallelize independent suites when shared resources and cost permit it

Match stages to the reviewed test strategy rather than assuming a generic default. Unsupported-flow or coexistence tests should run where they can actually stop an unsafe deploy.

### Step 4: Configure Delivery When In Scope

- Follow the authorized release triggers, environments, and approval policy
- Use infrastructure-as-code where it manages the actual target
- Verify the rollback/recovery path before enabling deployment

For validation-only or package-build pipelines, record deployment as out of scope. A pipeline definition does not authorize a live deployment or bypass release approval.

If release boundaries or sync semantics remain constrained, use staging and gated rollout steps that fail closed rather than pipelines that assume instant full production rollout.

### Step 5: Configure Notifications

- Notify the responsible owner on actionable failure
- Link to logs and artifacts for quick debugging
- Report deployment completion according to the project's notification policy

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Configured triggers enforce the required validation and release boundaries
- [ ] Selected stages have current execution evidence; unrun stages remain explicitly unverified
- [ ] Feedback time is measured against the project's target
- [ ] Deployment environments and tested rollback apply when deployment is in scope
- [ ] Brownfield coexistence or release-boundary checks are enforced where applicable

## Anti-Patterns

1. **"It works on my machine"** -- Match supported build/runtime assumptions; containers do not replace platform requirements.
2. **Slow pipelines** -- Measure queue and execution bottlenecks before optimizing.
3. **Flaky tests in CI** -- Fix or quarantine with an owner and an explicit disposition for any affected required gate.
4. **Hidden manual steps** -- Document necessary approval or recovery actions; automate repeatable operations within that authority.
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
