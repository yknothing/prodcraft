---
name: pc-estimation
description: Use when reviewed tasks exist and the team must size them with explicit assumptions, confidence, and risk awareness before committing to a timeline or sprint scope.
metadata:
  phase: 03-planning
  inputs:
  - task-list
  - risk-register
  outputs:
  - estimate-set
  prerequisites:
  - pc-task-breakdown
  quality_gate: Tasks have comparable estimate ranges or explicit unknowns, with units, assumptions, and evidence sufficient for the planning decision
  roles:
  - tech-lead
  - developer
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/03-planning/pc-estimation/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Estimation

> Estimate to expose uncertainty and trade-offs, not to pretend the future is certain.

## Context

Estimation converts a task list into a planning signal the team can actually use.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Identify the Planning Decision

Estimate only enough to compare scope, sequence work, or assess a requested deadline. A single authorized short task may need only an uncertainty note unless the route requires more. Reuse accepted estimates when scope, dependencies, capacity, and execution assumptions still match.

### Step 2: State Units and Evidence

Choose compatible units for the decision. Keep relative size separate from elapsed time; never add story points to hours or convert them without calibration. Use comparable completed work when available and state differences.

Separate active work, external waiting, review/integration, and risk contingency. For agent-assisted execution, identify human review and tool/runtime dependencies; do not convert human days into agent minutes or assume speedup without comparable measured runs.

### Step 3: Size the Work With Visible Uncertainty

For each relevant task, record a range or size bucket, confidence, assumptions, and evidence. Mark unresolved work unknown when a credible range is unavailable; name the fact or bounded investigation that would make it estimable. Do not manufacture a point estimate to fill the table.

Include shared setup and dependencies once. Show sequencing constraints so parallel-looking tasks do not imply elapsed-time savings they cannot deliver.

### Step 4: Hand Off the Planning Signal

Publish the `estimate-set` under its I/O contract. Distinguish schedulable from blocked or low-confidence work and state re-estimation triggers. The estimate informs `pc-sprint-planning`; it does not promise delivery or assign capacity.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Relevant tasks have comparable ranges/buckets or explicit unknowns
- [ ] Units, evidence, confidence, dependencies, and assumptions are visible
- [ ] Active work and waiting are distinguished without invented agent-speed claims
- [ ] The consumer can identify schedulable work and re-estimation triggers

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/03-planning/pc-estimation/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
