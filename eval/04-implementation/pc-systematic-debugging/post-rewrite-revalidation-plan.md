# Systematic Debugging Post-Rewrite Revalidation Plan

> Status: pending. The 2026-07 rewrite substantially changed the skill body, so
> the isolated benchmark and integration evidence recorded before the rewrite
> describe the previous contract and must be regenerated before the next status
> advance. Existing evidence paths are retained for audit lineage.

## What Changed

The rewrite added or strengthened these behaviors, which the previous evidence
does not cover:

- Iron Law framing: no fix without a reproduced failure and a falsifiable root cause
- Step 1 evidence discipline: full error reading and stale-artifact verification
  before any theory forms
- Reproduce-then-minimize step with bisection and differential-debugging routing
  into `references/techniques.md`
- Explicit hypothesis loop: single falsifiable hypothesis, prediction, cheapest
  experiment, one variable per iteration, debug journal
- Two-way fix causality proof: repro passes with the fix, fails again without it
- Same-failure vs new-failure interpretation in the escalation rule
- Flaky-failure discipline: no rerun-until-green, condition-based waits
- Three new gotchas: stale artifact, flaky rerun, victim-vs-culprit traces

## Revalidation Scope

1. **Isolated explicit benchmark (gemini runner, N>=3 per scenario per arm)**
   - Scenario A: multi-hypothesis regression where the obvious first fix is wrong
     (asserts hypothesis journal, one-variable discipline, no fix stacking)
   - Scenario B: intermittent/flaky failure (asserts refusal to rerun-until-green,
     stabilization before fix)
   - Scenario C: stale-artifact trap where the observed behavior contradicts the
     source (asserts marker verification before further theory work)
   - Scenario D: structural mismatch after repeated failed fixes (asserts
     course-correction-note escalation instead of a fourth patch)
2. **Machine-checkable assertions first**: bug-fix-report presence and required
   fields, two-way causality statement present, named downstream skills resolve
   against manifest.yml.
3. **Integration review**: one handoff chain bug-history-retrieval ->
   systematic-debugging -> tdd on a brownfield fixture.

## Acceptance Bar

- All machine-checkable assertions pass in every run (N>=3)
- Zero gate-bypass in scenario D across all runs
- Judge-scored assertions pass in the majority of runs with no contradiction
  between judge verdict and machine checks
