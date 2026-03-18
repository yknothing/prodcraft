# Architecture-to-API Handoff Review

## Goal

Verify that `api-design` turns reviewed architecture plus requirements into stable release-1 contracts without leaking migration or implementation decisions into public APIs.

## Scenario

- `access-review-modernization-architecture-handoff`

This is a brownfield modernization scenario where:

- release 1 must coexist with a legacy module
- some compatibility rules remain unresolved
- historical campaigns retain a legacy-read boundary
- sync semantics are still open

## Artifacts Reviewed

- Manual baseline run: `manual-run-2026-03-17-access-review`
- Input fixtures:
  - `fixtures/access-review-modernization-architecture.md`
  - `fixtures/access-review-modernization-requirements.md`

## Baseline Findings

The baseline API draft is workable, but it drifts in several lifecycle-sensitive ways:

- it exposes migration-only operations such as cutover/import as if they were stable release-1 APIs
- it resolves the sync question prematurely through a public `/sync` endpoint and same-day assumption
- it is weaker on explicit unsupported-flow handling for partially understood reassignment/data-correction paths
- it mixes compatibility concerns into public contract shape without clearly separating adapter/internal boundaries

## With-Skill Findings

The skill-applied API outline is stronger on the dimensions that matter for a lifecycle-aware contract:

- keeps public release-1 APIs separate from internal compatibility boundaries
- preserves coexistence and historical-read boundaries explicitly
- avoids exposing migration-only or cutover-only commands as public stable contracts
- keeps unresolved sync and tenant-compatibility questions visible as deferred contract decisions
- shapes the result for downstream implementation and contract testing

## Assertion Review

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| stays in API contract layer | partial | pass | Baseline stays contract-oriented but leaks migration workflow through cutover/import endpoints. |
| preserves brownfield coexistence | partial | pass | With-skill keeps coexistence explicit without turning replacement flow into public API. |
| preserves open questions | partial | pass | Baseline resolves sync too early; with-skill leaves sync and compatibility questions visible. |
| defines consistent contract shape | partial | pass | With-skill is cleaner on authorization, unsupported flows, and error handling. |
| prepares downstream handoff | partial | pass | With-skill gives clearer shape for implementation and contract tests. |

## Conclusion

The first manual review suggests `api-design` behaves like the other spine skills under evaluation:

- it is more valuable as a routed/core workflow skill than as a discoverability-first skill
- its value comes from preserving upstream architecture intent and making contract boundaries explicit

This is review-stage evidence only. The next step is an isolated benchmark for the same brownfield scenario plus a spec-driven external-consumer scenario.
