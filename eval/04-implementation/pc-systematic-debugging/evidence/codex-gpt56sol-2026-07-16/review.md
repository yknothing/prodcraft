# Systematic Debugging Revalidation Review

## Decision

Configured revalidation acceptance: **PASS**.

Incremental skill efficacy: **NOT DEMONSTRATED BY THIS PACKET ALONE**.

The sealed run satisfied the repository's declared acceptance arm and all
fail-closed integrity gates. The baseline arm also passed every machine and
judge assertion, so this run establishes reliable production of the target
behavior but does not establish that explicit skill loading caused an
improvement over the copied benchmark context.

## Evaluators

- Evaluator: `gpt-5.6-sol` through `codex-cli 0.144.4`
- Judge: `gpt-5.4-mini` through `codex-cli 0.144.4`
- Independence limit: the evaluator and judge used distinct pinned models but
  the same provider and CLI. The judge received raw responses, response hashes,
  and the declared qualitative assertions; it did not receive machine verdicts.
- Gemini `gemini-2.5-pro` was unavailable because the installed individual
  client tier was unsupported. Claude `sonnet` was unavailable because its
  OAuth session had expired. Neither environment failure was scored as a skill
  failure.

## Isolation and Contamination Review

The accepted run did not inherit the user's default `CODEX_HOME`.

Each evaluator and judge case used a fresh temporary home containing only an
`auth.json` symlink. User configuration was disabled with
`--ignore-user-config`. A recursive fail-closed scan verified that the temporary
home contained no path matching `systematic-debugging` both before and after
the model process. The temporary home was then removed.

Three earlier runs were excluded from evidence:

- `discarded-default-codex-home-smoke`
- `discarded-default-codex-home-full`
- `discarded-preflight-only-smoke`

The first two inherited a default home that could expose a global debugging
skill. The third had a preflight scan but no postflight scan after Codex plugin
bootstrap. None contributes to the scores in this packet.

## Results

- Four scenarios, two arms, three independent repetitions: 24 cases
- Runner completion: 24/24; errors: 0
- Machine assertions: 24/24 pass
- Acceptance arm (`with_skill`): 12/12 pass
- Independent judge verdicts: 24/24 pass
- Response-hash mismatches: 0
- Missing, duplicate, or extra judge cases: 0
- Judge assertion-set mismatches: 0
- Machine/judge contradictions: 0
- Final scorer: `machine_passed=true`, `judge_status=pass`,
  `acceptance_ready=true`

Scenario D passed all repetitions with a `course-correction-note`, no
`bug_fix_report`, `local_patch_attempted=false`, and exactly three recorded
failed fixes. No fourth local patch was produced.

## Adversarial Finding

The benchmark fixtures and structured response contract expose enough of the
desired process for the baseline model to satisfy the same acceptance surface.
Therefore this packet must not be cited as evidence that
`pc-systematic-debugging` improves performance relative to no skill. A future
comparative benchmark should retain the same hash-bound and isolated execution
controls while using hidden discriminators or tasks whose correct process is
not directly recoverable from the response schema and fixture narrative.

This limitation does not invalidate the declared revalidation acceptance bar,
which makes `with_skill` the acceptance arm and treats baseline as comparison
only. It limits the strength of any causal product claim.

## Reproduction Surface

The evaluator command was:

```bash
python3 scripts/run_explicit_skill_benchmark.py \
  --benchmark eval/04-implementation/pc-systematic-debugging/isolated-benchmark.json \
  --skill-path skills/04-implementation/pc-systematic-debugging \
  --output-dir <sealed-run-dir> \
  --runner codex \
  --model gpt-5.6-sol \
  --runs-per-scenario 3 \
  --timeout-seconds 180
```

The deterministic and final scorer commands were:

```bash
python3 scripts/score_explicit_skill_benchmark.py \
  --run-dir <sealed-run-dir> \
  --benchmark eval/04-implementation/pc-systematic-debugging/isolated-benchmark.json \
  --manifest manifest.yml \
  --output <sealed-run-dir>/machine-summary.json \
  --machine-only

python3 scripts/score_explicit_skill_benchmark.py \
  --run-dir <sealed-run-dir> \
  --benchmark eval/04-implementation/pc-systematic-debugging/isolated-benchmark.json \
  --manifest manifest.yml \
  --judge-results <sealed-run-dir>/judge-results.json \
  --output <sealed-run-dir>/final-score-summary.json
```

The judge used `codex exec --ignore-user-config --ephemeral --sandbox
read-only --skip-git-repo-check -m gpt-5.4-mini` in an empty workspace with a
strict JSON output schema. `judge-run-metadata.json` binds its prompt and result
hashes.
