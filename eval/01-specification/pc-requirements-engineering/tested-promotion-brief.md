# Tested Promotion Brief

Use this template when a `review` skill is being considered for promotion to `tested`.

Keep the brief small. Its purpose is to make the promotion decision auditable, not to restate the entire skill.

## Promotion Target

- `skill_name`: `requirements-engineering`
- `phase`: `01-specification`
- `current_status`: `review`
- `evaluation_mode`: `routed`
- `promotion_target`: `tested`
- `current_wave`: `Wave 1`

## Why This Skill Is In Scope Now

- This skill is part of the public-release path from entry shaping into specification.
- It is in scope now because the public core path cannot honestly claim a tested upstream chain while requirements definition is still review-grade.
- If it stays at `review`, the strongest public route still weakens at the point where scoped direction turns into canonical requirements.

## Existing Evidence

- `findings_path`: `eval/01-specification/requirements-engineering/findings.md`
- `eval_strategy_path`: `eval/01-specification/requirements-engineering/evals/eval-strategy.md`
- `benchmark_plan_path`: `eval/01-specification/requirements-engineering/explicit-invocation-benchmark.md`
- `benchmark_results_path`: `eval/01-specification/requirements-engineering/problem-framing-routed-benchmark-review.md`
- `integration_test_path`: `eval/01-specification/requirements-engineering/intake-handoff-review.md`
- other relevant evidence:
  - `eval/01-specification/requirements-engineering/problem-framing-handoff-review.md`
  - `eval/01-specification/requirements-engineering/user-research-handoff-review.md`
  - `eval/01-specification/requirements-engineering/user-research-semi-isolated-benchmark-review.md`

Summarize only the evidence that still counts as current proof.

- Current proof is strongest on preserving release boundaries, non-goals, explicit open questions, and downstream handoff shape.
- The skill now has a clean isolated routed benchmark on the strongest public default chain plus substantial downstream review-stage evidence across more than one routed chain.

## Evidence Quality Checks

- contamination check:
  - the older explicit baseline remains contaminated and should stay non-primary
  - the new routed benchmark is isolated and now closes the main contamination gap
- downstream usefulness check:
  - yes; the skill has current routed evidence from both `problem-framing` and `user-research`

## Promotion Gaps

- gap: no single clean isolated benchmark or equivalent drill that can serve as tested-grade primary proof
- why it blocks promotion: no longer blocking after the clean routed benchmark completed on the public default chain
- whether it is an evidence gap, contamination gap, or contract gap: closed contamination gap

## Proposed Smallest Honest Next Step

- exact scenario or fixture to use:
  - completed using `problem-framing -> requirements-engineering` on the access-review modernization chain
- exact artifact to generate:
  - completed as `problem-framing-routed-benchmark-review.md`
- exact success condition:
  - satisfied: current benchmark shows stronger preservation of scope boundaries, non-goals, explicit assumptions, and downstream handoff than baseline without contamination
- what would still remain unresolved after this step:
  - any future discoverability work, which is not required for routed `tested`

## Promotion Decision

- decision: `promote`
- rationale:
  - the new routed benchmark closes the primary contamination gap and confirms the lift already suggested by broader handoff evidence
- evidence relied on:
  - current findings, routed handoff reviews, user-research downstream benchmark review, clean routed benchmark review
- evidence explicitly not relied on:
  - contaminated explicit baseline artifacts and trigger recall as a promotion gate

## Follow-Up

- validator/test commands to rerun:
  - `python3 scripts/validate_prodcraft.py`
  - `pytest -q`
- manifest changes required:
  - update `status` to `tested` and point `benchmark_results_path` at the clean routed benchmark review
- eval artifact updates required:
  - completed for this batch
- docs or public-surface changes required:
  - none in this batch unless promotion is approved
- next skill in the wave:
  - `system-design`
