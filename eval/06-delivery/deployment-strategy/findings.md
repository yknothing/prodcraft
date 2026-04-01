# Deployment Strategy QA Findings

## Summary

`deployment-strategy` has moved to `review` status.

## What Changed

1. The skill is now under manifest-backed QA instead of remaining a critical-but-untracked draft.
2. Review-stage evidence was defined around the actual downstream handoff from `ci-cd` and release planning into rollout and rollback decisions.
3. The benchmark lane is now explicit, so future isolated Gemini runs can compare risk-aware rollout planning against baseline delivery advice.

## What We Learned

1. `deployment-strategy` is valuable when delivery risk is no longer binary. It decides rollout shape, stop conditions, and rollback path, not just "how to deploy."
2. The strongest early signal is routed handoff quality from release context, not discoverability.
3. The main regression risk is treating pipeline automation as if it already decided rollout safety.

## Current Interpretation

At this stage, `deployment-strategy` appears to be:

- a core delivery skill on the lifecycle spine
- stronger as a routed workflow skill than as a discoverability-first skill
- still in need of isolated benchmark evidence before it can leave `review`

## Next QA Step

Run the isolated benchmark for one standard release and one higher-risk staged rollout, then compare whether the with-skill branch produces clearer verification gates and rollback readiness than baseline.
