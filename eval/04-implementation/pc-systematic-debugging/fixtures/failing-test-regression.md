# Failing Test Regression

## Current Failure

- `test_reassignment_rejects_unsupported_type` is now failing
- expected error code: `UNSUPPORTED_REASSIGNMENT_TYPE`
- actual result: handler returns `200`

## Recent Change

- a cleanup refactor merged yesterday in the reassignment handler

## Constraint

- do not patch first; determine whether the failure is behavioral regression, test drift, or contract mismatch
