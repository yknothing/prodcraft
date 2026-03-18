---
name: feasibility-study
description: Evaluate whether a product, migration, or modernization direction is viable across technical, economic, operational, and delivery constraints. Use when discovery has narrowed the opportunity enough to support a go/no-go, pivot, or scope-down decision before requirements, architecture, or major implementation begins.
metadata:
  phase: 00-discovery
  inputs:
  - market-research-report
  - user-persona-set
  outputs:
  - feasibility-report
  prerequisites:
  - market-analysis
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

Feasibility is the gate between "interesting idea" and "committed project." It prevents wasting months on ideas that are technically impossible, economically unviable, or operationally unsustainable. The output is a go/no-go/pivot decision.

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

## Quality Gate

- [ ] All four feasibility dimensions assessed
- [ ] Highest-risk technical assumption validated with POC or research
- [ ] Cost/revenue model documented with assumptions explicit
- [ ] Clear go/no-go/pivot recommendation with rationale

## Anti-Patterns

1. **Feasibility theater** -- Going through the motions when the decision is already made.
2. **Only checking technical feasibility** -- A technically brilliant product that no one will pay for is still a failure.
3. **Ignoring operational costs** -- Building is 20% of total cost. Operating, maintaining, and supporting is 80%.
4. **Binary thinking** -- "Can we build it?" is less useful than "What's the simplest version we can build?"

## Related Skills

- [market-analysis](../market-analysis/SKILL.md) -- provides market context
- [user-research](../user-research/SKILL.md) -- provides user validation
- [requirements-engineering](../../01-specification/requirements-engineering/SKILL.md) -- next step if go decision
- `tech-selection` (planned) -- builds on technical feasibility findings
