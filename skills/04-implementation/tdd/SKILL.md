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
  - source-code
  prerequisites:
  - task-breakdown
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

TDD is the core implementation discipline in Prodcraft. It ensures every piece of code is born with a test, creating a safety net for refactoring and a living specification of behavior. TDD is not about testing -- it's about design. Writing the test first forces you to think about the interface before the implementation.

In a lifecycle-aware system, TDD should start from the next planned slice of work, while preserving upstream contract and coexistence boundaries. Do not use implementation pressure as an excuse to skip characterization, contract, or unsupported-flow tests in brownfield work.

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

### Step 2: GREEN -- Make it Pass

1. Write the MINIMUM code to make the test pass
2. It's okay to be ugly, hardcode values, take shortcuts
3. The only goal is a green test
4. Do NOT add code the test doesn't require

Do not silently implement behavior that upstream planning marked as blocked, unsupported, or deferred.

### Step 3: REFACTOR -- Improve the Design

1. Now that tests are green, improve the code structure
2. Remove duplication, improve naming, simplify logic
3. Run tests after EVERY refactoring step -- they must stay green
4. This is where design emerges organically

### Step 4: Repeat

Pick the next requirement, write the next failing test. The test suite grows incrementally alongside the implementation.

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

TDD is a default, not a religion. Skip test-first for:
- Exploratory prototypes (write tests after, once the design stabilizes)
- Pure UI layout (visual regression testing is more appropriate)
- Configuration and glue code (test the behavior it enables instead)

## Quality Gate

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

## Related Skills

- [acceptance-criteria](../../01-specification/acceptance-criteria/SKILL.md) -- provides the test specifications
- `feature-development` (planned) -- the broader implementation context
- `refactoring` (planned) -- the REFACTOR step, applied more broadly
- [code-review](../../05-quality/code-review/SKILL.md) -- reviews both code and tests
