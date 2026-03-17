# Requirements Engineering from User Research Semi-Isolated Benchmark

## Purpose

This benchmark exists to answer a stronger question than the basic downstream handoff review:

**when `requirements-engineering` is deliberately invoked from evidence-backed user-research artifacts, does it produce a cleaner release-1 requirements set than a baseline response under a fixed brownfield B2B/SaaS scenario?**

This is still **semi-isolated manual benchmark** evidence, not a true isolated runtime benchmark.

## Why This Benchmark Exists

The manual downstream review already showed useful signal, but the next meaningful step is to tighten the evidence:

- fixed user-research fixture
- fixed baseline vs with-skill prompts
- copied `skill-under-test/SKILL.md`
- explicit contamination review

This makes the evidence stronger than a loose review while still staying honest about the lack of an external harness.

## Benchmark Scenario

- `seat-guest-management-user-research-handoff`

Why this is the preferred routed benchmark:

- it is a representative classic B2B/SaaS brownfield case
- it tests whether requirements stay grounded in user evidence rather than drifting into a broad admin-program rewrite
- it forces the skill to preserve release-1 non-goals while still writing actionable requirements

## Validity Rules

- baseline and with-skill branches must both be preserved
- both branches must use the same persona and journey fixtures
- the with-skill branch must snapshot only `./skill-under-test/SKILL.md`
- prompts and raw outputs must be stored for auditability
- the review must check for repo-local context contamination
- the review must state clearly that the upstream research artifacts are QA fixtures, not real production field data

## What a Good Delta Looks Like

Relative to baseline, with-skill should:

- preserve guest-first coexistence as the release-1 boundary
- keep pricing redesign, org-wide policy, and forced seat migration explicit as non-goals
- translate persona and journey evidence into traceable P0/P1 requirements
- keep governance-heavy enterprise pressure as open questions or later-scope triggers instead of silently mixing it into day-one scope
- stay in the requirements layer and prepare a clean downstream handoff

## Preferred Next Stronger Step

After this semi-isolated benchmark, the next stronger evidence step is either:

1. a true isolated benchmark with an external runtime harness
2. a cross-reviewer execution drill on the same brownfield fixture
