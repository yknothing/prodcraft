---
name: feature-development
description: Use when a reviewed task slice has tests or acceptance targets and the team must turn it into a small, mergeable implementation increment without expanding scope, breaking contracts, or hiding release-boundary risk.
metadata:
  phase: 04-implementation
  inputs:
  - task-list
  - architecture-doc
  - api-contract
  - test-suite
  outputs:
  - source-code
  prerequisites:
  - tdd
  quality_gate: The planned slice is implemented behind passing tests, contract and scope boundaries remain explicit, and the change is ready for code review
  roles:
  - developer
  - tech-lead
  methodologies:
  - all
  effort: large
  internal: false
  distribution_surface: curated
  source_path: skills/04-implementation/feature-development/SKILL.md
---

# Feature Development

> Implement the next reviewed slice as a small, test-backed increment that can be reviewed and delivered safely.

## Context

Feature development is where plans become working behavior. In Prodcraft, it sits between test-first design and formal review: the task is not "write a lot of code," but "land the smallest useful slice that satisfies the current plan and keeps downstream delivery safe."

This skill is especially important when the architecture, contract, and release boundary are already known. It prevents implementation from drifting into hidden scope expansion, accidental product decisions, or broad rewrites disguised as progress.

## Inputs

- **task-list** -- Defines the current slice, scope boundary, and success criteria.
- **test-suite** -- Gives the executable safety net that the implementation must satisfy.
- **architecture-doc** -- Provides component boundaries and constraints.
- **api-contract** -- Protects externally visible behavior when the slice changes a public or inter-service interface.

## Process

### Step 1: Pick the Smallest Reviewable Slice

Choose one reviewed task or thin vertical slice. Rewrite it in concrete implementation terms: what behavior lands now, what stays out of scope, and what boundary must remain stable.

If the slice is still too large to review comfortably, split it before coding.

### Step 2: Implement Behind the Test Boundary

Use the failing or targeted tests as the implementation guardrail. Add only the code needed to satisfy the current slice. Keep new abstractions local until a second use proves they belong.

Prefer vertical progress over partial framework setup. A small end-to-end slice is more valuable than three half-finished layers.

### Step 3: Preserve Scope and Contract Boundaries

Before each commit or reviewable checkpoint, verify:

- unsupported or deferred behavior is still explicit
- public contract changes are intentional and reflected in tests
- brownfield coexistence or compatibility seams still hold
- configuration, observability, and rollout hooks required by downstream phases are not skipped

### Step 4: Prepare the Increment for Review

Clean up obvious naming, dead code, and accidental noise that would distract review, but do not turn implementation into a refactoring detour. The output should be a small, understandable diff with passing tests and explicit notes on any trade-offs.

## Outputs

- **source-code** -- The implementation for the planned slice, ready for code review and downstream quality checks.

## Quality Gate

- [ ] One reviewed task slice is fully implemented
- [ ] Relevant tests pass locally or in CI
- [ ] Scope, unsupported behavior, and release boundaries remain explicit
- [ ] Public contract changes are intentional and documented
- [ ] The diff is small enough for effective review

## Anti-Patterns

1. **Scope creep by implementation** -- quietly adding adjacent features because the code is nearby.
2. **Framework-first progress** -- building scaffolding for future work instead of landing a usable slice now.
3. **Contract drift** -- changing externally visible behavior without updating tests and reviewers.
4. **Cleanup avalanche** -- turning a feature slice into a broad refactor that hides the real change.

## Related Skills

- [tdd](../tdd/SKILL.md) -- provides the test-first guardrail for the slice
- [refactoring](../refactoring/SKILL.md) -- improves structure after behavior is working and protected
- [code-review](../../05-quality/code-review/SKILL.md) -- validates correctness, maintainability, and scope discipline
- [ci-cd](../../06-delivery/ci-cd/SKILL.md) -- consumes the resulting code in automated delivery

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/04-implementation/feature-development/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
