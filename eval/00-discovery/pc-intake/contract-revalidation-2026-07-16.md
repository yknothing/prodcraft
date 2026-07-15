# pc-intake Contract Revalidation — 2026-07-16

## Claim

The current intake contract, including mechanically enforced micro eligibility,
is structurally valid and remains compatible with its routing, artifact, curated,
and identity contracts.

## Contract Binding

`contract-sha256:fe01dc30dd81c7e9c100d8f34a0f6b01493a34b66dbc931c634af3087b7800a5`

## Fresh Verification

```bash
python3 -m unittest \
  tests.test_intake_qa_posture \
  tests.test_intake_schema_semantics \
  tests.test_artifact_schema_registry \
  tests.test_execution_state_completion \
  tests.test_curated_distribution_surface \
  tests.test_skill_identity_prefix \
  tests.test_p0_execution_gap_skills
```

Result: `Ran 59 tests in 5.119s — OK`.

The micro-specific negative cases reject missing eligibility, any false
eligibility assertion, non-small scope, draft status, an alternate approver,
explicit primary workflow metadata, and micro fields on non-micro briefs.

## Boundary

This run verifies repository contracts and deterministic behavior. It does not
replace the historical model benchmark or claim fresh model-behavior evidence.

