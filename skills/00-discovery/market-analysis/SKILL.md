---
name: market-analysis
description: Use when exploring a new product idea, evaluating market opportunity, or assessing competitive landscape
metadata:
  phase: 00-discovery
  inputs: []
  outputs:
  - market-research-report
  prerequisites: []
  quality_gate: Market research report reviewed and opportunities ranked by viability
  roles:
  - product-manager
  methodologies:
  - all
  effort: medium
---

# Market Analysis

> Understand the market before building the product. Validate that a real opportunity exists.

## Context

Market analysis is the first analytical step after intake routes work to the discovery phase. It answers: "Is there a market for this?" before investing in specification or architecture. Skip this for internal tools or when the market is already well-understood.

## Process

### Step 1: Define Market Scope

Identify the target market segment. Be specific -- "project management for freelance designers" not "project management."

### Step 2: Analyze Competitors

Map existing solutions:
- Direct competitors (same problem, same approach)
- Indirect competitors (same problem, different approach)
- Adjacent solutions (related problem, potential pivot)

For each: note pricing, features, strengths, weaknesses, user reviews.

### Step 3: Identify Market Gaps

Where do existing solutions fall short? Look for:
- Underserved user segments
- Missing features repeatedly requested in reviews
- Pricing gaps (too expensive or too cheap for a segment)
- UX problems that create friction

### Step 4: Assess Market Size

Estimate TAM (Total Addressable Market), SAM (Serviceable Available Market), SOM (Serviceable Obtainable Market). Use bottom-up estimation when possible (number of potential users x willingness to pay).

### Step 5: Document Opportunities

Rank opportunities by: market size, competition intensity, team capability fit, and time-to-market.

## Outputs

- **market-research-report**: Competitor map, gap analysis, market size estimates, ranked opportunities with rationale.

## Quality Gate

- [ ] At least 5 competitors analyzed
- [ ] Market gaps identified with evidence (user reviews, forum posts, survey data)
- [ ] TAM/SAM/SOM estimated with methodology documented
- [ ] Opportunities ranked with clear criteria

## Anti-Patterns

1. **Analysis paralysis** -- Spending weeks on research when a week suffices. Set a timebox.
2. **Confirmation bias** -- Only looking for evidence that supports the idea. Actively seek disconfirming evidence.
3. **Ignoring indirect competitors** -- Users solve problems with spreadsheets, email, or manual processes. These are competitors too.
4. **Vanity TAM** -- "The global software market is $500B." Narrow to the specific segment you can actually serve.

## Related Skills

- [user-research](../user-research/SKILL.md) -- runs in parallel to validate personas
- [feasibility-study](../feasibility-study/SKILL.md) -- consumes market-research-report
- [requirements-engineering](../../01-specification/requirements-engineering/SKILL.md) -- consumes market-research-report
