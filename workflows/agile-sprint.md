---
name: agile-sprint
description: Iterative sprints with just-enough planning and continuous delivery
cadence: 1-2 week sprints
workflow_kind: primary
composes_with: [greenfield, brownfield, hotfix]
entry_skill: pc-intake
required_artifacts: [intake-brief]
best_for: [product-teams, saas, startups, rapid-iteration]
phases_included: [all]
contract:
  version: workflow.v2
  overview:
    summary: Apply all lifecycle phases as concurrent lenses inside short iterations, favoring rapid feedback and working software over upfront completeness.
    distinctive: Discovery, specification, architecture, quality, delivery, and evolution recur inside every sprint instead of forming a one-way sequence.
  entry_gate:
    summary: Begin only after pc-intake classifies the work and the user approves the sprint route.
    artifact: intake-brief
    approval_required: true
    fast_track_rule: A shortened route is allowed only when the approved intake-brief records its scope, risks, and omitted phases.
  phase_sequence:
    - id: sprint-planning
      name: Sprint planning
      purpose: Select a capacity-bounded goal and refine only enough discovery, specification, architecture, and planning to start safely.
      skills: [pc-requirements-engineering, pc-acceptance-criteria, pc-task-breakdown, pc-risk-assessment, pc-estimation, pc-sprint-planning]
      inputs: [prioritized backlog, user evidence, team capacity, architecture constraints]
      outputs: [sprint goal, sprint backlog, accepted stories, risk notes]
      duration: 2-4 hours per sprint
    - id: build-and-verify
      name: Build and continuous quality
      purpose: Coordinate daily, implement vertical slices with tests and review, and fix defects inside the same sprint.
      skills: [pc-tdd, pc-feature-development, pc-refactoring, pc-code-review, pc-documentation, pc-testing-strategy, pc-security-audit]
      inputs: [accepted stories, architecture guidance, coding standards]
      outputs: [reviewed code, automated tests, updated documentation, defect evidence]
      duration: bulk of sprint with daily coordination
    - id: continuous-delivery
      name: Continuous delivery
      purpose: Release accepted slices through automation, flags, and progressive exposure as soon as each slice is ready.
      skills: [pc-ci-cd, pc-deployment-strategy, pc-documentation]
      inputs: [reviewed code, passing CI, deployment policy]
      outputs: [deployed slices, release evidence, rollback-ready state]
      duration: throughout sprint
    - id: inspect-and-adapt
      name: Review and retrospective
      purpose: Demonstrate working software, capture stakeholder feedback, review system health, and commit owned improvement actions.
      skills: [pc-retrospective, pc-tech-debt-management, pc-documentation]
      inputs: [deployed work, stakeholder feedback, delivery and defect metrics, incident signals]
      outputs: [accepted outcomes, backlog updates, 1-3 owned improvement actions]
      duration: 2-3 hours at sprint end
  quality_gates:
    - name: Story acceptance
      after: each story
      criteria: [acceptance criteria verified, peer review approved, automated tests passing, applicable documentation updated]
      approvers: [product manager, developer peer]
      enforcement: blocking
    - name: Sprint release
      after: sprint delivery
      criteria: [sprint goal met or explicitly renegotiated, no new critical defects, deployment pipeline green]
      approvers: [tech lead, QA engineer]
      enforcement: advisory
    - name: Quarterly architecture review
      after: quarterly sprint cycle
      criteria: [decision log reviewed, tech-debt inventory updated, system-health trends reviewed]
      approvers: [architect, tech lead]
      enforcement: advisory
---

# Agile Sprint Workflow

## Adaptation Notes

- Solo operators replace ceremonies with weekly planning and checklist-based self-review.
- Small teams may pair instead of running formal review; large teams add cross-team coordination and architecture review.
- Remote teams may use asynchronous standups and recorded reviews.
- Regulated work adds traceability and compliance approval to story acceptance without removing sprint feedback loops.
