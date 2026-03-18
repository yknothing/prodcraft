# Access Review Modernization Architecture Draft

## Proposed Architecture

Build a new access-review platform alongside the legacy module using a separate web application, an API layer, and a set of supporting services for workflow, audit, notifications, and synchronization.

## Major Components

1. **Modern Access Review UI**
   - New admin interface for campaign setup, review execution, and evidence download.
2. **Access Review API**
   - Central API for campaign creation, reviewer actions, reminders, and audit access.
3. **Workflow Service**
   - Manages campaign states, delegated approvals, and reviewer reassignment.
4. **Policy Service**
   - Evaluates tenant-specific reviewer hierarchies and exception rules.
5. **Audit Service**
   - Stores tamper-evident records and evidence package metadata.
6. **Notification Service**
   - Sends reminder emails and escalation notices.
7. **Sync Worker**
   - Synchronizes campaign state between the new platform and the legacy module.

## Data and Integration

- Use the new platform as the primary experience for release 1.
- Synchronize campaign data with the legacy module daily until full cutover.
- Copy historical campaigns into the new reporting store so auditors can search them from one place.
- Store audit records for seven years.

## Key Decisions

- Use a service-oriented architecture so workflow, policy, and audit concerns can scale independently.
- Keep the legacy module running during audit season, then complete migration after stability is proven.
- Move tenant-specific reviewer rules into the Policy Service.

## Risks

- Tenant-specific rule migration may take longer than expected.
- Reviewer reassignment workflows need deeper discovery.

## Next Step

Define APIs for the Access Review API, Workflow Service, and Policy Service, then break implementation into migration phases.
