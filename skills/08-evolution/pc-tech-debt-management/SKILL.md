---
name: pc-tech-debt-management
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
  prerequisites: []
  quality_gate: Debt is evidenced and prioritized, with ownership, next decisions, and proposed versus committed remediation explicit
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

Every codebase accumulates technical debt -- shortcuts taken, technologies that aged, architectures that evolved beyond their original design.

See [context notes](references/context.md).

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Identify Debt from Repeated Evidence

Use the available sources; a single evidenced recurring cost or known workaround can establish an initial item:
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
- How much time does it waste per operation or planning period?
- What risk does it expose (security, reliability)?
- Does it block other improvements?
- What's the remediation cost?
- Does it widen brownfield coexistence or release-boundary risk?

### Step 4: Prioritize

Compare ongoing impact, risk, and remediation cost using consistent units and confidence. Do not force security/reliability risk into an invented numeric ratio. Prefer high-value corrections and record trade-offs with competing work.

Favor debt items that:
- reduce recurrence of known incidents
- remove unsafe manual workarounds
- strengthen handoffs between lifecycle phases

### Step 5: Propose and Secure Remediation Capacity

Fit remediation to the actual sprint, milestone, or maintenance schedule. Propose effort and a decision owner; record capacity as committed only after the responsible owner allocates it. An unfunded item remains explicit, with a review trigger rather than a fictional deadline.

For each top debt item, define:
- owner or the named decision needed to assign one
- proposed or committed target window
- success signal
- next lifecycle destination (`pc-intake`, `planning`, `implementation`, or `delivery`)

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Debt registry is current and accessible to the team
- [ ] Top items have a bounded next action, effort range or investigation need, and decision owner
- [ ] Proposed timing/capacity is distinguished from authorized commitment
- [ ] Next lifecycle destination and success signal are clear
- [ ] Initial baseline or comparable trend is recorded; missing history is not invented

## Anti-Patterns

1. **Ignoring debt until crisis** -- By then, remediation cost has multiplied.
2. **"Debt sprint"** -- A one-time debt cleanup sprint doesn't work. Debt accumulates continuously; reduction should be continuous too.
3. **Tracking without acting** -- A beautiful Jira board of debt items that never gets worked on.
4. **Gold-plating as debt reduction** -- Rewriting working code for aesthetic reasons is not debt reduction. Focus on items with measurable impact.
5. **Debt bucket for every annoyance** -- If everything is debt, nothing is prioritized. Use evidence and recurrence, not frustration alone.
