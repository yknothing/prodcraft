# Architecture-to-Task Breakdown Handoff Review

## Goal

Verify that `task-breakdown` turns reviewed architecture and API contracts into implementation-ready work items without flattening brownfield coexistence constraints into a rewrite-style plan.

## Scenario

- `access-review-modernization-planning-handoff`

This is a brownfield modernization scenario where:

- release 1 must coexist with the legacy module
- sync semantics are still unresolved
- some policy and reassignment scope remains incomplete
- rollback and compatibility work must remain explicit

## Artifacts Reviewed

- Manual baseline run: `manual-run-2026-03-17-access-review`
- Input fixtures:
  - `fixtures/access-review-modernization-architecture.md`
  - `fixtures/access-review-modernization-api-contract.md`

## Baseline Findings

The baseline task list is usable as a rough checklist, but it drifts in planning-critical ways:

- it plans as if migration/history work can simply be "built" rather than treated as bounded coexistence work
- it hides blockers from unresolved sync and compatibility questions
- it uses broad horizontal tasks instead of contract-tested vertical slices
- rollback and coexistence safety are missing as first-class work items

## With-Skill Findings

The skill-applied task breakdown is stronger on the dimensions that matter for lifecycle-aware planning:

- sequences work around reversible seams and safety-net tasks first
- keeps coexistence, unsupported-flow handling, and rollback preparation explicit
- exposes open questions as blockers instead of hiding them inside implementation
- organizes work into clearer vertical slices tied to contract and architecture boundaries
- shapes the output for downstream `tdd`, `feature-development`, and `testing-strategy`

## Assertion Review

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| stays in planning layer | partial | pass | Baseline is task-like but too coarse and solution-flattened. |
| preserves brownfield coexistence | partial | pass | With-skill keeps rollback/coexistence work explicit. |
| preserves open-question blockers | fail | pass | Baseline hides unresolved sync/compatibility assumptions. |
| uses vertical slices and dependencies | partial | pass | With-skill shows slice sequencing and a dependency outline. |
| prepares downstream handoff | partial | pass | With-skill points cleanly to `tdd`, `feature-development`, and `testing-strategy`. |

## Conclusion

The first manual review suggests `task-breakdown` follows the same pattern as the upstream spine skills:

- it is more valuable as a routed/core workflow skill than as a discoverability-first skill
- its value comes from preserving upstream boundaries while making implementation sequencing explicit

This is review-stage evidence only. The next step is an isolated benchmark for the same brownfield scenario plus a non-migration scenario to ensure the skill does not overfit to brownfield work.
