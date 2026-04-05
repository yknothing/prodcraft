# System Design QA Findings

## Summary

`system-design` has moved to `review` status.

## What Changed

1. The skill contract was aligned with actual Prodcraft workflow usage.
2. `requirements-doc` is now treated as the minimum required architecture input.
3. `spec-doc` and `domain-model` are now treated as optional amplifying inputs rather than universal hard prerequisites.
4. The architecture phase entry criteria were updated to match multi-methodology reality instead of forcing spec-heavy preconditions in every workflow.
5. A first brownfield routed handoff review was added using an access-review modernization scenario.

## What We Learned

1. There was a real contract mismatch between the prior `system-design` metadata and the actual workflow graph.
2. Brownfield and agile paths need architecture to start from reviewed requirements plus visible open questions; they cannot wait for a heavyweight spec package every time.
3. The first manual handoff review suggests the skill improves architecture discipline around coexistence boundaries, unresolved-question handling, and downstream handoff clarity.
4. The skill needed stronger decision depth around measurable quality attributes, reversibility, exit cost, and fitness functions so architecture reviews do not collapse into prose-only trade-off discussions.
5. A true isolated benchmark asset now exists for the brownfield access-review scenario.
6. The isolated baseline branch completes cleanly and is strong enough to serve as a real control artifact.
7. The current blocker is no longer "missing benchmark design." The blocker is runner instability on the with-skill branch:
   - first `copilot` fallback run timed out at `300s`
   - second `copilot` rerun at `600s` failed with `Connection error.` after loading the skill and fixture
   - a later 2026-04-05 rerun attempt became operationally invalid because concurrent benchmark processes wrote into the same output lane
8. Because the with-skill branch has not yet produced a clean response artifact, `system-design` still lacks the tested-grade benchmark result needed for promotion.

## Current Interpretation

At this stage, `system-design` appears to be:

- a core architecture skill on the lifecycle spine
- likely stronger as a routed workflow skill than as a discoverability-first skill
- materially stronger once architecture decisions are tied to measurable driver tables and follow-up fitness functions
- still in need of isolated benchmark evidence before it can leave `review`

## Next QA Step

Rerun the same isolated brownfield benchmark once the with-skill runner lane is stable.

Do not widen to the spec-driven second scenario until the current brownfield with-skill branch completes cleanly.
