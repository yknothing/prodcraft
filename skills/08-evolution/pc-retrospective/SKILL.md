---
name: pc-retrospective
description: Use when a sprint, release, or incident has ended and the team needs to turn evidence about what worked, what failed, and what should change into a small set of owned follow-up actions.
metadata:
  phase: 08-evolution
  inputs:
  - incident-timeline
  - postmortem-report
  - review-report
  outputs:
  - retrospective-report
  - improvement-actions
  prerequisites: []
  quality_gate: Retrospective identifies a small set of system-level improvements, each with owner, deadline, and intake-ready follow-up
  roles:
  - tech-lead
  - product-manager
  methodologies:
  - all
  effort: small
---

# Retrospective

> The team that doesn't reflect doesn't improve. Retrospectives close the feedback loop.

## Context

Retrospective is the skill that completes the lifecycle loop.

See [context notes](references/context.md).

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Set the Stage

Establish psychological safety. The retrospective must be a blame-free zone:
- "We're here to improve the system, not to assign blame"
- Check in: how is everyone feeling about the last sprint/phase?

### Step 2: Gather Evidence

What happened? Use facts and metrics before opinions:
- delivered outcomes, user feedback, and what helped work succeed
- incident timeline and postmortem findings
- review findings that should have stopped the issue earlier
- deployment or rollback decisions
- bugs found in production
- team coordination friction that was visible during execution

### Step 3: Generate Insights

Why did it happen? Techniques:
- **5 Whys**: Trace causes using evidence; stop at an actionable explanation, not a fixed question count
- **Fishbone diagram**: Categorize causes (people, process, tools, environment)
- **Start/Stop/Continue**: What should we begin, stop, or keep doing?
- **4Ls**: Liked, Learned, Lacked, Longed-for

Stay at the system/process level. If a problem belongs in a concrete downstream skill (`pc-testing-strategy`, `pc-ci-cd`, `pc-incident-response`, `pc-tech-debt-management`), call that out explicitly.

### Step 4: Decide Actions

Choose only evidence-backed changes the team can act on. One action is sufficient; zero is valid when no useful new action is supported and the reason is recorded. Each selected action must be:
- **Specific**: "Add integration tests for payment flow" not "improve testing"
- **Assigned**: One person owns it
- **Timeboxed**: An agreed target or explicit pending scheduling decision
- **Measurable**: How will we know it's done?
- **Routable**: It is clear whether the action should go through intake, planning, delivery, or evolution next

Prefer actions that reduce recurrence risk and improve future handoffs instead of vague morale language.

### Step 5: Close

- Recap the action items
- Appreciations: call out what went well and who helped
- Confirm which follow-up items become intake-ready work
- Change the review format only when it would address observed friction

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] The selected actions are justified and manageable; no-action decisions explain why
- [ ] Each action has an owner and agreed timing or an explicit scheduling decision
- [ ] Each action has a measurable success signal
- [ ] Each action identifies its next lifecycle destination
- [ ] Previous actions reviewed when available; the first review does not invent history
- [ ] Insights documented for future reference

## Anti-Patterns

1. **Retro without follow-through** -- The #1 killer. If actions from last retro weren't done, why would new ones be?
2. **Blame fest** -- Degenerates into finger-pointing. Facilitator must redirect to systems thinking.
3. **Too many actions** -- 3 completed improvements > 10 abandoned ones. Be selective.
4. **Skipping retro when things went well** -- Good sprints have learnings too. What made it good? How do we replicate it?
5. **Ceremony without a decision** -- Use the lightest format that explains the evidence and next action; do not rotate formats just for novelty.
6. **Action items with no route back into the system** -- If follow-ups never become planned work, the retro is theater.
