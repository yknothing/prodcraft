# User Research Semi-Isolated Benchmark

## Purpose

This benchmark exists to answer a stronger question than the basic handoff review:

**when `user-research` is deliberately invoked from a `problem-frame`, does it produce a cleaner discovery plan than a baseline response under a fixed brownfield B2B/SaaS scenario?**

This is still **semi-isolated manual benchmark** evidence, not a true isolated runtime benchmark.

## Why This Benchmark Exists

The handoff review already showed useful signal, but the next meaningful step is to tighten the evidence:

- fixed fixture
- fixed baseline vs with-skill prompts
- copied `skill-under-test/SKILL.md`
- explicit review for repo-local context contamination

This gives stronger evidence than a loose narrative review while remaining honest about the lack of an external runtime harness.

## Benchmark Scenario

- `seat-guest-management-problem-framing-handoff`

Why this scenario is the preferred stress case:

- it is a classic B2B/SaaS brownfield admin-modernization problem
- it includes coexistence pressure from an existing seat model
- it forces the skill to separate guest collaboration, seat governance, and procurement concerns without collapsing into requirements too early

## Validity Rules

- baseline and with-skill branches must both be preserved
- both branches must use the same fixture
- the with-skill branch must snapshot only `./skill-under-test/SKILL.md`
- prompts and raw outputs must be stored for auditability
- the review must check for repo-local context contamination
- the review must state the evidence tier explicitly

## What a Good Delta Looks Like

Relative to baseline, with-skill should:

- preserve `guest-first coexistence` as the direction being validated
- keep brownfield coexistence and non-goals explicit
- translate unresolved questions into sharper research questions
- define the evidence threshold before `requirements-engineering` may begin
- stay in discovery rather than sliding into specification, pricing redesign, or policy-system design

## Preferred Next Stronger Step

After this semi-isolated benchmark, the next stronger evidence step is either:

1. a true isolated benchmark with an external runtime harness
2. a cross-reviewer execution drill on the same brownfield fixture
