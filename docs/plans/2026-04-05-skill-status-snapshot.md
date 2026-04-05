# Skill Status Snapshot

> Date: 2026-04-05

## Current Counts

- total skills: `44`
- `tested`: `31`
- `review`: `13`
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

## Tested Skills

### 00-discovery

- `intake`
- `problem-framing`
- `user-research`

### 01-specification

- `requirements-engineering`
- `acceptance-criteria`

### 02-architecture

- `tech-selection`
- `api-design`

### 03-planning

- `task-breakdown`
- `estimation`
- `risk-assessment`
- `sprint-planning`

### 04-implementation

- `tdd`
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
- `runbooks`

### 08-evolution

- `tech-debt-management`
- `retrospective`

### cross-cutting

- `documentation`
- `verification-before-completion`

## Review Skills

| Phase | Skill | QA Tier | Current review posture | Required to reach `tested` |
|---|---|---|---|---|
| `00-discovery` | `market-analysis` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |
| `00-discovery` | `feasibility-study` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |
| `01-specification` | `spec-writing` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |
| `01-specification` | `domain-modeling` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |
| `02-architecture` | `system-design` | `critical` | benchmark plan and findings already exist | one clean `benchmark_results_path`; keep `findings_path` current; preserve a valid routed integration artifact |
| `02-architecture` | `data-modeling` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |
| `02-architecture` | `security-design` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |
| `07-operations` | `monitoring-observability` | `critical` | benchmark plan and findings already exist | add `benchmark_results_path`; preserve routed `integration_test_path`; keep `findings_path` current |
| `cross-cutting` | `observability` | `critical` | benchmark plan and findings already exist | add `benchmark_results_path`; add routed `integration_test_path`; keep `findings_path` current |
| `cross-cutting` | `bug-history-retrieval` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |
| `cross-cutting` | `accessibility` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |
| `cross-cutting` | `internationalization` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |
| `cross-cutting` | `compliance` | `standard` | eval strategy seeded | one routed benchmark result plus one downstream handoff or integration review |

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
