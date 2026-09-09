---
name: pc-refactoring
description: Use when existing structure creates a concrete maintenance cost or risk and a bounded change can improve it while preserving externally observable behavior.
metadata:
  phase: 04-implementation
  inputs:
  - source-code
  - test-suite
  - review-report
  - tech-debt-registry
  outputs:
  - source-code
  prerequisites: []
  quality_gate: The targeted maintenance problem improves with explicit before/after evidence while behavior and compatibility remain stable
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

Refactoring keeps implementation quality from decaying between releases.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Name the Cost and the Preservation Boundary

Identify one costly change path, duplication problem, hidden dependency, or unclear responsibility. Show where it causes work or risk and state what must stay stable: results, errors, ordering, side effects, persisted data, and public interfaces as applicable. Existing code need not have been produced by Prodcraft.

Compare the smallest local change with leaving the code alone. A new layer, generic framework, or future extension point needs a present benefit. Do not mix a behavior correction into structural work; route that separately when approved.

### Step 2: Establish Relevant Behavioral Protection

Inspect existing tests and real callers. Add characterization for uncovered preservation boundaries before moving code. Preserve known behavior, including unusual edge cases, unless a separate change is approved. If evidence is insufficient, narrow the transformation or report the blocked boundary rather than claiming equivalence.

### Step 3: Change in Reversible Increments

Rename, move, extract, inline, or consolidate only what addresses the chosen problem. Keep a usable rollback point and verify at each meaningful transformation; dependent moves can share one coherent check. Avoid updating tests merely to endorse changed behavior. Test doubles may isolate external dependencies, not replace the code being refactored.

### Step 4: Compare the Result With the Original Cost

Show the same concrete maintenance operation before and after: fewer places to edit, a clearer dependency direction, or a directly testable boundary. Quantify a relevant metric when useful; do not require every complexity, coupling, or line-count metric to decrease. Explain any added indirection and its payoff. If the benefit does not justify it, simplify or revert the refactor.

Hand off the changed source with preservation evidence, the demonstrated benefit, and any unverified scope. Tests support the checked boundaries; they do not prove universal equivalence.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] One concrete maintenance cost or risk has improved with before/after evidence
- [ ] Relevant preservation boundaries are checked and unverified scope is explicit
- [ ] The change is narrow, reviewable, and reversible
- [ ] Added structure is justified and no unapproved behavior change is hidden in it
