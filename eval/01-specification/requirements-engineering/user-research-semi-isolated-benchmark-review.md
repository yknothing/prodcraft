# Requirements Engineering from User Research Semi-Isolated Benchmark Review

## Scope

This review summarizes the current **semi-isolated manual benchmark** evidence for `requirements-engineering` consuming `user-research` outputs.

It does **not** claim automated isolated benchmark status. The run under review preserves:

- separate baseline and with-skill branches
- a copied `skill-under-test/SKILL.md`
- prompts and raw outputs per branch
- fixed persona and journey fixtures

but the outputs were still authored in one reviewer context.

## Reviewed Artifacts

| Artifact | Scenario | Notes |
|---|---|---|
| `user-research-handoff-manual-run-2026-03-17-team-invite` | `team-invite-user-research-handoff` | Non-brownfield comparison case |
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

| Scenario | Baseline | With skill | Judgment |
|---|---|---|---|
| `team-invite-user-research-handoff` | Produces a plausible invite requirements draft, but enterprise and later-stage onboarding concerns re-enter the draft too easily and evidence traceability is light | Keeps `email-invite-first` explicit, preserves later enterprise paths as non-goals or open questions, and ties requirements more clearly to persona/journey signals | **Positive lift** |
| `seat-guest-management-user-research-handoff` | Produces a plausible requirements draft, but broadens the admin problem and weakens segment separation | Keeps `guest-first coexistence` explicit, preserves brownfield non-goals, and ties obligations back to persona/journey evidence more cleanly | **Positive lift** |

## What the Benchmark Shows

### 1. The skill adds value under deliberate routed invocation

Baseline can already produce a plausible requirements draft. The with-skill delta is strongest on:

- preserving release-1 scope discipline
- keeping non-goals explicit
- making persona and journey evidence more auditable
- preventing governance-heavy secondary concerns from silently becoming the default design center

### 2. The signal is no longer brownfield-only

The non-brownfield `team-invite` case shows the same underlying value pattern:

- better preservation of the chosen release-1 path
- clearer non-goals
- cleaner traceability from user evidence into requirements

The brownfield case remains the stronger stress test, but the lift is now visible in both environments.

### 3. The evidence is stronger, but still not final-form

This benchmark is stronger than plain downstream review, but weaker than a true isolated run. It is enough to strengthen `review` confidence, not enough to justify `tested`.

## Current Judgment

`requirements-engineering` now has credible review-stage evidence that it:

- is strong as a **routed specification skill**
- can consume evidence-backed user-research fixtures without flattening them into generic admin requirements
- is especially valuable in classic B2B/SaaS brownfield scope-setting work

## Next Required Evidence

1. run a true isolated benchmark or cross-reviewer execution drill on the preferred brownfield scenario
2. keep the non-brownfield case as a standing comparison scenario in future reruns
