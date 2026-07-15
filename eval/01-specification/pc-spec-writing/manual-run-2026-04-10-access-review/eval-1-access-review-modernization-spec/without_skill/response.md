# Access Review Modernization Spec Draft

## Goal

Replace the legacy access-review module with a new service and UI before the
next audit season.

## Included Work

- campaign creation and listing
- reviewer assignment and reassignment
- evidence export and audit logs
- legacy sync worker
- historical campaign import

## Implementation Shape

- build a Review Coordination Service
- build a Policy Service for tenant hierarchy rules
- build a Sync Worker so legacy and new stay aligned the same day
- build an Evidence Service for downloads

## Rollout

1. import historical campaigns
2. enable sync between new and legacy
3. cut all release-1 tenants over to the new UI

## Assumptions

- same-day sync between legacy and new is required
- historical campaigns will gradually move into the new platform
- reassignment flows can be implemented as a normal create/update path

## Next Step

Produce architecture and database designs for the new services and begin the
sync worker first because coexistence depends on it.
