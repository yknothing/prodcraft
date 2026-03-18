---
name: refactoring
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
  - feature-development
  quality_gate: Behavior remains stable under tests, structural complexity is reduced, and the refactor stays narrow enough for confident review
  roles:
  - developer
  - tech-lead
  methodologies:
  - all
  effort: medium
---

# Refactoring

> Improve the design of working code without changing what the system does.

## Context

Refactoring keeps implementation quality from decaying between releases. It is not cleanup for its own sake. In Prodcraft, refactoring is justified when reviews, tech-debt evidence, or repeated implementation friction show that the current structure is increasing future cost or risk.

The constraint is strict: externally observable behavior must stay stable. If behavior changes, the work is feature development or defect fixing, not refactoring.

## Inputs

- **source-code** -- The current implementation that needs structural improvement.
- **test-suite** -- The safety net that proves behavior has not changed.
- **review-report** -- Concrete findings from review that identify structural problems worth fixing.
- **tech-debt-registry** -- Evidence that the refactor addresses recurring cost rather than personal preference.

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

- **source-code** -- Behaviorally equivalent code with improved structure and lower ongoing change cost.

## Quality Gate

- [ ] Tests prove behavior stayed stable
- [ ] The refactor addresses a concrete structural problem
- [ ] The change is narrow, reviewable, and reversible
- [ ] Complexity, coupling, or duplication is measurably lower
- [ ] No opportunistic feature work is mixed into the refactor

## Anti-Patterns

1. **Refactor by intuition** -- changing structure because it "feels cleaner" without evidence of real cost.
2. **Behavior change in disguise** -- sneaking in requirement changes under the label of cleanup.
3. **Unsafe large-step rewrite** -- moving too much code at once to reason about regressions.
4. **Testless cleanup** -- improving structure without a safety net strong enough to catch breakage.

## Related Skills

- [feature-development](../feature-development/SKILL.md) -- produces the working slice that may reveal structural friction
- [tdd](../tdd/SKILL.md) -- provides the behavioral safety net
- [code-review](../../05-quality/code-review/SKILL.md) -- validates the refactor stayed behavior-preserving and worthwhile
- [tech-debt-management](../../08-evolution/tech-debt-management/SKILL.md) -- prioritizes larger or recurring refactor targets
