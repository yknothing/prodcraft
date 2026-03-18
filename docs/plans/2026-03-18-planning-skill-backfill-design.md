# Planning Skill Backfill Design

## Goal

Complete the planning phase by replacing the remaining core placeholders with real skill packages:

- `estimation`
- `risk-assessment`
- `sprint-planning`

## Why This Batch

Prodcraft already had a strong bridge from architecture into task decomposition, but the path from decomposed tasks into realistic execution planning remained underspecified. This batch fills that gap with explicit effort sizing, risk handling, and iteration planning.

## Design Decisions

1. Add a new artifact, `estimate-set`, so estimates are first-class planning outputs rather than hidden inside prose.
2. Make `risk-assessment` feed both `estimation` and downstream operations learning, rather than treating risk as a one-off planning note.
3. Wire `sprint-planning` most explicitly into agile planning while keeping the skill available as a reusable planning tool.
