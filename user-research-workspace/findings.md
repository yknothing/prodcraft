# User Research QA Findings

## Summary

`user-research` moves from `draft` to `review`.

The skill is now treated as a **routed discovery skill** whose current evidence comes from a staged handoff review from `problem-framing`.

## What Changed

1. The skill package now acknowledges that `problem-frame` can be a valid upstream input.
2. The skill contract now explicitly forbids inventing "validated" personas when real user evidence does not yet exist.
3. `research-plan` is now declared as a first-class output so the current review evidence matches the actual pre-evidence behavior of the skill.
4. The first review-stage handoff review now checks whether `user-research` can turn a framed discovery direction into a concrete research plan without drifting into requirements.

## What We Learned

1. `problem-framing` is a meaningful upstream consumer test for `user-research`; it exposes whether the skill preserves non-goals and unresolved questions instead of flattening them.
2. The correct early output in this situation is often a **research plan**, not a pretend persona set.
3. The skill's value is strongest when the team already has a candidate direction but still needs user evidence before requirements should start.
4. The first signal no longer comes from a single product-direction scenario only; it now also appears in a classic B2B/SaaS brownfield admin-modernization case.
5. The preferred brownfield scenario now has semi-isolated manual benchmark evidence, which is stronger than plain handoff review but still weaker than a true isolated benchmark.
6. A downstream specification-consumption review now exists for the same brownfield scenario, showing that evidence-backed user-research artifacts improve later requirements work rather than just producing cleaner discovery documents.
7. That downstream specification-consumption path now also has semi-isolated manual benchmark evidence, so the value of `user-research` is no longer supported only by discovery-local reviews.

## Contract Implication

`research-plan` should be treated as a legitimate intermediate discovery artifact:

- it improves observability and handoff discipline
- it does **not** satisfy the full user-research quality gate by itself
- downstream specification work should start from evidence-backed personas and journeys, not from a research plan alone

The new downstream review follows that rule: it uses evidence-shaped persona and journey fixtures, not the earlier `research-plan`, when testing `requirements-engineering`.

## Implication for Prodcraft

`user-research` should be evaluated as a routed discovery skill:

- invoked after `intake` or `problem-framing`
- judged on evidence quality and handoff discipline
- not primarily judged on discoverability in a crowded skill ecosystem

## Next QA Step

Run a true isolated benchmark or cross-reviewer execution drill on `seat-guest-management-problem-framing-handoff`, then show how the resulting research outputs improve a downstream skill such as `requirements-engineering`.
