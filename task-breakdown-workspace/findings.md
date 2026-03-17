# Task Breakdown QA Findings

## Summary

`task-breakdown` has moved to `review` status.

## What Changed

1. The skill description and body were tightened to reflect lifecycle-aware planning rather than generic decomposition advice.
2. Brownfield coexistence, reversible seams, and blocker visibility are now explicit parts of the skill.
3. A first manual architecture-to-task handoff review was added using the access-review modernization scenario.

## What We Learned

1. Generic decomposition tends to drift toward coarse horizontal work items and hidden blockers.
2. The skill improves preservation of rollback/coexistence work and exposes unresolved questions as planning blockers.
3. The skill appears most valuable as a routed workflow skill downstream of `system-design` and `api-design`.

## Current Interpretation

At this stage, `task-breakdown` appears to be:

- a core planning skill on the lifecycle spine
- stronger as a routed workflow skill than as a discoverability-first skill
- still in need of isolated benchmark evidence before it can leave `review`

## Next QA Step

Run an isolated benchmark for the same brownfield scenario, then add a feature-oriented non-migration scenario to verify that the skill does not overfit to modernization work.
