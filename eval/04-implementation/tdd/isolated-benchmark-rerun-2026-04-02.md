# TDD Isolated Benchmark Rerun - 2026-04-02

## Scope

This note records the `2026-04-02` repository-owned rerun of `eval/04-implementation/tdd/isolated-benchmark.json` using the repaired benchmark runner.

The goal of this rerun was to verify two things at once:

- whether the Gemini lane could now produce a full comparable control pair
- whether successful Gemini outputs would be self-captured into `response.md` instead of external temp-file pointers

## Result

The rerun did **not** produce any comparable baseline/with-skill control pair.

No `response.md` artifacts were retained for either scenario.

## Observed Failure Pattern

The rerun failed across both scenarios with mixed runtime blockers:

### Forward Feature Slice

- `without_skill` failed after repeated transient retries and ended in `TerminalQuotaError` (`429 QUOTA_EXHAUSTED`)
- `with_skill` exhausted its retry budget and ended in timeout

### Brownfield Regression Fix

- `without_skill` failed on Gemini startup/auth transport with `fetchAdminControls` `ECONNRESET`
- `with_skill` failed with `TerminalQuotaError` (`429 QUOTA_EXHAUSTED`)

## Interpretation

This rerun changes the repository judgment in one important way:

- the blocker is no longer best described as only "Gemini quota exhaustion"

It is now clearer that the current Gemini execution lane is unstable along three dimensions:

- quota availability
- startup/auth transport reliability
- completion latency within the benchmark timeout budget

Because no successful branch completed, the runner self-capture fix was **not** meaningfully exercised on a real Gemini plan output in this rerun.

## What This Does And Does Not Prove

This rerun does prove:

- the repository benchmark contract still executes end-to-end
- the current Gemini lane remains unsuitable for `tdd` graduation evidence

This rerun does **not** prove:

- that `tdd` got weaker
- that the self-capture fix is incorrect
- that the benchmark design itself is flawed

## Next Step

Do not revisit `tdd` promotion yet.

The next useful step is one of:

1. rerun the same benchmark after Gemini quota and transport conditions stabilize, or
2. establish a replacement non-Gemini lane that can produce a clean two-scenario control pair without repository-contamination drift

Until then, `tdd` remains `review`.
