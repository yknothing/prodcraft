# Live Pressure-Test Record

## Metadata

- `run_id`: `2026-03-27-PT-03-brownfield-overlay-live`
- `scenario_id`: `PT-03-brownfield-migration`
- `evidence_class`: `live`
- `operator`: `codex`
- `date`: `2026-03-27`

## Request

- `request_text`: |
    We need to migrate a legacy subsystem without shutting the existing path off all at once.

    The current system has coexistence risk, shared contracts, and a staged rollout constraint.
    Please route this so we do not jump straight into implementation before the seams are understood.
- `hidden_context_used`: `repo-local Prodcraft contracts only`

## Routing Outcome

- `first_route_correct`: `yes`
- `clarification_rounds`: `0`
- `work_type`: `Migration`
- `entry_phase`: `00-discovery`
- `workflow_primary`: `agile-sprint`
- `workflow_overlays`: `[brownfield]`
- `next_skill`: `problem-framing`

## Preserved Intake Brief

```markdown
## Intake Brief

**Work type**: Migration
**Entry phase**: 00-discovery
**Intake mode**: full
**workflow_primary**: agile-sprint
**workflow_overlays**: [brownfield]
**Key skills needed**: problem-framing, system-design, task-breakdown, tdd, ci-cd
**Scope assessment**: large
**routing_rationale**: The request is a staged modernization with coexistence and shared-contract risk, so the system must start with brownfield discovery and architecture rather than implementation. The brownfield overlay is what keeps rollback boundaries, coexistence seams, and characterization safety visible across the route.
**Key risks**: Hidden legacy dependencies may invalidate early architecture assumptions; migration pressure may collapse coexistence planning into a rewrite if the route is not kept explicit.

### Proposed Path
1. problem-framing -- define the modernization wedge, preserved constraints, and migration success criteria
2. system-design -- identify seams, facades, rollback boundaries, and coexistence architecture
3. task-breakdown -- sequence reversible increments instead of a replacement-only build
4. tdd -- establish characterization and seam-protection tests before code changes
```

## Evidence

- `cross_cutting_triggered`: `documentation`
- `artifacts_produced`: `intake-brief`
- `unused_artifacts`: `none observed at intake stage`
- `course_corrections`: `none`
- `low_value_friction`:
  - `none observed at intake stage`
- `subtraction_candidate`: `none`

## Judgment

- `essential_or_accidental`: `essential`
- `follow_up`: `verify in a later downstream run that brownfield-specific artifacts are still consumed after architecture and planning`
- `notes`: |
    This run confirms the opposite of the earlier degenerate-route finding:
    explicit workflow metadata is necessary here. The `brownfield` overlay is
    what keeps coexistence and rollback discipline alive, and the explicit
    primary workflow still matters because brownfield does not determine whether
    governance stays iterative or phase-gated.
