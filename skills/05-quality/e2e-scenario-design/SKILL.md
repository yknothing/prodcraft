---
name: e2e-scenario-design
description: Use when designing or implementing E2E tests that need to go beyond shallow happy-path flows — especially for multi-step user journeys, stateful session scenarios, cross-boundary state consistency, and failure-mode edge cases. Applies across platforms (web, mobile, desktop), languages (Swift, TypeScript, Python, Java), and test frameworks (XCUITest, Playwright, Cypress, Selenium). Use this skill when tests feel too thin, when the test suite passes but production breaks, or when you need to write tests that simulate realistic, extended usage rather than single feature checks.
metadata:
  phase: 05-quality
  inputs:
    - source-code
    - task-list
    - test-strategy-doc
  outputs:
    - test-suite
    - test-report
  prerequisites:
    - testing-strategy
  quality_gate: Scenario tests cover at least one multi-step stateful journey per critical persona; edge cases cover input boundaries, navigation failures, and dependency unavailability; no test uses fixed sleeps; assertions verify business state, not only UI visibility
  roles:
    - qa-engineer
    - developer
  methodologies:
    - all
  effort: large
---

# Deep E2E Scenario Design

> Shallow tests verify that features exist. Deep tests verify that the product holds up when used.

## Diagnosis: The Shallow Test Trap

If every test in the suite can be described as "open X, do Y, see Z" in one sentence, the suite is shallow. It verifies what the developer already checked manually. Real production failures happen at state accumulation, cross-boundary navigation, session re-entry, input boundaries, and mid-session dependency failure — none of which appear in single-step tests.

## Process

**Step 1 — Extract journeys from personas.** Start with real users, not the feature list. Write out what each primary persona actually does in an extended session. This is the scenario.

**Step 2 — Map the state machine.** For each scenario step, identify what changed and what invariants must still hold. Assert both the new state and the preserved prior state at every checkpoint.

**Step 3 — Identify the re-entry point.** Every multi-session scenario has a point where the user leaves and returns. Design one test that navigates completely away via the product's own navigation, then re-enters. This is the persistence test — a tab switch is not.

**Step 4 — Write edge cases from a taxonomy.** After the scenario is stable: input boundaries (empty, partial, max-length, invalid), navigation boundaries (unknown route, rapid switching, deep link), lifecycle events (interrupt/resume, process restart), concurrency (rapid taps, optimistic-update rollback).

## Suite Architecture

Organize in four layers — each with a different contract. Read [`references/methodology.md`](references/methodology.md) for the full layer definitions, implementation principles, debugging methodology, and platform-specific gotcha classes.

| Layer | Backend | Depth | Purpose |
|---|---|---|---|
| Fixture / stub | Controlled stub | Shallow | Routing, chrome, loading states |
| Live flow | Real backend | 2–4 steps | Per-feature smoke coverage |
| Scenario | Real backend | 8–20 steps | Multi-step session, state accumulation |
| Edge case | Real + offline | Variable | Boundaries, failure modes, lifecycle |

## What to Assert

Structure and assertions are both required. Read [`references/assertion-patterns.md`](references/assertion-patterns.md) for guidance on asserting business state beyond UI visibility — including consistency across system boundaries, concurrency, and failure recovery.

## Platform References

For platform-specific gotchas that cause silent failures:
- **iOS + WKWebView (XCUITest)**: [`references/platform/xcuitest-webview.md`](references/platform/xcuitest-webview.md) — document-coordinate frames, aria-modal accessibility blocking, disabled button no-ops

## Related Skills

- [testing-strategy](../testing-strategy/SKILL.md) — defines pyramid ratios and CI integration; this skill implements the scenario and edge-case layers
- [tdd](../../04-implementation/tdd/SKILL.md) — test-first discipline that prevents the shallow test trap at the unit layer
