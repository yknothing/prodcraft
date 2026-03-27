# 2026-03-27 Live Pressure-Test Cycle 2 Summary

> Status: historical direct-route verification pass. See `2026-03-27-live-cycle-3-summary.md` for the complementary overlay-bearing verification.

## Included Runs

- `runs/2026-03-27-PT-02-fast-track-bugfix-post-change-live.md`
- `runs/2026-03-27-PT-05-docs-only-post-change-live.md`

## Purpose

This cycle is a post-change verification pass for the narrow `intake-brief`
contract update that:

- allows `workflow_primary` to stay implicit for direct `fast-track` routes
- omits `workflow_overlays` when no overlay is active

## High-Signal Outcomes

1. The route stayed correct in both reruns.
2. The previously repeated workflow-metadata friction did not recur.
3. The control plane is now simpler on the two degenerate routes that originally surfaced the subtraction candidate.

## Resolution Check

| Prior friction | Post-change result | Judgment |
|---------------|--------------------|----------|
| `workflow_primary` was required on narrow direct routes | absent in both reruns, with no routing loss | resolved |
| `workflow_overlays=[]` added bookkeeping with no signal | omitted in both reruns | resolved |

## What Remains Open

- `brownfield`, `greenfield`, or `hotfix` overlay routes still need live verification after this cleanup.
- No evidence yet suggests further narrowing of workflow metadata beyond this direct-route case.

## Recommended Next Move

Do not tighten the `intake-brief` contract any further yet.

Prefer the next live pressure-test on a route where workflow metadata should
remain explicit, such as:

- a `hotfix` with the `hotfix` overlay
- a modernization effort using the `brownfield` overlay
