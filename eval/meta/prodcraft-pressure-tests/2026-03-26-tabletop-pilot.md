# 2026-03-26 Tabletop Pressure-Test Pilot

> Status: provisional historical evidence. Treat this as the pre-live hypothesis pass; use the live cycle summaries for current conclusions.

> Scope note: this is a **tabletop routing replay**, not a live runtime execution trace. It uses the current repository contracts (`intake`, `gateway`, workflows, matrix, schemas) to identify the first subtraction candidates worth checking in real runs.

## Scenarios Run

| scenario_id | first_route_correct | clarification_rounds | workflow_primary | cross_cutting_triggered | unused_artifacts | course_corrections | low_value_friction | deletion_candidate |
|------------|---------------------|----------------------|------------------|-------------------------|------------------|--------------------|--------------------|-------------------|
| `PT-02-fast-track-bugfix` | yes | 2 | `agile-sprint` | none | none | none | `workflow_primary=agile-sprint` and `workflow_overlays=[]` are still recorded even though the route is nearly deterministic for a small clear bug fix | candidate: hide empty overlay noise from the user-facing brief before changing schema |
| `PT-03-brownfield-migration` | yes | 3 | `agile-sprint` + `brownfield` overlay | `documentation`, `observability` | none observed | none | choosing whether migration starts in discovery or architecture still depends on a human judgment call about unknowns | none yet; overlay looks justified |
| `PT-05-docs-only-change` | yes | 0 | `agile-sprint` | `documentation` | `workflow_primary` feels ceremonial because the route bypasses primary workflow composition | none | full `intake-brief` shape still carries workflow metadata that does not materially change the path | candidate: evaluate making `workflow_primary` implicit or optional when `entry_phase=cross-cutting` and only one cross-cutting skill is routed |

## Scenario Notes

### PT-02-fast-track-bugfix

- Request shape: small parser crash fix in one file, root cause already known.
- Expected route: `intake_mode=fast-track` -> `04-implementation` -> `tdd` -> `feature-development` -> `code-review`.
- Observation: the fast-track path is clear and the new cross-cutting obligation model correctly allows documentation to be considered without forcing output.
- Friction: the brief still asks the operator to carry empty workflow metadata that does not change the downstream path.

### PT-03-brownfield-migration

- Request shape: staged migration of a legacy subsystem with coexistence risk.
- Expected route: discovery/architecture/planning with `brownfield` overlay.
- Observation: this is the strongest case for keeping overlay semantics explicit. `brownfield` changes the actual design and planning posture.
- Friction: the system still relies on judgment to decide whether unknowns are large enough to start in discovery instead of architecture, but this looks like essential complexity rather than accidental complexity.

### PT-05-docs-only-change

- Request shape: update technical documentation with no product or runtime behavior change.
- Expected route: direct handoff to `cross-cutting/documentation`.
- Observation: the route hides most of the lifecycle correctly.
- Friction: `workflow_primary` is still present even though no primary workflow composition is meaningfully used after routing.

## Initial Findings

1. `workflow_primary` and empty `workflow_overlays` are the first credible subtraction candidates, but only for narrow routes such as docs-only and obvious fast-track fixes.
2. The `brownfield` overlay still appears essential. No evidence yet supports collapsing it.
3. The new `course-correction-note` contract did not add obvious friction in these scenarios; it should stay until live runs show otherwise.
4. The next live pressure-test cycle should prioritize `PT-04-hotfix-incident` because it is most likely to reveal whether the current `04-implementation` vs `07-operations` entry split is confusing under pressure.

## Follow-Up

- Convert the next live `PT-02`, `PT-04`, and `PT-05` runs into the same table format.
- If `workflow_primary` remains low-signal across live docs-only and fast-track scenarios, open a follow-on proposal to narrow the `intake-brief` contract for those routes instead of broadening more rules.
