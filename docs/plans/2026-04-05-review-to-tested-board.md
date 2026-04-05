# Review To Tested Board

> Date: 2026-04-05

> Rule: do not promote a `review` skill to `tested` unless the repository contains the actual evidence required by its QA contract.

## Tested Gate

For the current manifest, every `review` skill is `routed`.

- `standard` routed skills require:
  - `qa.benchmark_results_path`
  - `qa.integration_test_path`
- `critical` routed skills require:
  - `qa.benchmark_results_path`
  - `qa.integration_test_path`
  - current `qa.findings_path`

## Current Review Pool

| Phase | Skill | QA tier | What exists now | Smallest honest next step before `tested` |
|---|---|---|---|---|
| `00-discovery` | `market-analysis` | `standard` | structure validation + review strategy | add one routed benchmark result and one downstream integration or handoff review |
| `00-discovery` | `feasibility-study` | `standard` | structure validation + review strategy | add one routed benchmark result and one downstream integration or handoff review |
| `01-specification` | `spec-writing` | `standard` | structure validation + review strategy | add one routed benchmark result and one downstream integration or handoff review |
| `01-specification` | `domain-modeling` | `standard` | structure validation + review strategy | add one routed benchmark result and one downstream integration or handoff review |
| `02-architecture` | `system-design` | `critical` | findings, benchmark plan, routed integration review, benchmark asset | land one clean promote-grade benchmark result on the existing brownfield scenario |
| `02-architecture` | `data-modeling` | `standard` | structure validation + review strategy | add one routed benchmark result and one downstream integration or handoff review |
| `02-architecture` | `security-design` | `standard` | structure validation + review strategy | add one routed benchmark result and one downstream integration or handoff review |
| `07-operations` | `monitoring-observability` | `critical` | findings, benchmark plan, routed observability review | add first isolated benchmark result exercised against a concrete post-deploy or incident drill |
| `cross-cutting` | `observability` | `critical` | findings, benchmark plan, runtime contract review | add first isolated benchmark result and add a routed integration artifact path in manifest |
| `cross-cutting` | `bug-history-retrieval` | `standard` | structure validation + review strategy | add one routed benchmark result and one downstream integration or handoff review |
| `cross-cutting` | `accessibility` | `standard` | structure validation + review strategy | add one routed benchmark result and one downstream integration or handoff review |
| `cross-cutting` | `internationalization` | `standard` | structure validation + review strategy | add one routed benchmark result and one downstream integration or handoff review |
| `cross-cutting` | `compliance` | `standard` | structure validation + review strategy | add one routed benchmark result and one downstream integration or handoff review |

## Immediate Order

1. `system-design`
2. `monitoring-observability`
3. `observability`
4. the new `standard` review batch, grouped by lifecycle adjacency rather than alphabetically

## Notes

- `system-design` is the closest honest promotion candidate because everything except a clean benchmark result already exists.
- `security-audit` moved to `tested` once the existing isolated benchmark lane was converted into a checked-in benchmark review and the first routed `release-management` handoff review was added.
- `estimation` moved to `tested` once the first clean isolated benchmark review landed and the existing `sprint-planning` handoff review was reused as downstream evidence.
- `acceptance-criteria` moved to `tested` once the first clean isolated benchmark review landed and the existing `testing-strategy` handoff review was reused as downstream evidence.
- `monitoring-observability` and `observability` are the remaining critical reviews because they already have review-depth evidence instead of only evaluation strategies.
- The remaining 10 newly reviewed `standard` skills should not be mass-promoted to `tested` from paperwork alone. They now have review posture; they still need real benchmark and handoff evidence.
