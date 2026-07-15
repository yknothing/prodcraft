---
name: brownfield
description: Incremental change to an existing system with characterization and migration safety
cadence: incremental, weeks to months
workflow_kind: overlay
composes_with: ["*"]
entry_skill: pc-intake
required_artifacts: [intake-brief]
best_for: [legacy-modernization, migrations, existing-products, technical-debt]
phases_included: [all]
contract:
  version: workflow.v2
  overview:
    summary: Change an existing system through evidence-backed seams, characterization tests, reversible increments, and parallel operation where needed.
    distinctive: Brownfield treats undocumented behavior and coexistence constraints as part of the product contract; it modifies risk handling without replacing primary governance.
  entry_gate:
    summary: Begin only after pc-intake confirms access, ownership, desired outcomes, coexistence boundaries, and the approved primary workflow.
    artifact: intake-brief
    approval_required: true
    fast_track_rule: Intake may narrow archaeology to the changed seam, but may not waive characterization of critical behavior or rollback planning.
  phase_sequence:
    - id: 00-discovery
      name: System archaeology
      purpose: Establish the real implementation, dependency, data, operational, and ownership surfaces before proposing change.
      skills: [pc-documentation, pc-user-research, pc-feasibility-study]
      inputs: [system access, source and infrastructure, logs, operators, users]
      outputs: [as-is system map, pain-point inventory, coverage assessment, dependency and risk inventory]
      duration: 2-4 weeks or a bounded seam study
    - id: 01-specification
      name: Baseline current behavior
      purpose: Turn observed behavior into characterization tests and explicit preservation or change decisions.
      skills: [pc-spec-writing, pc-acceptance-criteria, pc-documentation, pc-tdd]
      inputs: [system map, production evidence, source behavior, user workflows]
      outputs: [characterization tests, current-behavior specification, target state, modernization scope]
      duration: 2-4 weeks or per increment
    - id: 02-architecture
      name: Define migration seams
      purpose: Design an incremental target path, coexistence boundaries, data migration, and rollback strategy.
      skills: [pc-system-design, pc-api-design, pc-data-modeling, pc-security-design, pc-tech-selection]
      inputs: [as-is map, behavioral baseline, target state, constraints]
      outputs: [migration architecture, seam map, facade contracts, data strategy, ADRs]
      duration: 2-4 weeks or per major seam
    - id: 03-planning
      name: Order safe increments
      purpose: Sequence changes so each increment is independently valuable, observable, and reversible.
      skills: [pc-task-breakdown, pc-risk-assessment, pc-estimation]
      inputs: [migration architecture, pain points, capacity, dependency constraints]
      outputs: [increment backlog, per-increment plan, success metrics, rollback conditions]
      duration: 1-2 weeks per increment
    - id: 04-implementation
      name: Characterize then change
      purpose: Add missing tests first, change one seam, preserve compatibility, and record deviations.
      skills: [pc-tdd, pc-feature-development, pc-refactoring, pc-code-review, pc-documentation, pc-ci-cd]
      inputs: [increment plan, characterization tests, migration contract]
      outputs: [modernized slice, updated tests, compatibility evidence, migration metrics]
      duration: ongoing increments
    - id: 05-quality
      name: Prove no regression
      purpose: Compare new and old behavior, performance, integrations, security, and data outcomes.
      skills: [pc-testing-strategy, pc-code-review, pc-security-audit, pc-documentation]
      inputs: [modernized slice, characterization suite, historical benchmarks]
      outputs: [regression report, performance comparison, integration and data validation]
      duration: per increment
    - id: 06-delivery
      name: Parallel rollout
      purpose: Introduce the new path behind controlled routing and retain a tested fallback until evidence supports cutover.
      skills: [pc-ci-cd, pc-release-management, pc-deployment-strategy, pc-documentation]
      inputs: [verified slice, deployment pipeline, rollback and traffic plan]
      outputs: [controlled deployment, routing configuration, rollout evidence, rollback readiness]
      duration: per increment
    - id: 07-operations
      name: Observe coexistence
      purpose: Compare old and new systems, detect divergence, and keep incident ownership explicit during transition.
      skills: [pc-incident-response, pc-documentation]
      inputs: [coexisting systems, monitoring, operational thresholds]
      outputs: [comparative dashboards, incident records, cutover evidence]
      duration: through rollback window and coexistence
    - id: 08-evolution
      name: Review migration
      purpose: Measure risk reduction and delivered value, retire obsolete paths only with evidence, and re-plan remaining seams.
      skills: [pc-retrospective, pc-tech-debt-management, pc-market-analysis]
      inputs: [migration metrics, operational evidence, team and user feedback]
      outputs: [updated roadmap, decommission decisions, next increments, learning record]
      duration: quarterly and after major cutovers
  quality_gates:
    - name: Baseline established
      after: 01-specification
      criteria: [critical paths characterized, current behavior documented, target state and preservation boundaries approved]
      approvers: [tech lead, product manager, architect]
      enforcement: blocking
    - name: Pre-migration
      after: increment planning
      criteria: [changed area characterized, rollback documented and tested where feasible, success and abort thresholds explicit]
      approvers: [tech lead, architect]
      enforcement: blocking
    - name: Post-migration
      after: coexistence window
      criteria: [no unacceptable regression, performance and data accepted, rollback window complete, decommission evidence reviewed]
      approvers: [tech lead, QA engineer, operations lead]
      enforcement: blocking
  overlay_delta:
    applies_to: [agile-sprint, spec-driven, iterative-waterfall]
    changes:
      - dimension: discovery
        effect: Replace blank-slate assumptions with implementation-derived archaeology, behavioral evidence, and ownership mapping at the affected seam.
      - dimension: implementation
        effect: Require characterization before change and preserve coexistence boundaries through small reversible increments.
      - dimension: delivery
        effect: Prefer parallel run, controlled traffic, comparative telemetry, and evidence-backed decommissioning over one-step replacement.
---

# Brownfield Workflow

## Adaptation Notes

- Poorly tested systems spend more time on characterization before the first change.
- Monoliths require careful seam selection; distributed systems require stronger dependency and contract mapping.
- Data migrations need reconciliation, idempotency, backup, and rollback evidence in every affected increment.
- Regulated systems retain audit trails for baseline, approval, rollout, and decommission decisions.
