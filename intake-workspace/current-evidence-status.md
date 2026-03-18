# Intake Current Evidence Status

## Current Status

`intake` remains in `review`.

That status is intentional. The skill's current body contract changed after the entry-stack redesign, so previously gathered evidence should not be presented as if it directly proves the redesigned behavior.

## What Still Counts

- the historical trigger eval remains useful for understanding earlier discoverability behavior
- the historical benchmark remains useful for understanding the kind of routing discipline `intake` can add versus baseline
- the redesign notes remain valid context for why the skill returned to `review`

## What No Longer Counts as Current Proof

The following artifacts are now treated as **historical evidence**, not current primary proof:

- `optimization/iter-2/results-mixed.json`
- `iteration-1/benchmark.md`

Why:

1. the redesigned `intake` is narrower and more explicitly routing-only
2. the redesigned skill now hands fuzzy routed cases to `problem-framing`
3. current QA needs to verify lower question load, stronger observability, and cleaner handoff behavior, not just the old trigger/benchmark shape

## What Must Be Re-Generated

Before `intake` can move beyond `review`, regenerate:

1. a post-redesign trigger eval using the bucketed strategy in `evals/eval-strategy.md`
2. a post-redesign benchmark focused on routing discipline, approval gating, and handoff quality
3. an integration review that checks whether the `intake-brief` now supports direct downstream use and `problem-framing` handoff without missing routing context

## Repository Convention

`manifest.yml` now records the old artifacts under `historical_*_path` so the audit trail is preserved without overstating current evidence quality.
