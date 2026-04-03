# Tested Promotion Board

> Status: active execution board for public-release hardening.

> Iteration rule: move only a small batch at a time. Do not widen scope while a batch is still gathering clean evidence.

## Fast-Track Intake Brief

**Work type**: Enhancement  
**Entry phase**: 03-planning  
**Intake mode**: fast-track  
**workflow_primary**: agile-sprint  
**Key skills needed**: `task-breakdown`, `documentation`, `verification-before-completion`  
**Scope assessment**: medium  
**routing_rationale**: The public-release direction is approved. The next high-leverage move is to productize the promotion workflow before promoting more skills one by one.  
**Key risks**:
- adding ceremony without increasing promotion throughput
- widening beyond the public core spine

## Why This Board Exists

Prodcraft currently has a strong control plane but a narrow `tested` set. Promotion work has been happening skill-by-skill, which is honest but slow.

This board exists to make `review -> tested` promotion:

- batchable
- comparable across skills
- evidence-driven
- small-slice friendly

Use this board to decide which skills move now, which stay in `review`, and which should remain outside the current promotion wave.

## Promotion Rule

For routed skills, do not promote to `tested` unless all of the following are true:

1. a clean benchmark result exists for the intended scenario
2. a downstream or handoff integration review exists
3. the findings document is current and matches the evidence
4. the conclusion is explicit: promote, hold, or redesign

If evidence is contaminated, partial, or superseded, record that and hold the skill at `review`.

## Current Public-Core Spine

Already `tested`:

- `intake`
- `problem-framing`
- `requirements-engineering`
- `task-breakdown`
- `tdd`
- `verification-before-completion`

Current target review skills for public-release hardening:

- `system-design`
- `feature-development`
- `code-review`
- `ci-cd`
- `deployment-strategy`

## Wave Strategy

### Wave 1: Entry -> Specification -> Architecture

Goal:
- prove that the public path stays strong from route selection into design-ready architecture handoff

Skills:
- `problem-framing`
- `requirements-engineering`
- `system-design`

Why this wave first:
- these three skills form one continuous upstream chain
- they already have meaningful review-stage evidence
- they can share benchmark fixtures and handoff scenarios

### Wave 2: Implementation -> Quality

Goal:
- prove that the core implementation path stays small-slice, reviewable, and contract-aware

Skills:
- `feature-development`
- `code-review`

### Wave 3: Delivery

Goal:
- prove that the public path can carry a reviewed slice into release and rollout decisions

Skills:
- `ci-cd`
- `deployment-strategy`

## Wave 1 Board

| Skill | Current Status | Existing Evidence | Missing for `tested` | Smallest Honest Next Step | Decision |
|---|---|---|---|---|---|
| `problem-framing` | `tested` | manual handoff review, isolated brownfield benchmark review, downstream consumption reviews | no current blocker for `tested`; next gaps are wider variance and security review | keep the isolated benchmark as the primary artifact and move the next Wave 1 benchmark to `system-design` | promoted |
| `requirements-engineering` | `tested` | clean routed benchmark review, routed handoff reviews, downstream chain reviews from `problem-framing` and `user-research` | no current blocker for `tested`; next gaps are broader rerun coverage and security review | keep the clean routed benchmark as the primary artifact and return Wave 1 focus to `system-design` | promoted |
| `system-design` | `review` | manual routed handoff review, isolated benchmark asset, clean baseline artifact, failed with-skill reruns at 300s and 600s | one clean with-skill completion for the existing brownfield isolated benchmark | rerun the same benchmark once the runner lane is stable; do not broaden scope first | blocked by runner instability |

## Wave 1 Exact Gap Summary

### `problem-framing`

- brief: `eval/00-discovery/problem-framing/tested-promotion-brief.md`
- Current manifest wiring is already close to tested-grade: benchmark and integration paths exist.
- The blocker is evidence quality, not missing manifest structure.
- The primary blocker is now closed by the isolated brownfield rerun and the skill has moved to `tested`.

### `requirements-engineering`

- brief: `eval/01-specification/requirements-engineering/tested-promotion-brief.md`
- The skill has broad review-stage evidence, but its first explicit benchmark baseline was contaminated.
- That blocker is now closed by a clean routed benchmark on the public default chain:
  - `problem-framing -> requirements-engineering`
- The remaining gaps are broader rerun coverage and later security review, not `tested` eligibility.

### `system-design`

- brief: `eval/02-architecture/system-design/tested-promotion-brief.md`
- This skill has the cleanest artifact gap in the batch.
- The benchmark asset now exists and the baseline branch is clean.
- The blocker is now narrower: the with-skill branch has not completed cleanly despite 300s and 600s `copilot` fallback attempts.
- Do not widen to the second scenario until the current with-skill lane succeeds once.

## Batch 1 Deliverables

This batch is complete only when all of the following exist:

1. this promotion board
2. a reusable promotion template for future waves
3. an explicit Wave 1 gap summary for each target skill
4. the next evidence-producing task order for Wave 1

Batch 1 is now complete.

## Batch 2 Deliverables

This batch is complete only when all of the following exist:

1. a checked-in tested-promotion packet for `problem-framing`
2. a checked-in tested-promotion packet for `requirements-engineering`
3. a checked-in tested-promotion packet for `system-design`
4. an explicit execution order for the first evidence-producing Wave 1 tasks

Batch 2 is now complete.

## Batch Exit Rule

Wave 1 does not require all three skills to graduate together.

This batch is successful if:

- at least one skill reaches `tested`, and
- the other two leave the batch with sharper blockers than "needs more evidence"

Current Wave 1 outcome:

- `problem-framing` promoted to `tested`
- `requirements-engineering` promoted to `tested`
- `system-design` remains `review` with a sharply defined runner-lane blocker

## Immediate Task Order

1. treat Wave 1 as provisionally closed with `2 promoted + 1 held`
2. run the smallest missing clean evidence step for `feature-development`
3. tighten `code-review` review-output discipline and rerun the same brownfield benchmark in a fresh output directory
4. return to `system-design` only when runner stability is good enough to justify another same-scenario rerun

Wave 2 note:

- `feature-development` now has a benchmark asset, but the first isolated attempt showed that an implementation skill needs a minimal code fixture, not just slice and contract text
- `code-review` now has a usable isolated brownfield benchmark result at `eval/05-quality/code-review/run-2026-04-03-copilot-brownfield-only`
- the execution blocker is closed for `code-review`, but the current hold reason has shifted to output discipline: the with-skill branch adds implementation advice, approval-style closure, and duplicate checklist noise
- the next `code-review` rerun should use a fresh output directory because the current primary artifact reused the same directory and appended observability/progress history

## Non-Goals

- do not promote second-ring or outer-ring skills in the same batch
- do not redesign the lifecycle or workflow model
- do not widen the public surface while the tested set is still narrow
- do not rewrite skill bodies unless the evidence shows a concrete defect
