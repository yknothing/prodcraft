---
name: pc-risk-assessment
description: Use when planned work must be challenged for delivery, dependency, migration, security, or operational risk before the team commits to scope or sequence.
metadata:
  phase: 03-planning
  inputs:
  - task-list
  - dependency-graph
  - architecture-doc
  outputs:
  - risk-register
  prerequisites:
  - pc-task-breakdown
  quality_gate: Material delivery risks are identified, prioritized, and paired with concrete mitigation or sequencing decisions
  roles:
  - tech-lead
  - architect
  - devops-engineer
  methodologies:
  - all
  effort: medium
---

# Risk Assessment

> Make delivery risk visible before it becomes schedule surprise or production pain.

## Context

Risk assessment identifies what could derail the plan and what the team will do about it.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Identify Risk Categories

Scan for risks in at least these buckets:

- architecture or design uncertainty
- dependency and coordination risk
- migration or coexistence risk
- operational or rollback risk
- security or compliance exposure

### Step 2: Score What Matters

For each material risk, record:

- likelihood
- impact
- earliest point of detection
- mitigation or contingency
- owner

Do not clutter the register with trivialities. Focus on risks that could change sequence, scope, or release posture.

### Step 3: Convert Risk Into Planning Action

A risk register is only useful if it changes something. For each high or medium risk, decide whether to:

- change the order of tasks
- add a spike or validation step
- reduce scope
- add contingency or observability
- defer commitment until a dependency clears

### Step 4: Hand Off a Live Risk Register

Make the register concrete enough that estimation, sprint planning, and later retrospectives can reuse it. If a risk is accepted, that acceptance should be explicit.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Material technical and delivery risks are identified
- [ ] Each major risk has owner and mitigation or contingency
- [ ] The register changes sequencing, estimates, or scope where needed
- [ ] Brownfield, migration, or rollback risks are explicit when relevant
- [ ] Accepted risks are documented rather than implied
