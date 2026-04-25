# Runtime Feedback Loop

Prodcraft now treats execution observability as a closed loop, not only a schema.

## Inputs

- `execution-observability.jsonl` from benchmark, eval, and runtime paths
- manual incident notes when the event stream is incomplete
- pressure-test notes from `eval/meta/prodcraft-pressure-tests/`

## Operating Cadence

- Owner: maintainers of the touched skills and workflows; if no owner is named, repository maintainers own the review
- Monthly: summarize execution observability traces
- Quarterly or after any major contract change: run the pressure-test scenario matrix

## Monthly Review

1. Run `python3 scripts/summarize_execution_observability.py <path-to-jsonl>`
   - The script accepts one or more JSONL files or directories, can write a machine-readable summary via `--output`, and can apply run-specific threshold checks via `--thresholds rules/execution-observability-thresholds.yml --fail-on-breach`
2. Review summary buckets:
   - recurring failures
   - missing usage data
   - high-risk actions
   - exact token usage by runner and skill
   - estimated token usage in a separate bucket
   - unknown token usage when usage precision is absent or unsupported
   - invalid token usage when explicit exact totals are incomplete or inconsistent
   - exact token branch deltas for with-skill versus without-skill comparisons
   - estimated token branch deltas only as advisory comparisons
   - skill context byte/character measurements, loaded ratios, and deferred ratios
   - usage-quality coverage: exact usage, estimated usage, and unavailable usage
3. Promote only high-signal findings into:
   - `skills/_gotchas.md`
   - skill-specific `references/gotchas.md`
   - ADR updates when the issue changes a system contract

## Pressure-Test Review

1. Run the scenario set in `eval/meta/prodcraft-pressure-tests/scenario-matrix.md`
2. Capture:
   - first-route correctness
   - clarification rounds required before routing stabilized
   - cross-cutting skills actually triggered
   - artifacts produced but never consumed downstream
   - course-correction jumps taken
   - friction that added cost without changing the outcome
   - exact with-skill token delta versus the without-skill baseline when exact usage exists
   - estimated with-skill token delta only as advisory data
   - deferred byte/character ratio from progressive skill loading
3. Convert repeated low-value friction into subtraction candidates rather than adding a new rule by default

## Automation

- GitHub Actions now includes `.github/workflows/runtime-feedback-loop.yml`
- The workflow runs on manual dispatch, monthly schedule, and PRs that change observability inputs or the loop contract
- If checked-out observability JSONL files exist, the workflow summarizes them into `build/legacy-execution-observability-summary.json` as a compatibility report without threshold failure
- Thresholded exact-accounting gates are scoped runs: use the manual `exact_accounting_paths` input, or call the summarizer directly with `--thresholds rules/execution-observability-thresholds.yml --fail-on-breach` for the current run artifact
- If no observability JSONL inputs are present, the workflow exits as an explicit no-op instead of pretending review happened
- Exact-token count and context-size sampling thresholds are present but non-blocking by default, so benchmark-specific runs can raise the minimum required exact-usage and skill-context event counts.
- Precision-integrity thresholds are strict when the threshold file is used: missing, estimated, unknown, or invalid usage must be explicitly allowed by a run-specific override.
- Estimated model usage fails the default threshold when present. A run must explicitly loosen that threshold if advisory estimated usage is acceptable.
- `token_usage.min_exact_coverage_ratio` gates exact usage coverage across exact, estimated, unknown, invalid, and unavailable usage events.
- `unknown_token_usage.max_count: 0` means missing `usage_precision` is forbidden in exact-accounting runs, even when `usage_source` is `provider`.
- `invalid_token_usage.max_count: 0` means explicit exact usage with incomplete or inconsistent totals is forbidden before it can contribute to exact KPIs.
- `estimated_token_usage.max_count: 0` means estimated usage is forbidden in exact-accounting runs; if a suite permits it, the report remains advisory and cannot be used to claim exact token savings.
- `skill_context.min_measured_count` and `skill_context.min_sampling_ratio` gate whether progressive-loading byte/character samples exist for the run.

## Principles

- Do not invent gotchas from imagination alone.
- Prefer repeated real failures over one-off surprises.
- Keep runtime summaries structured enough to support future trace grading.
- Use pressure-test evidence to justify deletion, downgrade, or simplification decisions.
- Treat only explicit `usage_precision: exact` provider or runner usage with self-consistent totals as token evidence; keep runner-estimated usage in a separate advisory bucket.
- Treat provider usage without `usage_precision` as unknown. It is compatibility telemetry, not exact token evidence.
- Treat static skill-context byte/character counts as optimization evidence only; do not convert them into token estimates without a model-specific tokenizer or provider token-count API.
- Without provider usage or a tokenizer-backed exact count, report context efficiency only as exact character/byte loading and deferral efficiency. Do not call it token savings.
- Optimize context by improving skill loading, supporting-file boundaries, and stable prompt prefixes before compressing skill instructions.

## Outputs

- updated gotchas
- benchmark/eval follow-up tasks
- explicit backlog items for missing telemetry or risky runner behavior
- subtraction candidates backed by observed pressure-test friction
