# TDD Isolated Benchmark Rerun - 2026-04-01

## Scope

This note records the partial Gemini rerun of `eval/04-implementation/tdd/isolated-benchmark.json` executed on `2026-04-01`.

It is benchmark evidence for `tdd`, but it is **not** yet sufficient graduation evidence because only one scenario completed and the raw runner output still relied on external temp-file references.

## Run Shape

- runner: `gemini`
- scenarios requested: `forward-feature-slice`, `brownfield-regression-fix`
- completed control pair: `forward-feature-slice`
- incomplete control pair: `brownfield-regression-fix`

## Forward Feature Slice

Both branches completed and produced plan artifacts.

### Baseline branch

The baseline plan did follow a RED -> GREEN -> REFACTOR structure, but it stayed generic in two important ways:

- it opened with a non-pending-status test instead of the central business trigger
- existing-flow protection was left as "write or run existing tests" rather than as explicit characterization coverage

### With-skill branch

The skill-applied plan was materially tighter:

- it separated characterization/regression, contract/new-behavior, and unsupported-flow tests
- it explicitly protected the brownfield state machine before new reminder logic
- it added a concrete unsupported-flow guard that only email reminders are allowed in this slice
- it kept the implementation constraint explicit: no SMS, no push, no escalation chain, no state-machine redesign

### Judgment

For `forward-feature-slice`, the with-skill branch outperformed baseline on:

- unsupported-flow precision
- coexistence and regression protection
- scope discipline
- downstream implementation readiness

This is the strongest isolated benchmark signal for `tdd` so far.

## Brownfield Regression Fix

The rerun stalled after starting the baseline branch for `brownfield-regression-fix`. No comparable baseline/with-skill artifact pair was retained for judgment.

Current interpretation:

- the Gemini lane did better than the `2026-03-31` attempt because one full control pair completed
- the rerun still did **not** finish the full benchmark set
- the run therefore improves confidence in the benchmark contract, but does not yet justify promotion beyond `review`

## Artifact Hygiene Note

The raw local rerun stored `response.md` as pointers to external Gemini temp files rather than as self-contained plan content. The authoritative evidence for this rerun is therefore this note plus the updated findings, not the raw local `run-*` directory.

## Next Step

Rerun the same benchmark set after the runner self-capture fix lands, so completed branches write the actual plan body into `response.md` instead of temp-file pointers. Treat the next full two-scenario control pair as the earliest candidate for revisiting `tdd` graduation.
