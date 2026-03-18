# Intake Post-Redesign Benchmark Plan

This benchmark exists to answer the post-redesign question:

**does the current routing-only `intake` still improve lifecycle entry discipline without drifting back into a full design workshop?**

## Validity Rules

- baseline and with-skill runs must execute in isolated temporary workspaces outside the Prodcraft repo
- with-skill runs may read only `./skill-under-test/SKILL.md`
- baseline runs must not read local repo files
- both branches must receive the same user request and surrounding task context
- review must compare routing quality, approval-gate discipline, question load, and downstream handoff clarity

## Scenario 1: New Feature With Ambiguous Scope

Prompt:

`Add dark mode to the settings experience, but we are not sure whether this belongs only in web settings or across all surfaces.`

Assertions:

- produces an `intake-brief`
- classifies work type and entry phase clearly
- chooses a workflow and records key risks
- keeps questions to the minimum needed for routing
- does not expand into detailed architecture or solution ideation

## Scenario 2: Large Migration Request

Prompt:

`We need to move our legacy permissions model to a new access-review system over several quarters.`

Assertions:

- routes to a brownfield/discovery-appropriate path
- records why a multi-phase workflow is needed
- preserves uncertainty instead of inventing a concrete migration plan
- names the next skill or handoff destination explicitly

## Scenario 3: Fuzzy but Research-Oriented Request

Prompt:

`We think admins hate the current seat management flow, but we are not sure whether the real issue is permissions, procurement, or guest users.`

Assertions:

- recognizes that the route is known but direction remains fuzzy
- keeps intake focused on routing rather than doing the framing itself
- hands off cleanly to `problem-framing` or another discovery skill
- captures enough observability for downstream work

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is materially stronger than baseline on approval gating and routing clarity
- question load remains low unless additional questions demonstrably change routing
- no scenario turns into an architecture/specification answer as the primary output
