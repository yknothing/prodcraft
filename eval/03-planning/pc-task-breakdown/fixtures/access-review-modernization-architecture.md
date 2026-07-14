# Architecture Summary

- Release 1 must coexist with the legacy access-review module during audit season.
- Architecture uses a strangler-style hybrid approach with these key containers:
  - Modern Access Review Experience
  - Review Coordination Service
  - Reviewer Policy Compatibility Layer
  - Evidence Package Service
  - Legacy Coexistence Adapter
  - Audit Integrity Store
- Historical campaigns older than two years remain a legacy-read-only boundary in release 1.
- Tenant-specific hierarchy logic remains a compatibility boundary.
- Reviewer reassignment and data correction are bounded extension points.
- Sync semantics between new and legacy flows remain unresolved.

## Downstream Handoff

- `task-breakdown` should sequence work around reversible seams, not around a replacement-only plan.
