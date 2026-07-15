---
name: greenfield
description: New-project bootstrap from idea through first production deployment
cadence: one-time, days to weeks
workflow_kind: overlay
composes_with: ["*"]
entry_skill: pc-intake
required_artifacts: [intake-brief]
best_for: [new-products, proof-of-concept, hackathon, side-projects]
phases_included: [all]
contract:
  version: workflow.v2
  overview:
    summary: Bootstrap a new system from validated problem through first production operation while deferring choices that do not yet need commitment.
    distinctive: Greenfield changes the starting assumptions and foundation decisions; it does not replace the selected primary governance workflow.
  entry_gate:
    summary: Begin only after pc-intake classifies the work as greenfield and the user approves its primary workflow, scope, and initial risks.
    artifact: intake-brief
    approval_required: true
    fast_track_rule: Intake may compress depth for a prototype, but must record which production foundations are deferred.
  phase_sequence:
    - id: 00-discovery
      name: Validate problem
      purpose: Identify a real user, current alternatives, switching trigger, and smallest valuable scope.
      skills: [pc-feasibility-study, pc-user-research, pc-market-analysis]
      inputs: [product idea, potential-user access, initial constraints]
      outputs: [problem statement, target user, alternatives, initial MVP scope]
      duration: 1-3 days
    - id: 01-specification
      name: Bound MVP
      purpose: Define a testable MVP and explicit non-goals before technology choices expand the scope.
      skills: [pc-requirements-engineering, pc-spec-writing, pc-acceptance-criteria]
      inputs: [validated problem, target user, MVP hypothesis]
      outputs: [MVP stories, non-goals, acceptance criteria, success measures]
      duration: 1-3 days
    - id: 02-architecture
      name: Choose foundations
      purpose: Decide the costly-to-reverse stack, data, security, hosting, and system-boundary choices with written rationale.
      skills: [pc-system-design, pc-api-design, pc-data-modeling, pc-security-design, pc-tech-selection]
      inputs: [MVP specification, team skills, budget and operational constraints]
      outputs: [ADRs, system diagram, technology stack, initial threat model]
      duration: 2-5 days
    - id: 03-planning
      name: Sequence vertical slices
      purpose: Order deployable slices so the riskiest assumptions receive evidence first.
      skills: [pc-task-breakdown, pc-risk-assessment, pc-estimation]
      inputs: [MVP specification, foundation decisions, team capacity]
      outputs: [ordered vertical slices, rough timeline, first-week tasks]
      duration: 1-2 days
    - id: 04-implementation
      name: Build deployable slices
      purpose: Establish repository and CI conventions, deploy immediately, and grow the MVP through tested vertical slices.
      skills: [pc-tdd, pc-feature-development, pc-refactoring, pc-code-review, pc-documentation, pc-ci-cd]
      inputs: [ordered slices, architecture decisions, coding standards]
      outputs: [working MVP, test suite, decision log, deployment pipeline]
      duration: 1-4 weeks
    - id: 05-quality
      name: Establish quality baseline
      purpose: Create repeatable test, security, and observability patterns rather than pursuing exhaustive pre-launch coverage.
      skills: [pc-testing-strategy, pc-code-review, pc-security-audit, pc-documentation]
      inputs: [working MVP, tests, acceptance criteria]
      outputs: [CI quality checks, coverage baseline, security scan, monitoring baseline]
      duration: 2-3 days
    - id: 06-delivery
      name: Harden first delivery
      purpose: Make production deployment automated, reversible, secret-safe, and repeatable.
      skills: [pc-ci-cd, pc-release-management, pc-deployment-strategy, pc-documentation]
      inputs: [release candidate, infrastructure configuration, rollback design]
      outputs: [production deployment, tested rollback, release record, environment configuration]
      duration: 1-2 days
    - id: 07-operations
      name: Operate from day one
      purpose: Detect failures through error tracking, uptime checks, searchable logs, alerts, and a minimal runbook.
      skills: [pc-incident-response, pc-documentation]
      inputs: [production system, monitoring services, ownership model]
      outputs: [monitoring dashboard, alerts, log access, basic runbook]
      duration: launch onward
    - id: 08-evolution
      name: Learn and transition
      purpose: Measure real use, collect feedback, resolve early debt, and transition to the ongoing primary workflow.
      skills: [pc-retrospective, pc-tech-debt-management, pc-market-analysis]
      inputs: [usage data, feedback, incidents, decision log]
      outputs: [validated learning, roadmap update, debt actions, ongoing workflow route]
      duration: after MVP launch
  quality_gates:
    - name: Problem and scope
      after: 01-specification
      criteria: [target user and problem explicit, MVP outcomes testable, non-goals recorded]
      approvers: [founder or product lead]
      enforcement: blocking
    - name: Foundation review
      after: 02-architecture
      criteria: [key choices recorded as ADRs, team accepts stack, hosting and data boundaries selected, critical risks owned]
      approvers: [tech lead or team-designated reviewer]
      enforcement: blocking
    - name: MVP launch
      after: 06-delivery
      criteria: [core flow works end to end, CI passing, baseline security and monitoring active, rollback tested]
      approvers: [tech lead, QA reviewer]
      enforcement: blocking
  overlay_delta:
    applies_to: [agile-sprint, spec-driven, iterative-waterfall]
    changes:
      - dimension: system state
        effect: Assume no inherited implementation, data, operational history, or architecture constraints until intake identifies external dependencies.
      - dimension: architecture
        effect: Front-load costly-to-reverse foundation choices and default to a monolith and managed commodity services unless evidence requires otherwise.
      - dimension: delivery
        effect: Treat the first deployable slice, rollback path, and observability baseline as bootstrap outputs rather than later optimization.
---

# Greenfield Workflow

## Adaptation Notes

- Hackathons compress discovery and architecture but must record production gaps before handoff.
- Proofs of concept optimize for the named technical uncertainty and must not imply production readiness.
- Solo operators use written rationale and delayed self-review for foundation choices.
- Startup MVPs should invest early in deployment and observability because prototypes often remain in production.
