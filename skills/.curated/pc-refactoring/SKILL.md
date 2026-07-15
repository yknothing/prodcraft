---
name: pc-refactoring
description: Use when existing code is correct but structurally costly to change, and the team needs to improve clarity, coupling, duplication, or seam quality without changing externally observable behavior.
metadata:
  phase: 04-implementation
  inputs:
  - source-code
  - test-suite
  - review-report
  - tech-debt-registry
  outputs:
  - source-code
  prerequisites:
  - pc-feature-development
  quality_gate: Behavior remains stable under tests, structural complexity is reduced, and the refactor stays narrow enough for confident review
  roles:
  - developer
  - tech-lead
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/04-implementation/pc-refactoring/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Refactoring

> Improve the design of working code without changing what the system does.

## Context

Refactoring keeps implementation quality from decaying between releases.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Choose One Structural Problem

Pick a focused target such as duplication, oversized functions, unstable seams, hidden dependencies, or naming that obscures intent. Define the invariant that must not change.

Avoid combining unrelated cleanup goals into one refactor.

### Step 2: Strengthen the Behavioral Safety Net

Before moving code, verify the tests protect the behavior that matters. Add characterization or regression coverage first if the current suite would allow a silent behavior change.

### Step 3: Refactor in Reversible Steps

Make the change as a sequence of small transformations:

- rename for clarity
- extract or inline with tests green
- move responsibilities to cleaner seams
- remove duplication after the new shape is proven

Run the relevant tests after every step.

### Step 4: Prove the Design Actually Improved

Before review, state what got better: smaller surface area, clearer boundaries, lower duplication, simpler control flow, or safer extension points. If you cannot name the gain, the change is probably unnecessary.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Tests prove behavior stayed stable
- [ ] The refactor addresses a concrete structural problem
- [ ] The change is narrow, reviewable, and reversible
- [ ] Complexity, coupling, or duplication is measurably lower
- [ ] No opportunistic feature work is mixed into the refactor

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/04-implementation/pc-refactoring/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
