# Input and Output Contract Notes

## Inputs

- **source-code** -- The implementation under audit, including configuration and integration points visible in the change.
- **architecture-doc** -- Trust boundaries, component interactions, and intended control points.
- **threat-model** -- Known attacker capabilities, abuse cases, and assumptions to verify when one exists.
- **intake-brief** -- Must include `quality_target_context` with `runtime_context`, `exposure_profile`, `production_target`, `non_targets`, and `evidence_refs`.

## Outputs

- **security-report** -- Findings, risk classification, evidence, remediation guidance, and explicit release recommendation.
