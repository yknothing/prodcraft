# v1.x Skill Maturity Wave Plan

> Status: proposed roadmap for post-`1.0.0` skill maturation.

> Goal: move the public path forward without pretending the whole repository must leave `draft` and `review` at once.

## Current Snapshot

From `manifest.yml`:

- total skills: `44`
- `draft`: `12`
- `review`: `26`
- `tested`: `6`

If "non-final" means "below `tested`", Prodcraft currently has `38` non-final skills.

If "final" means `secure` or `production`, then the current count is still effectively all `44`, because the repository does not yet use either status in live manifest entries.

From `schemas/distribution/public-skill-registry.json`:

- public install surface entries: `15`
- `readiness: core`: `6`
- `readiness: beta`: `9`
- `readiness: experimental`: `0`
- `stability: beta`: `15`

The important implication is that versioning should track the public path, not the full repository backlog.

## Planning Rule

Do **not** mass-promote all `draft` skills to `review`.

That would inflate the review queue without increasing the strength of the public path.

Use this narrower rule instead:

1. Pull a `draft` skill into `review` only if it is likely to enter the public path within the next `1-3` version waves.
2. Promote a `review` skill to `tested` only when the minimum evidence packet exists:
   - one clean benchmark result
   - one meaningful handoff or integration review
   - a current `findings.md`
   - an explicit promote/hold decision
3. Keep outer-ring or speculative skills at `draft` until they are actually needed by the public spine.

## Which Draft Skills Should Move

### Pull Into `review` Soon

No additional `draft -> review` promotion is justified right now.

The recent review-stage additions already widened the review pool:

- `release-management`
- `observability`
- `risk-assessment`
- `sprint-planning`
- `documentation`

That means the next honest move is to consume the existing review backlog rather
than pulling more draft skills forward.

### Keep In `draft` For Now

These should stay out of the next `1.1` / `1.2` / `1.3` waves unless a new product requirement pulls them in:

- discovery outer ring:
  - `market-analysis`
  - `feasibility-study`
- specification completeness layer:
  - `spec-writing`
  - `domain-modeling`
  - `acceptance-criteria`
- architecture second ring:
  - `data-modeling`
  - `security-design`
- planning completeness layer:
  - `estimation`
- cross-cutting outer ring:
  - `bug-history-retrieval`
  - `accessibility`
  - `internationalization`
  - `compliance`

Reason:

- they are useful, but they do not currently decide whether the public core path is honest
- promoting them first would widen scope before the main spine is hardened

## Review Queue Triage

### Near-Term `tested` Candidates

These should drive the next three version waves.

#### Version `1.1`

- `system-design`
  - Why now: it is the last open Wave 1 architecture blocker on the public spine.
  - Current blocker: with-skill lane instability, not missing benchmark design.
  - Smallest honest next step: rerun the existing brownfield isolated benchmark until one clean with-skill artifact exists.
  - Exit condition: one clean isolated benchmark result that shows stronger architecture boundary handling than baseline.

#### Version `1.2`

- `feature-development`
  - Why now: it anchors the implementation step after `tdd`.
  - Current blocker: the minimum code fixture now exists, but the benchmark has not yet been rerun on that fairer implementation context.
  - Smallest honest next step: rerun the same brownfield benchmark with the new fixture before adding any second scenario.
  - Exit condition: one clean isolated benchmark where with-skill stays smaller-slice and more reviewable than baseline.

- `code-review`
  - Why now: it closes the implementation-to-quality transition on the public spine.
  - Current blocker: the clean rerun removed implementation drift and approval-style closure, but the with-skill output still overstates or duplicates some blockers.
  - Smallest honest next step: tighten review precision around false positives and duplicate-root-cause findings, then rerun the same brownfield scenario once more.
  - Exit condition: one clean rerun where blockers stay sharp without false-positive or duplicate-root-cause noise.

#### Version `1.3`

