# 2026-03-26 Live Pressure-Test Cycle 1 Summary

> Status: historical. The narrow `intake-brief` follow-on identified here was implemented on 2026-03-27. See `2026-03-27-live-cycle-2-summary.md` for the post-change verification pass.

## Included Runs

- `runs/2026-03-26-PT-02-fast-track-bugfix-live.md`
- `runs/2026-03-26-PT-05-docs-only-live.md`
- `runs/2026-03-26-PT-06-mixed-language-live.md`

## High-Signal Outcomes

1. The control-plane route itself still looks correct across all three live runs.
2. `PT-06` justified the first language-boundary contract work because the ambiguity appeared inside artifact semantics, not in routing.
3. `PT-02` and `PT-05` repeated the same low-value friction: `workflow_primary` and empty `workflow_overlays` carry little or no routing value once the path is a narrow fast-track or direct cross-cutting handoff.

## Repeated Friction

| Friction | Runs | Classification | Action |
|---------|------|----------------|--------|
| `workflow_primary` remains required even when the route is effectively direct and degenerate | `PT-02`, `PT-05` | accidental | open a follow-on proposal to test narrowing or hiding this field for narrow routes only |
| empty `workflow_overlays` still appears in the artifact even when no overlay is active | `PT-02`, `PT-05`, `PT-06` | accidental but low severity | consider making empty overlays implicit before changing broader workflow semantics |
| mixed-language ambiguity in canonical artifact records | `PT-06` | accidental | already addressed by the current language-boundary contract pass |

## What Did Not Repeat

- `brownfield` overlay complexity has not shown up as low-value friction in a live run yet.
- `course-correction-note` has not yet produced evidence of unnecessary overhead.
- cross-cutting obligation semantics did not create obvious confusion in these runs.

## Recommended Next Move

Do not widen the language-boundary contract any further yet.

Instead, treat the next follow-on candidate as:

- a narrow proposal against `intake-brief`
- limited to docs-only and obvious fast-track routes
- focused on whether `workflow_primary` and empty `workflow_overlays` should become optional, implicit, or user-hidden for those routes
