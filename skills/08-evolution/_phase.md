# Phase 08: Evolution

## Purpose

Learn from operations, manage technical debt, plan migrations, retire deprecated components, and feed insights back into the next development cycle. Evolution closes the lifecycle loop.

## When to Enter

- System is stable in production with established SLOs met.
- Sufficient operational data exists to identify improvement opportunities.
- Sprint/phase has completed and retrospective is due.
- Postmortem or review evidence is available and ready to be converted into next-cycle improvements.

## Entry Criteria

- Operational metrics are being collected and reviewed.
- Capacity constraints and the decision owner are known; record proposed work separately from committed capacity.
- Recent incidents, quality findings, or delivery misses are documented well enough to drive specific follow-up actions.

## Exit Criteria (Quality Gate)

The selected retrospective or debt review is complete. Record evidence-backed actions with owners, agreed timing or a pending scheduling decision, and the next lifecycle destination; an explicit no-new-action decision is valid when supported by the evidence. Catalog and prioritize relevant debt. Feed applicable insights back to discovery/planning without inventing an action quota.

Improvement items should be small enough to route back through intake and planning instead of remaining as vague "we should do better" notes.
Debt items should be prioritized by real recurrence cost and routed to the right next phase rather than left as an undifferentiated backlog.

When evolution produces a concrete upstream correction, capture it as a `course-correction-note` and route directly to `01-specification`, `02-architecture`, or `03-planning`.

## Key Skills

| Skill | Purpose | Effort |
|---|---|---|
| pc-tech-debt-management | Catalog, prioritize, and plan debt remediation | medium |
| pc-migration-strategy | Plan and execute platform/architecture migrations | xlarge |
| pc-deprecation | Retire features, APIs, and services safely | medium |
| pc-retrospective | Capture learnings and improve process | small |

## Typical Duration

- Retrospective: 1-2 hours per sprint
- Tech debt management: ongoing within owner-approved capacity; a proposed allocation is not a commitment
- Migration: weeks to months (project-level)
- Deprecation: weeks to months per item

## Anti-Patterns

- **No retrospective** -- Without reflection, the team repeats the same mistakes.
- **Debt ignored until crisis** -- By then, remediation cost has multiplied.
- **Big bang migration** -- Incremental migration reduces risk dramatically.
- **Deprecation without communication** -- Surprising consumers with removed features destroys trust.

## Cross-Cutting Matrix

See `rules/cross-cutting-matrix.yml` for `must_consider`, `must_produce`, `skip_when_fast_track`, and `conditional` cross-cutting obligations at this phase.
