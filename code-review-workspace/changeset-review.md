# Changeset Review Evaluation

## Goal

Verify that `code-review` catches blocking correctness and boundary violations in a concrete brownfield changeset.

## Scenario

- `access-review-modernization-code-review`

This is a brownfield modernization slice where:

- unsupported reassignment variants must fail explicitly
- tenant authorization remains partly unresolved
- no public contract guarantees immediate legacy synchronization

## Artifacts Reviewed

- Manual baseline review: `manual-run-2026-03-17-access-review`
- Input fixtures:
  - `fixtures/access-review-modernization-task-slice.md`
  - `fixtures/access-review-modernization-api-contract.md`
  - `fixtures/reassignments.py`
  - `fixtures/test_reassignments.py`

## Baseline Findings

The baseline review produces reasonable but weak feedback:

- it suggests more tests
- it asks about sync timing
- it comments on readability

But it misses the real blockers.

## With-Skill Findings

The skill-applied review identifies the issues that should actually stop merge:

- unsupported reassignment variants are silently accepted instead of returning `UNSUPPORTED_RELEASE1_FLOW`
- the code hard-codes immediate legacy synchronization even though sync semantics remain unresolved
- tests do not cover the highest-risk contract boundary
- tenant-policy ambiguity is being deferred into guessed implementation behavior

## Assertion Review

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| finds blocking contract violations | fail | pass | Baseline misses the contract-breaking fallback behavior. |
| preserves brownfield safety | partial | pass | With-skill treats unresolved sync/coexistence behavior as review concerns. |
| checks test adequacy | partial | pass | With-skill points to the missing unsupported-flow test specifically. |
| prioritizes findings | fail | pass | Baseline under-prioritizes real blockers. |
| stays within review scope | pass | pass | Neither branch requests unrelated redesign. |

## Conclusion

The first manual review suggests `code-review` also fits the emerging core-spine pattern:

- it is more valuable as a routed/core workflow skill than as a discoverability-first skill
- its value comes from stopping scope-boundary and contract violations before merge

This is review-stage evidence only. The next step is an isolated benchmark on the same changeset plus a non-brownfield feature changeset.
