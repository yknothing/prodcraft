# TDD QA Findings

## Summary

`tdd` moved to `tested` and now advances to `production` after a clean package security review.

## What Changed

1. The skill description and body were tightened to reflect task-slice-driven implementation rather than generic TDD advice.
2. Brownfield safety nets, unsupported-flow tests, and contract-aware RED ordering are now explicit parts of the skill.
3. A first manual task-to-TDD handoff review was added using the access-review modernization scenario.

## What We Learned

1. Generic implementation planning tends to mention tests, but not anchor behavior in explicit failing tests first.
2. The skill improves discipline around unsupported-flow handling and contract-aware test ordering.
3. The skill appears most valuable as a routed workflow skill downstream of `task-breakdown` and `api-design`.

## Current Interpretation

At this stage, `tdd` appears to be:

- a core implementation skill on the lifecycle spine
- stronger as a routed workflow skill than as a discoverability-first skill
- now backed by enough isolated benchmark evidence to leave `review`
- now supported by security-review evidence as well as routed benchmark and handoff artifacts

## 2026-03-31 Benchmark Smoke Attempt

A repository-owned isolated benchmark smoke attempt was executed for the forward feature slice.

Retained evidence for that attempt:

- this findings note
- `eval/meta/prodcraft-pressure-tests/2026-03-31-gemini-benchmark-lane-status.md`

Current interpretation of that run:

- the benchmark dataset and runner wiring are now in place
- the run did **not** yet produce usable baseline/with-skill content for judgment
- baseline timed out after `120s`
- the with-skill branch failed in Gemini runtime startup with `loadCodeAssist` / `fetchAdminControls` `ECONNRESET` failures after MCP startup noise

This means the current blocker is the Gemini execution lane, not the benchmark contract itself.

## 2026-03-31 Copilot Fallback Attempt

A second repository-owned fallback attempt was executed on the same benchmark set.

Retained evidence for that attempt:

- this findings note
- `eval/meta/prodcraft-pressure-tests/2026-03-31-gemini-benchmark-lane-status.md`

Current interpretation of that run:

- the runner itself completed and wrote observability artifacts
- both baseline branches still timed out after `120s`
- only one with-skill branch produced a `response.md`
- the surviving response still showed repo exploration and broad assumption-making, so it is not a clean controlled comparison against baseline

This means `copilot` is not yet a valid replacement benchmark lane for `tdd`.

## 2026-04-01 Gemini Partial Rerun

A second Gemini-owned isolated rerun was executed on the same benchmark set.

Retained evidence for that rerun:

- this findings note
- `eval/04-implementation/tdd/isolated-benchmark-rerun-2026-04-01.md`

Current interpretation of that rerun:

- `forward-feature-slice` did complete with both baseline and with-skill branches
- the with-skill branch clearly outperformed baseline on unsupported-flow precision, explicit brownfield safety, and scope discipline
- `brownfield-regression-fix` did **not** complete, so the overall benchmark set still lacks a full two-scenario control pair
- the raw runner output was not yet self-contained because `response.md` pointed to external Gemini temp files instead of storing the plan body directly

This rerun improved confidence in the benchmark contract, but on its own it still was not enough to move `tdd` beyond `review`.

## 2026-04-02 Gemini Rerun

A follow-up Gemini rerun was executed after the benchmark runner gained self-capture support for external temp-file outputs.

Retained evidence for that rerun:

- this findings note
- `eval/04-implementation/tdd/isolated-benchmark-rerun-2026-04-02.md`

Current interpretation of that rerun:

- no scenario produced a comparable baseline/with-skill `response.md` pair
- the rerun failed through a mixed blocker set rather than a single failure mode
- observed blockers included `429 QUOTA_EXHAUSTED`, `fetchAdminControls` `ECONNRESET`, and branch-level timeout exhaustion
- because no successful plan output was retained, the self-capture improvement was not meaningfully exercised on a real Gemini completion

This means the repository can now separate "artifact capture" from "runtime lane health" more cleanly, but the Gemini lane alone still was not enough to promote `tdd`.

## 2026-04-02 Copilot Fallback Review

The decisive current benchmark judgment comes from the isolated fallback review recorded in:

- `eval/04-implementation/tdd/isolated-benchmark-review.md`

Current interpretation of that review:

- a forward feature slice produced a clear baseline vs with-skill comparison
- a clean brownfield regression slice comparison also completed through the fallback lane
- in both scenarios, the with-skill branch stayed closer to the requested artifact shape and showed better regression discipline, scope control, and coexistence protection than baseline

This is enough to justify moving `tdd` to `tested`.

## Next QA Step

The primary Gemini lane should still be revalidated when it becomes stable enough to serve as a comparable benchmark runner again, but the current package now has enough evidence for `production`.
