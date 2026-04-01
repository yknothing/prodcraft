# Feature Development QA Findings

## Summary

`feature-development` has moved to `review` status.

## What Changed

1. The skill is now under manifest-backed QA instead of remaining a critical-but-untracked draft.
2. Review-stage evidence was defined around the real routed handoff: reviewed task slice plus tests into a small mergeable increment.
3. The benchmark lane is now explicit, so future isolated Gemini runs can measure whether the skill improves slice discipline over a baseline.

## What We Learned

1. `feature-development` is not generic "write code" guidance. Its value is preserving slice size, contract boundaries, and reviewability after `tdd`.
2. The strongest first evidence for this skill is routed handoff quality, not discoverability.
3. The main regression risk is scope creep: generic implementation behavior often widens the change once coding starts.

## Current Interpretation

At this stage, `feature-development` appears to be:

- a core implementation skill on the lifecycle spine
- stronger as a routed workflow skill than as a discoverability-first skill
- still in need of isolated benchmark evidence before it can leave `review`

## Next QA Step

Run the isolated benchmark for one forward slice and one brownfield slice, then compare whether the with-skill branch stays smaller, more test-bound, and more reviewable than baseline.