- `ci-cd`
  - Why now: it starts the delivery wave and already has review-stage evidence.
  - Current blocker: no isolated benchmark yet.
  - Smallest honest next step: run the existing brownfield isolated benchmark, then add one non-brownfield delivery scenario.
  - Exit condition: with-skill output shows clearer gating and rollback checks than baseline.

- `deployment-strategy`
  - Why now: it is the last delivery decision layer on the public spine.
  - Current blocker: no isolated benchmark yet.
  - Smallest honest next step: run the planned isolated benchmark for one standard release and one staged rollout case.
  - Exit condition: with-skill output shows materially better rollout shape, stop conditions, and rollback readiness than baseline.

### Review Skills To Hold, Not Force Into `tested`

These are real review-stage skills, but they should not consume the next three version waves.

- discovery/spec/architecture second ring:
  - `user-research`
  - `api-design`
- quality second ring:
  - `receiving-code-review`
  - `testing-strategy`
  - `e2e-scenario-design`
  - `security-audit`
- delivery/operations side lanes:
  - `release-management`
  - `delivery-completion`
  - `incident-response`
  - `monitoring-observability`
  - `runbooks`
- evolution:
  - `tech-debt-management`
  - `retrospective`
- implementation tooling:
  - `systematic-debugging`
  - `task-execution`
- planning and cross-cutting support:
  - `risk-assessment`
  - `sprint-planning`
  - `documentation`

Reason:

- many still need first isolated benchmarks or stronger cross-skill reuse evidence
- they are valuable, but they are not the shortest path to a hardened public spine

## Versioning Policy

The repository is already at `version: 1.0.0`.

That should be interpreted as:

- the lifecycle model and public install surface are real
- not every skill is mature
- public maturity is expressed through `status` and `readiness`, not through the repo version alone

Use version bumps this way:

### Patch

Use `1.0.x`, `1.1.x`, `1.2.x` patch releases for:

- validator changes
- benchmark harness fixes
- evidence wording corrections
- curated export and docs alignment
- non-breaking maturity metadata changes

Patch releases should not depend on promoting new skills.

### Minor

Use `1.1.0`, `1.2.0`, `1.3.0` style minor releases for:

- one completed promotion wave on the public spine
- one or more `review -> tested` changes that materially strengthen the public path
- a deliberate `draft -> review` feeder move that supports the next wave

### Major

Reserve `2.0.0` for contract change, not for "more coverage."

Major is justified only when one of these happens:

- public skill naming changes
- install/update semantics change
- the meaning of `stability` or `readiness` changes incompatibly
- the curated/public contract is redefined in a breaking way

Increasing benchmark coverage or promotion depth alone is **not** a reason for a major bump.

## Proposed v1.x Roadmap

### `1.1`

Theme:

- close Wave 1 honestly

Target outcomes:

- `system-design` moves to `tested`
- no broad draft expansion
- keep the public surface at `stability: beta`

Optional feeder work:

- keep `release-management` review evidence warm, but do not let it delay `system-design`

### `1.2`

Theme:

- harden the implementation-quality loop

Target outcomes:

- `feature-development` moves to `tested`
- `code-review` moves to `tested`
- no new draft promotion unless an already-reviewed public-path dependency is blocked without it

### `1.3`

Theme:

- harden the delivery wave

Target outcomes:

- `ci-cd` moves to `tested`
- `deployment-strategy` moves to `tested`
- `release-management` stays an honest `review` candidate with stronger delivery-path evidence
- `observability` stays an honest `review` candidate until runner-backed evidence exists

## Anti-Patterns To Avoid

- promoting all `draft` skills just to shrink the draft count
- widening beyond the public spine before the current wave has clean evidence
- using a major version bump to hide incomplete maturity thinking
- mixing evidence collection, status promotion, and public contract changes into one oversized batch

## Decision Summary

Use a dual-track strategy:

1. aggressively move the current public-spine `review` skills to `tested`
2. keep the remaining `draft` set intentionally deferred until a real public-path dependency pulls one forward

That keeps the repository honest while still making visible version-by-version progress.
