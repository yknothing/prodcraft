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
  quality_gate: The accepted slice works with current verification, preserved contracts, and a consumable review handoff
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

### Step 1: Consume the Accepted Slice

Identify the approved outcome, acceptance conditions, exclusions, and stable boundaries from current task or decision references. Do not rewrite an adequate plan or create architecture/API documents for a local change that needs none. If a required decision is missing, stop only the dependent work and route that decision to its owner.

### Step 2: Check the Behavioral Starting Point

Inspect the current implementation and relevant tests. Reuse current test-first evidence from `pc-tdd`; do not regenerate tests to repeat the handoff. If new behavior lacks a meaningful failing check, return to the applicable TDD step. Passing characterization protects existing behavior and does not prove new behavior. Continue an already-implemented slice from its actual state after checking freshness.

### Step 3: Implement One Reviewable Increment

Add the code needed for the slice. Introduce an abstraction only for a present boundary, invariant, or shared concept; a second use is neither mandatory nor sufficient by itself. Prefer vertical progress, preserving configuration, observability, compatibility, and rollout obligations that actually apply.

Record discovered contract changes instead of silently choosing new product behavior. Keep opportunistic cleanup outside the slice. Invoke `pc-task-execution` only if batching or coordination adds value; it is not another mandatory implementation pass.

### Step 4: Hand Off the Actual Result

Verify affected behavior and callers, remove accidental diff noise, and hand off the actual result under the I/O contract. Passing implementation checks do not authorize integration or replace independent approval.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] The accepted slice is implemented without unapproved scope changes
- [ ] Current relevant verification supports the implemented behavior
- [ ] Compatibility and release obligations are preserved where applicable
- [ ] The review handoff identifies the diff, evidence, and unresolved boundaries
