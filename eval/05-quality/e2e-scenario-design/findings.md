# E2E Scenario Design QA Findings

## Status

- Current status: `tested`
- Evidence type:
  - explicit benchmark packet
  - routed handoff review from `testing-strategy`
  - consumer review for CI / implementation reuse
- Scope covered:
  - shallow SPA test diagnosis
  - mobile scenario design
  - collaboration scenario design
  - downstream handoff into repository-local quality workflow

## What Changed

1. The skill is now registered in `manifest.yml` and its inputs/outputs are linked into `artifact_flow`.
2. The `SKILL.md` body was reshaped to match the repository schema instead of living as an unstructured long-form note.
3. Existing benchmark evidence was kept, but the stored repo-absolute skill path was scrubbed so eval artifacts remain portable.

## What We Learned

1. The strongest observed lift is structural: the skill is good at diagnosing shallow E2E suites and replacing them with persona-driven, stateful scenarios.
2. The skill is weaker on assertion guidance than on scenario architecture, so the body now makes business-state assertions explicit instead of outsourcing that entirely to references.
3. The benchmark packet is not uniformly differentiating, but it is strong enough for a narrow `tested` judgment once routed handoff and consumer evidence are added.

## Current Interpretation

At this stage, `e2e-scenario-design` appears to be:

- a routed quality skill downstream of `testing-strategy`
- useful when the suite needs deeper scenario discipline rather than more generic pyramid advice
- strong enough for a narrow `tested` posture because the repo now shows both benchmark lift and downstream artifact usability

## Current Limits

- one benchmark scenario is non-discriminating
- the benchmark packet is stronger on scenario architecture than on detailed assertion mechanics
- the stale `benchmark.md` summary should not be used as the source of truth

## Next QA Step

Add a fresh runner-backed benchmark summary and at least one follow-on implementation artifact that consumes the scenario design directly.
