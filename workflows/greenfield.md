---
name: greenfield
description: "New project bootstrap from idea through first deployment"
cadence: "one-time, days to weeks"
workflow_kind: "overlay"
composes_with: ["*"]
entry_skill: "intake"
required_artifacts: ["intake-brief"]
best_for: ["new-products", "proof-of-concept", "hackathon", "side-projects"]
phases_included: ["all"]
---

# Greenfield Workflow

## Overview

The greenfield workflow guides a new project from initial idea through first production deployment. Unlike ongoing workflows, this is a one-time bootstrap sequence that establishes the foundations everything else will build on.

Greenfield projects carry a unique mix of freedom and risk. Every decision is available, but early choices in language, framework, data store, and hosting are the hardest to change later. This workflow front-loads the decisions that matter most and defers the ones that can wait.

The goal is not perfection -- it is a working system in production with solid foundations. You can iterate once you have something real. Choose this workflow for new products, proof-of-concept builds, hackathon projects, or any situation where you are starting from zero.

Greenfield is an overlay. It adjusts assumptions about existing system constraints while leaving the primary governance workflow (`agile-sprint`, `spec-driven`, or `iterative-waterfall`) intact.

## Entry Gate

This workflow starts only after `intake` classifies the request as new-product or greenfield work and the user approves the path. The required handoff artifact is the `intake-brief`, which anchors the scope, starting assumptions, and initial risks before bootstrap begins.

## Phase Sequence

### Phase 0: Discovery (1-3 days)

**Purpose:** Validate the problem is worth solving and define the minimum viable product.

**Skills:** Apply `feasibility-study`, `user-research` (lightweight), and `market-analysis` (quick scan).

This is not a months-long market research phase. The goal is to answer three questions:
1. **Who** has this problem? Can you name specific people or segments?
2. **How** are they solving it today? What is painful about the current approach?
3. **Why** would they switch to your solution? What is the compelling trigger?

**Inputs:** An idea, access to potential users (even a few).
**Outputs:** Problem statement (1 page), target user description, list of existing alternatives, initial MVP scope.

Skip this phase only if you have strong prior evidence (e.g., you are the user, you have customer interviews from another project). Even then, write down the problem statement -- it anchors every subsequent decision.

### Phase 1: Specification (1-3 days)

**Purpose:** Define what the MVP does -- and crucially, what it does not do.

**Skills:** Apply `requirements-engineering`, `spec-writing` (lightweight), and `acceptance-criteria`.

Write user stories for the MVP. Be ruthless about scope. For each proposed feature, ask: "Can we launch without this?" If yes, cut it. The specification is a short document, not a comprehensive PRD.

**Inputs:** Problem statement, target user, MVP scope.
**Outputs:** MVP feature list (10-20 user stories max), non-goals list (what you are explicitly deferring), success criteria (how you will know the MVP works).

**Key output: the non-goals list.** This is more important than the feature list. It prevents scope creep during implementation.

### Phase 2: Architecture (2-5 days)

**Purpose:** Make the foundational technical decisions that are expensive to change later.

**Skills:** Apply `system-design`, `api-design`, `data-modeling`, `security-design`, and `tech-selection`.

This is the highest-leverage phase in a greenfield project. Focus decisions on:

**Language and framework:** Choose based on team expertise first, ecosystem second, performance third. A framework your team knows well beats a theoretically superior one.

**Data store:** Relational (PostgreSQL) is the default unless you have a specific reason for something else. Document that reason if you choose otherwise.

**Hosting platform:** Choose based on team expertise and operational simplicity. A platform you can deploy to in an afternoon beats one that requires weeks of setup.

**Monolith vs. services:** Start with a monolith. Extract services later when you have evidence of where the boundaries should be. Premature decomposition is a leading cause of greenfield project failure.

**Build vs. buy:** For authentication, payments, email, and other commodity functions, buy or use a service. Build only what is your core differentiator.

**Inputs:** MVP specification, team skills inventory, budget constraints.
**Outputs:** Architecture Decision Records (ADRs) for each foundational choice, high-level system diagram, technology stack document.

### Gate: Foundation Review

- **Criteria:** Key technology decisions documented as ADRs. Team agrees on stack. Hosting platform selected. Data model sketched.
- **Approvers:** Tech lead (or the team collectively for small teams).
- **Type:** BLOCKING -- changing these decisions after implementation starts is expensive.

### Phase 3: Planning (1-2 days)

**Purpose:** Sequence the MVP build for maximum learning with minimum waste.

**Skills:** Apply `task-breakdown`, `risk-assessment`, and `estimation`.

Break the MVP into vertical slices -- each slice delivers a working user flow end-to-end. Prioritize slices that validate the riskiest assumptions first.

**Inputs:** MVP specification, architecture decisions.
**Outputs:** Ordered list of vertical slices, rough timeline, first-week tasks.

**Planning heuristic:** The first slice should be deployable. Even if it does almost nothing, getting the deployment pipeline working on day one saves pain later.

### Phase 4: Implementation (1-4 weeks)

**Purpose:** Build the MVP in vertical slices, deployed incrementally.

**Skills:** Apply `tdd`, `feature-development`, `refactoring`, `code-review`, `documentation`, and `ci-cd`.

**Week 1 priorities:**
1. Repository setup (version control, branching strategy, CI pipeline).
2. Project scaffolding (framework setup, directory structure, linting, formatting).
3. Deployment pipeline -- deploy a "hello world" to production on day one.
4. First vertical slice.

**Ongoing priorities:**
- Write tests from the start. It is easier to maintain a testing culture than to retrofit one.
- Review code even on a solo project (use checklists or rubber-duck review).
- Deploy every slice to production as it is completed.
- Track decisions and trade-offs in a lightweight log.

