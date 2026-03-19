# Intake Current Evidence Status

## Current Status

`intake` remains in `review`.

That status is intentional. The skill's current body contract changed after the entry-stack redesign, so previously gathered evidence should not be presented as if it directly proves the redesigned behavior.

## What Still Counts

- the historical trigger eval remains useful for understanding earlier discoverability behavior
- the historical benchmark remains useful for understanding the kind of routing discipline `intake` can add versus baseline
- the redesign notes remain valid context for why the skill returned to `review`
- the 2026-03-18 bucketed rerun in `optimization/iter-2/results-{core,overlap,non-trigger,mixed}.json` is current evidence for the tightened routing-only description that began `Route engineering work before execution.`
- the 2026-03-19 isolated Gemini benchmark in `post-redesign-benchmark-run-2026-03-19-gemini-naming-rerun` is current evidence for the redesigned body contract under explicit invocation
- the 2026-03-19 integration review in `post-redesign-integration-review.md` is current evidence that the generated `intake-brief` usually preserves enough routing context for downstream use

## New Evidence From 2026-03-18

A valid bucketed rerun was completed after Claude CLI preflight passed.

Results for the tightened routing-only description:

- core recall: `0/5`
- overlap recall: `0/5`
- non-trigger precision: `10/10`
- mixed continuity accuracy: `10/20`

Interpretation:

- false-positive control is strong
- the tightened metadata became too narrow to surface `intake` for its own highest-signal entry prompts
- this is now a valid product signal, not a quota artifact

After reviewing those results, the description was revised again to restore high-signal user language such as:

- building a new product, app, or internal tool
- starting from scratch
- migration
- multi-sprint tech-debt or documentation effort
- "not sure where to start"

That newer description has **not** been validly rerun yet.

## New Evidence From 2026-03-19

A clean isolated Gemini benchmark was completed after fixing runner-side Gemini startup-noise contamination.

Reviewed artifacts:

- `post-redesign-benchmark-run-2026-03-19-gemini-clean`
- `post-redesign-benchmark-run-2026-03-19-gemini-naming-rerun`

Current benchmark conclusion:

- baseline still drifts strongly into implementation plans or direct research execution
- with-skill output consistently restores routing discipline, approval gating, and observable handoff shape
- the redesign split with `problem-framing` is visible in current evidence, especially on fuzzy discovery requests
- a follow-up rerun after tightening downstream naming improved first-hop handoff specificity on the brownfield migration path

The same run also supported a manual integration review:

- `post-redesign-integration-review.md`

Current integration conclusion:

- the generated `intake-brief` now usually preserves enough context for downstream use
- the remaining quality gap is mostly later-stage route specificity, not missing routing context or first-hop handoff ambiguity

## Current Blocker

An immediate rerun of the updated description on **2026-03-18** was blocked by Claude quota:

- message: `You're out of extra usage · resets Mar 20, 6pm (Asia/Singapore)`

Treat the latest metadata revision as pending evaluation until a post-reset rerun completes.

## What No Longer Counts as Current Proof

The following artifacts are now treated as **historical evidence**, not current primary proof:

- `optimization/iter-2/results-mixed.json`
- `iteration-1/benchmark.md`

Why:

1. the redesigned `intake` is narrower and more explicitly routing-only
2. the redesigned skill now hands fuzzy routed cases to `problem-framing`
3. current QA needs to verify lower question load, stronger observability, and cleaner handoff behavior, not just the old trigger/benchmark shape

The following artifact is also treated as **superseded exploratory evidence**, not current primary proof:

- `post-redesign-benchmark-run-2026-03-19-gemini`
- `post-redesign-benchmark-run-2026-03-19-gemini-clean`

Why:

1. `post-redesign-benchmark-run-2026-03-19-gemini` was generated before the benchmark runner stripped Gemini MCP startup noise from stored responses
2. `post-redesign-benchmark-run-2026-03-19-gemini-clean` was generated before the skill body was tightened again to improve downstream handoff naming
3. `post-redesign-benchmark-run-2026-03-19-gemini-naming-rerun` now reflects the current body contract

## What Must Be Re-Generated

Before `intake` can move beyond `review`, regenerate:

1. a post-redesign trigger eval using the bucketed strategy in `evals/eval-strategy.md`
2. a tighter follow-up benchmark only if the skill body changes again after the 2026-03-19 clean benchmark
3. a deeper downstream execution drill if we want stronger proof than the current review of benchmark-produced handoff artifacts

The trigger-eval requirement now splits into two sub-parts:

1. keep the valid 2026-03-18 rerun as evidence that one tightened description regressed on core discoverability
2. rerun the current high-signal description after quota resets on **2026-03-20 18:00 Asia/Singapore**

## Repository Convention

`manifest.yml` now records the old artifacts under `historical_*_path` so the audit trail is preserved without overstating current evidence quality.
