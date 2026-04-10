---
name: tech-debt-management
description: Use when repeated findings from reviews, incidents, retrospectives, or delivery friction need to be turned into a prioritized technical-debt registry and remediation plan, especially when brownfield seams, release-boundary gaps, or operational workarounds are accruing real engineering cost.
metadata:
  phase: 08-evolution
  inputs:
  - review-report
  - retrospective-report
  - postmortem-report
  outputs:
  - tech-debt-registry
  - remediation-plan
  prerequisites:
  - retrospective
  quality_gate: Debt registry is prioritized by impact and recurrence risk, top items have owners and routes, and capacity is allocated for remediation
  roles:
  - tech-lead
  - developer
  - architect
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/08-evolution/tech-debt-management/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Tech Debt Management

> Technical debt is a loan against your future velocity. Track it, price it, and pay it down strategically.

## Context

Every codebase accumulates technical debt -- shortcuts taken, technologies that aged, architectures that evolved beyond their original design. The problem isn't debt itself (it's sometimes a rational trade-off), but unmanaged debt that silently drains velocity and increases risk.

In a lifecycle-aware system, technical debt should be grounded in evidence. Do not dump every annoyance into a debt bucket. Focus on structural issues that repeatedly show up in reviews, incidents, slow delivery, or brittle coexistence boundaries.

## Inputs

- **review-report** -- produced by the preceding skill in the lifecycle
- **retrospective-report** -- produced by the preceding skill in the lifecycle
- **postmortem-report** -- produced by the preceding skill in the lifecycle
## Process

### Step 1: Identify Debt from Repeated Evidence

Catalog debt from multiple sources:
- **Code review findings** tagged as "tech debt"
- **Retrospective actions** that imply recurring structural fixes
- **Postmortems** showing the same release, rollback, or observability weakness
- **Architecture drift** (system no longer matches the architecture doc)
- **Missing tests or guards** in critical paths
- **Operational toil** that repeats because the system boundary is weak

Separate:
- one-off defects to fix directly
- feature work that belongs in normal roadmap planning
- real debt that is accruing interest every cycle

### Step 2: Classify Debt Type

Use the Technical Debt Quadrant (Martin Fowler):

|  | Deliberate | Inadvertent |
|---|---|---|
| **Prudent** | "We know this is a shortcut, we'll fix it in v2" | "Now we know how we should have done it" |
| **Reckless** | "We don't have time for design" | "What's a design pattern?" |

Prudent deliberate debt is a valid business choice. Reckless debt needs prevention, not just remediation.

### Step 3: Quantify Impact and Interest

For each debt item, estimate its "interest rate" -- the ongoing cost:
- How much developer time does it waste per sprint?
- What risk does it expose (security, reliability)?
- Does it block other improvements?
- What's the remediation cost?
- Does it widen brownfield coexistence or release-boundary risk?

### Step 4: Prioritize

Rank by: (impact per sprint) / (remediation cost). High-interest, low-cost debt is fixed first.

Favor debt items that:
- reduce recurrence of known incidents
- remove unsafe manual workarounds
- strengthen handoffs between lifecycle phases

### Step 5: Allocate Capacity

Dedicate a consistent percentage of sprint capacity to debt reduction:
- 20% is a common target for healthy codebases
- 30-40% for codebases with significant accumulated debt
- Track debt reduction as a team metric

For each top debt item, define:
- owner
- target window
- success signal
- next lifecycle destination (`intake`, `planning`, `implementation`, or `delivery`)

## Outputs

- **tech-debt-registry** -- produced by this skill
- **remediation-plan** -- produced by this skill
## Quality Gate

- [ ] Debt registry is current and accessible to the team
- [ ] Top debt items have remediation plans with effort estimates
- [ ] Each prioritized item has owner, timeline, and next lifecycle destination
- [ ] Sprint capacity is allocated for debt reduction
- [ ] Debt trends tracked over time (is it growing or shrinking?)

## Anti-Patterns

1. **Ignoring debt until crisis** -- By then, remediation cost has multiplied.
2. **"Debt sprint"** -- A one-time debt cleanup sprint doesn't work. Debt accumulates continuously; reduction should be continuous too.
3. **Tracking without acting** -- A beautiful Jira board of debt items that never gets worked on.
4. **Gold-plating as debt reduction** -- Rewriting working code for aesthetic reasons is not debt reduction. Focus on items with measurable impact.
5. **Debt bucket for every annoyance** -- If everything is debt, nothing is prioritized. Use evidence and recurrence, not frustration alone.

## Related Skills

- [code-review](../../05-quality/code-review/SKILL.md) -- identifies debt during review
- [refactoring](../../04-implementation/refactoring/SKILL.md) -- the primary tool for paying down debt
- [retrospective](../retrospective/SKILL.md) -- surfaces systemic debt issues
- `migration-strategy` (planned) -- for large-scale debt remediation

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/08-evolution/tech-debt-management/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
