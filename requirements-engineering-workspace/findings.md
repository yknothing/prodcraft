# Requirements Engineering QA Findings

## Summary

`requirements-engineering` remains in `review` status.

Three trigger-eval iterations were run on **2026-03-16**:

| Iteration | Artifact | Positive Recall | Negative Precision | Notes |
|---|---|---:|---:|---|
| 1 | `results-trigger-iter1.json` | 0/4 | 6/6 | Initial migrated description |
| 2 | `results-trigger-iter2-baseline.json` | 0/4 | 6/6 | Frontmatter fixed to single-line description |
| 3 | `results-trigger-iter3.json` | 0/4 | 6/6 | Description reframed as upstream "what should we build" skill |

## What We Learned

1. **Wrapped YAML descriptions were a real packaging defect** and are now prevented by the validator.
2. **Fixing the packaging defect did not improve recall.**
3. **Rewriting the description three times did not improve recall.**
4. The remaining issue is most likely **skill-ecosystem competition**, not missing keywords.
5. The official trigger harness measures **description discoverability only**. It does not evaluate the skill body once invoked.
6. The first explicit-invocation benchmark attempt (`explicit-benchmark-run-1`) is **context-contaminated** as a baseline artifact. The baseline response referenced local skill structure and template behavior, which means it was not a clean no-skill control.
7. The first **clean isolated** smoke benchmark shows early body-quality lift even though baseline quality is already decent. The skill improves requirements discipline more than raw binary pass/fail counts.
8. Cross-scenario isolated benchmarking shows the skill is useful under explicit invocation, but also exposed a real regression vector: **invented precision** in NFR quantification. The skill has been tightened to convert unsupported bounds into open questions or labeled assumptions instead.
9. The first routed handoff benchmark shows that the skill preserves intake constraints better than baseline, especially around explicit scope boundaries, carry-through risks, and downstream handoff shape.
10. A second routed handoff scenario has now been added for brownfield modernization, but the first official run was blocked by local Claude CLI authentication before either branch generated output.
11. A supplemental manual evaluation of the brownfield modernization scenario indicates the same pattern as the approvals scenario: baseline can produce a usable requirements draft, but the skill materially improves coexistence-boundary preservation, explicit open questions, and downstream handoff shape.

## Implication for Prodcraft

`requirements-engineering` should not currently be treated as a strong auto-discoverable skill in a crowded local environment.

For now, it is better understood as:

- a core specification skill in the lifecycle
- a strong candidate for workflow-driven or manual invocation
- a skill whose value must next be measured through explicit invocation quality and handoff quality, not just discovery metadata

For explicit-invocation QA:

- prior baseline evidence should be treated as exploratory only
- future benchmark evidence must come from isolated temp workspaces outside the repo
- benchmark tooling must preserve prompts and runtime context for auditability

## Next QA Step

Preserve the manual brownfield review as supplemental evidence, then rerun `access-review-modernization-handoff` through the isolated official harness once local Claude CLI authentication is restored so the second scenario has automated evidence as well.
