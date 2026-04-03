# Tested Promotion Brief

Use this template when a `review` skill is being considered for promotion to `tested`.

Keep the brief small. Its purpose is to make the promotion decision auditable, not to restate the entire skill.

## Promotion Target

- `skill_name`: `problem-framing`
- `phase`: `00-discovery`
- `current_status`: `review`
- `evaluation_mode`: `routed`
- `promotion_target`: `tested`
- `current_wave`: `Wave 1`

## Why This Skill Is In Scope Now

- This skill is part of the public-release upstream chain between `intake` and specification/discovery execution.
- It is in scope now because the public path remains weak if route selection is strong but direction shaping is still only review-grade.
- If it stays at `review`, the public default path still depends on a key entry-stack layer that lacks tested-grade evidence.

## Existing Evidence

- `findings_path`: `eval/00-discovery/problem-framing/findings.md`
- `eval_strategy_path`: `eval/00-discovery/problem-framing/evals/eval-strategy.md`
- `benchmark_plan_path`: `eval/00-discovery/problem-framing/explicit-invocation-benchmark.md`
- `benchmark_results_path`: `eval/00-discovery/problem-framing/isolated-benchmark-review.md`
- `integration_test_path`: `eval/00-discovery/problem-framing/intake-handoff-review.md`
- other relevant evidence:
  - `eval/01-specification/requirements-engineering/problem-framing-handoff-review.md`
  - `eval/00-discovery/user-research/problem-framing-handoff-review.md`

Summarize only the evidence that still counts as current proof.

- Current proof is strongest on observability, non-goal preservation, and downstream handoff discipline.
- The current evidence now includes one isolated brownfield benchmark plus two downstream-consumption reviews, which is enough for a tested-grade routed judgment.

## Evidence Quality Checks

- contamination check:
  - the current primary benchmark artifact is isolated and auditable
  - an earlier semi-isolated review still exists, but it is no longer the primary promotion artifact
- downstream usefulness check:
  - yes; both `requirements-engineering` and `user-research` have consumed the artifact as a real upstream input

## Promotion Gaps

- gap: no clearly tested-grade isolated benchmark or cleaner execution drill
- why it blocks promotion: no longer blocking after the isolated brownfield rerun
- whether it is an evidence gap, contamination gap, or contract gap: closed evidence gap

## Proposed Smallest Honest Next Step

- exact scenario or fixture to use:
  - completed using the reviewed brownfield access-review modernization intake brief
- exact artifact to generate:
  - completed as `isolated-benchmark-review.md`
- exact success condition:
  - satisfied: current artifact shows stronger direction choice observability, preserves non-goals, avoids repeating intake, and materially improves downstream handoff quality
- what would still remain unresolved after this step:
  - security-review work for any later move beyond `tested`

## Promotion Decision

- decision: `promote`
- rationale:
  - the new isolated brownfield benchmark closes the main evidence-quality gap, and the existing handoff reviews already prove downstream usefulness
- evidence relied on:
  - current findings, isolated benchmark review, intake handoff review, downstream handoff reviews
- evidence explicitly not relied on:
  - any older exploratory signal that predates the current reviewed downstream chain

## Follow-Up

- validator/test commands to rerun:
  - `python3 scripts/validate_prodcraft.py`
  - `pytest -q`
- manifest changes required:
  - update `status` to `tested` and point `benchmark_results_path` at the isolated benchmark review
- eval artifact updates required:
  - completed for this batch
- docs or public-surface changes required:
  - none in this batch unless promotion is approved
- next skill in the wave:
  - `requirements-engineering`
