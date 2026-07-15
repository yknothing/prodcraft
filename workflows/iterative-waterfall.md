---
name: iterative-waterfall
description: Sequential phases with iteration within each phase and formal handoffs
cadence: phase-based, weeks to months
workflow_kind: primary
composes_with: [greenfield, brownfield, hotfix]
entry_skill: pc-intake
required_artifacts: [intake-brief]
best_for: [enterprise, compliance, large-projects, distributed-teams]
phases_included: [all]
contract:
  version: workflow.v2
  overview:
    summary: Complete lifecycle phases in order while allowing draft-review-revise loops inside each phase.
    distinctive: Formal baselines and handoffs provide auditability, while controlled intra-phase iteration avoids treating first drafts as final.
  entry_gate:
    summary: Begin only after pc-intake approves phase-gated governance and records its assumptions and constraints.
    artifact: intake-brief
    approval_required: true
    fast_track_rule: Intake may shorten phase depth, but every active phase still requires a reviewable handoff and approved exit.
  phase_sequence:
    - id: 00-discovery
      name: Discovery
      purpose: Iteratively define the problem, stakeholders, constraints, and preliminary risks.
      skills: [pc-user-research, pc-market-analysis, pc-feasibility-study]
      inputs: [business case, strategic direction, market data]
      outputs: [discovery report, stakeholder register, problem definition, constraints list, preliminary risk assessment]
      duration: 2-4 weeks
    - id: 01-specification
      name: Specification
      purpose: Refine discovery into detailed, verifiable requirements and a traceable baseline.
      skills: [pc-requirements-engineering, pc-spec-writing, pc-domain-modeling, pc-acceptance-criteria]
      inputs: [discovery summary, stakeholder register, constraints list]
      outputs: [PRD, traceability matrix, acceptance criteria, prioritized feature list]
      duration: 3-6 weeks
    - id: 02-architecture
      name: Architecture
      purpose: Iterate the design until it satisfies the baselined requirements and material risks.
      skills: [pc-system-design, pc-api-design, pc-data-modeling, pc-security-design, pc-tech-selection]
      inputs: [baselined PRD, non-functional requirements, existing-system constraints]
      outputs: [technical design, ADRs, component diagrams, API specification, data model, infrastructure design]
      duration: 2-4 weeks
    - id: 03-planning
      name: Planning
      purpose: Break the design into traceable work units with an achievable schedule and risk treatment.
      skills: [pc-task-breakdown, pc-risk-assessment, pc-estimation]
      inputs: [architecture package, team capacity, dependency schedule]
      outputs: [work breakdown, milestones, resource allocation, dependency map, risk mitigation plan]
      duration: 1-3 weeks
    - id: 04-implementation
      name: Implementation
      purpose: Build to the approved design, integrate continuously, and record deviations for review.
      skills: [pc-tdd, pc-feature-development, pc-refactoring, pc-code-review, pc-documentation, pc-ci-cd]
      inputs: [implementation plan, architecture package, coding standards]
      outputs: [working software, tests, code documentation, progress reports, deviation log]
      duration: 4-12 weeks
    - id: 05-quality
      name: Quality
      purpose: Verify behavior, security, and performance against the baselined specification.
      skills: [pc-testing-strategy, pc-code-review, pc-security-audit, pc-documentation]
      inputs: [working software, specification, acceptance criteria, test plan]
      outputs: [test report, defect log, performance evidence, security assessment, release recommendation]
      duration: 2-4 weeks
    - id: 06-delivery
      name: Delivery
      purpose: Deploy with controlled risk, tested rollback, and a verifiable production handoff.
      skills: [pc-ci-cd, pc-release-management, pc-deployment-strategy, pc-documentation]
      inputs: [release-ready software, deployment plan, rollback plan, communication plan]
      outputs: [production deployment, release notes, deployment verification report]
      duration: 1-2 weeks
    - id: 07-operations
      name: Operations
      purpose: Maintain service health and feed incidents and operational evidence back into the lifecycle.
      skills: [pc-incident-response, pc-documentation]
      inputs: [production system, monitoring configuration, runbooks, SLAs]
      outputs: [operational dashboards, incident reports, postmortems, maintenance log]
      duration: ongoing
    - id: 08-evolution
      name: Evolution
      purpose: Review system outcomes and authorize improvements or a new phase cycle.
      skills: [pc-retrospective, pc-tech-debt-management, pc-market-analysis]
      inputs: [operational data, user feedback, market changes, tech-debt inventory]
      outputs: [evolution plan, updated roadmap, process improvements]
      duration: quarterly
  quality_gates:
    - name: Discovery review
      after: 00-discovery
      criteria: [problem defined, stakeholders consulted, constraints documented, risks catalogued, handoff packaged]
      approvers: [product manager, project sponsor]
      enforcement: blocking
    - name: Specification baseline
      after: 01-specification
      criteria: [requirements identified and traceable, acceptance criteria complete, stakeholder sign-off recorded, feasibility confirmed]
      approvers: [product manager, architect, QA engineer, project sponsor]
      enforcement: blocking
    - name: Architecture review
      after: 02-architecture
      criteria: [design covers requirements, ADRs and threat model complete, performance and infrastructure plans reviewed]
      approvers: [architect, tech lead, security lead, operations lead]
      enforcement: blocking
    - name: Code complete
      after: 04-implementation
      criteria: [planned work implemented, review complete, test target met, integrations passing, deviations resolved]
      approvers: [tech lead, reviewer]
      enforcement: blocking
    - name: Release readiness
      after: 05-quality
      criteria: [acceptance criteria verified, defect level accepted, performance target met, security findings resolved or accepted]
      approvers: [QA engineer, product manager, security lead, operations lead]
      enforcement: blocking
---

# Iterative Waterfall Workflow

## Adaptation Notes

- Change requests cross phase boundaries only after impact analysis and approval; revise every downstream baseline they affect.
- Small projects shorten phase durations and combine roles while retaining named artifacts and gates.
- Large programs may run workstreams independently, with explicit integration milestones.
- Regulated and distributed teams should increase traceability, review windows, and decision recording rather than adding narrative duplication.
