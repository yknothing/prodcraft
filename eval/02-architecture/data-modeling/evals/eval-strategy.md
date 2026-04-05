# Data Modeling QA Strategy

## Goal/Objective

Evaluate whether `data-modeling` turns reviewed architecture, domain language, and spec constraints into a durable persistence shape with explicit ownership, lifecycle rules, and migration safety.

## Why Routed Review First

`data-modeling` is downstream of `system-design` and should be judged by handoff quality, not discoverability.

The first review question is whether the skill preserves the architectural boundaries it receives instead of inventing schema convenience that will later break ownership, coexistence, or migration assumptions.

## Scenario(s)

1. `access-review-modernization-data-modeling`
   - reviewed architecture and domain model for a brownfield modernization slice
   - the model must preserve coexistence with legacy records and phased migration behavior

2. `team-invite-data-modeling`
   - a simpler non-brownfield comparison slice
   - used to confirm the skill still defines ownership and lifecycle rules when migration pressure is lower

## Assertions

1. `stays-in-persistence-design-layer`
   - output remains about schema, ownership, state, and retention
   - it does not collapse into implementation code, API design, or task sequencing

2. `assigns-canonical-ownership`
   - every core entity or aggregate has a clear owner
   - projections, caches, and derived views are explicitly marked as non-authoritative

3. `makes-lifecycle-and-mutation-rules-explicit`
   - identifiers, uniqueness, archival, deletion, and state transition rules are documented
   - brownfield migration hazards are visible rather than implied away

4. `preserves-boundaries-and-change-safety`
   - the model respects architectural seams and avoids cross-boundary schemas of convenience
   - future changes such as backfills, phased rollout, and coexistence remain feasible

5. `prepares-downstream-handoff`
   - the output is usable by `feature-development` and `tdd` without re-interpreting ownership or lifecycle rules

## Method

1. Produce a baseline data model review without the skill.
2. Produce a second review while explicitly using `data-modeling`.
3. Compare both outputs against the assertions above.
4. Record the result in a review artifact that states whether the model is ready to advance or still needs redesign.

## Exit Criteria for Review Stage

- The skill clearly improves ownership clarity and migration safety over baseline
- The output stays at the schema/ownership boundary
- Brownfield coexistence or backfill risk is addressed explicitly when relevant
- Downstream implementation teams can use the result without inventing missing persistence rules
- A follow-up benchmark can be written without first redesigning the review packet
