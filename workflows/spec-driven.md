---
name: spec-driven
description: "Full specification upfront, phased delivery with formal quality gates"
cadence: "milestone-based"
entry_skill: "intake"
required_artifacts: ["intake-brief"]
best_for: ["regulated-industries", "safety-critical", "contractual", "large-teams"]
phases_included: ["all"]
---

# Spec-Driven Workflow

## Overview

The spec-driven workflow is the most rigorous approach in the Prodcraft system. Every phase executes sequentially with formal quality gates that block progression until criteria are met. Nothing is built until it is fully specified, reviewed, and approved.

This workflow is designed for contexts where the cost of getting it wrong is high: regulated industries, safety-critical systems, contractual obligations, and large teams where alignment is expensive to achieve after the fact. The upfront investment in specification and review pays dividends by catching defects early, when they are cheapest to fix.

Choose this workflow when requirements are knowable upfront, when regulatory or contractual compliance demands traceability, or when the team is large enough that informal coordination breaks down.

## Entry Gate

This workflow may begin only after `intake` is completed, approved, and routed to a spec-driven path. The required artifact is the `intake-brief`, which serves as the formal record of why this higher-rigor workflow was selected.

If any earlier gate is skipped, the intake brief must document that decision explicitly as accepted process debt.

## Phase Sequence

### Phase 0: Discovery

**Purpose:** Exhaustive problem analysis and stakeholder alignment.

**Skills:** Apply `user-research`, `market-analysis`, and `feasibility-study`.

**Inputs:** Business case, market data, regulatory requirements, stakeholder access.
**Outputs:** Discovery report, stakeholder map, problem statement, initial risk register.
**Duration:** 1-4 weeks depending on domain complexity.

All stakeholders must be identified and interviewed. The problem space must be documented thoroughly before any solution is proposed. Regulatory constraints are catalogued here and tracked through every subsequent phase.

### Gate: Discovery Approval

- **Criteria:** Problem statement signed off by all stakeholders. Risk register reviewed. Regulatory landscape documented.
- **Approvers:** Product manager, sponsor, compliance officer (if applicable).
- **Type:** BLOCKING -- no specification work begins without this gate.

### Phase 1: Specification

**Purpose:** Complete, unambiguous requirements documentation.

**Skills:** Apply `requirements-engineering`, `spec-writing`, `domain-modeling`, and `acceptance-criteria`.

**Inputs:** Discovery report, stakeholder map, regulatory constraints.
**Outputs:** Product Requirements Document (PRD), functional specification, non-functional requirements, acceptance criteria for every requirement.
**Duration:** 2-6 weeks.

Every requirement gets a unique identifier for traceability. Acceptance criteria are written for every functional requirement. Non-functional requirements (performance, security, accessibility) are quantified with measurable thresholds.

### Gate: Specification Review

- **Criteria:** All requirements have unique IDs. Acceptance criteria exist for every functional requirement. Non-functional requirements are quantified. Stakeholder sign-off obtained. No unresolved open questions.
- **Approvers:** Product manager, architect, QA engineer, legal/compliance (if applicable).
- **Type:** BLOCKING.

### Phase 2: Architecture

**Purpose:** System design that satisfies all specified requirements.

**Skills:** Apply `system-design`, `api-design`, `data-modeling`, `security-design`, and `tech-selection`.

**Inputs:** PRD, functional specification, non-functional requirements, existing system documentation.
**Outputs:** Technical Design Document (TDD), Architecture Decision Records (ADRs), API specifications, data model diagrams, infrastructure plan.
**Duration:** 2-4 weeks.

Every architectural decision is recorded as an ADR with full rationale and alternatives considered. The architecture must demonstrably satisfy every non-functional requirement. Security threat modeling is mandatory.

### Gate: Architecture Review Board

- **Criteria:** TDD complete and peer-reviewed. All ADRs documented. Security threat model complete. Infrastructure cost estimate provided. Architecture maps to all non-functional requirements with justification.
- **Approvers:** Architect, tech lead, security lead, infrastructure lead.
- **Type:** BLOCKING.

### Phase 3: Planning

**Purpose:** Detailed work breakdown, scheduling, and resource allocation.

**Skills:** Apply `task-breakdown`, `risk-assessment`, and `estimation`.

**Inputs:** TDD, ADRs, team capacity, external dependencies.
**Outputs:** Work breakdown structure, project schedule, resource allocation, dependency map, risk mitigation plan.
**Duration:** 1-2 weeks.

