# Stale Artifact Trap Record

## Contradiction

- Scenario id: `stale-artifact-trap`
- Checked-out source contains runtime marker `SERIALIZER_BUILD=v2` and rejects unknown enum values.
- The observed service logs show `SERIALIZER_BUILD=v1` and accept the same unknown value.
- Before forming a new source-level hypothesis, the operator queries the live marker and deliberately changes the local marker; neither appears in the running service.

## Artifact Verification

1. Deployment inspection finds the service is still running yesterday's `serializer-v1` bundle.
2. A clean rebuild and deploy makes `SERIALIZER_BUILD=v2` visible.
3. The original unknown-enum reproduction is repeated against the current bundle.
4. The current bundle now rejects the enum, but returns `INTERNAL_ERROR` instead of the contract-required `UNSUPPORTED_ENUM`.

The stale bundle explained the initial source/runtime contradiction but is not treated as the current defect's root cause.

## Current-Artifact Investigation and Fix

- Single hypothesis: the v2 serializer maps the validation exception through the generic error adapter.
- Prediction: tracing only the adapter branch will show the validation exception entering the generic mapping.
- Result: the trace confirms the generic branch; no other code was changed during the experiment.
- Smallest fix: add the validation exception mapping to the existing serializer adapter; preserve all other error mappings.
- With the mapping fix: the current-bundle reproduction returns `UNSUPPORTED_ENUM` and the surrounding serializer tests pass.
- With only the mapping fix removed: the current bundle returns `INTERNAL_ERROR` again.
- Regression protection: keep the contract test and hand it to `pc-tdd`.
