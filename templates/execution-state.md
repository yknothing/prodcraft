# Execution State

## Required Artifact

- artifact: `execution-state`
- schema_version: `execution-state.v1`
- work_id:
- state_revision:
- updated_at:
- route_binding:
- previous_execution:
- lifecycle_state:
- workflow_cursor:

## Histories And Bindings

- lifecycle_transitions:
- phase_events:
- artifact_bindings:
- block_contexts:
  - transition_sequence:
    resume_transition_sequence:
    reason:
    evidence_refs:

## Completion

- completion_attempts:
  - verification_commitment:
    - verification_record_ref:
      verification_record_sha256:
      evidence_bindings:
      work_snapshot:
- current_completion_attempt_id:

## Authority Check

```bash
python scripts/validate_prodcraft.py \
  --authorize-execution-state .prodcraft/artifacts/<work_id>/execution-state.json \
  --approved-route-digest sha256:<operator-pinned-route-digest> \
  --approved-completion-digest sha256:<operator-pinned-completion-digest>
```

`--artifact-instance` is structural inspection only. It does not emit gate or
terminal authority.
