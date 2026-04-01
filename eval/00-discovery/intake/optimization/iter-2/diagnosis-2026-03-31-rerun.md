# Intake Trigger Rerun Diagnosis

Date: 2026-03-31

## Scope

This note records the first valid rerun of the **current** `intake` description revision:

`Route new engineering work before execution. Use when a user wants to build a new product, app, or internal tool, start from scratch, plan a migration, run a multi-sprint tech-debt or documentation effort, or says they are not sure where to start. Also use when a feature, refactor, or hotfix needs scope triage before implementation. Do not use for ongoing work, concrete debugging, trivial edits, direct commands, PR review, or pure questions.`

## Runtime Validity

The rerun was not blocked by quota or raw Claude reachability:

- direct `claude -p "say only OK" --output-format text` returned `OK`
- `eval/00-discovery/intake/scripts/preflight_claude_eval.py` returned `{"ok": true, ...}`

## Artifacts

- `results-core-2026-03-31.json`
- `results-core-2026-03-31.observability.jsonl`
- `results-non-trigger-2026-03-31.json`
- `results-non-trigger-2026-03-31.observability.jsonl`

## Results

- core recall: `0/5`
- non-trigger precision: `10/10`

## Interpretation

The current description revision still over-indexes on false-positive control.

What this means:

- the description is validly rerun now
- the current problem is not quota
- the current problem is not the vendored harness
- the current problem is that `intake` still does not surface on its strongest entry prompts in the present skill ecosystem

## Practical Conclusion

Treat the latest description as **validated but still underperforming on core discoverability**.

Do not describe the current revision as "awaiting rerun" any longer.

The next decision is strategic, not operational:

1. widen the description again to recover core recall, or
2. accept weaker metadata recall and rely more explicitly on routed invocation through `prodcraft` and downstream workflow contracts
