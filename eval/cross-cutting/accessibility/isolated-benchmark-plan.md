# Accessibility Isolated Benchmark Plan

## Goal

Prove that `accessibility` turns a concrete UI surface into a reviewable accessibility contract that downstream `acceptance-criteria` work can consume directly.

## Planned Scenario

1. `invite-modal-accessibility-contract`
   - a user-facing invite modal with validation, async submission, success, and error states

## Comparison

1. a generic baseline prompt
2. the same prompt with explicit `accessibility` skill invocation

## Assertions

1. `names-the-affected-surface`
   - the output identifies the specific controls, states, and interactions in scope
2. `covers-keyboard-focus-semantics-feedback-and-contrast`
   - the contract covers keyboard access, focus order/return, labels/semantics, announcements/error feedback, and visual contrast or non-visual equivalent cues
3. `stays-at-contract-level`
   - the output avoids drifting into redesign or implementation detail
4. `produces-reviewable-checks`
   - QA and reviewers can execute the result without inventing extra policy
5. `prepares-acceptance-handoff`
   - the result can be translated into downstream acceptance criteria directly

## Candidate Inputs

- `fixtures/invite-modal-ui-summary.md`
- `fixtures/invite-modal-product-constraints.md`

## Exit Criteria for Tested Promotion

- one clean benchmark run exists for the invite-modal slice
- one routed handoff review shows the resulting accessibility contract is directly usable by downstream acceptance-criteria work
