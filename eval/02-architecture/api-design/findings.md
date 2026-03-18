# API Design QA Findings

## Summary

`api-design` has moved to `review` status.

## What Changed

1. The skill description and body were tightened to reflect lifecycle-aware contract work rather than generic API advice.
2. Brownfield coexistence, backward compatibility, and unresolved-question preservation are now explicit parts of the skill.
3. A first manual architecture-to-API handoff review was added using the access-review modernization scenario.

## What We Learned

1. Without explicit guardrails, a generic baseline is likely to expose migration-only behavior as public contract.
2. The skill improves separation between public release-1 APIs and internal compatibility/migration boundaries.
3. The skill appears most valuable as a routed workflow skill immediately downstream of `system-design`.

## Current Interpretation

At this stage, `api-design` appears to be:

- a core architecture skill on the lifecycle spine
- stronger as a routed workflow skill than as a discoverability-first skill
- still in need of isolated benchmark evidence before it can leave `review`

## Next QA Step

Run an isolated benchmark for the same brownfield scenario, then add a spec-driven consumer-facing scenario with richer schema detail.
