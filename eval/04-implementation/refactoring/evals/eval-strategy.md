# Refactoring Evaluation Strategy

## Goal

Evaluate whether `refactoring` turns a structural `code-review` follow-up into a narrow, behavior-preserving cleanup slice instead of a disguised feature change or cleanup avalanche.

## Why This Skill Matters

Prodcraft already has strong implementation discipline around `tdd`, `feature-development`, and `code-review`. The remaining gap is what happens after review identifies a real structural problem in otherwise-correct code.

The key question is whether the skill:

- keeps behavior stability as a hard constraint
- chooses one structural problem instead of broad cleanup
- requires a real safety net before moving code
- stays distinct from feature work and bug fixing

## Initial Evaluation Mode

The first evaluation is a routed manual handoff review using one constrained post-review scenario:

1. a supported reassignment handler that is behaviorally correct but contains duplicated supported-path logic and a weak extension seam

## Assertions

1. **behavior-boundary-preserved**
   - the route keeps external behavior stable and rejects requirement changes in disguise

2. **single-structural-problem**
   - the slice targets one concrete problem such as duplication or seam quality instead of mixing many cleanup goals

3. **safety-net-required**
   - existing tests are treated as the prerequisite for the refactor, not as an optional follow-up

4. **reversible-steps-shaped**
   - the proposed refactor can be executed as small extract/rename/move steps

5. **does-not-swallow-feature-development**
   - behavior changes, policy changes, and unsupported-flow expansion remain outside the refactor slice

## Pass Standard

Treat the skill as strong review-stage evidence if the handoff artifact shows that `refactoring` creates a constrained, behavior-preserving follow-up from a real structural review finding.

## Next QA Step

- add an isolated benchmark comparing a generic cleanup baseline against the same constrained refactor slice
- add a second scenario driven by tech-debt evidence rather than direct code review
