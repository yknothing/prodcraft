# API Contract Summary

- Public release-1 APIs exist for:
  - campaigns
  - review actions
  - reminders
  - supported reassignments
  - evidence packages
  - audit events
- Legacy coexistence remains explicit; migration-only commands are not public release-1 APIs.
- Unsupported reassignment variants should return a structured unsupported response.
- Sync semantics, tenant-specific hierarchy variants, and dedicated historical-campaign search remain open questions.

## Downstream Handoff

- `feature-development` should implement only release-1 public contract surfaces.
- `testing-strategy` should derive contract tests for authorization, unsupported flows, pagination, and error-envelope consistency.
