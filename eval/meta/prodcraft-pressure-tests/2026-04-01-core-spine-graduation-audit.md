# Core Spine Evidence Audit

> Update 2026-04-03: this file remains correct as the historical `2026-04-01` audit snapshot, but the current repository state has changed. `tdd`, `verification-before-completion`, `task-breakdown`, and `intake` are now `tested`. `intake` moved under a routed QA posture after the repository confirmed that the Anthropic discoverability lane is blocked by the harness/CLI interaction while the explicit benchmark and integration evidence already satisfy the routed tested gate. All other target spine skills remain at `review`.

This audit evaluates whether each skill in the proposed core spine has sufficient evidence to graduate from `review` to `tested`, `secure`, or `production`.

**Graduation Rule:** A skill cannot move beyond `review` until it has at least one clean, isolated benchmark or multi-reviewer cross-validation that proves its value over a generic baseline.

## Audit Results

| Skill | Current Status | Missing Evidence | Recommendation |
|-------|----------------|------------------|----------------|
| `intake` | review at audit time; now `tested` | At audit time, the redesigned contract lacked a trustworthy current tested gate. On 2026-04-03 the repository formally treated `intake` as a routed gateway skill and used `eval/00-discovery/intake/post-redesign-benchmark-review.md` plus `eval/00-discovery/intake/post-redesign-integration-review.md` as the tested evidence; Anthropic trigger eval remains supplemental diagnostic only while the harness is blocked. | **Historical audit hold was correct on 2026-04-01. Current repo state: hold at `tested` until deeper downstream drill or security evidence exists.** |
| `problem-framing` | review | Has manual handoff reviews and semi-isolated evidence, but no clean automated benchmark pair. | **Hold at review**. Do not promote. |
| `requirements-engineering` | review | Has semi-isolated and manual reviews, but the isolated benchmark attempt was contaminated (runner artifacts). | **Hold at review**. Do not promote. |
| `system-design` | review | Needs isolated benchmark evidence. | **Hold at review**. Do not promote. |
| `task-breakdown` | review at audit time; now `tested` | 2026-04-02 fallback benchmark review completed cleanly enough to justify `tested`; see `eval/03-planning/task-breakdown/isolated-benchmark-review.md`. | **Historical audit hold was correct on 2026-04-01. Current repo state: hold at `tested`.** |
| `tdd` | review at audit time; now `tested` | 2026-03-31 benchmark lane attempt failed at audit time. A later 2026-04-02 fallback benchmark review completed cleanly enough to justify `tested`; see `eval/04-implementation/tdd/isolated-benchmark-review.md`. | **Historical audit hold was correct on 2026-04-01. Current repo state: hold at `tested` until security review exists.** |
| `feature-development` | review | Needs isolated benchmark evidence. | **Hold at review**. Do not promote. |
| `code-review` | review | Needs isolated benchmark evidence. | **Hold at review**. Do not promote. |
| `ci-cd` | review | Needs isolated benchmark evidence. | **Hold at review**. Do not promote. |
| `deployment-strategy` | review | Needs isolated benchmark evidence. | **Hold at review**. Do not promote. |
| `verification-before-completion` | review at audit time; now `tested` | 2026-04-02 fallback benchmark review completed cleanly enough to justify `tested` after fixing fast-track hallucination; see `eval/cross-cutting/verification-before-completion/isolated-benchmark-review.md`. | **Historical audit hold was correct on 2026-04-01. Current repo state: hold at `tested`.** |

## Conclusion

**At the 2026-04-01 audit point, no skills in the target spine could graduate in that iteration.**

The evidence gathered in `eval/` currently consists of manual reviews, semi-isolated checks, and benchmark plans. The actual execution of those benchmarks is blocked by the runtime issues documented in `eval/meta/prodcraft-pressure-tests/2026-03-31-gemini-benchmark-lane-status.md`.

Attempting to bump status without the required automated control-pair evidence would violate the repository's maturity contract. 

## Current Addendum

Current repo state after the follow-up benchmark work:

1. `tdd` has now moved to `tested`.
2. `verification-before-completion` has now moved to `tested` after closing the fast-track evidence hallucination loophole.
3. `task-breakdown` has now moved to `tested` based on solid isolated benchmark evidence across greenfield and brownfield scenarios.
4. `intake` has now moved to `tested` after the repository chose a routed QA posture and tied the claim to current explicit benchmark plus integration evidence instead of the blocked discoverability lane.
5. The rest of the target spine still honestly remains at `review`.
