---
name: agile-sprint
description: "Iterative sprints with just-enough planning and continuous delivery"
cadence: "1-2 week sprints"
workflow_kind: "primary"
composes_with: ["greenfield", "brownfield", "hotfix"]
entry_skill: "intake"
required_artifacts: ["intake-brief"]
best_for: ["product-teams", "saas", "startups", "rapid-iteration"]
phases_included: ["all"]
---

# Agile Sprint Workflow

## Overview

The agile sprint workflow organizes work into short, time-boxed iterations where all Prodcraft phases operate concurrently rather than sequentially. Instead of completing one phase before starting the next, the team continuously refines, builds, tests, and ships in tight loops.

This workflow is ideal for product teams operating in fast-moving markets where learning speed matters more than upfront completeness. Requirements emerge through iteration, architecture evolves incrementally, and working software is the primary measure of progress.

All nine phases are present, but they manifest differently: discovery becomes continuous user research, specification becomes story writing, architecture happens as just-in-time design decisions. The phases become lenses applied throughout each sprint rather than sequential stages.

This workflow may be paired with overlays such as `greenfield`, `brownfield`, or `hotfix` when system state or urgency changes the route but not the primary governance model.

## Entry Gate

This workflow starts only after `intake` is completed and the user approves the proposed path. The required handoff artifact is the `intake-brief`, which records work type, entry phase, workflow selection, scope, and key risks.

Fast-track work can still use this workflow, but only if intake explicitly documents why a shortened path is appropriate.

## Phase Sequence

In agile sprints, phases do not execute sequentially — they operate concurrently as lenses applied throughout each sprint. Discovery is continuous user research; specification is story writing; architecture is just-in-time design. The sprint rhythm below describes how phases weave through each iteration.

## Sprint Rhythm

A sprint follows a repeating cadence. The phases weave through this rhythm:

### Sprint Planning (2-4 hours)

**Phases active:** Discovery, Specification, Architecture, Planning.

**Skills:** Apply `requirements-engineering` (lightweight), `acceptance-criteria`, `task-breakdown`, `risk-assessment`, `estimation`, and `sprint-planning`.

The product manager brings a prioritized backlog. The team selects work for the sprint based on capacity. Stories are refined just enough to begin work -- detailed design happens during implementation. Architecture decisions are made at the story level, with the architect advising on system-wide implications.

**Inputs:** Prioritized backlog, velocity data, team capacity.
**Outputs:** Sprint backlog, sprint goal, story point commitment.

### Daily Standup (15 minutes)

**Phases active:** Planning, Implementation.

Quick synchronization. Each team member shares progress, plans, and blockers. The tech lead identifies coordination needs. This is not a status report -- it is a coordination mechanism.

### Development (bulk of sprint)

**Phases active:** Implementation, Quality.

**Skills:** Apply `tdd`, `feature-development`, `refactoring`, `code-review`, and `documentation`.

Development and testing happen together, not sequentially. Test-driven development is the default. Code review happens on every pull request. The definition of done includes tests, documentation, and review approval.

**Inputs:** Sprint backlog stories, architecture guidance, coding standards.
**Outputs:** Working, tested, reviewed code merged to main branch.

Branches are short-lived -- measured in hours or days, not weeks. Continuous integration runs on every push. If a build breaks, fixing it is the team's top priority.

### Continuous Quality (throughout sprint)

**Phases active:** Quality.

**Skills:** Apply `testing-strategy`, `security-audit`, and `code-review` (lightweight, throughout the sprint).

Quality is not a phase gate -- it is woven into every day. Automated tests run on every commit. QA engineers perform exploratory testing as features are completed, not after all features are done. Defects found in the current sprint are fixed in the current sprint.

### Continuous Delivery (throughout sprint)

**Phases active:** Delivery.

**Skills:** Apply `ci-cd`, `deployment-strategy`, and `documentation`.

