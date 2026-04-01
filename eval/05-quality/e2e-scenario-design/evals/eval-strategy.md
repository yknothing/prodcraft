# E2E Scenario Design Eval Strategy

## Goal

Measure whether `e2e-scenario-design` improves deep scenario design beyond what a strong baseline can already do without the skill.

## Primary Success Criteria

The with-skill branch should outperform baseline on at least three of these dimensions:

- identifies the shallow-test structural failure mode instead of only listing missing cases
- starts from user journeys or release-boundary scenarios rather than a flat feature checklist
- designs at least one stateful, multi-step scenario with explicit re-entry or persistence validation
- covers at least two edge-case classes that are realistic for the target platform
- specifies business-state or cross-boundary assertions instead of UI-only checks

## Evidence Types

1. **Explicit benchmark**
   - compare baseline vs with-skill on web, mobile, and collaboration-style scenarios
   - record pass/fail judgments per expectation
2. **Routed handoff review**
   - start from `testing-strategy`
   - verify that the downstream scenario design preserves the upstream risk priorities
3. **Consumer review**
   - verify that a reviewer, CI owner, or implementation owner can use the resulting artifacts without re-inventing the scenario structure

## Failure Modes To Watch

- scenario advice stays generic and never becomes executable
- platform details dominate while business-state assertions remain weak
- the skill duplicates `testing-strategy` instead of deepening it
- edge cases are listed, but no layered suite structure is produced

## Current Review Gate

Keep the skill in `review` until at least one routed handoff review exists in addition to the current explicit benchmark evidence.
