---
name: brownfield
description: "Legacy system modernization and incremental improvement"
cadence: "ongoing, months to years"
entry_skill: "intake"
required_artifacts: ["intake-brief"]
best_for: ["legacy-modernization", "platform-migration", "tech-debt-reduction"]
phases_included: ["all"]
---

# Brownfield Workflow

## Overview

The brownfield workflow guides the modernization of existing systems -- the careful, incremental replacement or improvement of software that is already in production and serving users. This is archaeology before architecture: you must understand what exists before you change it.

Brownfield work is fundamentally different from greenfield. The system has users, data, behavior (documented and undocumented), dependencies, and history. Changing one thing can break another. The goal is continuous improvement without disruption -- replacing the engine while the plane is flying.

This workflow is long-running, measured in months or years. Progress is incremental. Success is measured by reduction in incidents, improvement in developer velocity, and expansion of capabilities -- not by a single launch date.

Choose this workflow for legacy modernization, platform migrations, tech debt reduction campaigns, or any project where the existing system cannot be replaced all at once.

## Entry Gate

This workflow begins only after `intake` confirms that the work is modernization, migration, or long-running brownfield improvement. The required artifact is the `intake-brief`, which records current-system context, urgency, scope, and the reason a brownfield path is preferable to a fast-track fix.

## Phase Sequence

### Phase 0: Discovery -- System Archaeology (2-4 weeks)

**Purpose:** Understand the existing system before proposing changes.

**Skills:** Apply `documentation`, `user-research`, and `feasibility-study`.

This is the most critical phase in brownfield work. Resist the temptation to start fixing things immediately. Instead:

1. **Map the system:** Draw the actual architecture (not what the old docs say). Trace data flows. Identify integration points. Find the undocumented dependencies.
2. **Talk to the veterans:** Interview long-tenured team members. They know why weird things exist. "That looks wrong" is often "that was a deliberate trade-off."
3. **Inventory the pain:** Where are the incidents? What takes too long? What is everyone afraid to touch?
4. **Find the tests:** What is tested? What is not? Where are the gaps? Is there CI? Does it pass?
5. **Understand the data:** Data outlives code. Map the data model, find the inconsistencies, understand the migration history.

**Inputs:** Access to the existing system, codebase, infrastructure, and team members.
**Outputs:** System map (as-is architecture), pain point inventory, test coverage assessment, data model documentation, risk register, dependency inventory.

**Warning:** Discovery will reveal more problems than you expected. This is normal. Do not try to fix everything. Prioritize ruthlessly.

### Phase 1: Specification -- Document Current Behavior (2-4 weeks)

**Purpose:** Establish a behavioral baseline before changing anything.

**Skills:** Apply `spec-writing`, `acceptance-criteria`, `documentation`, and `tdd` (characterization tests).

Before you modernize, you must document what the system currently does -- including its quirks and bugs that users depend on.

1. **Write characterization tests:** Tests that capture current behavior, whether or not that behavior is "correct." These are your safety net.
2. **Document the implicit specification:** The code is the real spec. Extract it into explicit documentation. Pay special attention to edge cases and error handling.
3. **Identify behavioral contracts:** What do downstream systems depend on? What do users expect? These are constraints on any modernization.
4. **Define the target state:** Now that you know where you are, describe where you want to be. The gap between current and target is your modernization scope.

**Inputs:** System map, codebase, production logs, user behavior data.
**Outputs:** Characterization test suite, current behavior specification, behavioral contracts, target state definition, modernization scope.

### Gate: Baseline Established

- **Criteria:** Characterization tests cover critical paths. Current behavior documented. Target state defined. Modernization scope agreed.
- **Approvers:** Tech lead, product manager, architect.
- **Type:** BLOCKING -- do not start changing the system without a documented baseline.

### Phase 2: Architecture -- Strangler Fig Strategy (2-4 weeks)

**Purpose:** Design the modernization approach -- how to get from current state to target state incrementally.

**Skills:** Apply `system-design`, `api-design`, `data-modeling`, `security-design`, and `tech-selection`.

The default pattern is the strangler fig: build new functionality alongside the old, gradually routing traffic to the new system, and eventually decommissioning the old.

1. **Identify seams:** Find the natural boundaries in the existing system where you can intercept and redirect. These are your migration points.
2. **Design the facade:** Create an abstraction layer at each seam that can route to either old or new implementation. This enables incremental migration.
3. **Plan data migration:** Data is the hardest part. Design a strategy for keeping old and new data in sync during the transition period.
4. **Define rollback boundaries:** Every modernization step must be reversible. If the new component fails, traffic routes back to the old one.

**Inputs:** System map, target state definition, modernization scope.
**Outputs:** Migration architecture, seam identification, facade designs, data migration strategy, ADRs for key decisions.

**Anti-pattern: the big bang rewrite.** Do not try to replace the entire system at once. This approach fails more often than it succeeds because you lose the production-tested behavior of the old system.

### Phase 3: Planning -- Small, Safe Increments (1-2 weeks per increment)

**Purpose:** Sequence the modernization into increments that each deliver value and reduce risk.

**Skills:** Apply `task-breakdown`, `risk-assessment`, and `estimation`.

Break the modernization into increments where each one:
- Is independently deployable and reversible.
- Delivers measurable improvement (fewer incidents, faster deployments, better performance).
- Reduces the remaining modernization risk or scope.

**Sequencing principles:**
1. Start with the highest-pain, lowest-risk area. Quick wins build momentum and trust.
2. Tackle the riskiest migration early, while you still have budget and energy.
3. Leave the "it works, nobody touches it" components for last (or never).
4. Plan for parallel operation of old and new systems at every step.

