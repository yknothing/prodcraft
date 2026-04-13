# Spec Writing to API Design Handoff Review

## Goal

Verify that `spec-writing` produces a `spec-doc` that `api-design` can consume
without exposing migration-only operations or inventing contract answers to
unresolved brownfield questions.

## Scenario

- `access-review-modernization-spec`

This is a brownfield modernization scenario where:

- release 1 must coexist with the legacy module during audit season
- history older than two years remains behind a legacy-read boundary
- some reassignment and data-correction flows are intentionally unsupported
- sync semantics are not yet decided

## Artifacts Reviewed

- manual benchmark evidence:
  - `manual-run-2026-04-10-access-review/.../without_skill/response.md`
  - `manual-run-2026-04-10-access-review/.../with_skill/response.md`

## Review Findings

## 1. The baseline spec would mislead API design

The baseline draft makes API drift likely because it:

- treats sync as required behavior
- pulls historical import and cutover into release-1 scope
- prescribes service decomposition instead of contract boundaries

An API designer consuming that document would have strong pressure to expose
migration and consistency internals publicly.

## 2. The with-skill spec is downstream-usable

The skill-applied spec is fit for `api-design` because it:

- names supported release-1 flows separately from non-goals
- keeps migration-only and cutover-only behavior out of the public contract
- preserves unsupported-flow handling as explicit product behavior
- leaves sync and tenant-variant questions open instead of inventing endpoints

## Assertion Review

| Assertion | Review result | Notes |
|---|---|---|
| release-boundary-stays-contract-level | pass | The with-skill branch stays at policy/interface level instead of implementation design. |
| migration-operations-stay-non-public | pass | Import, sync, and cutover work remain outside the release-1 contract. |
| unsupported-flows-stay-explicit | pass | The spec keeps unsupported reassignment/data-correction variants visible. |
| open-questions-preserved-for-api-work | pass | Sync and tenant-support questions remain open instead of becoming assumed APIs. |

## Conclusion

This routed handoff review is enough to support a narrow `tested` decision when
combined with the manual benchmark review.
