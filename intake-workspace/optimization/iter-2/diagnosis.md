# Iteration 2 Trigger Eval Diagnosis

Date: 2026-03-14

## Status

Iteration 2 trigger-eval output exists in `results.json`, but the run is not valid for comparison.

## Why It Is Invalid

A direct diagnostic `claude -p` run against a known should-trigger query returned:

`You're out of extra usage · resets 6pm (Asia/Shanghai)`

The same quota error was reproduced for:

- default model
- `claude-sonnet-4-5`
- `claude-haiku-4-5`

Because `scripts.run_eval` treats failed invocations as non-triggers, the quota failure collapsed all 10 positive cases to false negatives and produced an artificial zero-recall result.

## What Can Be Trusted

- The raw file `results.json` was written successfully.
- The `10/20` pass rate only reflects that all negative cases remained negative.
- The `0/10` positive trigger count is not evidence that the description regressed.

## What Cannot Be Claimed

- No valid comparison to iteration 1
- No valid precision / recall trend
- No valid claim that the new description underperformed

## Next Valid Step

After quota resets at 6pm Asia/Shanghai on 2026-03-14:

1. Run a short Claude CLI preflight check.
2. Rerun `scripts.run_eval` into a fresh artifact.
3. Compare iteration 2 against iteration 1 only after a quota-clean rerun.

Suggested rerun target:

- overwrite `intake-workspace/optimization/iter-2/results.json` after preflight passes, or
- write to `intake-workspace/optimization/iter-2/results-rerun.json`

