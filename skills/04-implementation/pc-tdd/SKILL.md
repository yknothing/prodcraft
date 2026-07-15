---
name: pc-tdd
description: Use when a reviewed task is ready for implementation and the team must drive the work by writing failing tests first, especially when contract behavior, brownfield regressions, unsupported flows, or coexistence safety must be proven before code changes.
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
  quality_gate: All acceptance criteria have corresponding tests, all tests pass, coverage meets threshold
  roles:
  - developer
  methodologies:
  - all
  effort: medium
---

# Test-Driven Development

> RED -> GREEN -> REFACTOR. Write a failing test, make it pass with the simplest code, then improve the design. Repeat.

## Context

TDD is the core implementation discipline in Prodcraft.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

If you wrote implementation code before the failing test, delete it and start over from RED.

`Delete it` means:

- do not keep it as a "reference"
- do not lightly adapt it while pretending to start TDD
- do not look at it and then rewrite a cosmetically different version

If you did not watch the relevant test fail first, you do not yet know that the test proves the intended behavior.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: RED -- Write a Failing Test

1. Pick the next reviewed task slice, acceptance criterion, or contract behavior
2. Write a test that describes the expected behavior
3. Run the test -- it MUST fail (if it passes, you have a wrong test or the feature already exists)
4. The test name should read like a specification: `test_user_can_reset_password_with_valid_token`

For brownfield or coexistence work, decide first which safety net is needed:
- characterization test for legacy behavior that must not regress
- contract test for the new or changed API behavior
- unsupported-flow or compatibility test for cases intentionally excluded from release 1

If the test passes immediately, stop. You are either testing existing behavior or wrote the test after the implementation leaked in. Fix the test, or delete the implementation and start over.

### Step 2: GREEN -- Make it Pass

1. Write the MINIMUM code to make the test pass
2. It's okay to be ugly, hardcode values, take shortcuts
3. The only goal is a green test
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

When you hear one of these thoughts, treat it as a stop signal:

| Excuse | Required response |
|--------|-------------------|
| "I'll write the tests after" | Stop and return to RED now |
| "This code is tiny, I don't need TDD" | Tiny bugs still regress; write the test |
| "I already know what the fix is" | Knowledge without a failing test is unproven confidence |
| "I'll keep the code as reference" | Delete it and restart from the test |
| "This is just a workaround" | Workarounds still need failing and passing evidence |
| "Manual testing is enough for now" | Manual checks do not replace executable regression protection |
| "The feature is urgent" | Urgency increases the need for discipline |
| "The bug only happens in brownfield edge cases" | That is exactly when characterization tests matter |

## Red Flags -- Stop and Start Over

- implementation code appeared before a failing test
- the "RED" run was skipped
- the test passed on the first run without proving missing behavior
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

If an exception is used, state it explicitly. "We'll add tests later" without a named reason is rationalization, not an exception.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] The relevant RED run was observed before implementation code was accepted
- [ ] Every acceptance criterion has at least one corresponding test
- [ ] All tests pass
- [ ] Code coverage meets project threshold (e.g., 80% for new code)
- [ ] No tests are skipped or ignored
- [ ] Tests run in < 30 seconds (unit) / < 5 minutes (full suite)
