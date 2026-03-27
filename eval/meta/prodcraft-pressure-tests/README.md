# Prodcraft Pressure Tests

Use this package to measure whether Prodcraft hides lifecycle complexity in practice and to collect subtraction candidates for later cleanup.

## Goals

- verify that `intake` routes cold-start requests to the right first phase and workflow
- measure how many clarification rounds are needed before the route stabilizes
- record which cross-cutting skills actually fire
- detect artifacts that are produced but never consumed
- identify friction that should lead to deletion, downgrade, or simplification instead of another guardrail

## How To Run

1. Choose `3-5` scenarios from `scenario-matrix.md`
2. Start each run from a clean request with no hidden phase context
3. Preserve:
   - the approved `intake-brief`
   - any `course-correction-note`
   - the actual cross-cutting skills triggered
   - the artifacts handed to the next phase
4. For live runs, start from `templates/live-run-record.md` and save the completed result under `runs/`
5. Summarize each run with this record:

| Field | What to capture |
|------|------------------|
| `scenario_id` | Scenario from the matrix |
| `first_route_correct` | `yes` / `no` |
| `clarification_rounds` | Number of routing questions before the path stabilized |
| `workflow_primary` | Selected primary workflow when the route keeps it explicit |
| `workflow_overlays` | Active overlays only; omit when none are active |
| `cross_cutting_triggered` | Skills actually invoked |
| `unused_artifacts` | Artifacts produced but not consumed |
| `course_corrections` | Approved jump pairs taken, if any |
| `low_value_friction` | Extra steps that did not change the outcome |
| `deletion_candidate` | Optional skill, artifact, or rule to simplify |

## Review Standard

- One surprising run is a note
- Repeated friction across scenarios is a candidate for subtraction
- A new guardrail needs evidence of repeated failure, not just a plausible story

## Seed Evidence

- `2026-03-26-tabletop-pilot.md` is the initial tabletop replay used to identify the first live pressure-test targets. Treat it as provisional evidence until a real runtime run confirms or falsifies the same friction.
- `prompts/` contains canned requests for the first live cycle, including a mixed-language scenario that can unlock the later language-boundary contract work.
- `2026-03-26-live-cycle-1-summary.md` summarizes the first three live runs and identifies the first repeated subtraction candidate.
- `2026-03-27-live-cycle-2-summary.md` records the first post-change verification pass after that subtraction candidate was implemented.
- `2026-03-27-live-cycle-3-summary.md` verifies that overlay-bearing routes still need explicit workflow metadata after the direct-route cleanup.
- `2026-03-27-live-cycle-4-summary.md` verifies that the new execution-discipline skills now appear in the live routing path and that the machine-installed `prodcraft` gateway matches the repo-local gateway contract.
