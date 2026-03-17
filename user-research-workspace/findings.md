# User Research QA Findings

## Summary

`user-research` moves from `draft` to `review`.

The skill is now treated as a **routed discovery skill** whose current evidence comes from a staged handoff review from `problem-framing`.

## What Changed

1. The skill package now acknowledges that `problem-frame` can be a valid upstream input.
2. The skill contract now explicitly forbids inventing "validated" personas when real user evidence does not yet exist.
3. The first review-stage handoff review now checks whether `user-research` can turn a framed discovery direction into a concrete research plan without drifting into requirements.

## What We Learned

1. `problem-framing` is a meaningful upstream consumer test for `user-research`; it exposes whether the skill preserves non-goals and unresolved questions instead of flattening them.
2. The correct early output in this situation is often a **research plan**, not a pretend persona set.
3. The skill's value is strongest when the team already has a candidate direction but still needs user evidence before requirements should start.
4. The first signal no longer comes from a single product-direction scenario only; it now also appears in a classic B2B/SaaS brownfield admin-modernization case.

## Implication for Prodcraft

`user-research` should be evaluated as a routed discovery skill:

- invoked after `intake` or `problem-framing`
- judged on evidence quality and handoff discipline
- not primarily judged on discoverability in a crowded skill ecosystem

## Next QA Step

Upgrade the `seat-guest-management-problem-framing-handoff` review to a semi-isolated benchmark. It is the better representative stress case for classic B2B/SaaS brownfield discovery than `team-invite`.
