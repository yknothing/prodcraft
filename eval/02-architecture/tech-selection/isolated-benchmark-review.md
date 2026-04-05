# Tech Selection Isolated Benchmark Review

## Scope

This note reviews the first isolated explicit-invocation benchmark for `tech-selection`.

The benchmark uses one brownfield architecture slice and compares:

1. a generic baseline prompt
2. the same prompt with explicit `tech-selection` skill invocation

Runner: `copilot`
Run: `eval/02-architecture/tech-selection/run-2026-04-04-copilot-minimal`

## Scenario: Brownfield Modernization Tech Decision Record

### Baseline

The baseline was competent. It identified the major technology choices, kept dual-write and a routing facade visible, and did not drift into full implementation planning.

Its main weakness was minimum-stack discipline. It still selected queue infrastructure while sync semantics remained unresolved, which is exactly the kind of premature technology commitment this skill should avoid.

### With-Skill

The with-skill branch made the stronger bounded decision:

- it kept the modernization shape as an embedded module instead of escalating to a new service
- it preserved dual-write persistence for reversibility
- it explicitly deferred messaging/platform choice until sync semantics are resolved
- it kept rollout reversibility visible through feature-flag deployment rather than reopening architecture

This is the core contract of the skill: choose the minimum stack that satisfies the architecture and record what must remain undecided.

## Judgment

This is still a narrow evidence base, but it is now stronger than routed review alone:

- routed handoff review proves the lifecycle boundary
- one isolated benchmark shows a clearer and safer technology-decision record than baseline

Remaining gaps are real:

- only one scenario exists
- the benchmark is brownfield-only
- there is no downstream delivery evidence yet

Those gaps should be expanded later, but they no longer justify keeping the skill at `review` under the current minimal promotion bar.

## Status Recommendation

- Recommended status: `tested`
