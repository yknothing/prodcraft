# Task Breakdown QA Strategy

## Goal

Evaluate whether `task-breakdown` converts reviewed architecture and API contracts into implementation-ready work items without collapsing brownfield coexistence constraints or unresolved upstream decisions.

## Why Start with Routed Handoff

`task-breakdown` is the first planning skill on the core spine:

- `system-design` defines the structure
- `api-design` defines the contract surfaces
- `task-breakdown` decides how the work actually lands

The first QA question is therefore whether the skill produces a plan that:

- respects architecture and contract boundaries
- preserves coexistence and rollback concerns
- exposes blockers from unresolved questions instead of hiding them
- prepares clean handoff for implementation and testing

## Initial Evaluation Mode

The first evaluation is a **manual architecture-to-task handoff review** using the brownfield access-review modernization scenario.

This is review-stage evidence only. It does not replace future isolated automated benchmarks.

## Scenario

- `access-review-modernization-planning-handoff`

Inputs:

- reviewed architecture outline
- reviewed API contract outline

## Assertions

1. **stays-in-planning-layer**
   - output is task/dependency oriented
   - it does not collapse into code-level implementation detail or architecture redesign

2. **preserves-brownfield-coexistence**
   - coexistence, compatibility, and rollback work remain explicit tasks
   - the plan does not assume a replacement-only cutover

3. **preserves-open-question-blockers**
   - unresolved upstream questions appear as explicit blockers, assumptions, or deferred tasks

4. **uses-vertical-slices-and-dependencies**
   - work is sequenced in shippable or testable increments with visible dependencies

5. **prepares-downstream-handoff**
   - output is shaped for `tdd`, `feature-development`, and `testing-strategy`

## Pass Standard

Treat a run as strong review-stage evidence if it clearly outperforms a generic baseline on:

- coexistence/rollback preservation
- blocker visibility
- vertical slicing and dependency quality
- downstream readiness for implementation/testing

## Next QA Step

After this manual review:

- add an isolated benchmark for the same brownfield scenario
- add a greenfield/spec-driven scenario to verify that the skill does not overfit to migration planning
