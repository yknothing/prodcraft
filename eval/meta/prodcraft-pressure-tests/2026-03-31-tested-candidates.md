# 2026-03-31 Tested Candidates

## Scope

This note records which skills are currently closest to `tested` based on the repository evidence as of `2026-03-31`.

It is a prioritization note, not a promotion record.

## Current Conclusion

No skill should be promoted to `tested` today from the current in-repo evidence set alone.

## Closest Candidate

### `e2e-scenario-design`

Why it is closest:

- it already has explicit benchmark evidence in `eval/05-quality/e2e-scenario-design/skill-creator-run-2026-03-30/benchmark.json`
- that benchmark shows a real structural lift over baseline on two of three scenarios
- its remaining blocker is narrower than the rest of the spine: it mainly still needs cleaner routed integration evidence

What is still missing:

1. one routed handoff review from `testing-strategy`
2. at least one downstream consumer check showing the artifact is directly useful to implementation or CI

## Benchmark-Blocked Spine Skills

These remain strong candidates in importance, but not in immediate promotability:

- `tdd`
- `feature-development`
- `deployment-strategy`

Why they are blocked:

- they are core lifecycle-spine skills
- their next gate is isolated benchmark evidence
- the current Gemini lane is execution-blocked
- the current Copilot fallback is not yet a clean comparable control

## Still Earlier Than `tested`

These skills still need a broader evidence upgrade before promotion should even be considered:

- `problem-framing`
- `user-research`
- `requirements-engineering`
- `system-design`
- `api-design`
- `task-breakdown`
- `code-review`
- `testing-strategy`
- `ci-cd`
- `incident-response`
- `monitoring-observability`
- `runbooks`
- `retrospective`
- `tech-debt-management`

Common reasons:

- isolated benchmark still missing
- second scenario or downstream reuse still missing
- current evidence is strong enough for `review`, not yet for `tested`

## Practical Order

If the goal is to create the first believable batch of `tested` skills, the current best order is:

1. finish routed integration evidence for `e2e-scenario-design`
2. stabilize one benchmark lane that can produce clean baseline vs with-skill artifacts
3. use that lane on `tdd`, `feature-development`, and `deployment-strategy`
