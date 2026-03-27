# 2026-03-27 Live Pressure-Test Cycle 3 Summary

## Included Runs

- `runs/2026-03-27-PT-04-hotfix-overlay-live.md`
- `runs/2026-03-27-PT-03-brownfield-overlay-live.md`

## Purpose

This cycle verifies the other side of the `intake-brief` workflow-metadata
change: after simplifying direct fast-track routes, do overlay-bearing routes
still keep explicit workflow metadata where it is genuinely useful?

## High-Signal Outcomes

1. The route stayed correct in both overlay-bearing scenarios.
2. `workflow_overlays` remained explicit and materially useful in both runs.
3. `workflow_primary` remained explicit and justified because the overlays did not replace the primary governance model.

## Resolution Check

| Route shape | Metadata signal | Judgment |
|-------------|-----------------|----------|
| `PT-04` hotfix incident | `workflow_overlays=[hotfix]` distinguishes compressed incident-first handling from a normal implementation route | keep explicit |
| `PT-03` brownfield migration | `workflow_overlays=[brownfield]` preserves coexistence, rollback, and staged-modernization constraints | keep explicit |
| both runs | `workflow_primary=agile-sprint` still matters because overlay alone does not define governance | keep explicit |

## What Changed in the Overall Picture

- Direct fast-track routes were simplified successfully in cycle 2.
- Overlay-bearing routes still benefit from explicit workflow metadata.
- No new subtraction candidate emerged from this cycle.

## Recommended Next Move

Hold the current `intake-brief` contract as-is.

The evidence now supports a stable split:

- direct fast-track routes may keep workflow metadata implicit when it adds no routing value
- overlay-bearing or non-degenerate routes should keep explicit workflow metadata
