# CI/CD Isolated Benchmark Review

## Scope

This note reviews the first runner-backed benchmark packet strong enough to
promote `ci-cd` beyond routed review.

Reviewed runs:

- `eval/06-delivery/ci-cd/run-2026-04-04-copilot-brownfield-rerun`
- `eval/06-delivery/ci-cd/run-2026-04-04-copilot-minimal-clean`

Runner: `copilot`

The evidence now covers two scenarios:

1. `access-review-modernization-pipeline`
2. `low-risk-service-pipeline`

## Cross-Scenario Judgment

### Brownfield Access Review Pipeline

The baseline branch was not weak. It already proposed a comprehensive pipeline,
canary rollout, rollback triggers, and explicit release gates.

The with-skill branch was still better on the contract that matters here:

- it tied contract tests directly to `UNSUPPORTED_RELEASE1_FLOW`
- it kept coexistence validation and rollback verification as hard gates
- it treated manual approval and staged rollout as explicit release-boundary
  controls instead of generic safety theater
- it stayed closer to the reviewed slice instead of inventing broader platform
  assumptions

### Low-Risk Service Pipeline

The baseline branch was practical and appropriately lightweight.

The with-skill branch was still stronger because it:

- kept the fast PR feedback gate explicit
- preserved staging verification before production
- stayed operationally concrete without adding unnecessary ceremony
- made the boundary between “enough pipeline” and “rollout theater” clearer

## Judgment

This is no longer review-only evidence:

- the manual pipeline review proves the lifecycle boundary for brownfield
  delivery
- the clean brownfield rerun shows the skill can encode release-boundary gates
  under higher risk
- the clean low-risk scenario shows the skill can also avoid overengineering on
  simpler delivery slices

Current limits remain:

- both scenarios are still synthetic QA packets rather than real delivery
  pipelines
- the observed lift is moderate rather than dramatic because the baseline was
  already competent
- there is no downstream deployment rehearsal yet consuming these pipeline
  artifacts

Those gaps should be addressed next, but they no longer justify leaving the
skill at `review`.

## Status Recommendation

- Recommended status: `tested`
