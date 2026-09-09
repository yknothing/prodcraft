---
name: pc-task-breakdown
description: Use when an approved outcome needs implementation-ready tasks, acceptance evidence, and dependency ordering, including small changes within existing boundaries and reversible brownfield increments.
metadata:
  phase: 03-planning
  inputs:
  - architecture-doc
  - spec-doc
  - api-contract
  outputs:
  - task-list
  - dependency-graph
  prerequisites: []
  quality_gate: Each task delivers a bounded outcome with acceptance evidence, real dependencies, and no orphan work
  roles:
  - tech-lead
  - developer
  methodologies:
  - all
  effort: medium
---

# Task Breakdown

> Break work into the smallest independently reviewable outcomes, preserving real dependencies and a usable next step.

## Context

Task breakdown turns architecture and specs into actionable work items.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Identify Work Packages

Read the approved outcome and affected boundaries from current artifacts or source references. Require reviewed architecture decisions only where the change or approved workflow needs them. Identify work packages by observable behavior or contract boundary; do not invent backend, frontend, database, or infrastructure work when the target does not need it.

For brownfield work, identify work packages around **reversible seams**, coexistence adapters, compatibility boundaries, and characterization/regression safety rather than assuming replacement-only implementation.

### Step 2: Decompose into Tasks

Each task should be:
- **Bounded**: use 1-3 days as a sizing ceiling, not a minimum; a small change may be one short task
- **Independently testable** (has a clear "done" state)
- **Single-responsibility** (one concern per task)

Pattern: `[Verb] [noun] [context]`
- "Implement user registration API endpoint"
- "Create database migration for orders table"
- "Add input validation to checkout form"

Where possible, decompose into **vertical slices** that preserve user-visible or contract-visible value instead of layer-only sequences.

### Step 3: Map Dependencies

Add a dependency only when a task consumes an output or decision another task must produce. Record that dependency and why it blocks progress. Layer names alone do not establish execution order: an agreed contract can permit parallel implementation, while a risky edge case may need resolving first.

For a multi-task plan, represent dependencies as a DAG to identify the critical path. A small plan can use an inline list of edges; one task can record no dependencies. Avoid a separate diagram that adds no decision value.

Flag tasks that are blocked by unresolved upstream questions. Do not hide those blockers inside optimistic sequencing.

### Step 4: Define Done Criteria

For each task, state the observable outcome, affected boundary, acceptance evidence, and scope exclusions. Use code, tests, visual inspection, or document/contract checks according to the work. Add rollback conditions when the change has material side effects. A completed checklist without the requested behavior is not done.

### Step 5: Sequence for Optimal Flow

Order tasks to:
1. Reduce blocked time (dependencies resolved early)
2. Enable parallel work only when its coordination cost is lower than the delay it avoids
3. Deliver value incrementally (shippable slices, not layers)
4. Preserve rollback and coexistence safety when working in brownfield systems

## Brownfield Sequencing Heuristics

When the work is modernization or migration:

- sequence work around compatibility seams first
- land characterization or contract tests before risky implementation tasks
- keep legacy and new-path support explicit in the task list
- avoid public-API or data-migration commitments that depend on unresolved architecture questions
- make rollback or fallback work a first-class task where coexistence matters

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Every task is small enough to review and verify independently; short work was not expanded to meet a time quota
- [ ] Dependencies mapped and no circular dependencies
- [ ] Critical path identified
- [ ] Each task has clear done criteria
- [ ] Sequencing respects actual dependencies, risk, and coordination cost
- [ ] Brownfield tasks preserve coexistence and reversibility constraints where applicable
