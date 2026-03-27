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
   - The script now accepts one or more JSONL files or directories, can write a machine-readable summary via `--output`, and can apply threshold checks via `--thresholds rules/execution-observability-thresholds.yml --fail-on-breach`
2. Review three summary buckets:
   - recurring failures
   - missing usage data
   - high-risk actions
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
3. Convert repeated low-value friction into subtraction candidates rather than adding a new rule by default

## Automation

- GitHub Actions now includes `.github/workflows/runtime-feedback-loop.yml`
- The workflow runs on manual dispatch, monthly schedule, and PRs that change observability inputs or the loop contract
- If checked-out observability JSONL files exist, the workflow summarizes them into `build/execution-observability-summary.json` and fails when thresholds in `rules/execution-observability-thresholds.yml` are breached
- If no observability JSONL inputs are present, the workflow exits as an explicit no-op instead of pretending review happened

## Principles

- Do not invent gotchas from imagination alone.
- Prefer repeated real failures over one-off surprises.
- Keep runtime summaries structured enough to support future trace grading.
- Use pressure-test evidence to justify deletion, downgrade, or simplification decisions.

## Outputs

- updated gotchas
- benchmark/eval follow-up tasks
- explicit backlog items for missing telemetry or risky runner behavior
- subtraction candidates backed by observed pressure-test friction
