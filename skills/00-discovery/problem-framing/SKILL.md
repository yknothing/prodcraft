---
name: problem-framing
description: Use when intake has identified the likely lifecycle path but the problem statement, solution direction, or key trade-offs are still too fuzzy for requirements, research, or architecture work to start cleanly
metadata:
  phase: 00-discovery
  inputs:
  - intake-brief
  outputs:
  - problem-frame
  - options-brief
  - design-direction
  prerequisites:
  - intake
  quality_gate: Approved problem frame and recommended design direction recorded with trade-offs, assumptions, open questions, and next lifecycle destination
  roles:
  - product-manager
  - tech-lead
  - architect
  methodologies:
  - all
  effort: medium
---

# Problem Framing

> Turn an approved intake route into a crisp problem statement and a small set of decision-ready options.

## Context

Problem framing sits immediately after [intake](../intake/SKILL.md) when routing is clear but the work is still underspecified. It absorbs the strongest part of brainstorming-style collaboration without collapsing the entry gate into a full design workshop.

Use it to answer:
- What problem are we actually solving?
- What boundaries must stay fixed?
- What are the viable directions?
- Which direction should the team carry into specification, research, or architecture?

Do not use it when the route is already well-scoped enough for downstream work, or when the user is already in implementation, debugging, or review.

## Inputs

- **intake-brief** -- Must identify the work type, entry phase, recommended workflow, key risks, and the next likely skill.
  Preserve the intake language boundary fields instead of silently guessing them away: `source_language`, `artifact_record_language`, and `user_presentation_locale`.

## Process

### Step 1: Read the Intake Route

Review the intake brief before asking anything new.

Extract:
- the requested outcome
- the routing rationale
- the risks and unknowns already identified
- the downstream phase that this framing is meant to unlock

### Step 2: Ask Only Decision-Changing Questions

Ask questions one at a time.

Default budget:
- 1-3 questions in normal cases
- up to 5 only if each additional answer materially changes scope, risk, or option selection

Focus on:
- success criteria
- hard constraints
- non-goals
- irreversible decisions or dependencies

Do not restate intake questions unless the answer is still ambiguous or conflicting.

### Step 3: Write the Problem Frame

Produce a concise `problem-frame` covering:
- problem statement
- target users or operators
- constraints
- non-goals
- assumptions
- open questions

The canonical `problem-frame` record stays in English under current repo policy, but user-facing framing output may still be presented in the user's locale. Carry `source_language`, `artifact_record_language`, and `user_presentation_locale` forward explicitly.

The problem frame must be sharp enough that downstream skills do not have to rediscover the core problem.
Use plain language, default to Chinese for user-facing output unless the user asks for another language, and explicitly note system shape or collaboration quality when they materially affect the framing.

### Step 4: Compare 2-3 Directions

Produce an `options-brief` with 2-3 plausible directions.

For each direction, note:
- why it is viable
- what it optimizes for
- what it risks or defers
- when it should be rejected

Keep these at the level of product or solution direction, not low-level implementation detail.

### Step 5: Recommend One Direction

Record a `design-direction` that includes:
- the recommended option
- why it wins over the alternatives
- what must remain open for downstream skills
- the next lifecycle destination (`market-analysis`, `user-research`, `feasibility-study`, or `requirements-engineering`)

When the route depends on team boundaries, ownership clarity, workflow friction, or architectural sprawl, say so directly as a collaboration quality or system shape concern instead of hiding it inside generic risk wording.

### Step 6: Get Approval and Handoff

Ask the user to confirm the framing and chosen direction.

After approval, hand off the framing artifacts to the next skill named in the `design-direction`.

## Outputs

- **problem-frame** -- The clarified problem, constraints, and non-goals
- **options-brief** -- Small set of viable directions with trade-offs
- **design-direction** -- Approved recommendation plus next lifecycle destination

## Quality Gate

- [ ] `problem-frame` states the problem, constraints, non-goals, assumptions, and open questions
- [ ] `options-brief` compares 2-3 viable directions with explicit trade-offs
- [ ] `design-direction` recommends one direction and names the next skill to invoke
- [ ] The total question load stayed within the default budget or justified why it exceeded it
- [ ] The user approved the framing output before handoff

## Anti-Patterns

1. **Repeating intake** -- Intake already handled classification and routing. Framing should deepen the decision, not restart the entry gate.
2. **Premature architecture** -- Stay at the level of direction and trade-off. Leave system structure to [system-design](../../02-architecture/system-design/SKILL.md).
3. **Infinite discovery interviews** -- Use the minimum questions needed to make a decision. If more information is required, route to research skills.
4. **Single-option framing** -- If only one path is shown, there is no real trade-off analysis.

## Related Skills

- [intake](../intake/SKILL.md) -- provides the approved route and initial constraints
- [market-analysis](../market-analysis/SKILL.md) -- use when market uncertainty remains high
- [user-research](../user-research/SKILL.md) -- use when user behavior or pain points are still unclear
- [feasibility-study](../feasibility-study/SKILL.md) -- use when go/no-go needs deeper validation
- [requirements-engineering](../../01-specification/requirements-engineering/SKILL.md) -- consumes the approved design direction
