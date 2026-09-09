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
---

# Problem Framing

> Clarify the problem and the decision that prevents the approved route from continuing.

## Context

Use after [pc-intake](../pc-intake/SKILL.md) when routing is clear but scope or direction is not.
See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Consume the Current Route

Read the approved outcome, constraints, risks, current artifacts, and next phase. Identify exactly which missing decision framing must resolve. Preserve settled choices; do not restart intake or repeat answered questions.

### Step 2: Resolve Decision-Changing Unknowns

Ask only about success criteria, scope, non-goals, or dependencies that change the decision. Zero questions is valid when evidence suffices. Usually 1–3 questions suffice; exceed that only for material uncertainty, up to 5. If research is needed, hand off that question instead of extending an interview without evidence.

### Step 3: Record the Problem Frame

State the problem, affected users/operators, constraints, non-goals, assumptions, and open questions. Carry `source_language`, `artifact_record_language`, and `user_presentation_locale` from intake. Canonical records remain English; use plain language and the user's locale for presentation.

Preserve `quality_target_context`: an internal skill or local harness does not become a public service merely because an interface resembles HTTP. Note ownership, collaboration quality, or system shape only when they affect this decision.

### Step 4: Compare Viable Directions

In `options-brief`, compare materially different choices by fit, benefit, cost/risk, and rejection condition. If approved constraints leave one direction, explain exclusions and the remaining scope decision. Do not manufacture alternatives or reopen settled choices to reach a count.

Keep this at product/solution direction; system structure belongs to architecture.

### Step 5: Recommend and Hand Off

Record `design-direction` with the selected option, rationale, preserved assumptions, and next concrete skill: `pc-market-analysis`, `pc-user-research`, `pc-feasibility-study`, or `pc-requirements-engineering` as appropriate.

Reuse explicit approval only when the conversation already approves this framing and direction. Obtain missing approval before handoff; a new scope or direction requires its own decision. Pass the accepted frame, options, and direction without asking the next skill to rediscover them.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] `problem-frame` makes the problem, constraints, non-goals, assumptions, and questions explicit
- [ ] `options-brief` compares real alternatives or explains why only one remains
- [ ] `design-direction` records rationale, unresolved decisions, and the next skill
- [ ] Questions stayed within the stated budget and changed a material decision
- [ ] User approval covers the framing and direction before handoff
