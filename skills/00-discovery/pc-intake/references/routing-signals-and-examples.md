# Intake Routing Signals and Examples

Use this reference for a route decision, not as a full artifact template. The examples are partial routing projections; a saved brief must still contain every `intake-brief.v1` required field.

## Methodology Selection Signals

- `spec-driven`: explicit specifications, contractual delivery, or regulated work
- `agile-sprint`: iterative product work or no stronger methodology requirement
- `iterative-waterfall`: explicit phase gates and staged approval
- `hotfix` overlay: active production failure or urgent containment
- `greenfield` overlay: a new system without an existing implementation
- `brownfield` overlay: coexistence, compatibility, or migration constraints

An overlay supplements a primary workflow; it is not a replacement primary.

## Worked Decisions

| Request and available evidence | Route decision | Next useful action |
|---|---|---|
| "Continue the approved settings change"; scope and authority are unchanged | Reuse the approved route; `resume` if an updated brief is needed | Consume the current task and evidence at the next unmet step; ask no repeat approval |
| "Add dark mode"; requirements and accepted architecture already exist | `New Feature`, `01-specification`, `agile-sprint`; record which upstream obligations are already satisfied | Route to `pc-task-breakdown` only if the task slice is missing, otherwise continue the implementation discipline |
| "Checkout is returning 500"; cause is unknown | `Hotfix`, `04-implementation`, `agile-sprint` plus `hotfix` | Use `pc-incident-response` for active containment first; reuse current containment evidence before `pc-systematic-debugging` |
| "Fix this README typo"; reversible wording only | `Documentation`, `cross-cutting`, `micro` if all eligibility fields hold | Use `pc-documentation`; under the Claude Edit/Write adapter use approved `fast-track` instead |
| "Build a CLI migration tool"; desired users and problem are unclear | `New Product`, `00-discovery`, `agile-sprint` plus `greenfield` | Use `pc-problem-framing` to settle the problem before choosing a full design chain |

Existing files alone do not prove acceptance. Cite their current content and the actual approval. A new requested outcome in an old repository is new work, not automatically a resume.
