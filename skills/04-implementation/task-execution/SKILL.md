---
name: task-execution
description: Use when an approved task slice already exists and the team needs a 2-5 minute execution plan with checkpoints, stop conditions, and batch discipline before or during implementation, especially when brownfield seams or review-sensitive changes make ad hoc execution unsafe.
metadata:
  phase: 04-implementation
  inputs:
  - task-list
  - dependency-graph
  - architecture-doc
  - api-contract
  outputs:
  - execution-batch-plan
  - execution-checkpoint
  prerequisites:
  - task-breakdown
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

`task-execution` is the tactical companion to `task-breakdown`.

- `task-breakdown` decides the 1-3 day implementation slice
- `task-execution` turns that slice into the next batch of 2-5 minute steps, verification points, and stop conditions

This skill exists to prevent a common failure mode: a task is "small enough" on paper, but execution still drifts into long, unverified editing sessions, hidden blockers, or broad opportunistic changes.

It does **not** replace `feature-development`, `systematic-debugging`, or `tdd`. It prepares and governs the batch that those skills will execute.

## Inputs

- **task-list** -- The approved implementation slice and done criteria.
- **dependency-graph** -- Optional but strongly preferred when the task depends on other slices or sequencing constraints.
- **architecture-doc** -- Needed when execution must preserve component boundaries or brownfield seams.
- **api-contract** -- Needed when the current batch could change externally visible behavior.

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

- bug or failing behavior first -> `systematic-debugging`
- new or changed behavior -> `tdd`
- tested slice ready to code -> `feature-development`
- structural cleanup with protected behavior -> `refactoring`

`task-execution` is the tactical wrapper around these skills, not a substitute for them.

### Step 4: Make Blockers and Stop Conditions Explicit

Name what should pause execution immediately:

- unclear task or reviewer intent
- dependency missing or still blocked
- failing verification that contradicts the current plan
- evidence that the problem belongs upstream in architecture or requirements

If a blocker hits, stop and either:

- clarify the task
- invoke `systematic-debugging`
- produce a `course-correction-note`
- return to planning if the batch no longer fits the approved slice

### Step 5: Record the Checkpoint

Produce:

- an `execution-batch-plan` for the current tactical batch
- an `execution-checkpoint` after the batch that states what changed, what was verified, what remains open, and whether the next batch is safe to start

The checkpoint should be short, factual, and handoff-friendly.

## Outputs

- **execution-batch-plan** -- The next 2-5 minute step sequence, with files, commands, verification points, and stop conditions.
- **execution-checkpoint** -- What the batch completed, how it was verified, what remains open, and the next recommended action.

## Quality Gate

- [ ] The current slice is narrower than the parent `task-list` item and clear enough to execute now
- [ ] Each batch step has an expected output and verification method
- [ ] Stop conditions are explicit
- [ ] The selected implementation discipline matches the batch type
- [ ] The checkpoint states what changed and what remains unresolved

## Anti-Patterns

1. **Plan echoing** -- repeating the 1-3 day task in different words without producing executable steps.
2. **One giant batch** -- turning tactical execution into another half-day plan.
3. **Skill substitution** -- using `task-execution` to avoid `tdd`, `systematic-debugging`, or `feature-development`.
4. **Blocker denial** -- continuing after verification fails or the task stops matching the approved slice.
5. **Checkpoint theater** -- claiming a batch is complete without saying what was verified or what remains open.

## Reference Material

For tactical execution failure modes that cause hidden drift or false progress, see [Gotchas](references/gotchas.md).

## Related Skills

- [task-breakdown](../../03-planning/task-breakdown/SKILL.md) -- defines the 1-3 day slice that this skill tactically executes
- [systematic-debugging](../systematic-debugging/SKILL.md) -- handles bug-fix batches that need root-cause-first investigation
- [tdd](../tdd/SKILL.md) -- drives behavior-changing steps with failing tests first
- [feature-development](../feature-development/SKILL.md) -- implements the approved tested slice
- [verification-before-completion](../../cross-cutting/verification-before-completion/SKILL.md) -- verifies the batch checkpoint before completion claims
