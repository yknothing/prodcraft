---
name: pc-estimation
description: Use when reviewed tasks exist and the team must size them with explicit assumptions, confidence, and risk awareness before committing to a timeline or sprint scope.
metadata:
  phase: 03-planning
  inputs:
  - task-list
  - risk-register
  outputs:
  - estimate-set
  prerequisites:
  - pc-task-breakdown
  quality_gate: Each task has an estimate, confidence signal, and explicit assumption set suitable for sequencing or sprint commitment
  roles:
  - tech-lead
  - developer
  methodologies:
  - all
  effort: medium
---

# Estimation

> Estimate to expose uncertainty and trade-offs, not to pretend the future is certain.

## Context

Estimation converts a task list into a planning signal the team can actually use.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Normalize the Unit of Estimation

Pick one estimation approach for the planning horizon: hours, ideal days, story points, or size buckets. Keep it consistent within the same plan.

### Step 2: Estimate Task by Task

For each task, record:

- base size
- confidence level
- key assumptions
- blockers or external dependencies that could widen the range

If the estimate depends on an unresolved question, say so explicitly instead of guessing low.

### Step 3: Calibrate Against Risk and History

Adjust estimates when risk, novelty, or coordination cost makes the base number misleading. Compare against similar recent work when available.

### Step 4: Publish the Estimate Set

Package the estimates in a form sprint or milestone planning can consume directly. Distinguish between:

- confident work
- work with wide uncertainty
- work that should not be scheduled until a risk or dependency is resolved

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Every planned task has an estimate
- [ ] Confidence or uncertainty is explicit
- [ ] Key assumptions and blockers are recorded
- [ ] Risk materially changes estimates where appropriate
- [ ] The output is usable by downstream sprint or milestone planning
