---
name: spec-driven
description: Rigorous sequential development with formal specifications and blocking gates
cadence: sequential phases, weeks to months
workflow_kind: primary
composes_with: [greenfield, brownfield, hotfix]
entry_skill: pc-intake
required_artifacts: [intake-brief]
best_for: [regulated, safety-critical, large-teams, contractual]
phases_included: [all]
contract:
  version: workflow.v2
  overview:
    summary: Execute lifecycle phases sequentially and require reviewed, traceable artifacts before downstream work begins.
    distinctive: Specification and formal approval carry more weight than delivery speed because the cost of ambiguity or non-compliance is high.
  entry_gate:
    summary: Begin only after pc-intake selects and the user approves the higher-rigor spec-driven route.
    artifact: intake-brief
    approval_required: true
    fast_track_rule: Phase compression requires an amended intake approval and may not waive mandatory regulatory or contractual evidence.
  phase_sequence:
    - id: 00-discovery
      name: Discovery
      purpose: Establish the problem, stakeholders, constraints, regulatory context, and initial risks.
      skills: [pc-user-research, pc-market-analysis, pc-feasibility-study]
      inputs: [business case, market data, regulatory requirements, stakeholder access]
      outputs: [discovery report, stakeholder map, problem statement, initial risk register]
      duration: until stakeholder discovery is complete
    - id: 01-specification
      name: Specification
      purpose: Produce complete, uniquely identified, testable requirements with explicit non-functional constraints.
      skills: [pc-requirements-engineering, pc-spec-writing, pc-domain-modeling, pc-acceptance-criteria]
      inputs: [approved discovery report, stakeholder map, regulatory constraints]
      outputs: [PRD, functional specification, non-functional requirements, acceptance criteria, traceability matrix]
      duration: until specification review closes all blocking questions
    - id: 02-architecture
      name: Architecture
      purpose: Design a system that maps every material requirement to a reviewed technical decision.
      skills: [pc-system-design, pc-api-design, pc-data-modeling, pc-security-design, pc-tech-selection]
      inputs: [approved specification, non-functional requirements, existing-system constraints]
      outputs: [technical design, ADRs, API specifications, data model, infrastructure plan, threat model]
      duration: until architecture review approval
    - id: 03-planning
      name: Planning
      purpose: Map approved requirements and architecture to owned tasks, dependencies, schedule, and risk treatment.
      skills: [pc-task-breakdown, pc-risk-assessment, pc-estimation]
      inputs: [technical design, ADRs, team capacity, external dependencies]
      outputs: [work breakdown, schedule, resource allocation, dependency map, risk mitigation plan]
      duration: until plan approval
    - id: 04-implementation
      name: Implementation
      purpose: Build exactly the approved specification and record all deviations through change control.
      skills: [pc-tdd, pc-feature-development, pc-refactoring, pc-code-review, pc-documentation]
      inputs: [approved plan, technical design, coding standards, test strategy]
      outputs: [working software, unit and integration tests, code documentation, deviation log]
      duration: according to approved project plan
    - id: 05-quality
      name: Quality
      purpose: Verify the implementation against requirements, acceptance criteria, security, and performance commitments.
      skills: [pc-testing-strategy, pc-code-review, pc-security-audit, pc-documentation]
      inputs: [working software, approved specification, acceptance criteria, test plan]
      outputs: [test report, defect report, performance evidence, security results, release recommendation]
      duration: until release-readiness criteria pass
    - id: 06-delivery
      name: Delivery
      purpose: Release the approved candidate through a controlled, reversible production deployment.
      skills: [pc-ci-cd, pc-release-management, pc-deployment-strategy, pc-documentation]
      inputs: [release-ready software, deployment plan, rollback plan, communication plan]
      outputs: [production deployment, release notes, stakeholder notification, deployment verification]
      duration: approved release window
    - id: 07-operations
      name: Operations
      purpose: Operate the production system against agreed service and support commitments.
      skills: [pc-incident-response, pc-documentation]
      inputs: [production system, monitoring configuration, runbooks, SLAs]
      outputs: [operational metrics, incident reports, postmortems, maintenance records]
      duration: ongoing
    - id: 08-evolution
      name: Evolution
      purpose: Convert operational evidence and changed needs into a reviewed next lifecycle route.
      skills: [pc-retrospective, pc-tech-debt-management, pc-market-analysis]
      inputs: [operational metrics, user feedback, market changes, tech-debt inventory]
      outputs: [evolution plan, updated roadmap, improvement tickets, process adjustments]
      duration: planned review cadence
  quality_gates:
    - name: Discovery approval
      after: 00-discovery
      criteria: [problem and stakeholders approved, regulatory constraints catalogued, initial risks reviewed]
      approvers: [product manager, project sponsor, compliance officer when applicable]
      enforcement: blocking
    - name: Specification review
      after: 01-specification
      criteria: [requirements uniquely identified, acceptance criteria testable, traceability complete, open questions resolved]
      approvers: [product manager, architect, QA lead, affected stakeholders]
      enforcement: blocking
    - name: Architecture approval
      after: 02-architecture
      criteria: [technical design peer-reviewed, ADRs complete, security and non-functional requirements addressed]
      approvers: [architect, tech lead, security lead]
      enforcement: blocking
    - name: Code complete
      after: 04-implementation
      criteria: [approved scope implemented, reviews complete, test threshold met, no open critical or high defects]
      approvers: [tech lead, QA lead]
      enforcement: blocking
    - name: Release readiness
      after: 05-quality
      criteria: [acceptance criteria verified, performance commitments met, regression suite passing, security findings resolved or formally accepted]
      approvers: [QA engineer, product manager, security lead]
      enforcement: blocking
---

# Spec-Driven Workflow

## Adaptation Notes

- Scope changes after specification approval require impact analysis, updated artifacts, affected re-approval, and a recorded change decision.
- Small teams may combine roles, but must preserve independent evidence and explicit approvals.
- Regulated work adds domain-specific traceability and retention without weakening the common gates.
- Distributed teams should use asynchronous reviews with recorded decisions and clear response deadlines.
