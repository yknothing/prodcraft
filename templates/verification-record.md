# Verification Record

Use this template whenever `verification-before-completion` checks whether a completion, fix, phase, release, or handoff claim may be made.

## Required Artifact

- artifact: `verification-record`
- schema_version: `verification-record.v1`
- status:

## Claim

- claim:
- claim_scope:
- verified_at:
- work_state_ref:
  id:
  kind:
  ref:
  captured_at:
  status:
  diff_ref: # Required only when status is dirty.

## Evidence

- evidence_refs:
  - id:
    kind:
    ref:
    captured_at:
    work_state_ref:
    notes:
- checks_run:
  - name:
    result:
    evidence_ref:
    work_state_ref:
    notes:

## Result

- passed:
  -
- failed:
  -
- remaining_unverified:
  -
- claim_may_be_made:
