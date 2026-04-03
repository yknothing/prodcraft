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
4. A first isolated benchmark asset now exists for the brownfield compatibility slice.
5. The current benchmark context is too thin for a tested-grade implementation benchmark: task slice plus API contract is not enough on its own because the model still needs a minimal codebase and test fixture to implement against honestly.
6. The `copilot` fallback baseline completed and showed a non-trivial control artifact, but it also confirmed the same design gap by inventing local project structure.
7. The with-skill branch tried to discover and operate on a local codebase, then failed with `Connection error.` before producing a usable artifact. This means the current blocker is not just runner instability; it is also missing code fixture context.

## Current Interpretation

At this stage, `feature-development` appears to be:

- a core implementation skill on the lifecycle spine
- stronger as a routed workflow skill than as a discoverability-first skill
- still in need of a valid isolated benchmark with a minimal code fixture before it can leave `review`

## Next QA Step

Add a minimal code fixture to the brownfield benchmark, rerun that scenario cleanly, and only then decide whether a second forward slice is needed.
