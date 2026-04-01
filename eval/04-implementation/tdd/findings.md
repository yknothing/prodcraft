# TDD QA Findings

## Summary

`tdd` has moved to `review` status.

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
- still in need of isolated benchmark evidence before it can leave `review`

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

## Next QA Step

Stabilize or replace the current benchmark runner with a lane that can produce comparable baseline and with-skill `response.md` artifacts, then rerun the isolated benchmark for both the forward feature slice and the brownfield regression slice.
