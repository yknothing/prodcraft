# Estimate Set

- contract test stabilization: `1 day`, confidence `high`
- bounded modern reassignment path: `2 days`, confidence `medium`
- coexistence and rollback checks: `1.5 days`, confidence `medium`
- sync-semantics decision gate: `0.5 day`, confidence `low`
- release follow-up preparation: `1 day`, confidence `medium`

Assumptions:

- no new reassignment types are added in release 1
- legacy coexistence boundary stays intact
- unresolved sync semantics are not silently decided inside implementation
