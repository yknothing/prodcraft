# User-Research-to-Requirements Handoff Review

## Goal

Verify that `requirements-engineering` can consume evidence-backed user-research artifacts, then turn them into release-1 requirements without flattening segment evidence, reopening excluded scope, or collapsing discovery findings into premature solution commitments.

## Scenarios

### Scenario A: `team-invite-user-research-handoff`

This is a non-brownfield collaborative SaaS specification scenario where:

- user research has already validated that lightweight email invite is the dominant release-1 path
- the product still needs a simple onboarding flow rather than enterprise identity-first setup
- requirements work must sharpen release-1 obligations without turning the problem into SSO or bulk-admin scope too early

### Scenario B: `seat-guest-management-user-research-handoff`

This is a classic B2B/SaaS brownfield specification scenario where:

- user research has already validated that lightweight external collaboration is the dominant release-1 pain
- the current product already has a paid-seat model in production
- requirements work must sharpen release-1 obligations without turning the problem into a broad pricing, procurement, or policy redesign

## Artifacts Reviewed

### Scenario A

- Input fixture: `handoff-fixtures/team-invite-user-persona-set.md`
- Input fixture: `handoff-fixtures/team-invite-user-journey-map.md`
- Manual branch pair: `user-research-handoff-manual-run-2026-03-17-team-invite`

### Scenario B

- Input fixture: `handoff-fixtures/seat-guest-management-user-persona-set.md`
- Input fixture: `handoff-fixtures/seat-guest-management-user-journey-map.md`
- Manual branch pair: `user-research-handoff-manual-run-2026-03-17-seat-guest`

## Fixture Honesty Note

The user-research artifacts used here are **QA fixtures**, not real production customer research. That is acceptable for this review because the goal is to test downstream consumption behavior, not to prove market truth.

## Baseline Findings

Across both scenarios, the manual baseline requirements drafts are usable, but they show the generic drift expected when research evidence is not reinforced by the skill:

- major user needs are preserved, but evidence traceability is relatively light
- release-1 scope remains mostly sensible, yet non-goals and escalation triggers are under-specified
- primary and contrast segment pressures are more likely to blur together than remain intentionally separated

Scenario-specific drift also appears:

- in Scenario A, enterprise identity and bulk-admin extensions re-enter the conversation earlier than the research signal justifies
- in Scenario B, guest collaboration starts to blend with broader governance and procurement scope

## With-Skill Findings

Across both scenarios, the skill-applied responses are materially stronger on the downstream dimensions that matter here:

- keep the work in the requirements layer
- translate persona and journey evidence into clearer P0/P1 obligations
- keep later-scope expansions explicit as non-goals
- carry forward contrast-segment pressure as open questions or later-scope triggers instead of silently mixing it into day-one requirements

Scenario-specific advantages also appear:

- in Scenario A, `email-invite-first` remains the clear release-1 boundary instead of sliding toward SSO-first or bulk provisioning
- in Scenario B, `guest-first coexistence` remains the release-1 boundary instead of expanding into a generic admin-program rewrite

## Assertion Review

| Assertion | Expected baseline tendency | Expected with-skill tendency | Why it matters |
|---|---|---|---|
| stays in specification phase | partial | pass | This handoff should not jump to architecture, pricing redesign, or policy-system design. |
| preserves user-research evidence | partial | pass | Requirements should stay traceable to personas and journey evidence. |
| preserves non-goals | partial | pass | Release 1 should not silently become a broad seat-governance rewrite. |
| distinguishes primary vs contrast segment pressure | partial | pass | The guest-first path only holds if governance-heavy accounts remain a later-scope trigger rather than the default first-release center. |
| prepares downstream handoff | partial | pass | The resulting requirements should be shaped for system design and acceptance criteria. |

## Current Conclusion

This downstream-consumption review shows that evidence-backed `user-research` artifacts can improve `requirements-engineering` output quality in both non-brownfield and brownfield SaaS scenarios. The lift is strongest on scope discipline, segment-sensitive traceability, and preservation of release-1 non-goals.

## Remaining Limits

- this review is still manual evidence, not isolated benchmark evidence
- the fixtures are synthetic QA artifacts, not real field data
- the next stronger step is to keep upgrading one or both scenarios to semi-isolated or isolated benchmark evidence
