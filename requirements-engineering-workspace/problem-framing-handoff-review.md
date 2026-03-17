# Problem-Framing-to-Requirements Handoff Review

## Goal

Verify that `requirements-engineering` can consume an approved `problem-frame` and `design-direction`, then turn them into requirements without losing the upstream non-goals, coexistence boundary, or unresolved questions.

## Scenario

- `access-review-modernization-problem-framing-handoff`

This is a brownfield modernization scenario where:

- `problem-framing` has already compared release-1 directions
- the chosen direction is explicitly "campaign-and-evidence-first coexistence"
- requirements work should now sharpen obligations without collapsing framing into architecture or migration design

## Artifacts Reviewed

- Input fixture: `handoff-fixtures/access-review-modernization-problem-framing.md`
- Upstream framing source: `problem-framing-workspace/manual-run-2026-03-17-access-review`
- Manual branch pair: `problem-framing-handoff-manual-run-2026-03-17-access-review`

## Contract Alignment Note

This review also closes a real contract gap in Prodcraft:

- the artifact flow already said `problem-frame` and `design-direction` feed `requirements-engineering`
- but the skill metadata did not yet acknowledge those artifacts as valid upstream inputs

That mismatch has now been corrected in the skill package.

## Baseline Findings

The manual baseline requirements draft is usable, but it shows the generic drift expected when the framing artifact is not reinforced by the skill:

- it preserves the broad coexistence goal but weakens the explicit chosen direction
- it turns same-day synchronization into a requirement instead of preserving the unresolved consistency question cleanly
- it leaves non-goals and out-of-scope boundaries mostly implicit
- it points downstream toward system design and migration planning together, which weakens specification-phase discipline

## With-Skill Findings

The skill-applied response is materially stronger on the staged handoff dimensions that matter here:

- keep the work in the requirements layer
- preserve the campaign-and-evidence-first coexistence choice as a release boundary, not a migration plan
- translate framing constraints into explicit scope boundaries and out-of-scope statements
- carry forward unresolved tenant, historical-data, and sync questions as open questions instead of invented precision
- shape the output for downstream `system-design` and `acceptance-criteria`

## Assertion Review

| Assertion | Expected baseline tendency | Expected with-skill tendency | Why it matters |
|---|---|---|---|
| stays in specification phase | partial | pass | This handoff should not jump to architecture or migration sequencing. |
| preserves framing non-goals | partial | pass | Release-1 coexistence only works if non-goals remain explicit. |
| preserves design-direction boundary | partial | pass | The recommended direction should become requirements scope, not disappear into generic modernization language. |
| preserves open questions | partial | pass | Sync semantics and tenant obligations are still unresolved. |
| avoids invented precision | partial | pass | The skill should convert unsupported bounds into open questions or assumptions. |
| prepares downstream handoff | partial | pass | Output should be shaped for `system-design` and `acceptance-criteria`. |

## Current Conclusion

This staged handoff is now consistent with the other review-stage evidence already gathered for `requirements-engineering`:

- the skill is strongest as a **routed workflow skill**
- its value is especially visible when upstream artifacts contain scope boundaries, non-goals, and unresolved questions that must survive handoff

## Remaining Limits

- this review is still manual evidence, not isolated benchmark evidence
- the next stronger step is to run a cleaner semi-isolated or isolated benchmark using this exact framing fixture
