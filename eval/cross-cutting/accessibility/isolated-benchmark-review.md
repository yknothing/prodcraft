# Accessibility Isolated Benchmark Review

## Scope

This note reviews the first benchmark-grade baseline vs with-skill comparison for `accessibility`.

The comparison used the same invite-modal UI and product-constraint bundle for both branches.

Runner: `copilot`
Run: `eval/cross-cutting/accessibility/run-2026-04-06-copilot-clean-002350`

## Scenario: Invite Modal Accessibility Contract

### Baseline

The baseline branch was already usable.

From the preserved runner response, it did several important things correctly:

- read the same UI and product constraint inputs as the with-skill branch
- named the invite modal as the target surface
- produced explicit accessibility guidance instead of generic accessibility advice
- included control naming, ARIA-oriented expectations, and QA-facing checks

Its weakness was contract discipline, not obvious total failure.

The preserved response suggests a one-off artifact that mixes detailed implementation-leaning notes with accessibility expectations. That is usable, but it is looser than the intended skill contract and less clearly shaped as a downstream handoff for `acceptance-criteria`.

### With-Skill

The with-skill branch produced the stronger artifact shape.

From the preserved runner response, it:

- explicitly loaded `skill-under-test/SKILL.md`
- produced the canonical `accessibility-guidance.md` artifact
- named the affected controls and states as a scoped surface
- organized the result as an accessibility contract, acceptance criteria, QA review checks, and remediation notes
- stayed at contract level instead of drifting into redesign

That is the core contract of the skill: turn a concrete UI slice into a reviewable accessibility packet that downstream specification and QA work can consume directly.

## Judgment

This is still a narrow evidence base, but it is enough for a minimal `tested` posture:

- the routed handoff review already proves `acceptance-criteria` is the correct downstream consumer
- this clean isolated run shows the skill produces a more canonical accessibility contract than baseline on the same slice
- both branches completed cleanly, and the execution trace keeps missing usage accounting explicit through `model_usage.unavailable` events instead of inventing token data

Remaining gaps are real:

- only one benchmark scenario exists
- the checked-in review depends on preserved runner summaries rather than full generated artifacts

Those gaps matter for later maturity stages, but they do not justify holding the skill at `review` under the repository's current tested gate.

## Status Recommendation

- Recommended status: `tested`
