---
name: pc-user-research
description: Use when discovery needs evidence about target users, behaviors, and pain points, especially after intake or problem-framing surfaces open questions that must be validated before requirements are written
metadata:
  phase: 00-discovery
  inputs:
  - intake-brief
  - problem-frame
  - market-research-report
  outputs:
  - research-plan
  - user-persona-set
  - user-journey-map
  prerequisites:
  - pc-intake
  quality_gate: Research findings are backed by real user evidence, at least 3 personas or an explicit rationale for fewer segments are documented, and unresolved discovery questions are either answered or clearly carried forward
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

Start from the upstream artifact before inventing new questions:

- if a `problem-frame` exists, extract the target user hypothesis, non-goals, chosen direction, and open questions
- if market analysis exists, use it to narrow which segments are worth validating first
- if neither exists, stop and request clearer discovery framing rather than guessing

Then define the research questions. Focus on behavior, not opinions:
- What workflows do users currently follow?
- Where do they experience friction?
- What tools do they currently use (and why)?
- What would make them switch to a new solution?
- Which upstream assumptions most need validation before requirements should start?

### Step 2: Choose Research Methods

- **Interviews** (5-8 users): Deep qualitative understanding. Best for early discovery.
- **Surveys** (50+ responses): Quantitative validation. Best after interviews surface patterns.
- **Observation**: Watch users in their natural workflow. Reveals behavior they can't articulate.
- **Analytics review**: If existing product exists, mine usage data for behavioral patterns.

If no real-user evidence has been collected yet, produce a scoped research plan first:

- target segments to recruit
- key hypotheses or open questions to test
- method mix and sample size
- the evidence threshold required before moving to requirements

### Step 3: Synthesize into Personas

Create 3-5 personas, each representing a distinct user segment:
- Name and role (make them memorable)
- Goals (what they're trying to achieve)
- Pain points (what frustrates them today)
- Behaviors (how they work, tools they use)
- Quote (a real or representative statement capturing their perspective)

### Step 4: Map User Journeys

For each primary persona, map the journey through the problem space:
- Stages (awareness, consideration, adoption, retention)
- Actions at each stage
- Emotions and pain points
- Opportunities for your product to intervene

### Step 5: Validate Personas

Test personas against real data. Can you match each persona to at least 2-3 real users? If not, refine.

If the research has not yet been executed, do **not** fake this step. Record that the quality gate is still open and hand off the research plan for execution.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] At least 3 distinct personas documented, or an explicit justification exists for fewer segments
- [ ] Each persona backed by real user data (not assumptions)
- [ ] User journey mapped for primary persona
- [ ] Pain points prioritized by frequency and severity
- [ ] Upstream discovery questions are either answered or explicitly carried forward
