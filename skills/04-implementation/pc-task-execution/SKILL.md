---
name: pc-task-execution
description: Use when an approved task slice already exists and the team needs a 2-5 minute execution plan with checkpoints, stop conditions, and batch discipline before or during implementation, especially when brownfield seams or review-sensitive changes make ad hoc execution unsafe.
metadata:
  phase: 04-implementation
  inputs:
  - task-list
  - dependency-graph
  - architecture-doc
  - api-contract
  - route-decision
  - execution-state
  outputs:
  - execution-batch-plan
  - execution-checkpoint
  - execution-state
  prerequisites:
  - pc-task-breakdown
  quality_gate: The current batch is explicit, each step is small enough to verify, stop conditions are named, and blockers are escalated instead of guessed through
  roles:
  - developer
  - tech-lead
  methodologies:
  - all
  effort: medium
---

# Task Execution

> Turn an approved task slice into a tactical execution batch before code changes sprawl or checkpoints disappear.

## Context

`pc-task-execution` is the tactical companion to `pc-task-breakdown`.

It does **not** replace `pc-feature-development`, `pc-systematic-debugging`, or `pc-tdd`; it governs the batch those skills execute.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Re-read the Current Slice Before Touching Code

Pick one approved task or one thin vertical slice from the `task-list`. Restate:

- what lands in this batch
- what is explicitly out of scope
- what boundary must not move
- what proof will show the batch is complete

If the task still reads like a multi-hour blob instead of a sequence of verifiable steps, split it before proceeding.

### Step 2: Build the Next Execution Batch

Convert the current slice into a short batch of steps. Each step should usually be:

- 2-5 minutes of work
- independently checkable
- tied to a file, command, or concrete behavior change

For each step, record:

- action
- expected output
- verification method
- stop condition

Do not generate a long speculative script for the whole day. Produce only the next executable batch.

### Step 3: Choose the Right Implementation Discipline Per Step

For each batch, route to the right implementation discipline:

- bug or failing behavior first -> `pc-systematic-debugging`
- new or changed behavior -> `pc-tdd`
- tested slice ready to code -> `pc-feature-development`
- structural cleanup with protected behavior -> `pc-refactoring`

`pc-task-execution` is the tactical wrapper around these skills, not a substitute for them.

### Step 4: Make Blockers and Stop Conditions Explicit

Name what should pause execution immediately:

- unclear task or reviewer intent
- dependency missing or still blocked
- failing verification that contradicts the current plan
- evidence that the problem belongs upstream in architecture or requirements

If a blocker hits, stop and either:

- clarify the task
- invoke `pc-systematic-debugging`
- produce a `course-correction-note`
- return to planning if the batch no longer fits the approved slice

### Step 5: Record the Checkpoint

Produce:

- an `execution-batch-plan` for the current tactical batch
- an `execution-checkpoint` after the batch that states what changed, what was verified, what remains open, and whether the next batch is safe to start

The checkpoint should be short, factual, and handoff-friendly.

If the project has opted into `execution-state.v1`, update it only through legal
lifecycle, phase, and artifact-binding records in the shared
`recorded_sequence`. Never redefine route obligations in mutable state. A gate
advance is authoritative only when the canonical state validates against the
operator-supplied route digest; a structurally valid snapshot without that pin is
not advancement authority.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] The current slice is narrower than the parent `task-list` item and clear enough to execute now
- [ ] Each batch step has an expected output and verification method
- [ ] Stop conditions are explicit
- [ ] The selected implementation discipline matches the batch type
- [ ] The checkpoint states what changed and what remains unresolved
