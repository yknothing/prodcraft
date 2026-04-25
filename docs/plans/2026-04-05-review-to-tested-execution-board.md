# Review-To-Tested Execution Board

> Date: 2026-04-05
> Current manifest refresh: 2026-04-25

> Purpose: keep the remaining `review` pool honest by naming the smallest next evidence artifact for each skill instead of using "needs more QA" as a placeholder blocker.

## Current Review Pool

- total `review` skills: `6`
- closest to `tested`: `system-design`
- runner-blocked critical reviews: `system-design`
- remaining standard reviews: `5`

## Priority Order

1. `system-design`
2. the remaining standard review skills, grouped by lifecycle adjacency

## Review Skill Matrix

| Skill | Current posture | Smallest honest next artifact | Why that artifact is next |
|---|---|---|---|
| `system-design` | benchmark plan, findings, and routed handoff exist; no clean with-skill benchmark result yet | one clean `benchmark_results_path` on the existing brownfield isolated benchmark | this is already the narrowest remaining blocker for promotion |
| `market-analysis` | eval strategy seeded | first routed benchmark result on one opportunity-shaping scenario plus one handoff review into `feasibility-study` or `requirements-engineering` | it needs proof that it improves evidence quality instead of generating generic competitor prose |
| `feasibility-study` | eval strategy seeded | first routed benchmark result on one go/no-go scenario plus one handoff review into `requirements-engineering` or intake decisioning | it needs evidence that it sharpens decision quality rather than rewriting discovery notes |
| `bug-history-retrieval` | eval strategy seeded | first routed benchmark result on a lineage-sensitive bug scenario plus one handoff review into `systematic-debugging` | tested posture depends on grounding the next debugging step in canonical history |
| `internationalization` | eval strategy seeded | first routed benchmark result on a locale-sensitive UI/content scenario plus one handoff review into specification or QA | tested posture depends on executable locale rules, not generic i18n advice |
| `compliance` | eval strategy seeded | first routed benchmark result on one compliance-heavy release/spec scenario plus one handoff review into delivery or specification | it needs proof that obligations become engineering constraints and evidence checkpoints |

## Immediate Execution Rule

Do not promote any of the remaining `5` standard review skills to `tested` before both of these exist for the same scenario:

1. one checked-in benchmark result
2. one checked-in downstream handoff or integration review

For the remaining critical review `system-design`, do not bypass the runner-backed benchmark requirement just because manual review evidence exists elsewhere in the repo.

As of the 2026-04-25 manifest refresh, `spec-writing`, `domain-modeling`, `data-modeling`, and `security-design` are already `tested` and are no longer part of the live execution board.

## Completed In This Follow-Up

- `security-audit` moved to `tested` after converting the existing isolated raw lane into `isolated-benchmark-review.md` and adding `release-management-handoff-review.md`.
- `estimation` moved to `tested` after the first clean isolated benchmark review landed and the downstream `sprint-planning` handoff review was reused as the integration artifact.
- `acceptance-criteria` moved to `tested` after the first clean isolated benchmark review landed and the downstream `testing-strategy` handoff review was reused as the integration artifact.
- `observability` moved to `tested` after completed and failed execution traces were converted into a checked-in benchmark review and the runtime contract review was reused as the integration artifact.
- `accessibility` moved to `tested` after the first clean isolated benchmark review landed and the downstream `acceptance-criteria` handoff review was reused as the integration artifact.
- `monitoring-observability` moved to `tested` after the existing manual branch-pair evidence was formalized into `manual-benchmark-review.md` and the routed `observability-review.md` remained the integration artifact.
