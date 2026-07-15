---
name: pc-feature-development
description: Use when a reviewed task slice has tests or acceptance targets and the team must turn it into a small, mergeable implementation increment without expanding scope, breaking contracts, or hiding release-boundary risk.
metadata:
  phase: 04-implementation
  inputs:
  - task-list
  - architecture-doc
  - api-contract
  - test-suite
  outputs:
  - source-code
  prerequisites:
  - pc-tdd
  quality_gate: The planned slice is implemented behind passing tests, contract and scope boundaries remain explicit, and the change is ready for code review
  roles:
  - developer
  - tech-lead
  methodologies:
  - all
  effort: large
---

# Feature Development

> Implement the next reviewed slice as a small, test-backed increment that can be reviewed and delivered safely.

## Context

Feature development is where plans become working behavior.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Pick the Smallest Reviewable Slice

Choose one reviewed task or thin vertical slice. Rewrite it in concrete implementation terms: what behavior lands now, what stays out of scope, and what boundary must remain stable.

If the slice is still too large to review comfortably, split it before coding.

### Step 2: Implement Behind the Test Boundary

Use the failing or targeted tests as the implementation guardrail. Add only the code needed to satisfy the current slice. Keep new abstractions local until a second use proves they belong.

Prefer vertical progress over partial framework setup. A small end-to-end slice is more valuable than three half-finished layers.

### Step 3: Preserve Scope and Contract Boundaries

Before each commit or reviewable checkpoint, verify:

- unsupported or deferred behavior is still explicit
- public contract changes are intentional and reflected in tests
- brownfield coexistence or compatibility seams still hold
- configuration, observability, and rollout hooks required by downstream phases are not skipped

### Step 4: Prepare the Increment for Review

Clean up obvious naming, dead code, and accidental noise that would distract review, but do not turn implementation into a refactoring detour. The output should be a small, understandable diff with passing tests and explicit notes on any trade-offs.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] One reviewed task slice is fully implemented
- [ ] Relevant tests pass locally or in CI
- [ ] Scope, unsupported behavior, and release boundaries remain explicit
- [ ] Public contract changes are intentional and documented
- [ ] The diff is small enough for effective review
