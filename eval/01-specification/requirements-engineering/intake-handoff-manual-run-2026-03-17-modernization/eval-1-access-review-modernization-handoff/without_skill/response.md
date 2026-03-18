# Release 1 Requirements for Access Review Modernization

## Goal

Modernize the access-review experience for compliance admins in the existing compliance SaaS product while improving usability, auditability, and scalability for large reviewer lists.

## Functional Requirements

1. The system shall let admins create quarterly access-review campaigns from reusable templates.
2. The system shall send reviewer reminders for outstanding reviews.
3. The system shall support delegated approvals when a manager is unavailable.
4. The system shall generate downloadable evidence packages for auditors.
5. The system shall support tenant-specific reviewer hierarchies and exception rules for enterprise tenants.
6. The system shall enforce stronger segregation-of-duties checks during access reviews.
7. The system shall maintain tamper-evident audit trails for campaign activity.
8. The system shall allow historical campaigns to remain searchable and exportable.
9. The system shall support data correction and reviewer reassignment workflows.

## Release 1 Scope Notes

- Release 1 must work with the existing product and cannot require a same-day full cutover.
- The legacy module may continue to be used during audit season.
- Historical campaigns older than two years may remain read-only if evidence packages can still be searched and exported.

## Non-Functional Requirements

- Evidence packages must be retained for seven years.
- The new experience should feel faster than the legacy module for large reviewer lists.
- Campaign state should synchronize with the legacy module on the same day.
- Audit records must only be accessible to authorized users.

## Risks

- Tenant-specific hierarchy rules are not fully documented.
- Manual correction and reassignment workflows are not fully understood.

## Open Questions

- Which enterprise tenants require custom reviewer hierarchies in release 1?
- Is near-real-time synchronization required, or is end-of-day consistency acceptable?
- Can some data correction workflows stay manual in release 1?
