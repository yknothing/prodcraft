# Retrospective Manual Benchmark Review

## Scope

This note summarizes the current manual branch-pair benchmark evidence for
`retrospective`.

Reviewed branch pair:

1. `access-review-modernization-retrospective`

The evidence is narrow, but it uses a fixed baseline branch, a with-skill
branch, and checked-in raw outputs against the same postmortem and review
fixtures.

## Cross-Branch Judgment

The baseline retrospective is generic:

- it lists broad lessons like "improve testing" and "improve communication"
- it does not route actions back into the lifecycle
- it loses the specific release-boundary learning

The with-skill branch is materially stronger:

- actions stay grounded in evidence rather than morale commentary
- the action set stays small and real
- owners, targets, and success signals are explicit
- each action has a next lifecycle destination

This is enough to justify a narrow tested posture, especially now that
`tech-debt-management` is also being advanced so these actions have a stronger
evolution-side destination.

## Status Recommendation

- Recommended status: `tested`

Keep the tested posture narrow until:

1. a second non-incident scenario confirms the same behavior
2. a true isolated runner-backed benchmark replaces this manual branch-pair
   evidence
