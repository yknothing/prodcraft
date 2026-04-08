# Monitoring and Observability Manual Benchmark Review

## Scope

This note summarizes the current manual branch-pair benchmark evidence for
`monitoring-observability`.

It is not a true isolated runner-backed benchmark. It does preserve the minimum
comparison structure needed for a narrow `tested` decision:

- a baseline branch
- a with-skill branch
- fixed release-context fixtures
- raw output artifacts checked into the repo

Reviewed manual branch pairs:

1. `access-review-modernization-observability`
2. `team-invite-observability`

## Cross-Branch Judgment

### Scenario 1: Brownfield modernization release

The baseline monitoring plan is serviceable but generic. It names common
metrics, alerts, and dashboards, but it does not convert the reviewed release
boundary into an operational signal model responders can act on safely.

The with-skill plan is materially stronger:

- supported and unsupported flows stay separated
- rollback and fallback state remain visible
- queue age and retry amplification are treated as first-class release risk
- alerts are tied to decisions responders actually need to make during
  verification or containment

### Scenario 2: Non-brownfield service release

The second branch pair reduces the risk that the skill is overfit to brownfield
coexistence. The same lift remains visible:

- baseline stays generic
- with-skill maps signals to invite creation, invite acceptance, and email
  dispatch boundaries
- queue age, provider failure, and post-deploy validation remain tied to user
  impact instead of generic uptime graphs

## Supporting Evidence

`monitoring-observability` already has stronger-than-minimal downstream evidence
for this maturity level:

- routed review in `observability-review.md`
- manual review across both a brownfield and non-brownfield scenario
- a seeded isolated benchmark plan and fixture set for future runner-backed
  replacement

This should still be treated as a narrow `tested` posture rather than a final
operations gold standard.

## Status Recommendation

- Recommended status: `tested`

Keep the tested posture narrow until:

1. a true isolated runner-backed benchmark replaces this manual branch-pair
   evidence
2. at least one observability plan is exercised again against a concrete
   post-deploy or incident drill
3. incident-response and runbook evidence continue reusing the same signal model
