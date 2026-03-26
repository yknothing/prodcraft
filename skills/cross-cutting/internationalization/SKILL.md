---
name: internationalization
description: Use when user-facing text, locale-sensitive formatting, or multi-language behavior need explicit rules so copy, layout, and data presentation stay correct across locales.
metadata:
  phase: cross-cutting
  inputs: []
  outputs:
    - localization-guidance
  prerequisites: []
  quality_gate: Locale behavior, translation scope, and fallback rules are documented well enough for implementation and QA
  roles:
    - developer
    - product-manager
    - qa-engineer
  methodologies:
    - all
  effort: medium
---

# Internationalization

> Treat locale behavior as a system contract, not as a late translation task.

## Context

Use this skill when the work introduces or changes user-facing text, date and number formatting, pluralization, locale selection, or language fallback behavior.

## Inputs

- The affected user-facing flows or interfaces
- Supported locales, if already known
- Existing copy and formatting constraints

## Process

### Step 1: Define the locale surface

Identify all strings, formats, and locale decisions touched by the change.

### Step 2: Make fallback rules explicit

Document what happens when a translation is missing, a locale is unsupported, or layout expands because text length changes.

### Step 3: Capture formatting requirements

Record how dates, times, numbers, currency, and plural rules must behave.

### Step 4: Turn requirements into review checks

Describe what implementation and QA must verify before release.

## Outputs

- **localization-guidance** -- translation scope, formatting rules, fallback behavior, and QA checks for the affected surface

## Quality Gate

- [ ] Affected user-facing strings and locale-sensitive formats are identified
- [ ] Fallback behavior is explicit
- [ ] Reviewers can verify locale behavior without inventing policy during QA

## Anti-Patterns

1. **String extraction only** -- moving text to resource files does not solve locale behavior.
2. **English-first assumptions** -- hard-coded length, grammar, or format rules break quickly.
3. **No fallback policy** -- missing translations become runtime chaos if not designed upfront.

## Related Skills

- [requirements-engineering](../../01-specification/requirements-engineering/SKILL.md) -- records locale expectations in the spec
- [feature-development](../../04-implementation/feature-development/SKILL.md) -- implements the locale contract
- [documentation](../documentation/SKILL.md) -- records supported locale policy
