# Feature Development Isolated Benchmark Review

## Scope

This note records the current isolated benchmark state for `feature-development`.

It does **not** yet count as a tested-grade benchmark result artifact because the current benchmark context is too thin for an implementation skill and the with-skill branch did not complete cleanly.

The purpose of this note is to make the current blocker auditable and specific so the next rerun starts from a better fixture design instead of repeating an invalid benchmark shape.

## Runtime Notes

- The benchmark asset now exists at `isolated-benchmark.json`.
- The current scenario used only:
  - `access-review-modernization-task-slice.md`
  - `access-review-modernization-api-contract.md`
- A `gemini` lane did not yield a usable response artifact.
- A `copilot` fallback run completed the baseline branch, but the with-skill branch failed after exploring for a local codebase and hitting `Connection error.`.

## Scenario 1: Brownfield Compatibility Slice

### Baseline

The isolated baseline completed successfully.

Observed behavior:

- picked a concrete reassignment endpoint slice
- implemented a small set of files with tests and explicit unsupported-flow behavior
- preserved the compatibility boundary by isolating the new endpoint and explicit error contract
- still invented a local codebase shape because no code fixture was present

Why this matters:

- the baseline is non-trivial, so the comparison target is meaningful
- but it also exposes the benchmark-design gap: an implementation skill without a code fixture forces the model to fabricate project structure

### With-Skill

The with-skill branch did not produce a usable implementation artifact.

Observed behavior:

- read the reviewed slice and the skill body
- then tried to discover and operate on a local codebase (`src/`, `test/`, `package.json`)
- attempted to install dependencies and run tests inside the temporary workspace
- eventually failed with `Connection error.`

Why this matters:

- the current blocker is not only runner instability
- the benchmark context itself is under-specified for an implementation skill whose contract depends on an existing codebase and test suite
- rerunning the same prompt without a minimal code fixture is likely to reproduce the same failure pattern

## Current Judgment

`feature-development` should remain in `review`.

Why:

- the routed handoff review remains valid
- the benchmark asset exists and the brownfield scenario is directionally correct
- but the current isolated benchmark is not yet a fair tested-grade comparison because the implementation context is too thin

## Status Recommendation

- recommended status now: `hold at review`
- not yet justified: `tested`

## Next Smallest Honest Step

- add a minimal code fixture for the brownfield compatibility slice
- rerun the same scenario with that fixture in both baseline and with-skill branches
- only after a clean with-skill completion exists should the team decide whether a second forward slice is needed
