# Internationalization Evaluation Strategy

## Goal

Evaluate whether `internationalization` converts a user-facing change into explicit locale behavior, formatting rules, and fallback policy that survive implementation and QA.

## Why Routed Review First

This skill is routed because it is applied to a concrete flow with known locale-sensitive behavior, not to generic text discovery.
Review-stage evidence should show the skill can expose translation scope and locale risk before implementation hardens the wrong assumptions.

## Scenarios

1. A multi-language invite or onboarding screen with string expansion and fallback behavior.
2. A date, number, or currency display flow where locale formatting must be correct.
3. A pluralization or mixed-language copy case where layout and grammar may diverge across locales.

## Assertions

1. Affected strings and locale-sensitive formats are identified explicitly.
2. Missing translation and unsupported-locale fallback behavior are documented.
3. Formatting rules for date, time, number, currency, or plural logic are concrete.
4. Layout expansion or truncation risk is acknowledged where text length changes.
5. The result gives reviewers enough information to verify locale behavior without guessing policy.

## Method

1. Draft a baseline locale note for the same flow without the skill.
2. Draft a second note with `internationalization` explicitly invoked.
3. Compare whether the second output names the locale surface, fallback rules, and QA checks more precisely.
4. Record whether the skill turns translation work into a reviewable contract instead of a string-extraction task.

## Exit Criteria for Review Stage

- The locale surface is bounded and explicit.
- Fallback and formatting rules are written down.
- QA checks are actionable for at least one locale-sensitive scenario.
- The skill makes locale behavior easier to implement and review than the baseline.
