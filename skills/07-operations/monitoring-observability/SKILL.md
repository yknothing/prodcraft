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

# Monitoring and Observability

> If the system can fail in a way users notice, you should be able to see it before they tell you.

## Context

Monitoring and observability translate system behavior into signals responders can trust. The goal is not to collect every metric. The goal is to make risky boundaries, user impact, and recovery state visible fast enough to guide action.

In a lifecycle-aware system, observability should preserve release intent. For brownfield work, make sure dashboards and alerts distinguish safe supported behavior from unsupported or coexistence-sensitive paths.

## Inputs

- **architecture-doc** -- produced by the preceding skill in the lifecycle
- **ci-cd-pipeline** -- produced by the preceding skill in the lifecycle
- **api-contract** -- produced by the preceding skill in the lifecycle
## Process

### Step 1: Map User-Critical and Boundary-Critical Signals

Start from the reviewed architecture, API contract, and delivery slice:
- which flows must succeed
- which flows must fail closed
- which queues, bridges, or background workers can amplify failures
- which rollback or coexistence indicators matter after release

Do not start from "what metrics are easy to collect."

### Step 2: Define a Small Set of Actionable Signals

At minimum, cover:
- availability and latency for user-facing routes
- error-rate segmentation for supported vs unsupported paths where that distinction matters
- queue depth, retry rate, or backfill lag for async seams
- release or deploy markers so responders can correlate changes quickly
- rollback or fallback health signals if the current slice depends on them

### Step 3: Build Dashboards That Support Triage

Dashboards should answer:
- what is broken
- who is affected
- whether the system is degrading or recovering
- whether rollback, fail-closed behavior, or fallback mode is working

Prefer a small number of responder dashboards over a wall of charts.

### Step 4: Design Alerts for Actionability

Each alert should have:
- a clear trigger
- user or business impact context
- owner or escalation target
- immediate next step or linked runbook

Alerts that cannot change behavior are noise.

### Step 5: Validate with Release and Incident Scenarios

Before relying on the setup:
- verify alerts fire for the risky boundary you care about
- verify dashboards show release markers and recovery clearly
- verify the signal is strong enough to support incident-response and rollback decisions

## Outputs

- **monitoring-config** -- produced by this skill
- **alert-rules** -- produced by this skill
- **service-dashboard** -- produced by this skill
## Quality Gate

- [ ] User-facing and boundary-critical flows are explicitly instrumented
- [ ] Alerts are actionable and mapped to an owner or runbook
- [ ] Release markers and rollback or fallback health are visible
- [ ] Async seams or coexistence boundaries are observable where applicable
- [ ] Responder dashboard supports triage without requiring ad hoc queries first

## Anti-Patterns

1. **Metric soup** -- Thousands of charts, no operational clarity.
2. **CPU-first monitoring** -- Infra metrics without route or contract visibility.
3. **No release markers** -- Incidents take longer because nobody can correlate behavior to deploys.
4. **Alerts without action** -- Noise trains responders to ignore the system.
5. **No boundary-specific telemetry** -- Supported and unsupported behavior are merged until the incident is already expensive.

## Related Skills

- [ci-cd](../../06-delivery/ci-cd/SKILL.md) -- provides release and rollback context
- [incident-response](../incident-response/SKILL.md) -- consumes observability signals during incidents
- [runbooks](../runbooks/SKILL.md) -- attaches response steps to alerts
- `capacity-planning` (planned) -- uses operational signals for projection
