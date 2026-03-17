# Problem Framing Explicit Invocation Benchmark Review

## Scope

This review summarizes the current **semi-isolated manual benchmark** evidence for `problem-framing`.

It does **not** claim automated isolated benchmark status. The runs under review preserve:

- separate baseline and with-skill branches
- a copied `skill-under-test/SKILL.md`
- prompts and raw outputs per branch

but the outputs were still authored in one reviewer context.

## Reviewed Artifacts

| Artifact | Scenario | Notes |
|---|---|---|
| `manual-run-2026-03-17-team-invite` | `team-invite-direction` | Non-brownfield direction-setting scenario |
| `manual-run-2026-03-17-access-review` | `access-review-direction` | Brownfield modernization direction-setting scenario |

## Cross-Scenario Manual Review

| Scenario | Baseline | With skill | Judgment |
|---|---|---|---|
| `team-invite-direction` | Recommends a sensible release-1 path, but is weak on explicit invocation reason, non-goals, and auditable structure | Produces a clearer `problem-frame`, records zero added questions, preserves non-goals, and names `user-research` as the justified next step | **Positive lift** |
| `access-review-direction` | Chooses a plausible release-1 direction, but is weaker on brownfield boundary discipline and anti-goals | Preserves coexistence, avoids premature migration drift, records zero added questions, and hands off more cleanly to `requirements-engineering` | **Positive lift** |

## What the Benchmark Shows

### 1. The skill adds value under explicit invocation

Across both scenarios, the with-skill branch is stronger on the dimensions that matter for an entry-stack skill:

- explicit invocation reason
- structured problem framing
- visible non-goals and unresolved questions
- sharper next-step handoff

### 2. The skill's strongest value is not generic ideation

Baseline can already generate a plausible direction note. The meaningful delta is elsewhere:

- stronger observability
- tighter boundary discipline
- lower risk of silently collapsing framing into requirements or architecture

### 3. The skill can stay lightweight

In both reviewed scenarios, the with-skill branch records **zero** additional questions because the intake brief was already sufficient.

This matters because the benchmark is not just about better structure. It is also about avoiding a heavier user burden at the entry stack.

## Current Judgment

`problem-framing` now has credible review-stage evidence that it is:

- **not primarily a discoverability-first skill**
- **stronger as a routed workflow / entry-stack skill**
- valuable when the route is known but the direction still needs explicit trade-off framing

This is now reinforced by downstream-consumption reviews:

- `requirements-engineering-workspace/problem-framing-handoff-review.md`
- `user-research-workspace/problem-framing-handoff-review.md`

Those reviews show the artifact shape is not only locally neat; it is usable by both specification and discovery consumers.

## Status Implication

The skill should remain in `review` because:

1. current evidence is still semi-isolated manual benchmark evidence, not automated isolated benchmark evidence
2. no trigger/discoverability assessment has been run yet, even as a secondary signal
3. the sample size is still small, even though it now covers both non-brownfield and brownfield cases

## Next Required Evidence

1. Run one true isolated benchmark or cross-reviewer execution drill on either `team-invite-direction` or `access-review-direction`.
2. Upgrade at least one downstream-consumption chain to semi-isolated or isolated benchmark evidence.
3. Keep the "low user burden" assertion explicit in future reviews; over-questioning is a known failure mode for this skill class.
