---
name: iterative-waterfall
description: "Phase-gated development with iteration allowed within each phase"
cadence: "phase-based, 2-6 weeks per phase"
workflow_kind: "primary"
composes_with: ["greenfield", "brownfield", "hotfix"]
entry_skill: "intake"
required_artifacts: ["intake-brief"]
best_for: ["enterprise", "compliance-heavy", "large-scope", "distributed-teams"]
phases_included: ["all"]
---

# Iterative Waterfall Workflow

## Overview

The iterative waterfall workflow preserves the structure and predictability of phased development while allowing iteration within each phase. Each phase completes before the next begins, producing documented deliverables that serve as formal inputs to subsequent phases.

This workflow suits organizations that need the auditability and clear handoffs of waterfall development but recognize that first drafts are never perfect. Within each phase, the team drafts, reviews, revises, and finalizes -- iterating until the phase deliverables meet quality standards. Between phases, formal reviews ensure alignment before work proceeds.

Choose this workflow for enterprise projects with well-understood requirements, compliance obligations that demand phase documentation, large scope that benefits from structured decomposition, or distributed teams that need explicit handoff points.

This workflow may be paired with overlays such as `greenfield`, `brownfield`, or `hotfix` when system state or urgency changes the route but phase-gated governance remains primary.

## Entry Gate

This workflow starts only after `intake` is completed and approved. The required artifact is the `intake-brief`, which captures why a phase-gated workflow is appropriate and what assumptions or constraints must be carried into the first phase.

## Phase Sequence

### Phase 0: Discovery (2-4 weeks)

**Purpose:** Define the problem space, stakeholders, and constraints.

**Skills:** Apply `user-research`, `market-analysis`, and `feasibility-study`.

**Iteration within phase:** Conduct initial research, synthesize findings, review with stakeholders, refine understanding. Expect 2-3 iteration cycles.

**Inputs:** Business case, strategic direction, market data.
**Outputs:** Discovery report, stakeholder register, problem definition, initial constraints list, preliminary risk assessment.

**Handoff document:** Discovery Summary -- a concise package that the specification team can pick up independently.

### Gate: Discovery Review

- **Criteria:** Problem clearly defined. Stakeholders identified and consulted. Constraints documented. Risks catalogued.
- **Approvers:** Product manager, project sponsor.
- **Type:** BLOCKING.

### Phase 1: Specification (3-6 weeks)

**Purpose:** Translate discovery into detailed, verifiable requirements.

**Skills:** Apply `requirements-engineering`, `spec-writing`, `domain-modeling`, and `acceptance-criteria`.

**Iteration within phase:** Draft requirements, review with stakeholders and architects for feasibility, revise for clarity and completeness. Each requirement goes through at least one review cycle.

**Inputs:** Discovery summary, stakeholder register, constraints list.
**Outputs:** Product Requirements Document (PRD), requirements traceability matrix, acceptance criteria, prioritized feature list.

Requirements are versioned. Each revision is tracked with change rationale. The traceability matrix links every requirement to its origin in discovery and forward to architecture and test cases.

### Gate: Specification Baseline

- **Criteria:** All requirements uniquely identified. Acceptance criteria complete. Traceability matrix links to discovery. Stakeholder sign-off. Feasibility confirmed by architect.
- **Approvers:** Product manager, architect, QA engineer, project sponsor.
- **Type:** BLOCKING.

### Phase 2: Architecture (2-4 weeks)

**Purpose:** Design a system that fulfills all specified requirements.

**Skills:** Apply `system-design`, `api-design`, `data-modeling`, `security-design`, and `tech-selection`.

**Iteration within phase:** Propose architecture, review against requirements and quality attributes, revise. Prototype high-risk components if needed. Expect 2-3 design iterations.

**Inputs:** Baselined PRD, non-functional requirements, existing system constraints.
**Outputs:** Technical Design Document (TDD), Architecture Decision Records (ADRs), component diagrams, API specifications, data model, infrastructure design.

**Handoff document:** Architecture Package -- everything the implementation team needs to build without ambiguity.

### Gate: Architecture Review

- **Criteria:** TDD addresses all requirements. ADRs documented for every significant decision. Security threat model complete. Performance strategy defined. Infrastructure estimated and budgeted.
- **Approvers:** Architect, tech lead, security lead, operations lead.
- **Type:** BLOCKING.

### Phase 3: Planning (1-3 weeks)

**Purpose:** Break the architecture into implementable work units and schedule delivery.

**Skills:** Apply `task-breakdown`, `risk-assessment`, and `estimation`.

**Iteration within phase:** Create initial work breakdown, validate estimates with implementers, adjust sequencing based on dependencies and risk, finalize.

**Inputs:** Architecture package, team capacity, external dependency schedule.
**Outputs:** Work breakdown structure (WBS), project schedule with milestones, resource allocation, risk mitigation plan, dependency map.

**Handoff document:** Implementation Plan -- task assignments, schedule, and success criteria.

### Gate: Plan Approval

- **Criteria:** All requirements traced to tasks. Schedule realistic given capacity. Critical path identified. Risks mitigated or accepted.
- **Approvers:** Tech lead, product manager, project sponsor.
- **Type:** BLOCKING.

### Phase 4: Implementation (4-12 weeks)

**Purpose:** Build the software according to the architecture and plan.

