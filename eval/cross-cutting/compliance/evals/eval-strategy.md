# Compliance Evaluation Strategy

## Goal

Evaluate whether `compliance` translates a binding policy, contract, or regulatory obligation into engineering controls, evidence requirements, and release checkpoints.

## Why Routed Review First

This skill is routed because compliance is only meaningful when tied to a real policy and affected system boundary.
Review-stage evidence should prove the skill can separate binding obligations from preferences and make the release risk explicit.

## Scenarios

1. A data-retention or deletion obligation affecting stored user records.
2. A regulated release path requiring approval evidence before deployment.
3. A contractual data-handling requirement that changes architecture, logging, or rollback constraints.

## Assertions

1. Binding obligations are identified with source context.
2. Each obligation is mapped to a concrete engineering control.
3. Evidence and approval checkpoints are explicit before release.
4. Unresolved risk is named with an owner and escalation path.
5. The output is strong enough for planning, implementation, and release review to use directly.

## Method

1. Create a baseline compliance note from the same policy without the skill.
2. Create a second note with `compliance` explicitly invoked.
3. Compare whether the routed output is more specific about controls, evidence, and checkpoints.
4. Check that the result does not blur legal obligations with optional best practices.

## Exit Criteria for Review Stage

- The policy or obligation source is explicit.
- Required controls are mapped to engineering work.
- Evidence and approval checkpoints are concrete.
- The output makes the release risk and ownership clear enough for downstream planning.
