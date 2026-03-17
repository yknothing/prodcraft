# Monitoring and Observability Evaluation Strategy

## Objective

Evaluate whether `monitoring-observability` turns reviewed architecture and delivery context into actionable signals that support release verification and incident triage.

At review stage, use manual side-by-side evaluation rather than trigger scoring. This skill is expected to be a routed operations skill, not a discoverability-first skill.

A "non-brownfield comparison scenario" means a service or release that does not involve legacy coexistence, migration seams, or compatibility burden. It is used to check that the skill generalizes beyond modernization-specific constraints.

## Review Scope

Review the skill on:

1. `access-review-modernization-observability`
   - brownfield modernization release
   - unsupported reassignment variants should fail closed
   - async sync behavior and rollback health must be visible
2. `team-invite-observability`
   - non-brownfield service slice
   - no legacy coexistence or migration seam
   - invite delivery and acceptance health must still map to user impact clearly

## Assertions

1. `maps signals to real boundaries`
2. `avoids generic noisy monitoring`
3. `preserves brownfield safety visibility`
4. `supports incident handoff`
5. `supports release verification`

## Inputs

- `fixtures/access-review-modernization-architecture-summary.md`
- `fixtures/access-review-modernization-pipeline-summary.md`
- `fixtures/access-review-modernization-risk-summary.md`
- `fixtures/team-invite-architecture-summary.md`
- `fixtures/team-invite-pipeline-summary.md`
- `fixtures/team-invite-risk-summary.md`

## Method

1. Produce a baseline monitoring plan without the skill.
2. Produce a second output while explicitly using `monitoring-observability`.
3. Compare against the assertion list.
4. Record findings in `observability-review.md` and summarize status in `findings.md`.

## Exit Criteria for Review Stage

- At least one routed brownfield scenario reviewed
- At least one routed non-brownfield comparison scenario reviewed
- Clear manual evidence that the skill improves signal/actionability quality
- No claim of tested or production status until broader benchmark coverage exists
