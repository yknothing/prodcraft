---
name: task-breakdown
description: Use when reviewed architecture or API contracts must be decomposed into implementation-ready work items, especially when sequencing, reversible brownfield increments, dependency mapping, and vertical slices must be explicit before coding begins.
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

In a lifecycle-aware system, task breakdown must preserve upstream boundaries. Do not turn unresolved architecture questions into implementation commitments. Do not decompose a brownfield modernization as if it were a clean-slate rewrite.

## Inputs

- **architecture-doc** -- Required. Provides component boundaries, seam decisions, and coexistence constraints.
- **api-contract** -- Optional but strongly preferred when implementation work includes API-facing changes or compatibility surfaces.
- **spec-doc** -- Optional amplifying input for spec-driven or waterfall paths.

## Process

### Step 1: Identify Work Packages

From the architecture, identify major work areas:
- Backend API endpoints
- Data model and migrations
- Frontend components and pages
- Infrastructure and deployment
- Integration points and third-party services

For brownfield work, identify work packages around **reversible seams**, coexistence adapters, compatibility boundaries, and characterization/regression safety rather than assuming replacement-only implementation.

### Step 2: Decompose into Tasks

Each task should be:
- **Completable in 1-3 days** (if longer, decompose further)
- **Independently testable** (has a clear "done" state)
- **Single-responsibility** (one concern per task)

Pattern: `[Verb] [noun] [context]`
- "Implement user registration API endpoint"
- "Create database migration for orders table"
- "Add input validation to checkout form"

Where possible, decompose into **vertical slices** that preserve user-visible or contract-visible value instead of layer-only sequences.

### Step 3: Map Dependencies

Identify which tasks must complete before others can start:
- Data model before API, API before frontend
- Core functionality before edge cases
- Infrastructure before deployment

Visualize as a DAG (directed acyclic graph) to identify critical path and parallelism opportunities.

Flag tasks that are blocked by unresolved upstream questions. Do not hide those blockers inside optimistic sequencing.

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
4. Preserve rollback and coexistence safety when working in brownfield systems

## Brownfield Sequencing Heuristics

When the work is modernization or migration:

- sequence work around compatibility seams first
- land characterization or contract tests before risky implementation tasks
- keep legacy and new-path support explicit in the task list
- avoid public-API or data-migration commitments that depend on unresolved architecture questions
- make rollback or fallback work a first-class task where coexistence matters

## Quality Gate

- [ ] Every task is 1-3 days of effort
- [ ] Dependencies mapped and no circular dependencies
- [ ] Critical path identified
- [ ] Each task has clear done criteria
- [ ] Tasks are sequenced for maximum parallelism
- [ ] Brownfield tasks preserve coexistence and reversibility constraints where applicable

## Anti-Patterns

1. **Horizontal slicing** -- "Build all the database layer, then all the API layer, then all the UI." Vertical slices (one feature end-to-end) deliver value faster.
2. **Mega-tasks** -- "Implement authentication" is not a task. Break into: registration, login, password reset, session management, etc.
3. **No dependencies mapped** -- Developers blocked waiting for other tasks creates idle time and frustration.
4. **Over-decomposition** -- Tasks smaller than 2 hours create overhead. Find the sweet spot.
5. **Planning as rewrite fantasy** -- Turning a coexistence architecture into a replacement-only task plan that ignores rollback and compatibility work.

## Related Skills

- [system-design](../../02-architecture/system-design/SKILL.md) -- provides the architecture to decompose
- `estimation` (planned) -- estimates effort for each task
- `sprint-planning` (planned) -- selects tasks for the sprint
- [tdd](../../04-implementation/tdd/SKILL.md) -- implements tasks test-first
