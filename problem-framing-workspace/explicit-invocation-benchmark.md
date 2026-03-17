# Problem Framing Explicit Invocation Benchmark

This benchmark exists to answer a different question from trigger evaluation:

**when `problem-framing` is deliberately invoked after intake, does it produce a cleaner direction artifact than a baseline response?**

`problem-framing` is an entry-stack routed skill. Its benchmark should therefore focus on:

- **usability discipline**: does it keep additional questioning low?
- **observability**: does it leave behind a more auditable record of why a direction was chosen?
- **handoff quality**: does it prepare a clearer next step for downstream lifecycle work?

## Evidence Tier

Current evidence for this benchmark is **semi-isolated manual benchmark evidence**, not automated isolated benchmark evidence.

Why "semi-isolated":

- each scenario has separate baseline and with-skill branches
- the with-skill branch snapshots only `./skill-under-test/SKILL.md`
- prompts and raw outputs are preserved as checked-in artifacts

Why not "fully isolated":

- both branches were authored in one reviewer context rather than executed by an external runtime harness
- this means the evidence is stronger than a loose narrative review, but weaker than a true isolated benchmark

## Validity Rules for Current Review

- baseline and with-skill outputs must both be preserved
- each scenario must preserve the skill snapshot under test
- review must compare quality deltas, not just binary pass/fail
- findings must state the evidence tier explicitly

## Current Scenarios

### Scenario 1: Team Invite Product Direction

Fixture:
- `fixtures/team-invite-product-intake-brief.md`

What it tests:
- whether `problem-framing` avoids forcing enterprise scope into release 1
- whether it records invocation reason, non-goals, and next destination more clearly than baseline

### Scenario 2: Access Review Modernization Direction

Fixture:
- `fixtures/access-review-modernization-intake-brief.md`

What it tests:
- whether `problem-framing` preserves brownfield coexistence constraints
- whether it avoids prematurely turning release framing into migration or architecture decisions

## What a Good Delta Looks Like

Relative to baseline, with-skill should:

- make the invocation reason explicit
- record low or zero additional question load when intake is already sufficient
- preserve non-goals and open questions instead of silently resolving them
- compare 2-3 directions with sharper trade-off framing
- name a cleaner next lifecycle destination

## Next Stronger Evidence Step

Use one of the existing scenarios in a true isolated benchmark harness or a cross-reviewer execution drill so the current semi-isolated signal can be checked against a cleaner baseline.