**Inputs:** Migration architecture, pain point inventory, team capacity.
**Outputs:** Ordered increment list, per-increment plan, success metrics for each increment.

### Phase 4: Implementation -- Add Tests First, Then Change (Ongoing)

**Purpose:** Execute each modernization increment safely.

**Skills:** Apply `tdd`, `feature-development`, `refactoring`, `code-review`, `documentation`, and `ci-cd`.

The implementation cycle for each increment:

1. **Add tests to the legacy code** in the area you are about to change. If the characterization tests do not cover this area, add them now. Do not change code without tests around it.
2. **Introduce the seam:** Add the facade or abstraction layer that will allow routing between old and new.
3. **Build the new implementation** behind the facade.
4. **Test the new implementation** against the characterization tests. It must produce the same results as the old code for existing scenarios.
5. **Route a percentage of traffic** to the new implementation. Monitor closely.
6. **Increase traffic gradually** until 100% is on the new implementation.
7. **Remove the old code** once the new implementation is stable and verified.

**Inputs:** Increment plan, characterization tests, migration architecture.
**Outputs:** Modernized component, updated test suite, migration metrics.

**Rules for brownfield implementation:**
- Never delete old code until the new code is proven in production.
- Maintain backward compatibility at every step.
- If a migration step causes issues, roll back immediately. Debug later.
- Document every behavioral difference between old and new, no matter how small.

### Phase 5: Quality -- Regression Is the Enemy (Per increment)

**Purpose:** Verify that each increment preserves existing behavior and delivers the intended improvement.

**Skills:** Apply `testing-strategy`, `code-review`, `security-audit`, and `documentation`.

1. **Regression testing:** Run the full characterization test suite. No regressions allowed.
2. **Performance comparison:** Benchmark old vs. new. The new implementation must not degrade performance.
3. **Integration testing:** Verify all downstream systems continue to function.
4. **Data validation:** If data was migrated, verify completeness and correctness.

**Inputs:** Modernized component, characterization tests, performance benchmarks.
**Outputs:** Regression test results, performance comparison, integration verification, data validation report.

### Phase 6: Delivery -- Parallel Run (Per increment)

**Purpose:** Deploy the new component alongside the old with controlled traffic routing.

**Skills:** Apply `ci-cd`, `release-management`, `deployment-strategy`, and `documentation`.

1. Deploy the new component to production with traffic routing set to 0%.
2. Route 1-5% of traffic to the new component. Monitor for errors.
3. Gradually increase to 25%, 50%, 100% over days or weeks.
4. Keep the old component running but idle for a rollback window (1-4 weeks).
5. Decommission the old component after the rollback window.

**Inputs:** Modernized component, deployment pipeline, monitoring.
**Outputs:** Production deployment, traffic routing configuration, monitoring dashboards.

### Phase 7: Operations -- Monitor Both Systems (Ongoing)

**Purpose:** Maintain visibility into both old and new systems during transition.

**Skills:** Apply `incident-response` and `documentation`.

During the migration period, you are operating two systems. Monitoring must cover both:
- Error rates in old and new components.
- Performance comparison (latency, throughput).
- Data consistency between old and new data stores (if applicable).
- Rollback readiness -- can you route traffic back to old at any moment?

**Inputs:** Old and new systems in production, monitoring tools.
**Outputs:** Dual-system dashboards, comparative metrics, incident reports.

### Phase 8: Evolution -- Celebrate and Track (Quarterly)

**Purpose:** Measure modernization progress, celebrate milestones, adjust the plan.

**Skills:** Apply `retrospective`, `tech-debt-management`, and `market-analysis`.

1. **Track progress visually:** A migration dashboard showing percentage complete, components modernized, components remaining.
2. **Measure improvement:** Compare current metrics (incident rate, deployment frequency, developer velocity) to the baseline from discovery.
3. **Celebrate milestones:** Decommissioning a legacy component is a team achievement. Mark it.
4. **Adjust the plan:** Priorities shift. Re-evaluate the remaining increment order based on what you have learned.
5. **Know when to stop:** Not everything needs to be modernized. If a legacy component is stable, low-maintenance, and meeting its SLAs, it may be fine as-is.

**Inputs:** Migration dashboard, operational metrics, team feedback.
**Outputs:** Updated modernization roadmap, progress report, adjusted priorities.

## Quality Gates

### Pre-Migration Gate (per increment)

- **Criteria:** Characterization tests cover the area being changed. Rollback plan documented. Success metrics defined.
- **Approvers:** Tech lead, architect.
- **Type:** BLOCKING.

### Post-Migration Gate (per increment)

- **Criteria:** No regressions. Performance equal or better. Data validated. Rollback window completed without issues.
- **Approvers:** Tech lead, QA engineer, operations lead.
- **Type:** BLOCKING for decommissioning the old component.

## Adaptation Notes

- **Small team:** Focus on one increment at a time. Do not start the next migration until the current one is stable in production.
- **Large team:** Parallelize increments across sub-teams, but coordinate shared dependencies carefully. A shared migration dashboard is essential.
- **Tight deadline:** Prioritize the increments that reduce operational pain (incidents, manual processes). Defer cosmetic or architectural purity improvements.
- **Regulatory requirements:** Document the migration plan and each increment's impact on compliance. Maintain audit trail of what changed and when.
- **Political challenges:** Legacy systems have defenders. Involve them in discovery and planning. Show respect for the decisions that built the current system. Focus on measurable improvement, not "old vs. new."
