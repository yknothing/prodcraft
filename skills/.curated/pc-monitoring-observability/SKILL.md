---
name: pc-monitoring-observability
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
  - pc-ci-cd
  quality_gate: User-impactful signals, release-boundary indicators, and rollback-health checks are instrumented with actionable alerts and dashboards
  roles:
  - devops-engineer
  - developer
  - tech-lead
  methodologies:
  - all
  effort: large
  internal: false
  distribution_surface: curated
  source_path: skills/07-operations/pc-monitoring-observability/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Monitoring and Observability

> If the system can fail in a way users notice, you should be able to see it before they tell you.

## Context

Monitoring and observability translate system behavior into signals responders can trust.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

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

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] User-facing and boundary-critical flows are explicitly instrumented
- [ ] Alerts are actionable and mapped to an owner or runbook
- [ ] Release markers and rollback or fallback health are visible
- [ ] Async seams or coexistence boundaries are observable where applicable
- [ ] Responder dashboard supports triage without requiring ad hoc queries first

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/07-operations/pc-monitoring-observability/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
