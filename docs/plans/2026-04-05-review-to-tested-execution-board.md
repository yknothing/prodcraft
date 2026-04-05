# Review-To-Tested Execution Board

> Date: 2026-04-05

> Purpose: keep the remaining `review` pool honest by naming the smallest next evidence artifact for each skill instead of using "needs more QA" as a placeholder blocker.

## Current Review Pool

- total `review` skills: `12`
- closest to `tested`: `system-design`
- runner-blocked critical reviews: `system-design`, `monitoring-observability`
- newly reviewed standard skills: `10`

## Priority Order

1. `system-design`
2. `monitoring-observability`
3. the newly reviewed standard skills, grouped by lifecycle adjacency

## Review Skill Matrix

| Skill | Current posture | Smallest honest next artifact | Why that artifact is next |
|---|---|---|---|
| `system-design` | benchmark plan, findings, and routed handoff exist; no clean with-skill benchmark result yet | one clean `benchmark_results_path` on the existing brownfield isolated benchmark | this is already the narrowest remaining blocker for promotion |
| `monitoring-observability` | manual routed review exists across brownfield and non-brownfield scenarios | first benchmark result that compares baseline vs with-skill signal plans | the integration story exists; the missing proof is runner-backed quality lift |
| `market-analysis` | eval strategy seeded | first routed benchmark result on one opportunity-shaping scenario plus one handoff review into `feasibility-study` or `requirements-engineering` | it needs proof that it improves evidence quality instead of generating generic competitor prose |
| `feasibility-study` | eval strategy seeded | first routed benchmark result on one go/no-go scenario plus one handoff review into `requirements-engineering` or intake decisioning | it needs evidence that it sharpens decision quality rather than rewriting discovery notes |
| `spec-writing` | eval strategy seeded | first routed benchmark result plus one handoff review into `system-design` | tested posture depends on downstream architectural usability, not just spec completeness |
| `domain-modeling` | eval strategy seeded | first routed benchmark result plus one handoff review into `data-modeling` or `system-design` | it needs proof that the model actually improves later design choices |
| `data-modeling` | eval strategy seeded | first routed benchmark result plus one handoff review into `task-breakdown` or implementation planning | it needs proof that storage ownership and migration safety become clearer downstream |
| `security-design` | eval strategy seeded | first routed benchmark result plus one handoff review into `security-audit` or implementation | tested posture depends on concrete control design, not generic threat prose |
| `bug-history-retrieval` | eval strategy seeded | first routed benchmark result on a lineage-sensitive bug scenario plus one handoff review into `systematic-debugging` | tested posture depends on grounding the next debugging step in canonical history |
| `accessibility` | eval strategy seeded | first routed benchmark result on a UI acceptance scenario plus one handoff review into `acceptance-criteria` or QA | it needs proof that outputs become implementation- and review-ready checks |
| `internationalization` | eval strategy seeded | first routed benchmark result on a locale-sensitive UI/content scenario plus one handoff review into specification or QA | tested posture depends on executable locale rules, not generic i18n advice |
| `compliance` | eval strategy seeded | first routed benchmark result on one compliance-heavy release/spec scenario plus one handoff review into delivery or specification | it needs proof that obligations become engineering constraints and evidence checkpoints |

## Immediate Execution Rule

Do not promote any of the remaining `10` newly reviewed standard skills to `tested` before both of these exist for the same scenario:

1. one checked-in benchmark result
2. one checked-in downstream handoff or integration review

For the two remaining critical reviews, do not bypass the runner-backed benchmark requirement just because manual review evidence already exists.

## Completed In This Follow-Up

- `security-audit` moved to `tested` after converting the existing isolated raw lane into `isolated-benchmark-review.md` and adding `release-management-handoff-review.md`.
- `estimation` moved to `tested` after the first clean isolated benchmark review landed and the downstream `sprint-planning` handoff review was reused as the integration artifact.
- `acceptance-criteria` moved to `tested` after the first clean isolated benchmark review landed and the downstream `testing-strategy` handoff review was reused as the integration artifact.
- `observability` moved to `tested` after completed and failed execution traces were converted into a checked-in benchmark review and the runtime contract review was reused as the integration artifact.
