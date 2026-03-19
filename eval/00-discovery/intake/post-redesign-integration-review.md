# Intake Post-Redesign Integration Review

## Goal

Verify that the redesigned `intake` now leaves behind an `intake-brief` that downstream skills can use directly, especially:

- `problem-framing` when the route is discovery but the direction is still fuzzy
- direct downstream lifecycle work when the route is clearer

## Artifacts Reviewed

All reviewed artifacts come from:

- `eval/00-discovery/intake/post-redesign-benchmark-run-2026-03-19-gemini-naming-rerun`

Reviewed with-skill branches:

- `eval-1-ambiguous-dark-mode-scope/with_skill/response.md`
- `eval-2-legacy-permissions-migration/with_skill/response.md`
- `eval-3-seat-management-research-route/with_skill/response.md`

## Handoff Findings

### Scenario 1: `ambiguous-dark-mode-scope`

The output is handoff-ready for `problem-framing`:

- route is explicit: scope direction is fuzzy, so framing comes before specification
- key risk is explicit: cross-surface inconsistency and scope creep
- one routing question remains, but it is still within the intended low-question budget

This is a good example of the redesigned intake contract working as intended. The skill does not solve the scope question itself. It captures the ambiguity and hands it forward.

### Scenario 2: `legacy-permissions-migration`

The output is directionally handoff-ready for brownfield downstream work:

- migration is classified correctly as `00-discovery` plus `brownfield`
- hybrid-state, compatibility, and data-consistency risks are preserved
- the multi-phase path is clear enough for downstream execution planning

Remaining weakness:

- later path stages can still remain provisional depending on what the first discovery handoff finds

That is now a later-stage planning ambiguity, not a first-hop handoff failure.

### Scenario 3: `seat-management-research-route`

The output is strongly handoff-ready for the redesigned discovery stack:

- it explicitly routes first to `problem-framing`
- it names `user-research` and `requirements-engineering` as later steps
- it preserves the unresolved root-cause ambiguity instead of collapsing into a research plan or feature proposal

This is the clearest evidence that the redesign split between `intake` and `problem-framing` is now operationally real.

## Assertion Review

| Check | Judgment | Notes |
|---|---|---|
| explains why intake was invoked | pass | All three outputs make the routing reason explicit rather than silently acting on the request. |
| preserves risks or unknowns that changed routing | pass | Each output records the ambiguity or risk that justifies the route. |
| names the next step clearly enough for downstream use | pass | The first actionable downstream handoff is clear in all three reviewed artifacts. |
| supports `problem-framing` handoff when direction is fuzzy | pass | Scenarios 1 and 3 both show this clearly. |
| avoids requiring downstream skills to reconstruct routing context | pass | The benchmark outputs contain enough context for the next skill to understand why it is being invoked. |

## Current Conclusion

The redesigned `intake` now leaves behind a meaningfully better downstream artifact than the pre-redesign routing summaries:

- the route is observable
- the handoff reason is explicit
- the discovery split with `problem-framing` is preserved
- downstream skills no longer need to infer why intake chose this path

The main remaining integration gap is **later-stage route specificity**, not missing routing context or first-hop handoff ambiguity.

## Remaining Limits

- this is still a review of benchmark-produced handoff artifacts, not a full downstream execution drill
- one scenario still needs a single clarifying answer before handoff, which is acceptable but means the artifact is not yet fully finalized at that moment
- a future deeper check should confirm that concrete downstream skills consume these artifacts cleanly without requiring manual reinterpretation
