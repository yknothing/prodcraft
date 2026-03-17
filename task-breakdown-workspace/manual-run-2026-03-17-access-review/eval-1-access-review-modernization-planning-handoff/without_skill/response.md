# Release 1 Task Breakdown

## Tasks

1. Build the new campaign UI.
2. Build the Review Coordination Service.
3. Build the Reviewer Policy Compatibility Layer.
4. Build the Evidence Package Service.
5. Build the Legacy Coexistence Adapter.
6. Implement all public APIs.
7. Add audit-event storage.
8. Implement reminder scheduling.
9. Implement reassignment support.
10. Migrate historical campaigns.
11. Build sync between new and legacy systems.
12. Test the full system.
13. Deploy release 1.

## Dependencies

- Backend services before UI.
- APIs before frontend integration.
- Sync before deployment.
- Testing after all features are complete.

## Assumptions

- Historical campaigns will be migrated during release 1.
- Sync can be implemented as part of the main build phase.

## Next Step

Start with backend services, then move to frontend and testing.
