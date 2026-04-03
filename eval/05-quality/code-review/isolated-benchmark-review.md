# Code Review Isolated Benchmark Review

## Scope

This note records the first usable isolated benchmark result for `code-review`.

The benchmark uses the same brownfield access-review changeset as the earlier manual review, but runs both the baseline and with-skill branches inside isolated temporary workspaces. The current primary artifact is:

- `eval/05-quality/code-review/run-2026-04-03-copilot-brownfield-only`

This is now valid benchmark evidence. It is not yet a tested-grade promotion artifact.

## Runtime Notes

- The benchmark asset exists at `isolated-benchmark.json`.
- The run completed cleanly with the `copilot` runner.
- Both `without_skill` and `with_skill` branches produced usable response artifacts.
- The same output directory was reused for a rerun of the same scenario, so `progress.log` and `execution-observability.jsonl` contain appended history from both completed executions while `response.md` reflects the latest run.
- The scenario count was `1`, limited to the brownfield changeset:
  - `access-review-modernization-code-review`

This closes the earlier execution-lane gap for `code-review`. The remaining question is output quality, not runner stability, but the next rerun should use a fresh output directory so the evidence is cleaner.

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

The with-skill branch reinforced the intended review posture, but also introduced avoidable noise.

Observed behavior:

- grouped findings clearly into blocking issues, missing test coverage, and lower-severity follow-ups
- tied the main blocker explicitly to the contract and brownfield coexistence constraints
- caught both synchronous legacy sync call sites instead of only one
- but added explicit implementation advice and fix-directed wording beyond pure review feedback
- ended with explicit merge-decision language even though the prompt asked for review feedback rather than approval workflow
- duplicated the same root issue through secondary checklist framing such as `magic value`, TODO-tracker policy, and unreachable-path commentary

Why this matters:

- the skill still shows real value on blocker visibility, contract alignment, and brownfield safety
- but the benchmark plan requires with-skill output to be less noisy than baseline and to avoid approval-style feedback while blockers remain visible
- this run does not clearly satisfy that bar

## Judgment

`code-review` should remain in `review`.

Why:

- a usable isolated benchmark result now exists, so the evidence gap has narrowed materially
- the skill clearly helps keep contract violations, unsupported flows, and coexistence risks visible
- but the current skill wording still pulls the model toward implementation snippets, approval-style closure, and duplicate checklist issues

This means the blocker is no longer benchmark execution. The blocker is output discipline.

## Status Recommendation

- recommended status now: `hold at review`
- not yet justified: `tested`

## Next Smallest Honest Step

- tighten the skill output contract so benchmark responses stay review-only:
  - no fix snippets unless the prompt explicitly asks for remediation guidance
  - no approval-status footer unless the caller explicitly asks for approval state
  - no duplicate checklist issues when a higher-severity contract or brownfield blocker already captures the root problem
- rerun the same isolated brownfield scenario first
- only after a cleaner rerun exists add the non-brownfield feature slice promised in the QA strategy
