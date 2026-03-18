---
name: risk-assessment
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
  - task-breakdown
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

Risk assessment identifies what could derail the plan and what the team will do about it. In Prodcraft, this is not generic project management paperwork. It is the technical and delivery-focused pass that protects sequencing, scope, and release confidence.

This skill matters most when work crosses service boundaries, introduces migrations, depends on outside teams, or lands in brownfield systems where rollback and coexistence are real constraints.

## Inputs

- **task-list** -- The work items being considered for execution.
- **dependency-graph** -- The sequencing map that reveals where blockage or critical path fragility exists.
- **architecture-doc** -- The system context needed to identify structural and operational risk.

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

- **risk-register** -- A prioritized set of material risks with mitigations, owners, and planning consequences.

## Quality Gate

- [ ] Material technical and delivery risks are identified
- [ ] Each major risk has owner and mitigation or contingency
- [ ] The register changes sequencing, estimates, or scope where needed
- [ ] Brownfield, migration, or rollback risks are explicit when relevant
- [ ] Accepted risks are documented rather than implied

## Anti-Patterns

1. **Everything is a risk** -- noisy registers bury the few issues that matter.
2. **Risk without action** -- documenting threats but not changing the plan.
3. **Optimistic sequencing** -- keeping the same roadmap after major risks are known.
4. **Treating rollback as delivery-only** -- operational recovery constraints often have to change planning.

## Related Skills

- [task-breakdown](../task-breakdown/SKILL.md) -- supplies the work and dependency map to assess
- [estimation](../estimation/SKILL.md) -- uses the risk register to calibrate confidence
- [monitoring-observability](../../07-operations/monitoring-observability/SKILL.md) -- consumes operational risks later in the lifecycle
- [incident-response](../../07-operations/incident-response/SKILL.md) -- provides evidence when past incidents should alter future risk posture
