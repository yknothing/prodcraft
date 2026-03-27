# Phase 04: Implementation

## Purpose

Build the product according to the plan, architecture, and specification. Implementation turns designs into working software through disciplined coding, testing, and integration practices.

## When to Enter

- Tasks are planned, estimated, and assigned.
- Development environment and tooling are ready.
- The team has access to all specified dependencies and services.
- Contract and coexistence boundaries for the next slice are visible enough to test before coding.

## Entry Criteria

- Sprint or iteration plan exists with prioritized task list.
- Architecture and spec documents are accessible to all developers.
- API contracts or acceptance criteria exist when the slice changes externally visible behavior.
- CI pipeline is configured and functional.
- Coding standards and branching strategy are agreed upon.

## Exit Criteria (Quality Gate)

All planned features are code-complete. Unit and integration tests pass. Code meets agreed coding standards. No known P0/P1 defects remain open. Feature branches are merged or ready for review.

## Key Skills

| Skill | Purpose | Effort |
|---|---|---|
| tdd | Write tests first to drive design and catch regressions | medium |
| feature-development | Implement features incrementally and verifiably | large |
| refactoring | Improve code structure without changing behavior | medium |
| pair-programming | Collaborate in real-time for quality and knowledge sharing | small |

## Typical Duration

- Small feature: 1-5 days
- Medium feature: 1-4 weeks
- Large initiative: 1-3 months
- Platform build: 3-6 months

## Skill Sequence

```
tdd ←──→ feature-development ←──→ refactoring
              ↑
       pair-programming
```

Implementation skills are iterative and interwoven. TDD and feature development form a tight loop. Refactoring happens continuously. Pair programming applies to any of the above.

In brownfield work, implementation should start with the smallest safe slice and the tests that protect coexistence or contract behavior before new code expands.

If implementation discovers that requirements or architecture are materially wrong, produce a `course-correction-note` and jump directly to `01-specification` or `02-architecture` instead of silently patching around the mismatch.

## Anti-Patterns

- **Big bang integration.** Building all components in isolation and integrating at the end. Integrate early and continuously.
- **Skipping tests under pressure.** Cutting tests to meet a deadline creates a larger deadline problem later. Tests are not optional.
- **Gold-plating in code.** Implementing features beyond the spec because "it would be nice." Build what is specified, propose additions through the backlog.
- **Solo silos.** Each developer owns a component with no overlap. Rotate pairing partners and review across component boundaries.
- **Ignoring the scout rule.** Leaving code worse than you found it. Each change is an opportunity to improve the codebase incrementally.

## Cross-Cutting Matrix

See `rules/cross-cutting-matrix.yml` for `must_consider`, `must_produce`, `skip_when_fast_track`, and `conditional` cross-cutting obligations at this phase.
