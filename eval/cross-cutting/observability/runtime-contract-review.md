# Observability Runtime Contract Review

## Goal

Verify that `observability` is backed by real repository behavior rather than only by design documents.

## Artifacts Reviewed

### Skill and design contract

- `skills/cross-cutting/observability/SKILL.md`
- `docs/adr/ADR-001-execution-observability-envelope.md`
- `docs/observability/execution-event-schema-v1.md`
- `docs/observability/runtime-feedback-loop.md`

### Runtime consumers

- `scripts/summarize_execution_observability.py`
- `.github/workflows/runtime-feedback-loop.yml`

### Live emitted artifacts

- `eval/05-quality/code-review/run-2026-04-03-copilot-brownfield-only-clean/execution-observability.jsonl`
- `eval/02-architecture/system-design/run-2026-04-03-copilot-brownfield-only-v1-1-rerun/execution-observability.jsonl`

## Findings

## 1. The contract boundary is clear

The skill stays scoped to execution telemetry contracts:

- event schema
- instrumentation boundaries
- usage accounting rules
- runtime review loop

It does not collapse into production dashboards or alert design. That separation matches the intended split from `monitoring-observability`.

## 2. Real artifacts follow the declared schema

The reviewed JSONL artifacts use:

- `schema_version: "execution-event.v1"`
- canonical event names such as `runner_execution.started`, `runner_execution.completed`, `skill_invocation.started`, and `model_usage.unavailable`
- canonical usage fields `token_input`, `token_output`, and `token_total`

The code-review clean run shows both baseline and with-skill branches under the same envelope, including explicit skill metadata for the with-skill path.

## 3. Missing usage is handled honestly

The reviewed artifacts do not invent token counts when the runner cannot expose usage.

Instead, they record:

- `event_type: "model_usage.unavailable"`
- `usage_source: "unavailable"`
- `token_input: null`
- `token_output: null`
- `token_total: null`

This matches the skill contract and schema document exactly.

## 4. The feedback loop is executable today

The repository already contains:

- a summarizer that aggregates recurring failures, missing usage, and high-risk actions
- a GitHub Actions workflow that collects observability JSONL files, summarizes them, and enforces thresholds when inputs exist

Spot checks on the reviewed artifacts show the current summary loop works:

- the code-review clean run summarized with `missing_usage.count = 2`
- the in-progress system-design rerun summarized with `missing_usage.count = 1`
- neither summary produced recurring failures or high-risk actions

## 5. Partial traces remain visible

The reviewed system-design rerun is not fully complete, but it still emits enough structured events to show:

- the baseline branch completed
- the with-skill branch started
- the trace stopped after `runner_execution.started`

That is useful review-stage evidence because it shows incomplete execution remains inspectable instead of collapsing into opaque log output.

## Conclusion

`observability` now has enough repository-backed evidence to move from `draft` to `review`.

The contract is implemented, emitted, and consumable. What is still missing is broader coverage:

- no dedicated isolated benchmark has been executed for this skill yet
- current live checks are limited to benchmark-generated artifacts
- there is not yet a broader matrix covering completed, failed, and non-benchmark runtime paths

So the correct next state is `review`, not `tested`.