Features ship to production behind feature flags as soon as they pass review and automated testing. Canary releases expose new code to a small percentage of users first. The deployment pipeline is fully automated -- a merge to main triggers the release process.

**Inputs:** Reviewed, tested code on main branch.
**Outputs:** Features deployed to production (behind flags if incomplete).

### Sprint Review (1-2 hours)

**Phases active:** Quality, Evolution.

The team demonstrates completed work to stakeholders. Feedback is captured as new backlog items. Metrics are reviewed: velocity, defect rate, deployment frequency. Stakeholders see working software, not slide decks.

### Sprint Retrospective (1-1.5 hours)

**Phases active:** Evolution, Operations.

**Skills:** Apply `retrospective` and `tech-debt-management`.

The team reflects on how the sprint went. What went well? What could improve? What will we try differently? Action items are concrete, owned, and time-boxed. Operational issues from the sprint (incidents, monitoring gaps) are surfaced here.

**Outputs:** 1-3 concrete improvement actions for the next sprint.

## Quality Gates

Gates in agile sprints are lightweight but still present:

### Story Acceptance Gate

- **Criteria:** Acceptance criteria met. Code reviewed and approved. Automated tests passing. Documentation updated.
- **Approvers:** Product manager (functional), developer peer (technical).
- **Type:** BLOCKING per story -- stories not meeting Definition of Done do not count as complete.

### Sprint Release Gate

- **Criteria:** Sprint goal met (or explicitly adjusted mid-sprint with stakeholder agreement). No critical defects introduced. Deployment pipeline green.
- **Approvers:** Tech lead, QA engineer.
- **Type:** Advisory -- continuous delivery means individual stories ship as ready.

### Quarterly Architecture Review

- **Criteria:** Architecture decision log reviewed. Tech debt inventory updated. System health metrics trending positively.
- **Approvers:** Architect, tech lead.
- **Type:** Advisory -- produces action items for upcoming sprints, does not block current work.

## Definition of Done

Every story must satisfy all of these before it is considered complete:

- Code written and peer-reviewed
- Unit tests written and passing
- Integration tests passing
- Acceptance criteria verified
- Documentation updated (API docs, runbooks, user-facing docs as applicable)
- Feature deployed to staging environment
- No regressions introduced (CI pipeline green)

## Cross-Cutting Concerns

These are not separate phases but are embedded in the Definition of Done:

- **Security:** Threat modeling for new features. Dependency scanning on every build. Security-sensitive changes get additional review.
- **Accessibility:** Accessibility criteria included in acceptance criteria. Automated a11y testing in CI.
- **Observability:** New features include logging, metrics, and tracing. Alerting thresholds updated as needed.
- **Documentation:** Updated as part of the story, not as a separate task.

## Operations Integration

Production operations feed directly into the sprint process:

- **Monitoring alerts** that indicate product issues become backlog items.
- **On-call burden** is tracked as a team metric. If on-call is consuming too much capacity, it is discussed in retrospective and addressed.
- **Incident postmortems** produce action items that enter the backlog and are prioritized alongside feature work.

## Adaptation Notes

- **Solo developer:** Sprint ceremonies become personal planning sessions. Weekly planning replaces daily standup. Self-review using checklists. Ship at least weekly.
- **Small team (2-4):** Ceremonies can be shorter. Pair programming replaces formal code review when the team is co-located. Sprint review can be informal.
- **Large team (10+):** Consider Scrum of Scrums for coordination. Assign a dedicated Scrum Master. Architecture review becomes more important to prevent divergence.
- **Remote teams:** Async standup updates supplement (or replace) synchronous standup. Sprint review is recorded for stakeholders in other time zones. Retrospective uses collaborative tools to ensure all voices are heard.
- **Regulated environments:** Add compliance checks to the Definition of Done. Maintain traceability from stories to regulatory requirements. Sprint review includes compliance stakeholders.
