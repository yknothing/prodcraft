# Runtime Feedback Loop

Prodcraft now treats execution observability as a closed loop, not only a schema.

## Inputs

- `execution-observability.jsonl` from benchmark, eval, and runtime paths
- manual incident notes when the event stream is incomplete

## Monthly Review

1. Run `python3 scripts/summarize_execution_observability.py <path-to-jsonl>`
2. Review three summary buckets:
   - recurring failures
   - missing usage data
   - high-risk actions
3. Promote only high-signal findings into:
   - `skills/_gotchas.md`
   - skill-specific `references/gotchas.md`
   - ADR updates when the issue changes a system contract

## Principles

- Do not invent gotchas from imagination alone.
- Prefer repeated real failures over one-off surprises.
- Keep runtime summaries structured enough to support future trace grading.

## Outputs

- updated gotchas
- benchmark/eval follow-up tasks
- explicit backlog items for missing telemetry or risky runner behavior
