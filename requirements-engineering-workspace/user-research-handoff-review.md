# User-Research-to-Requirements Handoff Review

## Goal

Verify that `requirements-engineering` can consume evidence-backed user-research artifacts, then turn them into release-1 requirements without flattening segment evidence, reopening excluded scope, or collapsing discovery findings into premature solution commitments.

## Scenario

- `seat-guest-management-user-research-handoff`

This is a classic B2B/SaaS brownfield specification scenario where:

- user research has already validated that lightweight external collaboration is the dominant release-1 pain
- the current product already has a paid-seat model in production
- requirements work must sharpen release-1 obligations without turning the problem into a broad pricing, procurement, or policy redesign

## Artifacts Reviewed

- Input fixture: `handoff-fixtures/seat-guest-management-user-persona-set.md`
- Input fixture: `handoff-fixtures/seat-guest-management-user-journey-map.md`
- Manual branch pair: `user-research-handoff-manual-run-2026-03-17-seat-guest`

## Fixture Honesty Note

The user-research artifacts used here are **QA fixtures**, not real production customer research. That is acceptable for this review because the goal is to test downstream consumption behavior, not to prove market truth.

## Baseline Findings

The manual baseline requirements draft is usable, but it shows the generic drift expected when the research evidence is not reinforced by the skill:

- it captures the guest-access theme, but weakens the difference between primary and contrast segments
- it starts to blend guest collaboration needs with broader seat-governance and procurement concerns
- it keeps release-1 scope mostly sensible, but leaves non-goals and escalation thresholds under-specified
- it is less explicit about which requirements are directly traceable to observed persona and journey evidence

## With-Skill Findings

The skill-applied response is materially stronger on the downstream dimensions that matter here:

- keep the work in the requirements layer
- preserve `guest-first coexistence` as a release-1 boundary rather than a generic admin-program rewrite
- translate persona and journey evidence into clearer P0/P1 obligations
- keep pricing redesign, org-wide policy engines, and forced seat-model migration explicit as non-goals
- carry forward governance-heavy account behavior as open questions or later-scope triggers instead of silently mixing it into day-one requirements

## Assertion Review

| Assertion | Expected baseline tendency | Expected with-skill tendency | Why it matters |
|---|---|---|---|
| stays in specification phase | partial | pass | This handoff should not jump to architecture, pricing redesign, or policy-system design. |
| preserves user-research evidence | partial | pass | Requirements should stay traceable to personas and journey evidence. |
| preserves non-goals | partial | pass | Release 1 should not silently become a broad seat-governance rewrite. |
| distinguishes primary vs contrast segment pressure | partial | pass | The guest-first path only holds if governance-heavy accounts remain a later-scope trigger rather than the default first-release center. |
| prepares downstream handoff | partial | pass | The resulting requirements should be shaped for system design and acceptance criteria. |

## Current Conclusion

This downstream-consumption review shows that evidence-backed `user-research` artifacts can improve `requirements-engineering` output quality. The lift is strongest on scope discipline, segment-sensitive traceability, and preservation of release-1 non-goals.

## Remaining Limits

- this review is still manual evidence, not isolated benchmark evidence
- the fixtures are synthetic QA artifacts, not real field data
- the next stronger step is to upgrade this scenario to a semi-isolated or isolated benchmark
