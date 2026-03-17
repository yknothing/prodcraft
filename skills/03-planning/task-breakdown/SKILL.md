---
name: task-breakdown
description: Use when decomposing features, stories, or architecture into implementable tasks
metadata:
  phase: 03-planning
  inputs:
  - architecture-doc
  - spec-doc
  - api-contract
  outputs:
  - task-list
  - dependency-graph
  prerequisites:
  - system-design
  quality_gate: All tasks completable in 1-3 days, dependencies mapped, no orphan tasks
  roles:
  - tech-lead
  - developer
  methodologies:
  - all
  effort: medium
---

# Task Breakdown

> Break big work into small, shippable pieces. If a task takes more than 3 days, it's not broken down enough.

## Context

Task breakdown turns architecture and specs into actionable work items. It is the critical bridge between "what to build" and "how to build it incrementally." Good breakdown enables parallelism, reduces risk, and provides clear progress signals.

## Process

### Step 1: Identify Work Packages

From the architecture, identify major work areas:
- Backend API endpoints
- Data model and migrations
- Frontend components and pages
- Infrastructure and deployment
- Integration points and third-party services

### Step 2: Decompose into Tasks

Each task should be:
- **Completable in 1-3 days** (if longer, decompose further)
- **Independently testable** (has a clear "done" state)
- **Single-responsibility** (one concern per task)

Pattern: `[Verb] [noun] [context]`
- "Implement user registration API endpoint"
- "Create database migration for orders table"
- "Add input validation to checkout form"

### Step 3: Map Dependencies

Identify which tasks must complete before others can start:
- Data model before API, API before frontend
- Core functionality before edge cases
- Infrastructure before deployment

Visualize as a DAG (directed acyclic graph) to identify critical path and parallelism opportunities.

### Step 4: Define Done Criteria

Each task has explicit "done" criteria:
- Code written and self-reviewed
- Tests written and passing
- Documentation updated (if applicable)
- Ready for code review

### Step 5: Sequence for Optimal Flow

Order tasks to:
1. Reduce blocked time (dependencies resolved early)
2. Enable parallel work (independent tasks can happen simultaneously)
3. Deliver value incrementally (shippable slices, not layers)

## Quality Gate

- [ ] Every task is 1-3 days of effort
- [ ] Dependencies mapped and no circular dependencies
- [ ] Critical path identified
- [ ] Each task has clear done criteria
- [ ] Tasks are sequenced for maximum parallelism

## Anti-Patterns

1. **Horizontal slicing** -- "Build all the database layer, then all the API layer, then all the UI." Vertical slices (one feature end-to-end) deliver value faster.
2. **Mega-tasks** -- "Implement authentication" is not a task. Break into: registration, login, password reset, session management, etc.
3. **No dependencies mapped** -- Developers blocked waiting for other tasks creates idle time and frustration.
4. **Over-decomposition** -- Tasks smaller than 2 hours create overhead. Find the sweet spot.

## Related Skills

- [system-design](../../02-architecture/system-design/SKILL.md) -- provides the architecture to decompose
- [estimation](../estimation/SKILL.md) -- estimates effort for each task
- [sprint-planning](../sprint-planning/SKILL.md) -- selects tasks for the sprint
- [tdd](../../04-implementation/tdd/SKILL.md) -- implements tasks test-first
