# Security Audit Isolated Benchmark Review

## Scope

This note reviews the first isolated explicit-invocation benchmark for `security-audit`.

The benchmark uses one high-risk reviewed change slice and compares:

1. a generic baseline prompt
2. the same prompt with explicit `security-audit` skill invocation

Runner: `copilot`
Run: `eval/05-quality/security-audit/run-2026-04-04-copilot-minimal`

## Scenario: High-Risk Invite Acceptance Audit

### Baseline

The baseline was competent. It identified the main release blockers from the reviewed change:

- SQL construction risk from string interpolation
- missing authorization checks on the endpoint
- tenant-boundary trust in `tenant_id`
- API key and logging concerns
- dependency review risk around the legacy query builder

It also concluded that the release should be blocked.

Its main weakness was audit discipline rather than issue recall. The response found the right class of problems, but it was looser on exploitability framing, severity taxonomy, and what should remain a blocker versus follow-up work.

### With-Skill

The with-skill branch produced the stronger release-quality audit shape:

- preserved the same core trust-boundary, injection, secret-handling, and dependency findings
- separated critical, high, and advisory findings more deliberately
- tied findings to attack paths, impact, and remediation direction
- kept the release recommendation explicit: block until the blocking findings are resolved

This is the contract of the skill: not just "find security issues," but turn a risky slice into a release-useful `security-report`.

## Judgment

This is still a narrow evidence base, but it is now stronger than review-stage paperwork alone:

- the baseline proves the scenario is genuinely high risk and not a weak control
- the with-skill branch is materially stronger on severity discipline and release-focused reporting
- the skill-applied output is shaped more cleanly for downstream `release-management`

Remaining limits are real:

- only one isolated scenario exists
- the decisive lane used `copilot` because other runner lanes in this wave have been unstable
- no hotfix or low-risk comparison scenario exists yet

Those gaps still matter for later status levels, but they no longer justify holding the skill at `review` under the current minimal promotion bar.

## Status Recommendation

- Recommended status: `tested`
