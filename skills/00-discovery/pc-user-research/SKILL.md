---
name: pc-user-research
description: Use when discovery needs evidence about target users, behaviors, and pain points, especially after intake or problem-framing surfaces open questions that must be validated before requirements are written
metadata:
  phase: 00-discovery
  inputs:
  - intake-brief
  - problem-frame
  - design-direction
  - market-research-report
  outputs:
  - research-plan
  - user-persona-set
  - user-journey-map
  prerequisites:
  - pc-intake
  quality_gate: Delivered plans are executable; delivered findings require real evidence and method/sample limits, with unresolved questions explicit
  roles:
  - product-manager
  methodologies:
  - all
  effort: large
---

# User Research

> Know your users before you design for them. Assumptions are the enemy of good products.

## Context

User research transforms market understanding into actionable user profiles.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Define Research Questions

Start from the approved question and available context:

- use `problem-frame` for user hypotheses, non-goals, and open questions; preserve the chosen direction from `design-direction` or the approved handoff
- if market analysis exists, use it to narrow which segments are worth validating first
- otherwise use intake, observed workflows, or operator/user evidence when the audience, goal, and uncertainty are clear; clarify only what prevents choosing a useful study

Then define the research questions. Focus on behavior, not opinions:
- What workflows do users currently follow?
- Where do they experience friction?
- What tools do they currently use (and why)?
- What would make them switch to a new solution?
- Which upstream assumptions most need validation before requirements should start?

### Step 2: Choose Research Methods

- **Interviews**: Understand behavior and why it occurs.
- **Surveys**: Estimate patterns when recruitment and sample quality support that inference.
- **Observation**: Watch users in their natural workflow. Reveals behavior they can't articulate.
- **Analytics review**: If existing product exists, mine usage data for behavioral patterns.

Choose recruitment, sample size, and stopping criteria from the decision's risk and evidence gaps; counts alone do not establish validity. If evidence is missing, produce a scoped research plan:

- target segments to recruit
- key hypotheses or open questions to test
- method mix and sample size
- the evidence threshold required before moving to requirements

### Step 3: Synthesize into Personas

Group observed differences that change a product decision; use one segment when the evidence supports one. For each persona record:
- Role and evidence sources
- Goals (what they're trying to achieve)
- Pain points (what frustrates them today)
- Behaviors (how they work, tools they use)
- Verbatim sourced quotes when useful; label paraphrases and never invent participant testimony

### Step 4: Map User Journeys

For each primary persona, map the journey through the problem space:
- Stages of the actual task, including failure, recovery, and repeat use where relevant
- Actions at each stage
- Emotions and pain points
- Opportunities for your product to intervene

### Step 5: Validate Personas

Trace each segment and journey claim to observations. Identify contradictory cases, recruitment bias, and what the sample cannot establish.

If research has not run, deliver the plan with findings explicitly pending. Do not pass an evidence-dependent downstream gate using a plan.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] When a study is planned, its plan identifies the decision, audience, methods, recruitment, and evidence threshold
- [ ] Delivered personas and journeys trace to real evidence; unexecuted work is marked planned
- [ ] Findings distinguish observed frequency/severity from assumptions and sample limits
- [ ] Unanswered questions identify the next investigation and any blocked downstream decision
