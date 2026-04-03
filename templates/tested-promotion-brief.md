# Tested Promotion Brief

Use this template when a `review` skill is being considered for promotion to `tested`.

Keep the brief small. Its purpose is to make the promotion decision auditable, not to restate the entire skill.

## Promotion Target

- `skill_name`:
- `phase`:
- `current_status`:
- `evaluation_mode`:
- `promotion_target`: `tested`
- `current_wave`:

## Why This Skill Is In Scope Now

- why this skill matters to the current public-release path
- why it is being promoted now instead of later
- what would break or remain weak if it stays at `review`

## Existing Evidence

- `findings_path`:
- `eval_strategy_path`:
- `benchmark_plan_path`:
- `benchmark_results_path`:
- `integration_test_path`:
- other relevant evidence:

Summarize only the evidence that still counts as current proof.

## Evidence Quality Checks

- contamination check:
  - does the baseline avoid repo-local instructions, neighboring skills, and template leakage?
  - if not, what exactly is contaminated?
- downstream usefulness check:
  - does the current evidence show real handoff or consumer value, not just a plausible standalone output?

## Promotion Gaps

List the smallest remaining gaps that still block `tested`.

For each gap record:

- gap:
- why it blocks promotion:
- whether it is an evidence gap, contamination gap, or contract gap

## Proposed Smallest Honest Next Step

- exact scenario or fixture to use
- exact artifact to generate
- exact success condition
- what would still remain unresolved after this step

## Promotion Decision

- decision: `promote` / `hold` / `redesign`
- rationale:
- evidence relied on:
- evidence explicitly not relied on:

## Follow-Up

- validator/test commands to rerun:
- manifest changes required:
- eval artifact updates required:
- docs or public-surface changes required:
- next skill in the wave:
