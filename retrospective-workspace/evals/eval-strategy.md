# Retrospective Evaluation Strategy

## Objective

Evaluate whether `retrospective` converts incident and review evidence into a small set of owned, routed improvement actions instead of a generic discussion summary.

At review stage, use manual side-by-side evaluation rather than trigger scoring. This skill is expected to be used through workflow routing after incidents, releases, or sprint boundaries.

## Review Scope

Review the skill on:

1. `access-review-modernization-retrospective`
   - brownfield modernization release
   - post-incident learning after a failed release boundary
   - evidence already exists from incident response and prior review stages

## Assertions

1. `uses evidence rather than vague sentiment`
   - The retro is grounded in postmortem and review facts.
2. `produces a small actionable set`
   - The output selects a few improvements instead of a laundry list.
3. `routes actions back into the lifecycle`
   - Each action has a clear next destination or owning skill.
4. `preserves system-level learning`
   - The retro avoids blame and identifies process or boundary failures.
5. `supports recurrence reduction`
   - The chosen actions are likely to reduce repeat failure, not just document it.

## Inputs

- `fixtures/access-review-modernization-postmortem.md`
- `fixtures/access-review-modernization-review-summary.md`

## Method

1. Produce a baseline retrospective output without the skill.
2. Produce a second output while explicitly using `retrospective`.
3. Compare against the assertion list.
4. Record findings in `retro-review.md` and summarize status in `findings.md`.

## Exit Criteria for Review Stage

- At least one incident-driven retrospective reviewed
- Clear manual evidence that the skill improves specificity, routing, and follow-through quality
- No claim of tested or production status until broader benchmark coverage exists
