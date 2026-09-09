---
name: pc-market-analysis
description: Use when discovery needs evidence about market demand, competitors, pricing pressure, or underserved segments for a new product or expansion idea before feasibility, user research, or requirements are finalized.
metadata:
  phase: 00-discovery
  inputs: []
  outputs:
  - market-research-report
  prerequisites: []
  quality_gate: Reviewed market evidence supports ranked opportunities or an explicit no-supported-opportunity conclusion
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

For relevant alternatives, including manual work and doing nothing, record pricing, capability, constraints, and user evidence. Cite sources and dates; distinguish vendor claims from observed use.

### Step 3: Identify Market Gaps

Where do existing solutions fall short? Look for:
- Underserved user segments
- Missing features repeatedly requested in reviews
- Pricing gaps (too expensive or too cheap for a segment)
- UX problems that create friction

### Step 4: Assess Market Size

Size the reachable opportunity when it affects the decision. Use bottom-up assumptions for potential buyers, access, and willingness to pay; distinguish total, serviceable, and realistically obtainable demand. Show ranges and unknowns rather than inventing missing numbers.

### Step 5: Document Opportunities

Rank supported opportunities by reachable demand, alternatives, capability fit, and timing. If none is supported, report that conclusion and the search limits; do not invent a gap to justify entry.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Relevant direct, indirect, and status-quo alternatives covered; search limits explicit
- [ ] Evidence supports the stated gaps or an explicit no-supported-opportunity conclusion
- [ ] Decision-relevant market estimates state sources, method, uncertainty, and missing evidence
- [ ] Supported opportunities are ranked, or the no-entry/further-research recommendation is explained
