---
name: pc-sprint-planning
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
  - pc-estimation
  quality_gate: The plan separates supported commitments from stretch or blocked work using actual capacity, dependency constraints, and explicit ownership
  roles:
  - tech-lead
  - product-manager
  methodologies:
  - all
  effort: small
  internal: false
  distribution_surface: curated
  source_path: skills/03-planning/pc-sprint-planning/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Sprint Planning

> Choose the next iteration on purpose. A sprint plan is a capacity-constrained bet, not a wish list.

## Context

Sprint planning turns a backlog of valid work into a realistic short-horizon commitment.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Establish the Goal and Available Capacity

Read current tasks, estimates, risks, carry-over, operational load, and the actual iteration horizon. Reuse an accepted plan when these remain unchanged. Confirm availability of the people, reviewers, shared environments, and external dependencies that constrain the work.

If capacity or a necessary owner is unknown, publish a provisional plan and identify the missing decision; do not invent a team, velocity, approval, or delivery date. Solo or agent-assisted work does not require a fictional sprint ceremony.

### Step 2: Select a Feasible Slice

Choose the smallest task set that advances the goal and fits known capacity. Respect dependency order and avoid counting shared resources twice. Parallel agents do not create independent reviewer capacity or eliminate integration work. Keep blocked or poorly understood work outside committed scope until its constraint is resolved.

### Step 3: Record Ownership and Trade-offs

For selected tasks, identify the responsible owner, start dependencies, acceptance condition, and handoff. Separate committed, stretch, deferred, and blocked work. Explain the opportunity cost when a priority displaces another item. A proposed owner is not confirmed availability.

### Step 4: Publish and Replan Deliberately

Publish `sprint-plan` under its I/O contract. When a dependency or assumption changes, show the scope/capacity trade-off and obtain approval for changed commitments. Do not silently add overtime or extend the deadline.

For a one-task horizon, a compact section in the existing plan is enough. A provisional plan can be handed off for decisions, but cannot be described as an accepted sprint commitment.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] The plan is explicitly committed or provisional according to available capacity and authority
- [ ] Selected scope accounts for dependencies, review/integration, and shared resources
- [ ] Owners, acceptance conditions, stretch work, and deferred/blocked work are explicit
- [ ] Missing decisions and replan triggers are actionable without fabricated dates or capacity

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/03-planning/pc-sprint-planning/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
