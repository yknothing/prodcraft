# Phase 08: Evolution

## Purpose

Learn from operations, manage technical debt, plan migrations, retire deprecated components, and feed insights back into the next development cycle. Evolution closes the lifecycle loop.

## When to Enter

- System is stable in production with established SLOs met.
- Sufficient operational data exists to identify improvement opportunities.
- Sprint/phase has completed and retrospective is due.

## Entry Criteria

- Operational metrics are being collected and reviewed.
- Team has capacity allocated for improvement work (e.g., 20% of sprint).

## Exit Criteria (Quality Gate)

Retrospective complete. Tech debt cataloged and prioritized. At least 3 actionable improvements identified with owners. Insights documented and fed back to discovery/planning for the next cycle.

## Key Skills

| Skill | Purpose | Effort |
|---|---|---|
| tech-debt-management | Catalog, prioritize, and plan debt remediation | medium |
| migration-strategy | Plan and execute platform/architecture migrations | xlarge |
| deprecation | Retire features, APIs, and services safely | medium |
| retrospective | Capture learnings and improve process | small |

## Typical Duration

- Retrospective: 1-2 hours per sprint
- Tech debt management: ongoing (20% of sprint capacity)
- Migration: weeks to months (project-level)
- Deprecation: weeks to months per item

## Anti-Patterns

- **No retrospective** -- Without reflection, the team repeats the same mistakes.
- **Debt ignored until crisis** -- By then, remediation cost has multiplied.
- **Big bang migration** -- Incremental migration reduces risk dramatically.
- **Deprecation without communication** -- Surprising consumers with removed features destroys trust.
