---
name: sprint-planning
description: Use when the team has sized work and must choose a realistic iteration scope, sequence, and ownership model that fits capacity and current risk.
metadata:
  phase: 03-planning
  inputs:
  - task-list
  - estimate-set
  - risk-register
  outputs:
  - sprint-plan
  prerequisites:
  - estimation
  quality_gate: Sprint scope matches capacity, dependencies and risks are visible, and the team can explain why this slice is achievable now
  roles:
  - tech-lead
  - product-manager
  methodologies:
  - all
  effort: small
---

# Sprint Planning

> Choose the next iteration on purpose. A sprint plan is a capacity-constrained bet, not a wish list.

## Context

Sprint planning turns a backlog of valid work into a realistic short-horizon commitment. It is where business priority, engineering capacity, and delivery risk are forced into one explicit decision.

In Prodcraft, sprint planning should consume actual task, estimate, and risk artifacts. If it runs on optimism or memory, the system has already lost planning discipline.

## Inputs

- **task-list** -- Candidate work for the iteration.
- **estimate-set** -- Size and confidence data for each task.
- **risk-register** -- The risks that should constrain commitment or sequencing.

## Process

### Step 1: Start From Capacity, Not Desire

Confirm the real capacity for the iteration: available people, external blockers, carry-over work, and operational load. Adjust for on-call or release overhead when relevant.

### Step 2: Select Work That Fits the Goal

Choose the smallest set of tasks that:

- fits the available capacity
- preserves dependency order
- advances the sprint goal
- does not overload the team with too many simultaneous high-risk items

### Step 3: Make Sequence and Ownership Explicit

Document:

- what starts first
- what can run in parallel
- where handoffs occur
- which tasks are stretch goals versus committed work

### Step 4: Publish a Defensible Sprint Plan

The output should let anyone understand what the team is betting on, what was deferred, and which risks or assumptions could force replanning mid-sprint.

## Outputs

- **sprint-plan** -- Iteration scope, ordering, owners, stretch work, and explicit planning assumptions.

## Quality Gate

- [ ] Committed scope fits actual capacity
- [ ] Sequencing respects dependencies and major risks
- [ ] Stretch work is distinguished from committed work
- [ ] Deferred items are explicit
- [ ] The team can explain why the sprint is achievable

## Anti-Patterns

1. **Backlog stuffing** -- filling the sprint until capacity disappears.
2. **Risk-blind commitment** -- scheduling too many uncertain items at once.
3. **Invisible carry-over** -- pretending unfinished work from last sprint does not consume capacity.
4. **Priority without sequence** -- knowing what matters but not what must happen first.

## Related Skills

- [estimation](../estimation/SKILL.md) -- provides size and confidence data
- [risk-assessment](../risk-assessment/SKILL.md) -- keeps the plan honest about uncertainty
- [task-breakdown](../task-breakdown/SKILL.md) -- supplies the candidate task set
- [retrospective](../../08-evolution/retrospective/SKILL.md) -- feeds learnings into the next sprint plan
