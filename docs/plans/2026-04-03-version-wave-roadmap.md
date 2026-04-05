# Version Wave Roadmap

> Status: proposed versioning and promotion roadmap after `1.0.0`.

## Purpose

This roadmap answers two practical questions:

1. which non-final skills should move next
2. how version numbers should advance while the repository is still hardening its public path

It does **not** try to graduate the whole repository at once. It keeps the existing rule from the tested-promotion board: move a small batch at a time, and only promote status when the evidence is honest.

## Current State

As of this roadmap:

- total skills: `44`
- `tested`: `6`
- `review`: `26`
- `draft`: `12`

Public surface view:

- public installable skills: `15`
- public `core`: `6`
- public `beta`: `9`
- public `experimental`: `0`

The critical observation is that the next version waves should be driven by the **public path**, not by the full repository backlog.

## Working Rules

### Rule 1: Do not flood `review`

Do **not** pull every `draft` skill into `review`.

Only move a `draft` skill to `review` when at least one of these is true:

- it is needed by the current public hardening wave
- it is a direct dependency or adjacent handoff for an upcoming public beta skill
- it is already exposed on the public surface and should stop being "installable but not reviewable"

### Rule 2: `review -> tested` uses a minimum evidence packet

Before a skill moves from `review` to `tested`, it should have at minimum:

- one usable benchmark result for the intended scenario
- one integration or handoff review
- current `findings.md`
- an explicit promote/hold conclusion

If the benchmark lane is still contaminated, under-specified, or execution-unstable, the skill stays at `review`.

### Rule 3: Version bumps follow contract impact

- `patch`:
  - benchmark harness fixes
  - validator/test additions
  - evidence corrections
  - docs that do not change public maturity semantics
- `minor`:
  - one promotion wave completes
  - one or more public skills move materially in readiness or tested coverage
  - a small number of draft skills enter review because the next public wave now needs them
- `major`:
  - canonical public skill names change
  - install/update semantics change
  - public lifecycle contract changes in a way that can break existing users

Increasing coverage depth alone is **not** a reason for a major release.

## Review Pool Triage

### Public-path review skills to prioritize

These are the review skills that most directly affect the public path:

- `system-design`
- `feature-development`
- `code-review`
- `ci-cd`
- `deployment-strategy`
- `incident-response`
- `monitoring-observability`

These are public, high-leverage, and already have stronger routing value than the rest of the review pool.

### Review skills to keep out of the next hardening waves unless they become blockers

- `user-research`
- `api-design`
- `systematic-debugging`
- `task-execution`
- `receiving-code-review`
- `testing-strategy`
- `e2e-scenario-design`
- `security-audit`
- `delivery-completion`
- `runbooks`
- `tech-debt-management`
- `retrospective`

They are useful, but they are not the next release bottleneck for the public core path.

## Draft Pool Triage

### Keep `draft` in `1.1`

Do not move any new draft skill to `review` in `1.1`.

Reason:

- the current bottleneck is consuming the existing review pool honestly
- `system-design`, `feature-development`, and `code-review` already have known evidence gaps
- adding more review candidates in the same wave reduces evidence throughput

### Draft candidates for later waves

No additional `draft -> review` candidate is justified right now.

The review pool has already expanded to include:

- `release-management`
- `observability`
- `risk-assessment`
- `sprint-planning`
- `documentation`

Everything else should remain `draft` through at least `1.3` unless a public-path dependency changes.

### Drafts that should explicitly stay `draft` through `1.3`

- `market-analysis`
- `feasibility-study`
- `spec-writing`
- `domain-modeling`
- `acceptance-criteria`
- `data-modeling`
- `security-design`
- `estimation`
- `bug-history-retrieval`
- `accessibility`
- `internationalization`
- `compliance`

Reason:

- not on the immediate public hardening path
- not on the current tested-promotion board
- better treated as second-ring or outer-ring capability until the public spine is stronger

## Version Waves

## `1.1`

### Goal

Close the implementation/quality evidence gaps on the current public beta spine without adding new review load.

### `draft -> review`

- none

### `review -> tested` focus

- `system-design`
- `feature-development`
- `code-review`

### Smallest honest next step per skill

- `system-design`
  - rerun the same brownfield isolated benchmark after the with-skill runner lane is stable
- `feature-development`
  - rerun the same brownfield scenario now that the minimum code fixture exists
- `code-review`
  - tighten false-positive and duplicate-root-cause handling, then rerun the same brownfield benchmark once more

### Exit criteria

- each of the three skills has one updated, decision-ready benchmark review
- at least one of the three reaches `tested`
- the others have sharper blockers than "needs more evidence"

## `1.2`

### Goal

Harden the delivery path and pull only the minimum new draft skills needed for that path.

### `draft -> review`

- none currently required

### Draft-promotion rule for this wave

Do not add a new draft candidate unless the current review pool cannot advance the
delivery path without it.

### `review -> tested` focus

- `ci-cd`
- `deployment-strategy`

### Secondary review hardening in the same wave

- `observability`
- `incident-response`
- `monitoring-observability`

The goal for these secondary skills is not necessarily immediate promotion. The goal is to align their benchmark design with the same delivery/operations boundary used by `ci-cd` and `deployment-strategy`.

### Exit criteria

- `release-management` has stronger delivery-path evidence than its first review packet
- `observability` has review-stage evidence aligned with the delivery and operations path
- `ci-cd` and `deployment-strategy` each have a usable isolated benchmark result
- at least one delivery skill reaches `tested`

## `1.3`

### Goal

Stabilize operations handoff and selectively open the next second-ring review candidates.

### Conditional `draft -> review`

None by default.

Only name a new draft candidate if the current review pool is no longer the main
bottleneck.

### `review -> tested` focus

- `incident-response`
- `monitoring-observability`

### Secondary candidate if capacity remains

- `security-audit`

Only pull `security-audit` forward if it has moved past "no findings recorded yet" and has a real first structured eval lane.

### Exit criteria

- operations-path review skills are benchmark-backed rather than handoff-only
- any future draft promotion is tied to a concrete public-path blocker rather than count reduction
- no version wave is declared complete based on drafted paperwork alone

## Release Policy Summary

- Use `patch` releases to improve execution reliability, evidence accuracy, and validator/test coverage inside an existing wave.
- Use `minor` releases to close one promotion wave or materially advance one part of the public path.
- Reserve `major` releases for public contract changes, not for normal maturity hardening.

## Recommended Immediate Order

1. run `1.1` exactly as a review-pool digestion wave with no new draft promotions
2. carry `system-design`, `feature-development`, and `code-review` to clean benchmark conclusions
3. only after `1.1` settles, use the already-open review pool for `1.2`, including `release-management` and `observability`
4. treat all remaining draft skills as intentionally deferred, not forgotten
