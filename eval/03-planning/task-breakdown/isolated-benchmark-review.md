# Task Breakdown Isolated Benchmark Review

## Scope

This note summarizes the isolated explicit-invocation benchmark results for `task-breakdown`.

The benchmark evaluates whether the skill produces a more implementation-ready and safer plan than a generic baseline when invoked after reviewed design work, testing both a greenfield feature slice and a brownfield modernization.

The `copilot` runner was used as the fallback lane due to earlier Gemini lane timeouts.

## Scenario 1: Greenfield Vertical Slices

**Prompt:** "Break this reviewed architecture and API contract into implementation-ready tasks for a first-release approvals workflow..."

### Baseline
The baseline successfully identified the need to break down tasks and created an external `IMPLEMENTATION_TASKS.md` file. However, its summary indicated a drift toward generic technical tiers (Foundation, Document Service, Approval Service, Notification Service, Integration, Testing, Documentation) rather than strict vertical slices that deliver end-to-end functionality.

### With-Skill
The skill-applied branch followed the contract precisely. It output a detailed, inline plan.
- **Task Sizing:** All tasks explicitly bounded to 1-3 days.
- **Vertical Slices:** Specifically grouped tasks into vertical feature slices like "Phase 2: Core Document Operations" and "Phase 3: Approval Workflow" rather than purely horizontal tiers.
- **Dependencies:** Clearly mapped inline, accompanied by a visual Dependency Graph and a critical path estimation.
- **Quality Gate:** Explicitly validated its own output against the skill's quality gate checklist.

## Scenario 2: Brownfield Increment Plan

**Prompt:** "Break this brownfield modernization design into reversible increments that preserve release boundaries and rollback safety..."

### Baseline
The baseline generated a hidden `MIGRATION_PLAN.md`. While its summary referenced safety mechanisms like feature flags and dual writes, it abstracted the actual task breakdown into a generic output file without exposing explicit task sequencing, dependency chains, or per-task rollback details inline.

### With-Skill
The skill produced a highly structured, implementation-ready plan directly inline.
- **Coexistence & Safety:** Emphasized coexistence infrastructure first. Explicitly scheduled "characterization tests for legacy write paths" (T1.3) before any behavioral changes.
- **Reversible Increments:** Every single task included explicit "Done" criteria, "Dependencies", and crucially, a "Rollback" instruction (e.g., "Toggle feature flag off", "Service disabled, no client impact").
- **Migration Strategy:** Avoided big-bang cutovers, establishing a clear progression: Coexistence -> Dual-Write -> Read Path Migration (shadow mode/canary) -> Verification -> Cutover.
- **Dependencies:** Mapped a rigorous dependency graph ensuring safe, parallel execution where possible without violating rollback safety.

## Judgment

`task-breakdown` clearly outperformed the generic baseline:
1. It maintained a strict planning-layer focus with actionable 1-3 day tasks.
2. It proved highly effective at enforcing vertical slices over horizontal tech tiers.
3. In brownfield scenarios, it systematically embedded coexistence safety, regression/characterization tests, and granular rollback steps into the task fabric.
4. It provided high-visibility dependency graphs and critical path analysis directly suited for handoff to downstream implementation skills like `tdd`.

## Status Recommendation

The skill has demonstrated strong, isolated benchmark evidence that satisfies its quality gate and pass criteria.

- Recommended status: `tested`
