# Intake-to-Problem-Framing Handoff Review

## Goal

Verify that `problem-framing` can consume an approved `intake-brief` and produce a clearer, more auditable direction artifact without repeating intake or turning entry into a heavyweight workshop.

## Scenario A

- `team-invite-direction`

This is a non-brownfield direction-setting scenario where:

- the work has already been classified as new product work
- the route to discovery is clear
- the release-1 direction remains fuzzy
- downstream work would otherwise risk jumping straight into requirements with an implicit solution choice

## Artifacts Reviewed

- Manual run: `manual-run-2026-03-17-team-invite`
- Input fixture: `fixtures/team-invite-product-intake-brief.md`

## Baseline Findings

The baseline direction note is competent, but it is generic in the ways that matter for an entry-stack skill:

- it gives a recommendation quickly without explicitly stating why `problem-framing` was needed
- it compares options, but not as explicit artifacts with preserved assumptions and non-goals
- it does not record any question-budget discipline
- it is useful as a product note, but weaker as an auditable handoff artifact

## With-Skill Findings

The skill-applied response is stronger on the dimensions that justified adding `problem-framing`:

- it makes the invocation reason explicit instead of assuming the reader knows why the skill ran
- it records zero additional questions, showing that the skill can stay lightweight when the intake brief is already sufficient
- it turns the conversation into explicit `problem-frame`, `options-brief`, and `recommended direction` structure
- it preserves non-goals and open questions instead of silently converging too early
- it names a clean downstream destination (`user-research`) and explains why requirements should wait

## Assertion Review

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| does not repeat intake | partial | pass | Baseline avoids full re-triage, but with-skill makes the intake handoff cleaner and more explicit. |
| keeps extra burden low | unclear | pass | Baseline says nothing about question load; with-skill records zero additional questions. |
| compares 2-3 viable directions | pass | pass | Both do this, but with-skill preserves clearer trade-off structure. |
| preserves assumptions and non-goals | partial | pass | With-skill is much clearer about what release 1 should avoid. |
| names next lifecycle destination | partial | pass | Baseline suggests next work; with-skill ties it directly to the chosen direction and why it is next. |
| remains pre-requirements / pre-architecture | pass | pass | Neither branch collapses into implementation or architecture detail. |

## Scenario A Conclusion

This first manual review supports the intended shape of `problem-framing`:

- it is more useful as a **routed entry-stack skill** than as a discoverability-first skill
- its value is not just option generation, but better observability and cleaner downstream handoff
- it can add structure without adding more user burden when intake has already done its job

## Scenario B

- `access-review-direction`

This is a brownfield modernization scenario where:

- the route to modernization is already known
- coexistence with the legacy module is mandatory for release 1
- the release-1 direction is still open enough that direct requirements or architecture work would risk premature commitments

## Additional Artifacts Reviewed

- Manual run: `manual-run-2026-03-17-access-review`
- Input fixture: `fixtures/access-review-modernization-intake-brief.md`

## Brownfield Baseline Findings

The baseline response is sensible, but it is weaker on the aspects that matter most in brownfield discovery:

- it recommends a direction without explicitly framing why that direction is safer for the brownfield boundary
- it preserves open questions, but not as structured constraints and non-goals
- it points to requirements and architecture next, but does not clearly guard against premature migration choices

## Brownfield With-Skill Findings

The skill-applied response is materially stronger on the intended `problem-framing` dimensions:

- makes the brownfield invocation reason explicit
- records zero additional questions, showing that the skill can stay lightweight when the intake brief is already sufficient
- preserves coexistence, anti-goals, and unresolved synchronization scope as explicit framing elements
- compares release-1 directions without collapsing into architecture or migration sequencing
- hands off cleanly to `requirements-engineering` instead of jumping directly into system design

## Brownfield Assertion Review

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| does not repeat intake | partial | pass | With-skill is clearer about why it starts where it does. |
| keeps extra burden low | unclear | pass | With-skill explicitly records zero additional questions. |
| preserves brownfield coexistence | partial | pass | Baseline mentions coexistence; with-skill turns it into a sharper boundary and non-goal set. |
| avoids premature architecture drift | partial | pass | With-skill is more disciplined about staying pre-requirements / pre-architecture. |
| names next lifecycle destination | partial | pass | With-skill makes the handoff to `requirements-engineering` more explicit and justified. |

## Updated Conclusion

Across both the non-brownfield and brownfield manual scenarios, `problem-framing` now shows the same emerging shape:

- it is more valuable as a **routed entry-stack skill** than as a discoverability-first skill
- its main value is disciplined option comparison plus observable handoff, not generic idea generation
- it improves direction clarity without forcing additional questioning when intake has already captured the important context

## Updated Remaining Limits

- both completed scenarios are still manual review evidence, not isolated benchmark evidence
- the next stronger evidence step is an isolated or semi-isolated benchmark on one of the same scenarios
