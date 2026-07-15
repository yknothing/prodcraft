---
name: pc-market-analysis
description: Use when discovery needs evidence about market demand, competitors, pricing pressure, or underserved segments for a new product or expansion idea before feasibility, user research, or requirements are finalized.
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

Market analysis is the first analytical step after intake routes work to the discovery phase.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

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

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] At least 5 competitors analyzed
- [ ] Market gaps identified with evidence (user reviews, forum posts, survey data)
- [ ] TAM/SAM/SOM estimated with methodology documented
- [ ] Opportunities ranked with clear criteria
