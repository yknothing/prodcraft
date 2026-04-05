# Accessibility Evaluation Strategy

## Goal

Evaluate whether `accessibility` turns a user-facing flow into a concrete accessibility contract that implementation and QA can verify without inventing extra rules.

## Why Routed Review First

This skill is routed because it is applied to a known UI or flow, not discovered from metadata alone.
Review-stage evidence should prove the skill can translate a real surface into keyboard, semantics, feedback, and contrast requirements.

## Scenarios

1. A sign-in or invite modal with keyboard focus, error messaging, and dismiss behavior.
2. A form flow with inline validation, assistive text, and status announcements.
3. A destructive confirmation screen where contrast, labels, and focus return matter.

## Assertions

1. Affected UI surfaces are named explicitly.
2. Keyboard access, focus order, and visible focus are documented.
3. Semantic structure, labels, and error/announcement behavior are concrete.
4. Contrast and non-visual feedback are covered for the affected states.
5. The output is specific enough for reviewers to verify without making up accessibility policy on the fly.

## Method

1. Produce a baseline accessibility note for the same UI surface without the skill.
2. Produce a second note with `accessibility` explicitly invoked.
3. Compare specificity, completeness, and implementation-readiness of the resulting contract.
4. Check whether gaps are turned into explicit remediation steps rather than generic standards.

## Exit Criteria for Review Stage

- The affected surface and states are unambiguous.
- The output contains actionable checks for keyboard, semantics, focus, feedback, and contrast.
- QA can execute the result without adding new accessibility rules.
- The skill improves the clarity of the accessibility contract over baseline.
