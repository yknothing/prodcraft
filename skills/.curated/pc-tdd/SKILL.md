---
name: pc-tdd
description: Use before changing executable behavior that needs regression protection, or when adding characterization tests before a refactor. Distinguish new behavior from an existing baseline; use document, visual, or boundary checks for work that test-first does not model usefully.
metadata:
  phase: 04-implementation
  inputs:
  - acceptance-criteria-set
  - api-contract
  - task-list
  outputs:
  - test-suite
  prerequisites:
  - pc-task-breakdown
  quality_gate: Changed behavior has relevant failing-then-passing evidence, preserved behavior has a checked baseline, and applicable project test requirements pass
  roles:
  - developer
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/04-implementation/pc-tdd/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Test-Driven Development

> RED -> GREEN -> REFACTOR. Write a failing test, make it pass with the simplest code, then improve the design. Repeat.

## Context

TDD is the core implementation discipline in Prodcraft.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## The Iron Law

Default to writing and observing the behavioral test failure before changing implementation. Baseline verification after an early patch is recovery from that ordering mistake, not the normal TDD path.

```
NEW OR CHANGED BEHAVIOR NEEDS BASELINE FAILURE EVIDENCE
```

For new or changed executable behavior without an applicable exception below, observe the relevant failure before accepting the implementation. If your unaccepted change came first, isolate your own patch and prove the test fails against the unchanged baseline, then reapply the patch and observe GREEN. Record the order honestly. Never delete existing working code, another person's changes, or characterization tests to manufacture RED.

Characterization protects behavior that already exists. Its first run may pass; establish the baseline and show the assertion detects a meaningful contrary result before refactoring. Do not label it a new-feature RED run.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: RED -- Write a Failing Test

1. Pick the next reviewed task slice, acceptance criterion, or contract behavior
2. Write a test that describes the expected behavior
3. For new or changed behavior, run the test against the unchanged implementation; it must fail for the intended behavioral reason, not setup or import errors
4. The test name should read like a specification: `test_user_can_reset_password_with_valid_token`

For brownfield or coexistence work, decide first which safety net is needed:
- characterization test for legacy behavior that must not regress
- contract test for the new or changed API behavior
- unsupported-flow or compatibility test for cases intentionally excluded from release 1

If a new-behavior test passes immediately, inspect whether the behavior already exists or the assertion misses it. If the requirement is already satisfied, record that result instead of adding redundant code. For characterization, keep the passing baseline and check assertion sensitivity using an isolated contrary expectation or controlled mutation that is restored before proceeding.

### Step 2: GREEN -- Make it Pass

1. Write the MINIMUM code to make the test pass
2. Keep the implementation simple while respecting input, contract, security, and configuration boundaries
3. Make the behavioral test pass without hardcoding its fixture or bypassing the real logic
4. Do NOT add code the test doesn't require

Do not silently implement behavior that upstream planning marked as blocked, unsupported, or deferred.

If you catch yourself adding code "because the next test will need it anyway," stop. That is the exact moment TDD is being replaced by speculative implementation.

### Step 3: REFACTOR -- Improve the Design

1. Now that tests are green, improve the code structure
2. Remove duplication, improve naming, simplify logic
3. Run tests after EVERY refactoring step -- they must stay green
4. This is where design emerges organically

### Step 4: Repeat

Pick the next requirement, write the next failing test. The test suite grows incrementally alongside the implementation.

## Rationalization Prevention

Apply this section and the Red Flags below to new or changed executable behavior after checking the explicit exceptions. Characterization and a justified document or visual check do not need a fabricated RED run.

When you hear one of these thoughts, treat it as a stop signal:

| Excuse | Required response |
|--------|-------------------|
| "I'll write the tests after" | Stop and return to RED now |
| "This code is tiny, I don't need TDD" | Tiny bugs still regress; write the test |
| "I already know what the fix is" | Knowledge without a failing test is unproven confidence |
| "The implementation came first, so a green test proves it" | Isolate your patch and prove the failure against the unchanged baseline |
| "This is just a workaround" | Workarounds still need failing and passing evidence |
| "Manual testing is enough for now" | Manual checks do not replace executable regression protection |
| "The feature is urgent" | Urgency increases the need for discipline |
| "The bug only happens in brownfield edge cases" | That is exactly when characterization tests matter |

## Red Flags -- Stop and Start Over

- changed behavior has no demonstrated failure against the unchanged baseline
- the behavioral RED run was skipped for new or changed executable behavior without an applicable exception
- a new-behavior test passed immediately without checking whether the behavior already exists
- multiple behaviors are being added under one test because "they are related"
- you are defending extra code with "the next step will need it"
- the new behavior changes a contract or compatibility seam without an explicit test
- a brownfield bugfix only tests the happy path and not the legacy or unsupported boundary
- you are claiming the fix works before watching the regression test go green

## Brownfield Test Ordering Heuristics

When the work is modernization or compatibility-sensitive:

1. characterization/regression safety first
2. contract behavior for the public or compatibility boundary
3. unsupported/deferred behavior tests
4. only then the happy-path implementation slice

This keeps coexistence work honest and makes rollback safer.

## Test Pyramid

Follow the test pyramid -- more tests at the bottom, fewer at the top:

```
        /  E2E  \        (few, slow, high confidence)
       / Integr. \       (moderate, medium speed)
      /   Unit    \      (many, fast, focused)
```

- **Unit tests**: Test a single function/method in isolation. Mock dependencies. Fast.
- **Integration tests**: Test boundaries (API endpoints, database queries, service interactions).
- **E2E tests**: Test complete user flows. Few, slow, but high confidence.

## When NOT to Use TDD

TDD is the default. Narrow exceptions exist only when test-first does not yet model useful behavior:

- exploratory prototypes, with the explicit obligation to add tests once the design stabilizes
- pure UI layout work, where visual regression or interaction checks are the real proof
- configuration and glue code, where the enabled behavior should be tested at the boundary it affects
- documentation, skill prose, and reversible wording changes, where contract consistency, references, and runtime loading are the relevant checks

If an exception is used, state it explicitly. "We'll add tests later" without a named reason is rationalization, not an exception.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Changed behavior has an observed behavioral RED and GREEN; characterization has a checked baseline
- [ ] Each in-scope behavior has an appropriate test or an explicit applicable exception
- [ ] Relevant tests and project-required checks pass; skipped checks and limits are explicit
- [ ] Coverage and runtime meet project requirements where defined; no arbitrary percentage or duration was invented

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/04-implementation/pc-tdd/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
