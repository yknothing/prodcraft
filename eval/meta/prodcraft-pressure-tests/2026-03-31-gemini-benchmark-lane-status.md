# 2026-03-31 Gemini Benchmark Lane Status

## Scope

This note records the current execution status of the repository's Gemini-based explicit benchmark lane on `2026-03-31`.

It is runtime evidence, not skill-quality evidence.

## What Was Attempted

### 1. Direct headless probe

Command shape:

- `gemini -p "Reply only OK." --output-format text --approval-mode plan`

Observed behavior:

- the current CLI default lane identifies itself as `gemini-3.1-pro-preview`
- repeated requests returned `429 RESOURCE_EXHAUSTED`
- server detail: `MODEL_CAPACITY_EXHAUSTED`

### 2. TDD isolated benchmark smoke run

Command shape:

- `python3 scripts/run_explicit_skill_benchmark.py --benchmark eval/04-implementation/tdd/isolated-benchmark.json --skill-path skills/04-implementation/tdd --output-dir eval/04-implementation/tdd/isolated-benchmark-run-2026-03-31-smoke --scenario-id forward-feature-slice`

Observed artifacts:

- `run_metadata.json`
- `execution-observability.jsonl`
- `progress.log`
- per-branch `prompt.txt`
- per-branch `error.txt`

Missing artifacts:

- no `response.md` for baseline
- no `response.md` for with-skill

### 3. TopBrains direct Gemini worker probe

Command shape:

- `TOPBRAINS_ORCH_DIR=/tmp/topbrains-orch TOPBRAINS_WORKER_TIMEOUT_S=90 python3 <topbrains-root>/scripts/launch_worker_async.py --model gemini-3.1-pro --task-type documentation --work-dir <prodcraft-root> --prompt "Reply only OK."`

Observed artifacts:

- `/tmp/topbrains-orch/worker_runs/tasks/W1774959950_95414.json`
- `/tmp/topbrains-orch/worker_runs/status/W1774959950_95414.json`
- `/tmp/topbrains-orch/worker_runs/results/W1774959950_95414.md`

Observed status:

- worker launched successfully
- worker ran for `82.828s`
- final status was `completed` with `healthy: false`
- final reason was `worker_failed`

## Concrete Failure Modes

### Baseline branch

- `Timed out after 120s`

### With-skill branch

- Gemini startup/auth path failed before usable model output
- concrete errors included:
  - `loadCodeAssist` `ECONNRESET`
  - `fetchAdminControls` `ECONNRESET`
- MCP startup noise and local extension conflicts were present but were not the primary final blocker

### TopBrains direct worker lane

- TopBrains did successfully launch the direct Gemini worker and write task/status/result artifacts
- the final result artifact still failed inside Gemini startup/auth transport
- concrete error included:
  - `fetchAdminControls` `ECONNRESET`
- this was **not** a `capacity_exhausted` result
- this was **not** evidence that TopBrains wrapper logic alone was dropping a healthy Gemini completion

### Copilot fallback benchmark lane

- a repository-owned fallback run exists at `eval/04-implementation/tdd/isolated-benchmark-run-2026-03-31-copilot`
- both baseline branches timed out after `120s`
- only one with-skill branch produced a `response.md`
- this is not a clean enough control pair to count as benchmark evidence

## Current Judgment

The repository benchmark contract is now wired and runnable enough to create benchmark scaffolding and error artifacts.

The blocking issue is the current Gemini execution lane, even when routed through TopBrains:

- default lane capacity instability (`429`)
- intermittent runtime/auth transport failures (`ECONNRESET`)
- direct TopBrains worker launch does not remove the Gemini transport blocker

The first fallback lane is not sufficient yet either:

- current `copilot` benchmark output is too incomplete to serve as a comparable baseline/with-skill control

Until one lane stabilizes enough to produce comparable `response.md` artifacts, benchmark runs should be treated as **execution-blocked**, not as skill-quality evidence.

## Immediate Implication

Do not promote skills to `tested` based on these runs.

The next useful step is to stabilize or swap the runtime lane, then rerun the same benchmark scenario before expanding to multi-scenario reviews.
