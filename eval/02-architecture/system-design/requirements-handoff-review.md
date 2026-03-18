# Requirements-to-System-Design Handoff Review

## Goal

Verify that `system-design` can consume a reviewed requirements document and produce architecture that preserves upstream constraints instead of silently inventing migration or compatibility facts.

## Scenario

- `access-review-modernization-requirements-handoff`

This is a brownfield modernization scenario where:

- release 1 must coexist with a legacy module
- some tenant-specific rules are contractual but not fully inventoried
- historical-data treatment is partially bounded
- sync semantics remain unresolved

## Artifacts Reviewed

- Manual baseline run: `manual-run-2026-03-17-access-review`
- Input fixture: `fixtures/access-review-modernization-requirements.md`

## Baseline Findings

The baseline architecture draft is serviceable, but it shows the generic drift expected when architecture is produced without the system-design skill guiding boundary discipline:

- it moves quickly into solution shape without first naming architectural drivers
- it assumes a service-oriented split and a copied historical reporting store without preserving the legacy-read-only boundary as deliberately
- it converts unresolved sync semantics into a daily synchronization approach
- it prepares a useful starting point, but it is weaker on explicit downstream architectural constraints

## With-Skill Findings

The skill-applied architecture is stronger on the dimensions that matter for a lifecycle-aware system:

- names architectural drivers before structural decisions
- preserves release-1 coexistence with the legacy module as an explicit boundary
- keeps historical legacy-read-only treatment visible instead of flattening it into migration work
- preserves unresolved tenant and synchronization questions as architectural open questions
- shapes the output for downstream `api-design`, `data-modeling`, and `task-breakdown`

## Assertion Review

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| stays in architecture phase | partial | pass | Baseline stays mostly high-level but drifts faster into solution and migration choices. |
| preserves brownfield coexistence | partial | pass | With-skill protects coexistence and legacy-read-only boundaries more explicitly. |
| preserves upstream open questions | partial | pass | Baseline resolves sync cadence too early; with-skill keeps it open. |
| maps drivers to structure | partial | pass | With-skill ties structure back to compliance, compatibility, and coexistence drivers. |
| prepares downstream handoff | partial | pass | With-skill names downstream boundaries for `api-design`, `data-modeling`, and `task-breakdown`. |

## Conclusion

The first manual review suggests `system-design` has the same general shape as `requirements-engineering`:

- it is more valuable as a routed/core workflow skill than as a discoverability-first skill
- its value comes from boundary discipline, trade-off framing, and preservation of unresolved upstream facts

This is review-stage evidence, not tested-stage evidence. The next step is an isolated benchmark for the same scenario plus at least one spec-driven scenario where `spec-doc` and `domain-model` are present.
