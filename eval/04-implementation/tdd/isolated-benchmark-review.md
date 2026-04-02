# TDD Isolated Benchmark Review

## Scope

This note is the current benchmark-results artifact for `tdd`.

It summarizes the strongest isolated explicit-invocation evidence currently available for the skill and is the benchmark artifact referenced by `manifest.yml`.

The repository used a fallback `copilot` lane for the decisive runs because the primary Gemini lane remained unstable on `2026-04-02`.

## Runtime Notes

- Gemini remained blocked by a mix of `QUOTA_EXHAUSTED`, `ECONNRESET`, and timeout failures.
- The decisive evidence below comes from isolated tempdir runs through the `copilot` fallback lane.
- The retained judgment is about **skill quality**, not about runner preference. The runner choice only affected which lane could complete.

## Scenario 1: Forward Feature Slice

### Baseline

The baseline did not stay at the requested planning layer.

Observed behavior:

- created a mini implementation from scratch
- wrote tests, service code, job code, docs, and demo artifacts
- treated the request as a build task instead of a TDD-first implementation plan

Why this matters:

- it widened scope beyond the requested slice
- it blurred planning and implementation
- it protected the slice less clearly than the skill-applied branch

### With-Skill

The skill-applied branch stayed within the intended contract.

Observed behavior:

- preserved a phased RED -> GREEN -> REFACTOR structure
- separated characterization, core behavior, duplicate-prevention, unsupported-flow, and scheduling concerns
- kept the implementation boundaries explicit: no SMS, no push, no escalation chain, no status-logic redesign

### Judgment

For the forward feature slice, `tdd` clearly outperformed baseline on:

- plan-vs-implementation discipline
- unsupported-flow precision
- brownfield safety framing
- scope control

## Scenario 2: Brownfield Regression Fix

### Baseline

The clean fallback baseline completed in an isolated tempdir without a retry-contaminated workspace.

Observed behavior:

- built a toy code path and applied a direct fix
- captured the bug and preserved the core acceptance targets
- still drifted from the requested artifact shape by implementing instead of staying at the plan layer

### With-Skill

The skill-applied branch stayed centered on the requested TDD-first handoff plan.

Observed behavior:

- started from characterization and regression tests
- made coexistence and contract-preservation checks explicit
- documented unsupported-flow boundaries instead of silently widening scope
- proposed surgical fix patterns without redesigning the subsystem

### Judgment

For the brownfield regression slice, `tdd` outperformed baseline on:

- staying at the requested planning artifact
- explicit regression-first ordering
- coexistence protection
- contract and unsupported-flow discipline

## Overall Judgment

The current isolated evidence is now strong enough to move `tdd` from `review` to `tested`.

Why:

- explicit-invocation benchmark evidence exists
- integration evidence already exists in `task-handoff-review.md`
- the skill shows a material quality lift over baseline in both a forward feature slice and a brownfield regression fix
- the lift is on the dimensions that matter most for `tdd`: RED-first discipline, boundary control, regression protection, and coexistence safety

## Limits

This review does **not** justify `secure` or `production`.

Remaining limits:

- the primary Gemini lane is still unstable and should be revalidated later
- no security-review artifact exists yet
- broader multi-run variance evidence is still thin

## Status Recommendation

- recommended status: `tested`
- not yet justified: `secure`
- not yet justified: `production`
