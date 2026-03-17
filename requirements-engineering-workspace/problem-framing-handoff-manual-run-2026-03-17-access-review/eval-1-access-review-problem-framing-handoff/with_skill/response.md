# Requirements Document: Access Review Modernization Release 1

## Scope Boundary

- **Lifecycle layer**: requirements only; no migration sequencing, cutover planning, service decomposition, or replacement architecture decisions.
- **Chosen direction**: release 1 follows the approved **campaign-and-evidence-first coexistence** direction.
- **Brownfield boundary**: the modernized workflow must coexist with the legacy access-review module during audit season.

## Functional Requirements

### P0

- **REQ-001**: The system shall allow compliance admins to create quarterly access-review campaigns from reusable templates.
- **REQ-002**: The system shall send reviewer reminders for outstanding review tasks.
- **REQ-003**: The system shall support delegated approvals for campaign review actions.
- **REQ-004**: The system shall generate downloadable evidence packages for auditors for completed and in-progress campaigns.
- **REQ-005**: The system shall allow release 1 campaign workflows to operate while the legacy module remains in service during audit season.
- **REQ-006**: The system shall preserve required tenant-specific reviewer hierarchies and exception rules for the release-1 tenant set once that set is confirmed.
  - **Open question**: which tenant-specific rules are contractually mandatory in release 1?

### P1

- **REQ-007**: The system shall keep historical campaigns older than two years available in a read-only legacy experience if auditors can still search and export the required evidence package.
  - **Open question**: can all required historical evidence remain legacy-backed for release 1?
- **REQ-008**: The system shall support reviewer reassignment and data-correction handling only for the subset of flows confirmed to be required for release 1.
  - **Open question**: which reassignment and correction flows are mandatory immediately?
- **REQ-009**: The system shall enforce stronger segregation-of-duties rules in the access-review workflow.
- **REQ-010**: The system shall produce tamper-evident audit records for access-review actions.

### P3 / Explicitly Out of Scope for Release 1

- full legacy replacement
- migration or cutover sequencing decisions
- expanding release 1 to every undocumented tenant-specific exception path before the release-1 tenant set is confirmed
- forcing a synchronization implementation choice before the required consistency level is approved

## Non-Functional Requirements

- **NFR-001**: The system shall retain evidence packages for seven years.
- **NFR-002**: The system shall ensure only authorized users can access or act on access-review records and evidence packages.
- **NFR-003**: The system shall improve perceived responsiveness for large reviewer lists relative to the current legacy experience.
  - **Open question**: what acceptance threshold should define "faster" for release 1?
- **NFR-004**: The system shall support legacy/new module state consistency at the level approved for release-1 coexistence.
  - **Open question**: does the required consistency level mean near-real-time propagation or end-of-day synchronization?

## Risks to Preserve Downstream

- The chosen direction is intentionally narrower than near-parity modernization; downstream work must not silently re-expand it.
- Tenant-specific reviewer rules remain only partially inventoried and may hide contractual scope.
- Historical-data treatment and synchronization semantics remain unresolved and must not be treated as closed architectural decisions.

## Downstream Handoff Notes

- `system-design` should preserve the campaign-and-evidence-first coexistence direction as a scope boundary rather than translating it into migration sequencing.
- `acceptance-criteria` should turn the P0/P1 obligations into measurable checks without inventing unsupported thresholds.
