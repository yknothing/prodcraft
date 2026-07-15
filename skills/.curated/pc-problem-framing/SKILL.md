---
name: pc-problem-framing
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
  - pc-intake
  quality_gate: Approved problem frame and recommended design direction recorded with trade-offs, assumptions, open questions, and next lifecycle destination
  roles:
  - product-manager
  - tech-lead
  - architect
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/00-discovery/pc-problem-framing/SKILL.md
  public_stability: beta
  public_readiness: core
---

# Problem Framing

> Turn an approved intake route into a crisp problem statement and a small set of decision-ready options.

## Context

Problem framing sits immediately after [pc-intake](../pc-intake/SKILL.md) when routing is clear but the work is still underspecified.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

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

Carry `quality_target_context` forward explicitly when it affects scope, risk, or downstream QA. If the target is an agent-internal skill, host runtime tool, or local harness, do not let problem framing drift into a public service design unless the user chose that product target.

The problem frame must be sharp enough that downstream skills do not have to rediscover the core problem.
Use plain language, present user-facing output in the user's requested language or the `user_presentation_locale`, and explicitly note system shape or collaboration quality when they materially affect the framing.

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
- the next lifecycle destination (`pc-market-analysis`, `pc-user-research`, `pc-feasibility-study`, or `pc-requirements-engineering`)

When the route depends on team boundaries, ownership clarity, workflow friction, or architectural sprawl, say so directly as a collaboration quality or system shape concern instead of hiding it inside generic risk wording.

### Step 6: Get Approval and Handoff

Ask the user to confirm the framing and chosen direction.

After approval, hand off the framing artifacts to the next skill named in the `design-direction`.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] `problem-frame` states the problem, constraints, non-goals, assumptions, and open questions
- [ ] `options-brief` compares 2-3 viable directions with explicit trade-offs
- [ ] `design-direction` recommends one direction and names the next skill to invoke
- [ ] The total question load stayed within the default budget or justified why it exceeded it
- [ ] The user approved the framing output before handoff

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/00-discovery/pc-problem-framing/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `core`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
