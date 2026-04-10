---
name: estimation
description: Use when reviewed tasks exist and the team must size them with explicit assumptions, confidence, and risk awareness before committing to a timeline or sprint scope.
metadata:
  phase: 03-planning
  inputs:
  - task-list
  - risk-register
  outputs:
  - estimate-set
  prerequisites:
  - task-breakdown
  quality_gate: Each task has an estimate, confidence signal, and explicit assumption set suitable for sequencing or sprint commitment
  roles:
  - tech-lead
  - developer
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/03-planning/estimation/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Estimation

> Estimate to expose uncertainty and trade-offs, not to pretend the future is certain.

## Context

Estimation converts a task list into a planning signal the team can actually use. Good estimates make assumptions explicit, separate known work from uncertainty, and prevent schedules from quietly becoming fiction.

In Prodcraft, estimation follows task breakdown and should be informed by identified risks. The goal is calibrated planning, not false precision.

## Inputs

- **task-list** -- The reviewed implementation slices to size.
- **risk-register** -- Known delivery, integration, and scope risks that should affect confidence or contingency.

## Process

### Step 1: Normalize the Unit of Estimation

Pick one estimation approach for the planning horizon: hours, ideal days, story points, or size buckets. Keep it consistent within the same plan.

### Step 2: Estimate Task by Task

For each task, record:

- base size
- confidence level
- key assumptions
- blockers or external dependencies that could widen the range

If the estimate depends on an unresolved question, say so explicitly instead of guessing low.

### Step 3: Calibrate Against Risk and History

Adjust estimates when risk, novelty, or coordination cost makes the base number misleading. Compare against similar recent work when available.

### Step 4: Publish the Estimate Set

Package the estimates in a form sprint or milestone planning can consume directly. Distinguish between:

- confident work
- work with wide uncertainty
- work that should not be scheduled until a risk or dependency is resolved

## Outputs

- **estimate-set** -- A structured set of estimates with confidence and assumptions for each planned task.

## Quality Gate

- [ ] Every planned task has an estimate
- [ ] Confidence or uncertainty is explicit
- [ ] Key assumptions and blockers are recorded
- [ ] Risk materially changes estimates where appropriate
- [ ] The output is usable by downstream sprint or milestone planning

## Anti-Patterns

1. **Single-number theater** -- one precise number hiding wide uncertainty.
2. **Estimate equals commitment** -- treating a planning signal as a promise.
3. **Ignoring coordination cost** -- sizing coding work but not integration, review, or waiting time.
4. **Optimism by silence** -- leaving assumptions unstated so the smallest number wins.

## Related Skills

- [task-breakdown](../task-breakdown/SKILL.md) -- provides the work items to size
- [risk-assessment](../risk-assessment/SKILL.md) -- surfaces the uncertainties that affect confidence
- [sprint-planning](../sprint-planning/SKILL.md) -- consumes the estimate set to choose realistic scope
- [retrospective](../../08-evolution/retrospective/SKILL.md) -- can compare actuals vs estimates for calibration

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/03-planning/estimation/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
