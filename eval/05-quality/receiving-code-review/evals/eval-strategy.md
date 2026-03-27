# Receiving Code Review QA Strategy

## Goal

Evaluate whether `receiving-code-review` helps the author process review feedback with technical rigor instead of blind agreement or batch implementation.

## Why This Skill Matters

The current repo has strong reviewer-side guidance but no explicit author-side protocol. The key question is whether this skill:

- forces clarification before partial implementation
- verifies reviewer suggestions against the actual codebase
- supports evidence-based pushback when a comment is wrong
- keeps follow-up work test-backed and itemized

## Initial Evaluation Mode

The first evaluation is a routed manual review using a mixed feedback bundle:

1. one clearly correct blocking item
2. one ambiguous item that should trigger clarification
3. one context-poor suggestion that should trigger technical skepticism

## Assertions

1. **clarify-before-acting**
   - ambiguous items are surfaced before partial implementation begins

2. **verify-suggestions-against-reality**
   - accepted suggestions are checked against current code, tests, and boundaries

3. **pushback-is-technical**
   - rejected suggestions are answered with evidence, not tone

4. **response-record-is-explicit**
   - the output preserves an item-by-item response record

## Pass Standard

Treat the skill as strong review-stage evidence if it clearly outperforms a generic "apply review comments" baseline on clarification discipline, technical skepticism, and per-item verification.
