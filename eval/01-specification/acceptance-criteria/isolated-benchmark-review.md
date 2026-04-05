# Acceptance Criteria Isolated Benchmark Review

## Scope

This note reviews the first benchmark-grade baseline vs with-skill comparison for `acceptance-criteria`.

The comparison used the same password-reset requirements and spec bundle for both branches.

Runner: `copilot`
Run: `eval/01-specification/acceptance-criteria/run-2026-04-05-copilot-clean-213547`

## Scenario: Password Reset Acceptance Criteria

### Baseline

The baseline was already useful. It did several important things correctly:

- covered the main request and confirmation happy paths
- included error behavior such as invalid, expired, and reused tokens
- kept security-sensitive behavior visible
- stayed at a behavior-focused, testable level

Its main weakness was contract sharpness. The baseline looked like a good general criteria set, but it was looser on the exact handoff shape:

- it emphasized breadth and criterion count over deliberate structure
- it did not clearly signal a skill-shaped contract for downstream QA and TDD work
- the response summary claimed direct usability, but less explicitly than the with-skill branch

### With-Skill

The with-skill branch produced the stronger criteria artifact:

- explicitly followed the skill contract after reading `skill-under-test/SKILL.md`
- used Given-When-Then framing rather than a looser general checklist shape
- still covered happy path, edge cases, error paths, and security behavior
- stayed at the behavior layer instead of drifting into implementation detail
- was more clearly shaped for direct QA and TDD consumption

This is the core contract of the skill: turn reviewed requirements into an executable behavior contract, not just a comprehensive note.

## Judgment

This remains a narrow evidence base, but it is now enough for a minimal `tested` posture:

- the routed handoff review already proves `testing-strategy` is the correct downstream consumer
- this clean isolated run shows the skill can produce a stronger testing-facing contract than baseline on the same slice

Remaining gaps are real:

- only one benchmark scenario exists
- the benchmark has only been run cleanly on one runner lane so far

Those gaps matter for later promotion beyond `tested`, but they do not justify keeping the skill at `review` under the repository's current minimal promotion bar.

## Status Recommendation

- Recommended status: `tested`
