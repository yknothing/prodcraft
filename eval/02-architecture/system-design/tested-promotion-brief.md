# Tested Promotion Brief

Use this template when a `review` skill is being considered for promotion to `tested`.

Keep the brief small. Its purpose is to make the promotion decision auditable, not to restate the entire skill.

## Promotion Target

- `skill_name`: `system-design`
- `phase`: `02-architecture`
- `current_status`: `review`
- `evaluation_mode`: `routed`
- `promotion_target`: `tested`
- `current_wave`: `Wave 1`

## Why This Skill Is In Scope Now

- This skill is the architecture link in the public-release upstream chain.
- It is in scope now because Wave 1 is meant to prove that Prodcraft can carry a routed request from entry shaping into architecture with tested-grade evidence.
- If it stays at `review`, the public path still lacks a tested architecture step even if earlier upstream routing becomes stronger.

## Existing Evidence

- `findings_path`: `eval/02-architecture/system-design/findings.md`
- `eval_strategy_path`: `eval/02-architecture/system-design/evals/eval-strategy.md`
- `benchmark_plan_path`: `eval/02-architecture/system-design/isolated-benchmark-plan.md`
- `benchmark_attempt_review_path`: `eval/02-architecture/system-design/isolated-benchmark-review.md`
- `benchmark_results_path`: none yet
- `integration_test_path`: `eval/02-architecture/system-design/requirements-handoff-review.md`
- other relevant evidence:
  - current findings summary for the brownfield modernization review

Summarize only the evidence that still counts as current proof.

- Current proof shows meaningful routed handoff lift on brownfield boundary preservation, unresolved-question handling, and downstream handoff shape.
- The benchmark design now exists and the baseline branch is clean, but the with-skill branch has not yet completed cleanly.

## Evidence Quality Checks

- contamination check:
  - no contamination issue is currently blocking the benchmark lane
  - the current blocker is runner instability on the with-skill branch, not a dirty baseline
- downstream usefulness check:
  - partially; the current handoff review suggests downstream usefulness, but a tested decision still needs a benchmark result

## Promotion Gaps

- gap: no clean with-skill completion exists for the isolated brownfield benchmark
- why it blocks promotion: a routed skill cannot honestly move to `tested` while the benchmark lane fails before producing the skill-applied artifact
- whether it is an evidence gap, contamination gap, or contract gap: execution-lane gap

## Proposed Smallest Honest Next Step

- exact scenario or fixture to use:
  - the current brownfield access-review modernization scenario already used in the handoff review
- exact artifact to generate:
  - a clean with-skill completion for the existing isolated benchmark plus an updated benchmark review
- exact success condition:
  - current benchmark shows stronger architecture boundary discipline, coexistence preservation, unresolved-question handling, and downstream handoff than baseline
- what would still remain unresolved after this step:
  - whether a second spec-driven comparison scenario is still needed before promotion

## Promotion Decision

- decision: `hold`
- rationale:
  - the skill is blocked by a failed with-skill benchmark lane, not by unclear skill value
- evidence relied on:
  - current findings, current eval strategy, current requirements handoff review, isolated benchmark attempt review
- evidence explicitly not relied on:
  - the benchmark plan alone, which is not promotion evidence

## Follow-Up

- validator/test commands to rerun:
  - `python3 scripts/validate_prodcraft.py`
  - `pytest -q`
- manifest changes required:
  - add `benchmark_results_path` only after a clean with-skill benchmark artifact exists
- eval artifact updates required:
  - rerun the same isolated benchmark and replace the current attempt review with a clean result review
- docs or public-surface changes required:
  - none in this batch unless promotion is approved
- next skill in the wave:
  - `requirements-engineering`
