---
name: pc-task-execution
description: Use when an approved task needs bounded execution batches, checkpoints, or stop conditions because dependencies, review risk, or brownfield seams make direct execution difficult. Skip the wrapper when the next action and proof are already clear.
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
  internal: false
  distribution_surface: curated
  source_path: skills/04-implementation/pc-task-execution/SKILL.md
  public_stability: beta
  public_readiness: beta
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

If the next action and proof are already clear, execute them through the relevant implementation skill. Use this wrapper only when batching resolves a real coordination, dependency, or checkpoint problem. Do not recreate the upstream task list.

### Step 2: Build the Next Execution Batch

Convert the current slice into a short batch of steps. Each step should usually be:

- short enough to observe one meaningful result; 2-5 minutes is a planning heuristic, not a timing requirement
- independently checkable
- tied to a file, command, or concrete behavior change

For each step, record:

- action
- expected output
- verification method
- stop condition

Do not generate a long speculative script for the whole day. Produce only the next executable batch.

Keep accepted constraints and evidence as references to their existing artifacts. Crossing a batch boundary does not require another user approval when scope and authority are unchanged.

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

If a blocker hits, pause the dependent step and continue independent authorized work when useful. Resolve the blocker by choosing the smallest action:

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

- [ ] The current batch is clear enough to execute; it may equal a small parent task without artificial subdivision
- [ ] Each batch step has an expected output and verification method
- [ ] Stop conditions are explicit
- [ ] The selected implementation discipline matches the batch type
- [ ] The checkpoint states what changed and what remains unresolved

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/04-implementation/pc-task-execution/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
