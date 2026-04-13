# Domain Modeling Isolated Benchmark Plan

## Goal

Prove that `domain-modeling` turns reviewed requirements into a clearer shared vocabulary, entity model, and boundary map than a generic baseline.

## Planned Scenario

- `access-review-modernization-domain-model`

This scenario uses a brownfield access-review modernization slice where release-1 coexistence, tenant-specific policy terms, and evidence-retention concepts are all present at once.

## Comparison

1. baseline generic domain-summary prompt
2. the same prompt with explicit `domain-modeling` skill invocation

## Assertions

1. `core-entities-are-explicit`
   - the output identifies the main business entities without collapsing into tables or services
2. `ubiquitous-language-is-resolved`
   - ambiguous or overlapping terms are normalized into a shared glossary
3. `brownfield-boundaries-stay-visible`
   - legacy-only or compatibility-only concepts remain explicit instead of silently becoming the future canonical model
4. `bounded-contexts-are-justified`
   - contexts are introduced only when the slice actually needs them
5. `prepares-downstream-handoff`
   - the resulting artifact is usable by `spec-writing`, `api-design`, or `data-modeling`

## Candidate Inputs

- `fixtures/access-review-modernization-requirements.md`

## Exit Criteria for Tested Promotion

- one clean benchmark run exists for the bounded brownfield slice
- one routed handoff review shows a downstream consumer can use the domain model directly
