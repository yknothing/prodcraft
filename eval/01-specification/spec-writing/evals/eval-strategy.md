# Spec Writing Eval Strategy

## Goal

Evaluate whether `spec-writing` turns reviewed requirements into a shared specification that fixes scope, non-goals, interfaces, rollout concerns, and open questions before architecture or implementation begins.

## Why Routed Review First

This is a routed specification skill. Its review should check that the doc is strong enough for engineers to build from without guessing, while still staying above implementation detail. The core question is whether the spec creates a clean contract for downstream architecture work.

## Scenarios

Use two review scenarios:

1. A spec-driven first-release feature where the team needs a single written contract.
2. A brownfield modernization spec where coexistence, compatibility, and rollout constraints must stay explicit.

## Assertions

1. The spec follows the expected structure and completes the required sections.
2. Goals, non-goals, interfaces, testing, and rollout are all explicit.
3. Open questions are either resolved or called out as blocking the next phase.
4. The spec stays at WHAT level and does not drift into implementation details.
5. Security, edge cases, and rollout risks are visible enough for downstream review.
6. The document is specific enough for `system-design` to consume without reverse-engineering scope.

## Method

Compare a baseline requirements-to-spec outline with a version produced using `spec-writing` on the same input. Review the two outputs for:

- scope clarity
- completeness of the contract
- whether unresolved questions remain visible
- whether the result is actionable for architecture

## Exit Criteria

Promote the skill to `review` when the spec can be handed to architecture without hidden assumptions. If reviewers still need to infer scope, non-goals, or rollout constraints, the skill remains too weak.
