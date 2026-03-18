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

- overwrite `eval/00-discovery/intake/optimization/iter-2/results.json` after preflight passes, or
- write to `eval/00-discovery/intake/optimization/iter-2/results-rerun.json`

## Update: 2026-03-18 Valid Rerun

A later rerun was completed successfully after preflight returned `OK`.

For the tightened routing-only description that began `Route engineering work before execution.` the bucketed results were:

- core recall: `0/5`
- overlap recall: `0/5`
- non-trigger precision: `10/10`
- mixed-set accuracy: `10/20`

This means the earlier quota diagnosis is no longer the main explanation for iteration-2 failure. The tighter metadata truly over-corrected toward precision and lost discoverability on the strongest intake prompts.

## Update: 2026-03-18 Second Rerun Blocked

After revising the description again to restore more user-natural trigger phrases, another rerun was attempted on the same day.

That rerun did **not** start because Claude CLI returned:

`You're out of extra usage · resets Mar 20, 6pm (Asia/Singapore)`

So the current description revision is still awaiting a valid post-reset rerun.