**Skills:** Apply `tdd`, `feature-development`, `refactoring`, `code-review`, `documentation`, and `ci-cd`.

**Iteration within phase:** Implement in increments aligned to the WBS. Each increment includes coding, unit testing, code review, and integration. Weekly progress reviews allow course correction.

**Inputs:** Implementation plan, architecture package, coding standards.
**Outputs:** Working software, unit and integration tests, code documentation, weekly progress reports, deviation log.

Deviations from the architecture or specification are logged and escalated through the change request process. The implementation team does not make unilateral design changes.

### Gate: Code Complete

- **Criteria:** All planned work items implemented. Code reviewed. Unit test coverage meets target. Integration tests passing. Deviation log resolved.
- **Approvers:** Tech lead, reviewer.
- **Type:** BLOCKING.

### Phase 5: Quality (2-4 weeks)

**Purpose:** Verify the implementation against the specification.

**Skills:** Apply `testing-strategy`, `code-review`, `security-audit`, and `documentation`.

**Iteration within phase:** Execute test plan, report defects, fix defects, re-test. Iterate until exit criteria met.

**Inputs:** Working software, specification, acceptance criteria, test plan.
**Outputs:** Test results report, defect log, performance benchmarks, security assessment, release recommendation.

### Gate: Release Readiness

- **Criteria:** All acceptance criteria verified. Defect backlog at acceptable level (no critical, limited high). Performance benchmarks met. Security assessment clean.
- **Approvers:** QA engineer, product manager, security lead, operations lead.
- **Type:** BLOCKING.

### Phase 6: Delivery (1-2 weeks)

**Purpose:** Deploy to production with controlled risk.

**Skills:** Apply `ci-cd`, `release-management`, `deployment-strategy`, and `documentation`.

**Inputs:** Release-ready software, deployment plan, rollback plan, communication plan.
**Outputs:** Production deployment, release notes, deployment verification report.

Deployment follows a rehearsed plan. Rollback is tested before go-live. Stakeholders are notified per the communication plan.

### Phase 7: Operations (Ongoing)

**Purpose:** Maintain system health and respond to incidents.

**Skills:** Apply `incident-response` and `documentation`.

**Inputs:** Production system, monitoring configuration, runbooks, SLAs.
**Outputs:** Operational dashboards, incident reports, postmortems, maintenance log.

### Phase 8: Evolution (Quarterly)

**Purpose:** Assess system health and plan improvements.

**Skills:** Apply `retrospective`, `tech-debt-management`, and `market-analysis`.

**Inputs:** Operational data, user feedback, market changes, tech debt inventory.
**Outputs:** Evolution plan, updated roadmap, process improvements.

## Quality Gates

Phase gates are BLOCKING. Each gate must be cleared before the next phase begins. Gates operate as formal review events — deliverables are presented, criteria checked, and approval recorded.

### Discovery Review

- **Criteria:** Problem clearly defined. Stakeholders identified and consulted. Constraints documented. Risks catalogued. Discovery Summary packaged for handoff.
- **Approvers:** Product manager, project sponsor.
- **Type:** BLOCKING.

### Specification Review

- **Criteria:** Requirements detailed and verified against discovery. Domain model reviewed. Acceptance criteria testable. Iteration cycles within specification complete.
- **Approvers:** Product manager, architect, QA lead.
- **Type:** BLOCKING.

### Architecture Review

- **Criteria:** Architecture validated against requirements. Risk register updated. Non-functional requirements addressed. Implementation plan approved.
- **Approvers:** Architect, tech lead, product manager, project sponsor.
- **Type:** BLOCKING.

### Code Complete

- **Criteria:** All planned work items implemented. Code reviewed. Unit test coverage meets target. Integration tests passing. Deviation log resolved.
- **Approvers:** Tech lead, reviewer.
- **Type:** BLOCKING.

### Release Readiness

- **Criteria:** All acceptance criteria verified. Defect backlog at acceptable level (no critical, limited high). Performance benchmarks met. Security assessment clean or findings accepted.
- **Approvers:** QA engineer, product manager, security lead, operations lead.
- **Type:** BLOCKING.

## Cross-Phase Feedback: Change Requests

When a later phase discovers an issue with an earlier phase's deliverable, the formal process is:

1. **Identify** the issue and its impact on the current phase.
2. **Submit** a change request documenting the issue, proposed change, and impact assessment.
3. **Review** by the affected phase's approvers plus the current phase lead.
4. **Approve or reject** with documented rationale.
5. **Update** all affected deliverables (spec, architecture, plan, traceability matrix).
6. **Communicate** the change to all downstream teams.

This process adds overhead but ensures that changes are deliberate, tracked, and communicated.

## Adaptation Notes

- **Small teams (3-5):** Phase gates become team meetings rather than formal boards. Documentation is lighter but still versioned.
- **Distributed teams:** Each phase handoff includes a recorded walkthrough. Gate reviews are conducted via video with written decisions.
- **Compliance-heavy:** Map each gate to specific compliance requirements. Maintain an audit trail. Include compliance reviewers at every gate.
- **Large scope:** Break into workstreams that each follow this workflow independently, with integration points at defined milestones.
- **Accelerated timeline:** Compress phase durations but do not skip phases. Reduce iteration cycles within phases to 1-2 rather than 2-3.
