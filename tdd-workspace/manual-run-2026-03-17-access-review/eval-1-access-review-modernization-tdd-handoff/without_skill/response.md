# Reassignment Flow Implementation Plan

1. Add controller logic for `POST /v1/campaigns/{campaignId}/reassignments`.
2. Add service logic for supported reassignment types.
3. Add authorization checks for reassignment.
4. Add unsupported-flow handling.
5. Add tests for the endpoint.
6. Refine the code after tests pass.

## Notes

- Use the structured unsupported response for unsupported variants.
- Fill in tenant-specific details as needed during implementation.
