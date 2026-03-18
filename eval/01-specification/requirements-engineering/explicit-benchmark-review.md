# Requirements Engineering Explicit Invocation Benchmark Review

## Scope

This review summarizes the current isolated explicit-invocation evidence for `requirements-engineering`.

All valid benchmark runs in this review were executed using:

- isolated temp workspaces outside the Prodcraft repo
- a clean baseline prompt that forbids local file reads
- a with-skill prompt that permits only `./skill-under-test/SKILL.md`

## Valid Benchmark Artifacts

| Artifact | Scenario | Notes |
|---|---|---|
| `explicit-benchmark-run-2026-03-16-clean-smoke` | `approvals-feature-en` | First valid isolated smoke test |
| `explicit-benchmark-run-2026-03-16-expense-zh` | `expense-workflow-zh` | Chinese stakeholder-note scenario |
| `explicit-benchmark-run-2026-03-16-audit-log` | `audit-log-compliance-en` | Initial compliance-sensitive run; revealed over-quantification tendency |
| `explicit-benchmark-run-2026-03-16-audit-log-rerun` | `audit-log-compliance-en` | Re-run after tightening the skill against invented precision |

Exploratory but non-authoritative artifact:

- `explicit-benchmark-run-1` is **not valid baseline evidence** because it was run from inside the repo and showed local-context contamination.

## Cross-Scenario Manual Review

| Scenario | Baseline | With skill | Judgment |
|---|---|---|---|
| `approvals-feature-en` | Strong structured requirements doc | Stronger obligation-style requirements, clearer traceability, better downstream handoff shape | **Positive lift** |
| `expense-workflow-zh` | Good extraction of stakeholder notes into requirements | Clearer `shall` statements, cleaner source traceability, better explicit non-goals and open-question handling | **Positive lift** |
| `audit-log-compliance-en` initial | Strong baseline, cautious about unsupported bounds | Initially over-specified some unsupported precision and assumptions | **Mixed / exposed a skill defect** |
| `audit-log-compliance-en` re-run | Strong baseline, leaves some bounds open | Improved: converts unsupported precision into open questions or assumptions more often, while preserving traceability and requirements-layer discipline | **Improved after skill refinement** |

## What the Benchmark Shows

### 1. The skill adds value under explicit invocation

Across scenarios, the with-skill outputs consistently show better requirements discipline than baseline:

- stronger use of obligation-style requirement statements
- more systematic source traceability
- clearer scope boundaries and explicit non-goals
- better framing of unresolved ambiguity as open questions instead of silently baking design assumptions into requirements

### 2. Baseline models are already strong

The baseline is often good enough to pass coarse binary assertions. That means this benchmark must review **quality deltas**, not just assertion counts.

For this skill, the meaningful question is not "can Claude write a requirements document?" but:

- does the skill produce **more auditable requirements**
- does it reduce silent solutioning
- does it create a cleaner handoff into downstream specification/design work

### 3. The benchmark exposed a real skill defect

The initial audit-log run showed that the skill's guidance on quantifying NFRs could push the model toward **invented precision**:

- unsupported latency targets
- unsupported durability/SLA claims
- speculative long-term scalability bounds

This was a genuine defect in the skill guidance, not just model noise.

The skill was then refined to require:

- quantification only when supported by source evidence
- otherwise, use explicit assumptions or open questions

The audit-log re-run improved on exactly this dimension.

## Current Judgment

`requirements-engineering` now has credible evidence that it is:

- **weak as an auto-discoverable skill** in a crowded ecosystem
- **strong as a workflow-driven / manual-invocation skill**

That is a valid and useful shape for Prodcraft. Not every core skill needs to win at discoverability if it is reliably invoked by lifecycle routing and produces better downstream artifacts when loaded.

## Status Implication

Despite the positive explicit-invocation evidence, the skill should remain in `review` status for now because:

1. trigger discoverability still fails its current bar
2. benchmark evidence is strong but still limited in breadth
3. `intake -> requirements-engineering` handoff quality has not yet been evaluated

## Next Required Evidence

1. Run a formal `intake -> requirements-engineering` handoff benchmark using an approved intake brief.
2. Add at least one brownfield / legacy-modernization scenario to ensure the skill does not overfit greenfield discovery notes.
3. Keep the "invented precision" check in future benchmark reviews; it is now a known regression vector.
