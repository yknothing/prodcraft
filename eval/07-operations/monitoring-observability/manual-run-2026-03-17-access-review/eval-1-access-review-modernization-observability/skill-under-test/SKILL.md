---
name: monitoring-observability
description: Use when a live service or newly delivered release needs actionable telemetry, dashboards, and alerts that expose real user-impactful boundaries, especially when brownfield coexistence rules, unsupported-flow safety, rollback health, or queue/backfill behavior must be visible before incidents escalate.
metadata:
  phase: 07-operations
  inputs:
    - architecture-doc
    - ci-cd-pipeline
    - api-contract
  outputs:
    - monitoring-config
    - alert-rules
    - service-dashboard
  prerequisites:
    - ci-cd
  quality_gate: User-impactful signals, release-boundary indicators, and rollback-health checks are instrumented with actionable alerts and dashboards
  roles:
    - devops-engineer
    - developer
    - tech-lead
  methodologies:
    - all
  effort: large
---

# Snapshot

Manual review snapshot of the skill under test.
