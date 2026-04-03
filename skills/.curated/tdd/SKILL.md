---
name: tdd
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
  - task-breakdown
  quality_gate: All acceptance criteria have corresponding tests, all tests pass, coverage meets threshold
  roles:
  - developer
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/04-implementation/tdd/SKILL.md
  public_stability: beta
  public_readiness: core
---

# Test-Driven Development

> RED -> GREEN -> REFACTOR. Write a failing test, make it pass with the simplest code, then improve the design. Repeat.

## Context

TDD is the core implementation discipline in Prodcraft. It ensures every piece of code is born with a test, creating a safety net for refactoring and a living specification of behavior. TDD is not about testing -- it's about design. Writing the test first forces you to think about the interface before the implementation.

In a lifecycle-aware system, TDD should start from the next planned slice of work, while preserving upstream contract and coexistence boundaries. Do not use implementation pressure as an excuse to skip characterization, contract, or unsupported-flow tests in brownfield work.

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

- **task-list** -- Minimum required input. Identifies the next slice to implement and its done criteria.
- **api-contract** -- Optional but strongly preferred when the task changes public or inter-service behavior.
- **acceptance-criteria-set** -- Optional amplifying input when formal acceptance criteria already exist.

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

- **test-suite** -- produced by this skill
## Quality Gate

- [ ] The relevant RED run was observed before implementation code was accepted
- [ ] Every acceptance criterion has at least one corresponding test
- [ ] All tests pass
- [ ] Code coverage meets project threshold (e.g., 80% for new code)
- [ ] No tests are skipped or ignored
- [ ] Tests run in < 30 seconds (unit) / < 5 minutes (full suite)

## Anti-Patterns

1. **Test-after rationalization** -- "I'll write tests after I code." You won't, and the design suffers.
2. **Testing implementation, not behavior** -- Testing that a private method is called is fragile. Test the public behavior.
3. **Giant test setup** -- If setup is 50 lines, the unit under test is too large. Break it down.
4. **Ignoring the REFACTOR step** -- RED-GREEN without REFACTOR accumulates design debt rapidly.
5. **100% coverage obsession** -- Coverage is a guide, not a goal. 80% thoughtful coverage beats 100% mechanical coverage.
6. **Skipping safety-net tests in brownfield work** -- Writing only the new happy-path test while leaving coexistence, unsupported-flow, or legacy-read behavior unprotected.
7. **Reference-code cheating** -- Keeping implementation written before RED and "translating" it after the test exists.

## Related Skills

- [acceptance-criteria](../../01-specification/acceptance-criteria/SKILL.md) -- provides the test specifications
- [systematic-debugging](../systematic-debugging/SKILL.md) -- establishes the bug boundary before TDD drives the fix
- [feature-development](../feature-development/SKILL.md) -- turns the tested slice into the reviewable implementation increment
- [refactoring](../refactoring/SKILL.md) -- applies the REFACTOR step more broadly once behavior is protected
- [code-review](../../05-quality/code-review/SKILL.md) -- reviews both code and tests
- [verification-before-completion](../../cross-cutting/verification-before-completion/SKILL.md) -- verifies that the claimed green state is backed by fresh evidence

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/04-implementation/tdd/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `core`
