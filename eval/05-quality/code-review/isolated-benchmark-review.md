# Code Review Isolated Benchmark Review

## Scope

This note records the first usable isolated benchmark result for `code-review`.

The benchmark uses the same brownfield access-review changeset as the earlier manual review, but runs both the baseline and with-skill branches inside isolated temporary workspaces. The current primary artifact is:

- `eval/05-quality/code-review/run-2026-04-03-copilot-brownfield-only-precision-rerun-2`

This is now valid benchmark evidence. Under the current minimal promotion bar it is enough for a narrow `tested` posture, but the remaining checklist-leakage limitation should stay explicit.

## Runtime Notes

- The benchmark asset exists at `isolated-benchmark.json`.
- The run completed cleanly with the `copilot` runner.
- Both `without_skill` and `with_skill` branches produced usable response artifacts.
- Earlier reruns remain useful history, but the current primary artifact is the cleanest precision-focused rerun so far.
- The scenario count was `1`, limited to the brownfield changeset:
  - `access-review-modernization-code-review`

This closes the earlier execution-lane gap for `code-review`. The remaining question is now very narrow review precision, not runner stability.

## Scenario 1: Brownfield Access Review Changeset

**Prompt shape:** review a concrete reassignment-flow changeset using only the task slice, API contract, code, and tests. The required focus is blocking contract violations, brownfield coexistence risks, test adequacy, prioritization, and review-only feedback.

### Baseline

The isolated baseline was already strong on the core merge blockers.

Observed behavior:

- identified that unsupported reassignment types are accepted instead of returning `UNSUPPORTED_RELEASE1_FLOW`
- called out the silent substitution to `"manager_delegate"` as a dangerous guessed policy choice
- flagged immediate legacy synchronization as a brownfield coexistence risk
- identified missing unsupported-flow coverage and other meaningful test gaps
- stayed concise and mostly review-focused

Why this matters:

- the control case is now non-trivial, so the benchmark can measure quality delta instead of just baseline weakness
- any skill lift must therefore come from sharper prioritization, cleaner scope discipline, or materially better boundary awareness

### With-Skill

The with-skill branch is cleaner again and is now good enough for a narrow
`tested` posture, though one checklist-leakage limitation remains.

Observed behavior:

- kept the main findings focused on contract violation, coexistence risk, and missing unsupported-flow coverage
- removed the earlier magic-string nit
- no longer claimed that the fixture proves a supported-flow regression
- stayed fully in review mode without remediation snippets or approval theatrics
- but still reported a standalone blocking finding for the TODO-without-ticket checklist policy
- and still left a small amount of non-critical checklist leakage in the final output

Why this matters:

- the rerun shows real progress on precision: the previous false-positive and duplicate-root-cause issues were reduced materially
- but a code-review skill should not earn `tested` while an internal checklist-only policy can still surface as its own blocking finding in a concise merge-focused review
- the remaining blocker is now extremely narrow: checklist-policy leakage

## Judgment

`code-review` now qualifies for a narrow `tested` posture.

Why:

- a usable isolated benchmark result exists
- the skill clearly helps keep contract violations, unsupported flows, and coexistence risks visible
- the remaining checklist-only blocker leakage is now a known limitation, not a reason to leave the skill untested forever under the basic-coverage bar

## Status Recommendation

- recommended status now: `tested`

## Next Smallest Honest Step

- keep this rerun as the current primary artifact
- hold the skill at `review` until a rerun cleanly suppresses checklist-only blocker leakage
- only after that cleaner rerun exists add the non-brownfield feature slice promised in the QA strategy
