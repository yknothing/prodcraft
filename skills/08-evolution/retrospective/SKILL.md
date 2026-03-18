---
name: retrospective
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

Retrospective is the skill that completes the lifecycle loop. It feeds insights from operations and evolution back into discovery, making the next cycle better than the last. Without it, teams repeat the same mistakes and miss improvement opportunities.

In a lifecycle-aware system, a retrospective is not a generic feelings exercise. It must turn concrete evidence from postmortems, reviews, and delivery outcomes into a small number of changes the team will actually route back through intake and planning.

## Process

### Step 1: Set the Stage (5 min)

Establish psychological safety. The retrospective must be a blame-free zone:
- "We're here to improve the system, not to assign blame"
- Check in: how is everyone feeling about the last sprint/phase?

### Step 2: Gather Evidence (15 min)

What happened? Use facts and metrics before opinions:
- incident timeline and postmortem findings
- review findings that should have stopped the issue earlier
- deployment or rollback decisions
- bugs found in production
- team coordination friction that was visible during execution

### Step 3: Generate Insights (15 min)

Why did it happen? Techniques:
- **5 Whys**: For each problem, ask "why" five times to reach root cause
- **Fishbone diagram**: Categorize causes (people, process, tools, environment)
- **Start/Stop/Continue**: What should we begin, stop, or keep doing?
- **4Ls**: Liked, Learned, Lacked, Longed-for

Stay at the system/process level. If a problem belongs in a concrete downstream skill (`testing-strategy`, `ci-cd`, `incident-response`, `tech-debt-management`), call that out explicitly.

### Step 4: Decide Actions (10 min)

Select 3-5 improvements (not 20). Each must be:
- **Specific**: "Add integration tests for payment flow" not "improve testing"
- **Assigned**: One person owns it
- **Timeboxed**: Deadline within the next sprint/phase
- **Measurable**: How will we know it's done?
- **Routable**: It is clear whether the action should go through intake, planning, delivery, or evolution next

Prefer actions that reduce recurrence risk and improve future handoffs instead of vague morale language.

### Step 5: Close (5 min)

- Recap the action items
- Appreciations: call out what went well and who helped
- Confirm which follow-up items become intake-ready work
- Rate the retrospective itself (meta-improvement)

## Quality Gate

- [ ] No more than 5 improvement actions chosen
- [ ] Each action has an owner and a deadline
- [ ] Each action has a measurable success signal
- [ ] Each action identifies its next lifecycle destination
- [ ] Actions from previous retrospective reviewed (were they completed?)
- [ ] Insights documented for future reference

## Anti-Patterns

1. **Retro without follow-through** -- The #1 killer. If actions from last retro weren't done, why would new ones be?
2. **Blame fest** -- Degenerates into finger-pointing. Facilitator must redirect to systems thinking.
3. **Too many actions** -- 3 completed improvements > 10 abandoned ones. Be selective.
4. **Skipping retro when things went well** -- Good sprints have learnings too. What made it good? How do we replicate it?
5. **Same format every time** -- Rotate formats to prevent staleness (sailboat, timeline, mad/sad/glad).
6. **Action items with no route back into the system** -- If follow-ups never become planned work, the retro is theater.

## Related Skills

- [incident-response](../../07-operations/incident-response/SKILL.md) -- postmortems feed into retrospectives
- [tech-debt-management](../tech-debt-management/SKILL.md) -- retro surfaces debt patterns
- [sprint-planning](../../03-planning/sprint-planning/SKILL.md) -- retro improvements feed into next sprint
- [intake](../../00-discovery/intake/SKILL.md) -- retro insights trigger new work via intake
