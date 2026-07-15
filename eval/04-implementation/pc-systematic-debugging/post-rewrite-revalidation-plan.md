# Systematic Debugging Post-Rewrite Revalidation Plan

> Status: isolated benchmark complete; configured acceptance passed. The sealed
> evidence packet is in
> `evidence/codex-gpt56sol-2026-07-16/`. Comparative efficacy remains open because
> the baseline arm also passed every machine and judge assertion. Existing evidence
> paths are retained for audit lineage.

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

1. **Isolated explicit benchmark (pinned evaluator, N>=3 per scenario per arm)**
   - Scenario A: multi-hypothesis regression where the obvious first fix is wrong
     (asserts hypothesis journal, one-variable discipline, no fix stacking)
   - Scenario B: intermittent/flaky failure (asserts refusal to rerun-until-green,
     stabilization before fix)
   - Scenario C: stale-artifact trap where the observed behavior contradicts the
     source (asserts marker verification before further theory work)
   - Scenario D: structural mismatch after repeated failed fixes (asserts
     course-correction-note escalation instead of a fourth patch)
2. **Machine-checkable assertions first**:
   - scenarios A-C require a structured `bug-fix-report` envelope with required
     fields and boolean two-way causality evidence
   - scenario D requires a structured `course-correction-note` envelope, no
     `bug_fix_report`, `local_patch_attempted=false`, and exactly three recorded
     failed fixes
   - every named downstream skill must resolve exactly against `manifest.yml`
   - the `with_skill` arm is the acceptance arm; baseline is scored for comparison
     but is not required to satisfy the skill contract
3. **Integration review**: one handoff chain bug-history-retrieval ->
   systematic-debugging -> tdd on a brownfield fixture.

## Acceptance Bar

- All machine-checkable assertions pass in every `with_skill` run (N>=3)
- Zero gate-bypass in scenario D across all runs
- Judge-scored assertions pass in the majority of runs with no contradiction
  between judge verdict and machine checks

## Reproducible Commands

Pin the model explicitly. One runner invocation produces all four scenarios,
both arms, and three independent runs per scenario: 24 response cases total.

```bash
python3 scripts/run_explicit_skill_benchmark.py \
  --benchmark eval/04-implementation/pc-systematic-debugging/isolated-benchmark.json \
  --skill-path skills/04-implementation/pc-systematic-debugging \
  --output-dir <run-dir> \
  --runner codex \
  --model gpt-5.6-sol \
  --runs-per-scenario 3 \
  --timeout-seconds 180
```

The runner exits non-zero if any response case times out or the model command
fails. `execution_summary.json` records benchmark and skill hashes plus prompt
and response/error hashes for every case.

Run deterministic assertions separately. A successful machine-only command is
not final acceptance; its output always records `acceptance_ready=false` until
content-hash-bound judge results are supplied.

```bash
python3 scripts/score_explicit_skill_benchmark.py \
  --run-dir <run-dir> \
  --benchmark eval/04-implementation/pc-systematic-debugging/isolated-benchmark.json \
  --manifest manifest.yml \
  --output <machine-summary.json> \
  --machine-only
```

Judge results must use schema version `explicit-benchmark-judge-results.v1` and
identify each case by `scenario_id`, `run_number`, `arm`, and exact
`response_sha256`. Each case must return every named `judge_assertions` item from
the benchmark plus a `pass` or `fail` verdict. Cross-validate them with:

```bash
python3 scripts/score_explicit_skill_benchmark.py \
  --run-dir <run-dir> \
  --benchmark eval/04-implementation/pc-systematic-debugging/isolated-benchmark.json \
  --manifest manifest.yml \
  --judge-results <judge-results.json> \
  --output <final-score-summary.json>
```

The final command fails on missing judge cases, response-hash drift, omitted or
duplicate judge assertions, machine/judge contradiction, or any failing
`with_skill` acceptance case.

## Revalidation Result

- Evaluator: `gpt-5.6-sol`; judge: `gpt-5.4-mini`; CLI: `codex-cli 0.144.4`
- Per-case evaluator home: temporary auth-only `CODEX_HOME`, user config ignored,
  recursive `systematic-debugging` preflight and postflight matches both zero
- Runner: 24/24 completed, zero errors
- Machine assertions: 24/24 pass; `with_skill`: 12/12 pass
- Hash-bound judge: 24/24 pass; zero contradictions
- Final scorer: `acceptance_ready=true`
- Sealed packet:
  [`evidence/codex-gpt56sol-2026-07-16/`](evidence/codex-gpt56sol-2026-07-16/)
- Adversarial review:
  [`review.md`](evidence/codex-gpt56sol-2026-07-16/review.md)

The accepted evaluator and judge use distinct pinned models but the same provider
and CLI. The baseline arm also passed 12/12, so this result closes the declared
revalidation bar but must not be used as a standalone claim of incremental skill
lift.
