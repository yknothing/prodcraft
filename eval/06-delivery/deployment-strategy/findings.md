# Deployment Strategy QA Findings

## Status

- Current status: `tested`
- Evidence type: routed handoff review plus isolated benchmark
- Scope covered:
  - routed rollout-handoff review
  - one clean brownfield staged-rollout benchmark

## What Changed

1. The skill is now under manifest-backed QA instead of remaining a critical-but-untracked draft.
2. Review-stage evidence was defined around the actual downstream handoff from `ci-cd` and release planning into rollout and rollback decisions.
3. The benchmark lane is now explicit, so future isolated Gemini runs can compare risk-aware rollout planning against baseline delivery advice.
4. A clean brownfield rerun now exists for the highest-value rollout scenario.

## What We Learned

1. `deployment-strategy` is valuable when delivery risk is no longer binary. It decides rollout shape, stop conditions, and rollback path, not just "how to deploy."
2. The strongest early signal is routed handoff quality from release context, not discoverability.
3. The main regression risk is treating pipeline automation as if it already decided rollout safety.
4. The benchmark scaffolding is now complete enough to run the minimal tested lane.
5. The first `copilot` benchmark attempt failed on most branches, but the brownfield-only rerun now completes cleanly on both branches.
6. The current tested posture should remain narrow until the low-risk rollout scenario also completes cleanly.

## Current Interpretation

At this stage, `deployment-strategy` appears to be:

- a core delivery skill on the lifecycle spine
- stronger as a routed workflow skill than as a discoverability-first skill
- strong enough for a narrow `tested` posture because the brownfield staged-rollout benchmark now completes cleanly and shows a clearer release-boundary-aware plan than baseline

## Next QA Step

Rerun the low-risk scenario cleanly so the tested packet covers both simple and brownfield rollout shapes.
