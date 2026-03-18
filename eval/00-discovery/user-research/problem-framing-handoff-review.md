# Problem-Framing-to-User-Research Handoff Review

## Goal

Verify that `user-research` can consume an approved `problem-frame`, then turn it into a discovery-grade research plan without losing the chosen direction, non-goals, or unresolved user-behavior questions.

## Scenarios

### Scenario A: `team-invite-problem-framing-handoff`

This is a non-brownfield discovery scenario where:

- `problem-framing` has already compared release-1 directions
- the chosen direction is explicitly `email-invite-first`
- research should now test whether that direction matches the early user segment before requirements begin

### Scenario B: `seat-guest-management-problem-framing-handoff`

This is a classic B2B/SaaS brownfield discovery scenario where:

- an existing product already has paid full-member seats and manual support workarounds for external collaborators
- `problem-framing` selected `guest-first coexistence` as the leading release-1 direction
- research should now validate whether admins primarily need lightweight guest collaboration, tighter seat governance, or procurement-led control before requirements begin

## Artifacts Reviewed

### Scenario A

- Input fixture: `handoff-fixtures/team-invite-problem-framing.md`
- Upstream framing source: `eval/00-discovery/problem-framing/manual-run-2026-03-17-team-invite`
- Manual branch pair: `problem-framing-handoff-manual-run-2026-03-17-team-invite`

### Scenario B

- Input fixture: `handoff-fixtures/seat-guest-management-problem-framing.md`
- Manual branch pair: `problem-framing-handoff-manual-run-2026-03-17-seat-guest`

## Contract Alignment Note

This review also closes a real contract gap in Prodcraft:

- the artifact flow already said `problem-frame` feeds `user-research`
- but the skill metadata did not yet acknowledge `problem-frame` as a valid upstream input

That mismatch has now been corrected in the skill package.

## Baseline Findings

Across both scenarios, the manual baseline research notes are usable, but they show the generic drift expected when the framing artifact is not reinforced by the skill:

- the chosen direction is preserved only weakly
- non-goals remain partly implicit instead of governing the research scope
- research next steps are reasonable, but the evidence threshold before requirements is under-specified
- the audit trail for why this particular research path was chosen is relatively light

Brownfield-specific drift also appears in Scenario B:

- seat governance, guest collaboration, and procurement concerns start to blur together
- the coexistence intent is weaker, so the plan risks reopening a broad admin redesign instead of validating the first release boundary

## With-Skill Findings

Across both scenarios, the skill-applied responses are materially stronger on the staged handoff dimensions that matter here:

- keep the work in discovery rather than sliding into specification
- preserve the chosen direction as the thing being validated, not the final requirement set
- carry forward non-goals and unresolved questions as explicit research questions
- define who to interview, what to validate, and what evidence must exist before `requirements-engineering` should start
- leave a cleaner downstream handoff toward personas, journey maps, and later requirements work

Scenario B shows an additional brownfield-specific advantage:

- the plan preserves `guest-first coexistence` instead of flattening it into a generic "admin controls" program
- it separates external-collaboration evidence from billing/procurement scope, which keeps release-1 learning sharper

## Assertion Review

| Assertion | Expected baseline tendency | Expected with-skill tendency | Why it matters |
|---|---|---|---|
| stays in discovery | partial | pass | This handoff should produce a research plan, not requirements. |
| preserves chosen direction | partial | pass | Research should validate the selected release-1 direction, not reopen it casually. |
| preserves non-goals | partial | pass | Enterprise identity scope was explicitly ruled out for release 1 by default. |
| converts open questions into research questions | partial | pass | The framing artifact named exactly what still needs user evidence. |
| prepares downstream handoff | partial | pass | The output should clarify what evidence is needed before personas and requirements can mature. |

## Current Conclusion

This downstream-consumption review suggests that `user-research` is stronger as a **routed discovery skill** than as a generic auto-discovered assistant. Its value is clearest when upstream framing has already narrowed the direction but user evidence is still missing.

## Remaining Limits

- this review is manual evidence, not isolated benchmark evidence
- even with two scenarios, the sample is still small
- the next stronger step is to upgrade one scenario to semi-isolated benchmark evidence
