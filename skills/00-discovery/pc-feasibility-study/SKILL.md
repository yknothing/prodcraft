---
name: pc-feasibility-study
description: Use when discovery has narrowed an idea enough that the team must make a go/no-go, pivot, or scope-down decision based on technical, economic, operational, or timeline viability before requirements, architecture, or major implementation.
metadata:
  phase: 00-discovery
  inputs:
  - market-research-report
  - user-persona-set
  outputs:
  - feasibility-report
  prerequisites:
  - pc-market-analysis
  quality_gate: Go/no-go decision made with documented rationale across all feasibility dimensions
  roles:
  - product-manager
  - tech-lead
  - architect
  methodologies:
  - all
  effort: medium
---

# Feasibility Study

> Before committing resources, verify the idea can actually work -- technically, economically, and operationally.

## Context

Feasibility is the gate between "interesting idea" and "committed project." It prevents wasting months on ideas that are technically impossible, economically unviable, or operationally unsustainable.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Technical Feasibility

Can we build it?
- Are the core technical challenges solvable with known technology?
- Do we have (or can we acquire) the necessary expertise?
- Are there hard technical constraints (latency, data volume, regulatory)?
- What are the biggest technical risks?

Build a minimal proof-of-concept for the riskiest technical assumption.

### Step 2: Economic Feasibility

Should we build it?
- Estimated development cost (team size x duration x rate)
- Estimated operational cost (infrastructure, support, maintenance)
- Revenue model and projected income
- Break-even timeline
- Opportunity cost (what else could we build instead?)

### Step 3: Operational Feasibility

Can we run it?
- Do we have the team to maintain it long-term?
- What operational burden does it create (on-call, support, compliance)?
- Does it fit our existing operational capabilities?
- What new capabilities would we need to develop?

### Step 4: Timeline Feasibility

Can we ship in time?
- Is there a market window we need to hit?
- What's the minimum viable timeline?
- What scope can be delivered in that timeline?

### Step 5: Document Decision

Write a clear go/no-go/pivot recommendation:
- Summary of findings across all dimensions
- Key risks and mitigations
- Recommended next steps (proceed to specification, pivot direction, or shelve)

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] All four feasibility dimensions assessed
- [ ] Highest-risk technical assumption validated with POC or research
- [ ] Cost/revenue model documented with assumptions explicit
- [ ] Clear go/no-go/pivot recommendation with rationale
