---
name: user-research
description: Use when identifying target users, understanding their needs, pain points, and behaviors
metadata:
  phase: 00-discovery
  inputs:
  - market-research-report
  outputs:
  - user-persona-set
  - user-journey-map
  prerequisites: []
  quality_gate: At least 3 user personas validated with real user data
  roles:
  - product-manager
  methodologies:
  - all
  effort: large
---

# User Research

> Know your users before you design for them. Assumptions are the enemy of good products.

## Context

User research transforms market understanding into actionable user profiles. It can run in parallel with market-analysis but ideally uses market insights to focus the research scope.

## Process

### Step 1: Define Research Questions

What do you need to learn? Focus on behavior, not opinions:
- What workflows do users currently follow?
- Where do they experience friction?
- What tools do they currently use (and why)?
- What would make them switch to a new solution?

### Step 2: Choose Research Methods

- **Interviews** (5-8 users): Deep qualitative understanding. Best for early discovery.
- **Surveys** (50+ responses): Quantitative validation. Best after interviews surface patterns.
- **Observation**: Watch users in their natural workflow. Reveals behavior they can't articulate.
- **Analytics review**: If existing product exists, mine usage data for behavioral patterns.

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

## Quality Gate

- [ ] At least 3 distinct personas documented
- [ ] Each persona backed by real user data (not assumptions)
- [ ] User journey mapped for primary persona
- [ ] Pain points prioritized by frequency and severity

## Anti-Patterns

1. **Designing for yourself** -- You are not your user. Even if you're in the target market, your expertise makes you atypical.
2. **Too many personas** -- More than 5 personas dilutes focus. Consolidate similar users.
3. **Demographic-only personas** -- "25-35 year old male" is not a useful persona. Focus on goals and behaviors.
4. **One-time research** -- User understanding should be continuously refined, not a one-time exercise.

## Related Skills

- [market-analysis](../market-analysis/SKILL.md) -- provides market context for targeting research
- [requirements-engineering](../../01-specification/requirements-engineering/SKILL.md) -- consumes personas and journey maps
- [acceptance-criteria](../../01-specification/acceptance-criteria/SKILL.md) -- uses persona scenarios
