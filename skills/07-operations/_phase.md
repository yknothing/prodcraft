# Phase 07: Operations

## Purpose

Keep the product running reliably for users. Operations encompasses monitoring, incident response, capacity management, and the day-to-day work of maintaining a production system. The goal is to meet defined service level objectives (SLOs) consistently.

## When to Enter

- Code is deployed to production and verified.
- Monitoring and alerting are configured.
- On-call rotation is staffed.
- A live incident, repeated alert, or production degradation requires coordinated containment.

## Entry Criteria

- Production deployment is complete and smoke-tested.
- Monitoring dashboards are live with baseline metrics.
- Alerting rules are configured for SLO-derived thresholds.
- On-call runbooks exist for known failure modes.
- Escalation paths are documented and tested.
- Current release boundary and rollback options are clear enough to support containment decisions.

## Exit Criteria (Quality Gate)

SLOs are met over the defined measurement window (typically 30 days). Incident count and severity trend downward. Operational toil is measured and within acceptable bounds. The system is stable enough to shift focus to evolution.

## Key Skills

| Skill | Purpose | Effort |
|---|---|---|
| monitoring-observability | Instrument systems for visibility into health and behavior | large |
| incident-response | Detect, triage, and resolve production incidents | medium |
| runbooks | Document procedures for common operational tasks | medium |
| capacity-planning | Ensure resources match current and projected demand | medium |

## Typical Duration

Operations is continuous. The phase is "active" from first deployment until the product is decommissioned. Intensity peaks at launch and after major releases.

## Skill Sequence

```
monitoring-observability ──> incident-response
         │
         └──> runbooks
         │
         └──> capacity-planning
```

Monitoring is foundational. Incident response depends on monitoring signals. Runbooks codify operational knowledge. Capacity planning uses monitoring data to project needs.

In brownfield systems, incident response should preserve coexistence and fail-closed containment before any broader redesign work begins.
Monitoring should expose the actual release boundaries that matter, and runbooks should turn incident learning into steps another responder can execute safely.

If operations discovers an architectural or planning mismatch, produce a `course-correction-note` and jump directly to `02-architecture` or `03-planning`.

## Anti-Patterns

- **Monitor everything, alert on nothing meaningful.** Thousands of metrics but no actionable alerts. Derive alerts from SLOs, not from raw metrics.
- **Hero-driven operations.** One person who knows how everything works and is always on call. Document knowledge, rotate on-call, and invest in runbooks.
- **Reactive only.** Waiting for incidents instead of proactively identifying degradation. Use SLO burn-rate alerts to catch problems before users notice.
- **Toil acceptance.** Treating repetitive manual work as "just how operations works." Measure toil and automate systematically.
- **Post-incident blame.** Focusing on who caused an incident rather than what system conditions allowed it. Practice blameless post-mortems.

## Cross-Cutting Matrix

See `rules/cross-cutting-matrix.yml` for `must_consider`, `must_produce`, `skip_when_fast_track`, and `conditional` cross-cutting obligations at this phase.
