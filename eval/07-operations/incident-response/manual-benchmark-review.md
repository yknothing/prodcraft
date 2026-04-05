# Incident Response Manual Benchmark Review

## Scope

This note summarizes the current manual branch-pair benchmark evidence for
`incident-response`.

It is not a true isolated runner-backed benchmark. It does preserve the minimum
comparison structure needed for a narrow `tested` decision:

- baseline and with-skill branches
- fixed incident fixtures
- raw prompt/output artifacts checked into the repo

Reviewed branch pairs:

1. `access-review-modernization-incident`
2. `team-invite-email-backlog-incident`

## Cross-Branch Judgment

### Scenario 1: Brownfield release regression

The baseline incident plan is serviceable but generic. It names severity,
deploy freeze, and possible rollback, but it delays the key containment
decision and does not convert the reviewed release boundary into a fail-closed
operational plan.

The with-skill branch is materially stronger:

- containment comes before broad diagnosis
- brownfield coexistence, rollback, and legacy fallback remain explicit
- evidence capture is required before speculative debugging
- roles, update cadence, and post-incident handoff are concrete

### Scenario 2: Non-brownfield service incident

The second scenario reduces the risk that the skill is overfit to brownfield
modernization. The same lift remains visible:

- baseline stays generic
- with-skill gives clearer severity logic, degradation handling, cadence, and
  follow-up routing

## Status Recommendation

- Recommended status: `tested`

Keep the tested posture narrow until:

1. a true isolated runner-backed benchmark replaces this manual branch-pair
   evidence
2. the resulting incident artifact is exercised again through runbook reuse and
   observability-aligned follow-up
