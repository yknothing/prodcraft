# Tech Debt Management Evaluation Strategy

## Objective

Evaluate whether `tech-debt-management` turns retrospective and postmortem evidence into a prioritized debt registry with clear remediation routes.

At review stage, use manual side-by-side evaluation rather than trigger scoring. This skill is expected to be used through routed evolution workflows after incidents, reviews, or retrospectives.

## Review Scope

Review the skill on:

1. `access-review-modernization-tech-debt`
   - brownfield modernization release
   - incident and retrospective evidence already exist
   - the team needs to separate true structural debt from one-off bugs and roadmap work

## Assertions

1. `uses evidence-backed debt candidates`
   - The registry is grounded in review, incident, or retro evidence.
2. `prioritizes by interest and recurrence`
   - Top items reflect compounding cost or recurrence risk, not personal preference.
3. `separates debt from defects and feature work`
   - The output does not dump everything into one backlog.
4. `routes remediation cleanly`
   - Each top item has owner, timing, and next lifecycle destination.
5. `supports reduction of repeat failure`
   - The chosen debt items help prevent the same delivery/operations breakdowns.

## Inputs

- `fixtures/access-review-modernization-retro-summary.md`
- `fixtures/access-review-modernization-postmortem-summary.md`

## Method

1. Produce a baseline debt plan without the skill.
2. Produce a second output while explicitly using `tech-debt-management`.
3. Compare against the assertion list.
4. Record findings in `debt-review.md` and summarize status in `findings.md`.

## Exit Criteria for Review Stage

- At least one incident-informed debt scenario reviewed
- Clear manual evidence that the skill improves prioritization and routing quality
- No claim of tested or production status until broader benchmark coverage exists
