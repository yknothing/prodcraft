# Skill Status Snapshot

> Original snapshot date: 2026-04-05
> Current manifest refresh: 2026-04-25

## Current Manifest Snapshot

- total skills: `44`
- `production`: `6`
- `tested`: `32`
- `review`: `6`
- `draft`: `0`

## Tested Gate Contract

Prodcraft currently uses `routed` evaluation for all non-draft skills.

- `review -> tested` for `standard` routed skills:
  - `qa.benchmark_results_path`
  - `qa.integration_test_path`
- `review -> tested` for `critical` routed skills:
  - `qa.benchmark_results_path`
  - `qa.integration_test_path`
  - `qa.findings_path`

Review-stage evidence is intentionally smaller:

- every `review` skill must declare:
  - `qa.structure_validation_path`
  - `qa.eval_strategy_path`
- `critical` review skills must also keep:
  - `qa.findings_path`
  - at least one substantive review artifact such as `benchmark_plan_path`

## Production Skills

### 00-discovery

- `intake`
- `problem-framing`

### 01-specification

- `requirements-engineering`

### 03-planning

- `task-breakdown`

### 04-implementation

- `tdd`

### cross-cutting

- `verification-before-completion`

## Tested Skills

### 00-discovery

- `user-research`

### 01-specification

- `spec-writing`
- `domain-modeling`
- `acceptance-criteria`

### 02-architecture

- `data-modeling`
- `security-design`
- `tech-selection`
- `api-design`

### 03-planning

- `estimation`
- `risk-assessment`
- `sprint-planning`

### 04-implementation

- `systematic-debugging`
- `task-execution`
- `feature-development`
- `refactoring`

### 05-quality

- `code-review`
- `receiving-code-review`
- `testing-strategy`
- `e2e-scenario-design`
- `security-audit`

### 06-delivery

- `ci-cd`
- `delivery-completion`
- `deployment-strategy`
- `release-management`

### 07-operations

- `incident-response`
- `monitoring-observability`
- `runbooks`

### 08-evolution

- `tech-debt-management`
- `retrospective`

### cross-cutting

- `accessibility`
- `documentation`
- `observability`

## Review Skills

| Phase | Skill | QA Tier | Current review posture | Required to reach `tested` |
|---|---|---|---|---|
| `00-discovery` | `market-analysis` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |
| `00-discovery` | `feasibility-study` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |
| `02-architecture` | `system-design` | `critical` | benchmark plan and findings already exist | one clean `benchmark_results_path`; keep `findings_path` current; preserve a valid routed integration artifact |
| `cross-cutting` | `bug-history-retrieval` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |
| `cross-cutting` | `internationalization` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |
| `cross-cutting` | `compliance` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |

## Current Refresh Notes

The current manifest has a smaller `review` pool than the 2026-04-05 follow-up board. `spec-writing`, `domain-modeling`, `data-modeling`, and `security-design` are no longer pending review-stage skills in `manifest.yml`; they are now `tested`.

The current manifest also separates `production` from `tested`. The dated 2026-04-05 follow-up notes below remain historical wave records and should not be read as the live review queue.

## What Changed In This Wave

This wave moved `12` skills from `draft` to `review` by adding review-stage QA wiring and checked-in evaluation strategies:

- `market-analysis`
- `feasibility-study`
- `spec-writing`
- `domain-modeling`
- `acceptance-criteria`
- `data-modeling`
- `security-design`
- `estimation`
- `bug-history-retrieval`
- `accessibility`
- `internationalization`
- `compliance`

## Follow-Up Update

On the same date, `security-audit` moved from `review` to `tested` by converting an existing isolated benchmark lane into a checked-in benchmark review and adding its first routed handoff review into `release-management`.

Later the same day, `estimation` moved from `review` to `tested` after landing its first clean isolated benchmark review and reusing the existing `sprint-planning` handoff review as the downstream integration artifact.

Later the same day, `acceptance-criteria` moved from `review` to `tested` after landing its first clean isolated benchmark review and reusing the existing `testing-strategy` handoff review as the downstream integration artifact.

Later the same day, `observability` moved from `review` to `tested` after converting completed and failed execution traces into a checked-in benchmark review and reusing the existing runtime contract review as the integration artifact.

On 2026-04-06, `accessibility` moved from `review` to `tested` after its first clean isolated benchmark review landed and the downstream `acceptance-criteria` handoff review was checked in as the integration artifact.

On 2026-04-08, `monitoring-observability` moved from `review` to `tested` after a manual branch-pair benchmark review was checked in and the existing routed `observability-review.md` remained the downstream integration artifact.