**Inputs:** Ordered slice list, architecture decisions, coding standards.
**Outputs:** Working MVP in production (incrementally deployed), test suite, decision log.

**Anti-patterns to avoid:**
- Building the entire backend before any frontend (integrate vertically).
- Perfecting one feature before starting the next (get breadth first, then depth).
- Skipping tests because "it's just a prototype" (it will become production code).
- Over-engineering for scale you do not have (solve today's problems today).

### Phase 5: Quality (2-3 days)

**Purpose:** Establish the quality baseline that all future work builds on.

**Skills:** Apply `testing-strategy`, `code-review`, `security-audit`, and `documentation` (baseline scan).

For a greenfield project, quality is about establishing patterns, not exhaustive testing:

1. **CI pipeline:** Every push runs linting, type checking, and tests automatically.
2. **Test patterns:** At least one example of each test type you will use (unit, integration, end-to-end).
3. **Security baseline:** Dependency vulnerability scan. HTTPS everywhere. Authentication tested.
4. **Monitoring baseline:** Error tracking configured. Basic uptime monitoring active.

**Inputs:** Working MVP, test suite.
**Outputs:** CI pipeline running, test coverage baseline established, security scan clean, monitoring configured.

### Phase 6: Delivery (1-2 days)

**Purpose:** Ensure the deployment pipeline is robust and repeatable.

**Skills:** Apply `ci-cd`, `release-management`, `deployment-strategy`, and `documentation`.

If you deployed incrementally during implementation (as recommended), this phase is about hardening what you already have:

1. **Automated deployment:** Merge to main triggers deployment. No manual steps.
2. **Rollback procedure:** Tested and documented. Can roll back within minutes.
3. **Environment parity:** Staging mirrors production configuration.
4. **Secrets management:** No credentials in code. All secrets in a vault or environment configuration.

**Inputs:** Deployment pipeline, infrastructure configuration.
**Outputs:** Documented deployment process, rollback procedure tested, environments configured.

Invest here. The deployment pipeline is used every day for the life of the project. Time spent making it reliable pays back continuously.

### Phase 7: Operations (Day 1 onward)

**Purpose:** Observe the system in production and respond to issues.

**Skills:** Apply `incident-response` and `documentation`.

Basic operational readiness from day one:

1. **Error tracking:** Exceptions are captured and alerted on (Sentry, Datadog, or equivalent).
2. **Uptime monitoring:** External health check running every minute.
3. **Log aggregation:** Logs are searchable and retained for at least 30 days.
4. **Alerting:** On-call notification for critical issues (even if "on-call" is just your phone).

**Inputs:** Production system, monitoring tools.
**Outputs:** Monitoring dashboard, alerting configured, basic runbook.

### Phase 8: Evolution (After MVP launch)

**Purpose:** Learn from real usage and plan the next iteration.

**Skills:** Apply `retrospective`, `tech-debt-management`, and `market-analysis`.

After launch:
1. **Measure:** Are users doing what you expected? Where do they get stuck?
2. **Listen:** Collect feedback actively. Talk to users.
3. **Decide:** Double down on what works, cut what does not, experiment with unknowns.
4. **Transition:** Move from this greenfield workflow to an ongoing workflow (agile-sprint or iterative-waterfall).

## Quality Gates

Gates in the greenfield workflow are lightweight but must not be skipped — each decision locks in foundations that are expensive to change later.

### Discovery Gate

- **Criteria:** Problem statement written. Target user defined. At least two existing alternatives identified. Initial MVP scope agreed.
- **Approvers:** Founder or project lead.
- **Type:** BLOCKING -- do not specify without validating the problem.

### Architecture Gate

- **Criteria:** Language, framework, data store, and hosting decided and written down with rationale. Monolith vs. services choice made. No critical unknowns blocking implementation.
- **Approvers:** Tech lead (or solo developer self-review using the rationale log).
- **Type:** BLOCKING -- do not implement without these decisions documented.

### MVP Launch Gate

- **Criteria:** Core user workflow works end-to-end. Automated CI pipeline passing. HTTPS, authentication, and dependency scanning clean. Error tracking and uptime monitoring active. Rollback procedure tested.
- **Approvers:** Tech lead, QA (or solo self-review checklist).
- **Type:** BLOCKING -- do not declare launch without all criteria met.

## Key Decision Points

| Decision | When | Criteria | Hard to change later? |
|----------|------|----------|----------------------|
| Programming language | Architecture phase | Team skill, ecosystem, hiring | Very hard |
| Framework | Architecture phase | Team skill, community, longevity | Hard |
| Data store | Architecture phase | Data model fit, operational expertise | Hard |
| Hosting platform | Architecture phase | Cost, complexity, team experience | Moderate |
| Monolith vs. services | Architecture phase | Default to monolith | Moderate |
| Build vs. buy (auth, payments) | Architecture phase | Core differentiator test | Easy if abstracted |

## Adaptation Notes

- **Solo developer:** All phases still apply but are compressed. Architecture decisions are the most important -- you cannot get a second opinion easily, so write down your reasoning and review it after sleeping on it.
- **Hackathon (24-48 hours):** Compress discovery + specification to 1 hour. Architecture to 30 minutes (use what you know). Skip formal quality and delivery phases. Build and ship.
- **Proof of concept:** Quality and operations are minimal. Focus on validating the core technical risk. Document what you would do differently for production.
- **Startup MVP:** Invest more in delivery and operations than you think you should. If the product works, you will be running it in production longer than you expect.