Tasks are traced back to requirements. Every task has an estimate, an owner, and identified dependencies. The critical path is identified and monitored. Milestones align with quality gates.

### Gate: Plan Approval

- **Criteria:** All requirements mapped to tasks. Critical path identified. Resources allocated. Risks mitigated or accepted with documented rationale.
- **Approvers:** Tech lead, product manager, project sponsor.
- **Type:** BLOCKING.

### Phase 4: Implementation

**Purpose:** Build the system according to specification and architecture.

**Skills:** Apply `tdd`, `feature-development`, `refactoring`, `code-review`, and `documentation`.

**Inputs:** TDD, task breakdown, coding standards, test strategy.
**Outputs:** Working software, unit tests, integration tests, code documentation, implementation notes.
**Duration:** 4-16 weeks depending on scope.

Code is written against the specification -- deviations require a formal change request. All code is peer-reviewed before merge. Test coverage targets are enforced. Implementation notes document any specification ambiguities encountered.

### Gate: Code Complete

- **Criteria:** All planned features implemented. Code review completed for all changes. Unit test coverage meets threshold. No critical or high-severity defects open. All change requests resolved.
- **Approvers:** Tech lead, reviewer.
- **Type:** BLOCKING.

### Phase 5: Quality

**Purpose:** Comprehensive verification against specification.

**Skills:** Apply `testing-strategy`, `code-review`, `security-audit`, and `documentation`.

**Inputs:** Working software, specification, acceptance criteria, test plan.
**Outputs:** Test results, defect reports, performance benchmarks, security scan results, release readiness assessment.
**Duration:** 2-4 weeks.

Every acceptance criterion is verified. Performance is benchmarked against non-functional requirements. Security scanning is run and findings triaged. Regression testing covers all critical paths. Exploratory testing targets risk areas.

### Gate: Release Readiness

- **Criteria:** All acceptance criteria verified. Performance meets benchmarks. No critical or high-severity defects. Security scan clean or findings accepted. Regression suite passing.
- **Approvers:** QA engineer, product manager, security lead.
- **Type:** BLOCKING.

### Phase 6: Delivery

**Purpose:** Controlled release to production.

**Skills:** Apply `ci-cd`, `release-management`, `deployment-strategy`, and `documentation`.

**Inputs:** Release-ready software, deployment plan, rollback plan, stakeholder communication plan.
**Outputs:** Production deployment, release notes, stakeholder notification, deployment verification.
**Duration:** 1-3 days.

Deployment follows a documented, rehearsed plan. Rollback procedures are tested before go-live. Stakeholders are notified at each stage. Post-deployment verification confirms the release is healthy.

### Phase 7: Operations

**Purpose:** Monitor, maintain, and support the production system.

**Skills:** Apply `incident-response` and `documentation`.

**Inputs:** Production system, monitoring configuration, runbooks, SLAs.
**Outputs:** Operational metrics, incident reports, postmortems, maintenance logs.
**Duration:** Ongoing.

Monitoring covers all SLAs. Incident response follows documented procedures. Every production incident gets a postmortem. Operational findings feed back into the evolution phase.

### Phase 8: Evolution

**Purpose:** Continuous improvement based on operational data and changing needs.

**Skills:** Apply `retrospective`, `tech-debt-management`, and `market-analysis`.

**Inputs:** Operational metrics, user feedback, market changes, tech debt inventory.
**Outputs:** Evolution plan, updated roadmap, improvement tickets, process adjustments.
**Duration:** Periodic reviews (monthly or quarterly).

## Change Control

In this workflow, scope changes after the Specification Review gate require a formal change request:

1. Change request submitted with rationale, impact analysis, and effort estimate.
2. Impact assessment by architect and tech lead.
3. Approval by product manager and project sponsor.
4. Specification, architecture, and plan updated to reflect the change.
5. Traceability maintained -- the change is linked to affected requirements.

## Adaptation Notes

- **Small teams (2-5):** Gates can be lighter (a meeting rather than a formal board) but still must be documented.
- **Solo developer:** Self-review using checklists that cover each gate's criteria. Document decisions even if you are the only audience.
- **Distributed teams:** Asynchronous gate reviews with explicit approval deadlines. Use shared documents with comment threads.
- **Compliance overlay:** Map gate criteria to specific regulatory requirements. Maintain an audit trail of gate approvals.
