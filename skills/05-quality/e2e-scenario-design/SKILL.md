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

## Context

Use this skill when the existing test strategy is directionally correct, but the scenario depth is still too thin for real confidence. The failure mode it targets is not "there are no tests." It is "the tests pass, but the product still breaks under realistic extended use."

If every test in the suite can be described as "open X, do Y, see Z" in one sentence, the suite is shallow. It mostly verifies what the developer already checked manually. Real production failures happen at state accumulation, cross-boundary navigation, session re-entry, input boundaries, and mid-session dependency failure.

This skill does not replace [testing-strategy](../testing-strategy/SKILL.md). `testing-strategy` decides the test layers and coverage priorities. `e2e-scenario-design` deepens the scenario and edge-case layers once that strategy exists.

## Inputs

- **source-code** -- The product surface and implementation seams that the scenarios must exercise realistically.
- **task-list** -- The current slice, risk boundary, or release scope that the scenarios must protect.
- **test-strategy-doc** -- The upstream decision on which layers matter now, which risks are critical, and which flows belong in E2E versus lower layers.

## Process

### Step 1: Diagnose the Shallow Test Trap

Check whether the current E2E suite is mostly:

- one-screen happy-path checks
- UI visibility assertions without business-state proof
- per-feature smoke coverage with no state accumulation
- fixed-sleep timing hacks instead of deterministic waits

If that pattern dominates, treat the suite as structurally shallow before adding more cases.

### Step 2: Extract Journeys from Personas

Start with real users, not the feature list. Write out what each primary persona actually does in an extended session. This is the scenario.

### Step 3: Map the State Machine

For each scenario step, identify what changed and what invariants must still hold. Assert both the new state and the preserved prior state at every checkpoint.

### Step 4: Identify the Re-Entry Point

Every multi-session scenario has a point where the user leaves and returns. Design one test that navigates completely away via the product's own navigation, then re-enters. This is the persistence test; a tab switch is not.

### Step 5: Write Edge Cases from a Taxonomy

After the main scenario is stable, add edge cases from a deliberate taxonomy:

- input boundaries: empty, partial, max-length, invalid
- navigation boundaries: unknown route, rapid switching, deep link
- lifecycle events: interrupt/resume, process restart
- concurrency: rapid taps, optimistic-update rollback
- dependency failures: offline, timeout, partial backend availability

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

Prefer assertions that prove:

- persisted business state, not just visible widgets
- cross-boundary consistency, not just local UI updates
- deterministic recovery behavior, not just eventual absence of errors
- explicit failure handling when dependencies are unavailable

## Platform References

For platform-specific gotchas that cause silent failures:
- **iOS + WKWebView (XCUITest)**: [`references/platform/xcuitest-webview.md`](references/platform/xcuitest-webview.md) — document-coordinate frames, aria-modal accessibility blocking, disabled button no-ops

## Outputs

- **test-suite** -- Scenario and edge-case tests that cover at least one extended stateful journey for each critical persona or release boundary in scope.
- **test-report** -- What scenarios were added or exercised, which risk boundaries they protect, and any remaining blind spots or deferred coverage.

## Quality Gate

- [ ] At least one multi-step, stateful journey exists for each critical persona or release boundary in scope
- [ ] Edge cases cover boundaries that the upstream `test-strategy-doc` marked as risky or easy to miss
- [ ] Assertions verify business state or cross-boundary consistency, not just UI visibility
- [ ] No scenario relies on fixed sleeps when a deterministic wait or observable state change is available
- [ ] The resulting suite structure makes clear which cases belong to smoke, scenario, and edge-case layers

## Anti-Patterns

1. **Smoke-suite cosplay** -- calling a handful of happy-path checks an E2E strategy.
2. **UI-only proof** -- asserting that the badge or toast is visible without proving persisted or cross-boundary state.
3. **State reset blindness** -- never leaving and re-entering the flow, so session or persistence bugs stay invisible.
4. **Framework cargo cult** -- copying platform-specific tooling advice without tying it to the current product risk.
5. **Sleep-based timing** -- adding fixed waits instead of deterministic state or network-based synchronization.

## Related Skills

- [testing-strategy](../testing-strategy/SKILL.md) — defines pyramid ratios and CI integration; this skill implements the scenario and edge-case layers
- [tdd](../../04-implementation/tdd/SKILL.md) — test-first discipline that prevents the shallow test trap at the unit layer
