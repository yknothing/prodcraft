---
name: tech-debt-management
description: Use when cataloging, prioritizing, and planning remediation of technical debt
metadata:
  phase: 08-evolution
  inputs:
  - source-code
  - review-report
  - performance-report
  - retrospective-report
  outputs:
  - tech-debt-registry
  - remediation-plan
  prerequisites:
  - code-review
  quality_gate: Debt registry current, top 5 items have remediation plans, team has allocated capacity
  roles:
  - tech-lead
  - developer
  - architect
  methodologies:
  - all
  effort: medium
---

# Tech Debt Management

> Technical debt is a loan against your future velocity. Track it, price it, and pay it down strategically.

## Context

Every codebase accumulates technical debt -- shortcuts taken, technologies that aged, architectures that evolved beyond their original design. The problem isn't debt itself (it's sometimes a rational trade-off), but unmanaged debt that silently drains velocity and increases risk.

## Process

### Step 1: Identify Debt Sources

Catalog debt from multiple sources:
- **Code review findings** tagged as "tech debt"
- **TODO/FIXME/HACK comments** in source code
- **Outdated dependencies** with security vulnerabilities or missing features
- **Architecture drift** (system no longer matches the architecture doc)
- **Missing tests** in critical paths
- **Performance bottlenecks** deferred from previous sprints

### Step 2: Classify Debt Type

Use the Technical Debt Quadrant (Martin Fowler):

|  | Deliberate | Inadvertent |
|---|---|---|
| **Prudent** | "We know this is a shortcut, we'll fix it in v2" | "Now we know how we should have done it" |
| **Reckless** | "We don't have time for design" | "What's a design pattern?" |

Prudent deliberate debt is a valid business choice. Reckless debt needs prevention, not just remediation.

### Step 3: Quantify Impact

For each debt item, estimate its "interest rate" -- the ongoing cost:
- How much developer time does it waste per sprint?
- What risk does it expose (security, reliability)?
- Does it block other improvements?
- What's the remediation cost?

### Step 4: Prioritize

Rank by: (impact per sprint) / (remediation cost). High-interest, low-cost debt is fixed first.

### Step 5: Allocate Capacity

Dedicate a consistent percentage of sprint capacity to debt reduction:
- 20% is a common target for healthy codebases
- 30-40% for codebases with significant accumulated debt
- Track debt reduction as a team metric

## Quality Gate

- [ ] Debt registry is current and accessible to the team
- [ ] Top 5 items have remediation plans with effort estimates
- [ ] Sprint capacity is allocated for debt reduction
- [ ] Debt trends tracked over time (is it growing or shrinking?)

## Anti-Patterns

1. **Ignoring debt until crisis** -- By then, remediation cost has multiplied.
2. **"Debt sprint"** -- A one-time debt cleanup sprint doesn't work. Debt accumulates continuously; reduction should be continuous too.
3. **Tracking without acting** -- A beautiful Jira board of debt items that never gets worked on.
4. **Gold-plating as debt reduction** -- Rewriting working code for aesthetic reasons is not debt reduction. Focus on items with measurable impact.

## Related Skills

- [code-review](../../05-quality/code-review/SKILL.md) -- identifies debt during review
- [refactoring](../../04-implementation/refactoring/SKILL.md) -- the primary tool for paying down debt
- [retrospective](../retrospective/SKILL.md) -- surfaces systemic debt issues
- [migration-strategy](../migration-strategy/SKILL.md) -- for large-scale debt remediation
