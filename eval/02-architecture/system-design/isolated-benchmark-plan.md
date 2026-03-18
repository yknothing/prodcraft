# System Design Isolated Benchmark Plan

This benchmark exists to answer a routed-skill question:

**when `system-design` is deliberately invoked from reviewed upstream artifacts, does it produce a more decision-ready architecture artifact than baseline?**

## Validity Rules

- baseline runs must execute in an isolated temporary workspace outside the Prodcraft repo
- with-skill runs must execute in a separate isolated workspace containing only `./skill-under-test/SKILL.md`
- prompts must provide the same upstream artifact bundle to both branches
- baseline prompts must forbid local repo reads
- review must compare boundary discipline, trade-off quality, and downstream handoff quality, not just whether a diagram-like answer appears

## Scenario 1: Greenfield Core Product

Prompt:

`We have reviewed requirements for a first-release approvals workflow. Produce the system design needed before API design and task breakdown.`

Assertions:

- identifies architecture drivers before choosing style
- produces explicit component boundaries
- records unresolved questions instead of silently solving them in architecture
- captures at least one ADR-worthy decision with consequences

## Scenario 2: Brownfield Coexistence

Prompt:

`We have reviewed requirements for modernizing access reviews while legacy permissions remain in production. Produce the system design that preserves coexistence and reversible migration boundaries.`

Assertions:

- preserves legacy coexistence as a design constraint
- names seams, facades, or migration boundaries explicitly
- avoids big-bang replacement language
- prepares a cleaner handoff to `api-design` and `task-breakdown`

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is materially stronger than baseline on trade-off clarity and boundary discipline
- no scenario collapses directly into implementation sequencing as the primary artifact

## Review Focus

Do not score only for "looks architectural." Review for:

- whether drivers lead decisions rather than technology fashion
- whether open questions stay visible
- whether brownfield constraints are preserved instead of erased
- whether the result is more auditable and easier for downstream skills to consume
