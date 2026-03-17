# Requirements Engineering from User Research Semi-Isolated Benchmark Review

## Scope

This review summarizes the current **semi-isolated manual benchmark** evidence for `requirements-engineering` consuming `user-research` outputs.

It does **not** claim automated isolated benchmark status. The run under review preserves:

- separate baseline and with-skill branches
- a copied `skill-under-test/SKILL.md`
- prompts and raw outputs per branch
- fixed persona and journey fixtures

but the outputs were still authored in one reviewer context.

## Reviewed Artifact

| Artifact | Scenario | Notes |
|---|---|---|
| `user-research-handoff-manual-run-2026-03-17-seat-guest` | `seat-guest-management-user-research-handoff` | Preferred classic B2B/SaaS brownfield downstream benchmark |

## Fixture Honesty Note

The upstream persona and journey artifacts are QA fixtures shaped like completed user-research outputs. They are suitable for testing downstream consumption quality, but they are not real customer field data.

## Contamination Review

This run is stronger than a loose manual review because:

- the prompts reference only the user-research fixtures and the skill under test
- the outputs do not reference repo structure, neighboring skills, templates, or local project instructions
- the comparison is anchored to one fixed brownfield scenario rather than a general subjective impression

This run is **not** fully isolated because the same reviewer authored both branches.

## Cross-Branch Review

| Dimension | Baseline | With skill | Judgment |
|---|---|---|---|
| specification boundary | stays mostly in specification, but broadens the admin problem quickly | stays in specification and keeps the release-1 problem narrower | **Positive lift** |
| evidence traceability | captures major themes, but source linkage is light | links requirements more clearly back to persona and journey evidence | **Positive lift** |
| non-goals | mostly sensible, but under-specified | explicit and stable throughout the draft | **Positive lift** |
| primary vs contrast segment pressure | tends to blend guest collaboration and governance-heavy needs | keeps the primary guest-first segment centered and pushes governance-heavy signals into later-scope questions | **Positive lift** |
| downstream handoff | usable for later design | cleaner handoff into `system-design` and `acceptance-criteria` | **Positive lift** |

## What the Benchmark Shows

### 1. The skill adds value under deliberate routed invocation

Baseline can already produce a plausible requirements draft. The with-skill delta is strongest on:

- preserving release-1 scope discipline
- keeping non-goals explicit
- making persona and journey evidence more auditable
- preventing governance-heavy secondary concerns from silently becoming the default design center

### 2. The brownfield SaaS case is a good stress test

This scenario is harder than a generic feature request because it sits at the boundary between collaboration needs, admin controls, and commercial pressure. The skill helps keep the first release problem narrow enough to specify.

### 3. The evidence is stronger, but still not final-form

This benchmark is stronger than plain downstream review, but weaker than a true isolated run. It is enough to strengthen `review` confidence, not enough to justify `tested`.

## Current Judgment

`requirements-engineering` now has credible review-stage evidence that it:

- is strong as a **routed specification skill**
- can consume evidence-backed user-research fixtures without flattening them into generic admin requirements
- is especially valuable in classic B2B/SaaS brownfield scope-setting work

## Next Required Evidence

1. run a true isolated benchmark or cross-reviewer execution drill on this same scenario
2. keep the same rigor for one non-brownfield user-research handoff so the signal is not brownfield-only
