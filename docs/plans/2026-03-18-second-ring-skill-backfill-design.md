# Second-Ring Skill Backfill Design

## Goal

Strengthen the architecture-to-delivery chain by replacing the next highest-value planned nodes with real skill packages:

- `data-modeling`
- `security-design`
- `tech-selection`
- `release-management`

## Why This Batch

These skills already sit inside the architecture or delivery artifact model and are referenced by phase guidance or related-skill sections. Without them, the lifecycle still has silent handoff gaps around storage design, trust boundaries, technology decisions, and release coordination.

## Design Decisions

1. Keep all four skills at `draft` status.
2. Align workflows so architecture phases invoke the new architecture skills explicitly.
3. Reconcile delivery sequencing by treating `release-management` as the producer of `release-plan`, which then feeds `deployment-strategy`.
4. Update nearby skills and phase docs so they link to the real packages instead of stale planned placeholders.
