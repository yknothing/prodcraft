# Release 1 Spec Summary

## Included in Release 1

- create and list access-review campaigns
- assign and reassign reviewers for the confirmed release-1 subset
- capture review decisions with audit history
- generate downloadable evidence packages

## Explicit Non-Goals

- full migration of historical campaigns older than two years
- same-day or near-real-time sync guarantees before consistency semantics are resolved
- full support for every data-correction workflow

## Data-Relevant Constraints

- evidence and audit records must remain tamper-evident and retained for seven years
- legacy-read history remains available for older campaigns
- unsupported reassignment variants must fail explicitly rather than silently corrupt state
