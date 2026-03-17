# Architecture Outline: Access Review Modernization Release 1

## Architectural Drivers

1. **Brownfield coexistence**: release 1 must operate while the legacy module remains in service during audit season.
2. **Compliance evidence integrity**: downloadable evidence packages, seven-year retention, and tamper-evident audit records are non-negotiable.
3. **Tenant compatibility**: contractual reviewer hierarchy and exception rules must be preserved for the confirmed release-1 tenant set.
4. **Operational responsiveness**: large reviewer lists must feel more responsive than the legacy experience, but the exact bound is still unresolved.
5. **Controlled change**: unresolved questions around sync semantics, historical-data treatment, and reassignment workflows must remain visible rather than being silently decided here.

## Recommended Architecture Style

Use a **strangler-style hybrid architecture**:

- keep the legacy access-review module in service for release-1 coexistence
- add a modern review experience and orchestration layer beside it
- isolate compatibility and evidence concerns behind explicit architectural boundaries

This is a better fit than a big bang rewrite because coexistence, contractual exceptions, and unresolved migration questions are all first-order constraints.

## System Context

### Internal Containers

1. **Modern Access Review Experience**
   - Admin-facing interface for campaign setup, reviewer actions, reminders, and evidence access.
2. **Review Coordination Service**
   - Owns campaign lifecycle, reminder scheduling, delegated review flow, and release-1 orchestration decisions.
3. **Reviewer Policy Compatibility Layer**
   - Applies confirmed tenant-specific reviewer hierarchies and exception rules without forcing the architecture to assume every undocumented variation is already understood.
4. **Evidence Package Service**
   - Produces auditor-facing evidence packages and preserves retention and integrity constraints.
5. **Legacy Coexistence Adapter**
   - Encapsulates state exchange and coexistence behavior between the new release-1 flow and the legacy module.
6. **Audit Integrity Store**
   - Holds tamper-evident review activity records and evidence metadata for the required retention window.

### External / Existing Systems

- **Legacy Access Review Module**
  - Remains active during release 1 and continues to serve historical/read-only needs where required.
- **Notification Infrastructure**
  - Sends reminders and review notifications.
- **Enterprise Identity / Reviewer Sources**
  - Provides reviewer and hierarchy context used by the compatibility layer.

## Boundary Decisions

- Historical campaigns older than two years remain a **legacy-read-only boundary** in release 1 unless later design work proves a safer alternative.
- Tenant-specific hierarchy logic is treated as a **compatibility boundary**, not as fully normalized architecture knowledge.
- Reviewer reassignment and data correction remain **bounded extension points** until the mandatory release-1 subset is confirmed.

## Communication Patterns

- **Synchronous**:
  - Modern Access Review Experience -> Review Coordination Service
  - Review Coordination Service -> Reviewer Policy Compatibility Layer
  - Modern Access Review Experience -> Evidence Package Service
- **Asynchronous or deferred-consistency boundary**:
  - Review Coordination Service <-> Legacy Coexistence Adapter
  - Review Coordination Service -> Notification Infrastructure
  - Review Coordination Service -> Audit Integrity Store

The exact consistency target between new and legacy flows is not fixed yet. Architecture must preserve that as a follow-up decision rather than locking in near-real-time or batch semantics prematurely.

## Deployment Topology

- Deploy the new release-1 containers alongside the current product boundary rather than as a cutover replacement.
- Keep the legacy module reachable for coexistence and rollback protection during audit season.
- Avoid committing here to detailed rollout percentages, migration windows, or service-by-service extraction order; those belong in later planning and delivery work unless they become architectural constraints.

## ADR Candidates

### ADR-001: Use a strangler-style coexistence boundary for release 1

- **Context**: release 1 must coexist with the legacy module, and a full cutover is explicitly out of scope.
- **Decision**: isolate coexistence through a dedicated architectural adapter/facade instead of assuming replacement-only flow.
- **Consequence**: architecture stays reversible, but coexistence adds temporary complexity.

### ADR-002: Keep older historical campaigns in a legacy-read-only boundary for release 1

- **Context**: requirements allow campaigns older than two years to remain in the legacy experience if evidence export remains available.
- **Decision**: treat legacy-read-only history as an explicit release-1 boundary.
- **Consequence**: reduces migration risk now, but creates follow-up integration work later.

### ADR-003: Preserve unresolved tenant-specific reviewer logic as a compatibility concern

- **Context**: the exact contractual tenant list is incomplete.
- **Decision**: architecture isolates rule variability behind a compatibility layer and keeps the unresolved tenant scope visible.
- **Consequence**: downstream design can proceed without pretending the entire contract matrix is already known.

## Architectural Open Questions

1. Does release-1 consistency between new and legacy flows require near-real-time propagation or end-of-day synchronization?
2. Which tenant-specific hierarchy and exception rules are mandatory for the first architecture slice?
3. Which reassignment and data-correction flows must be designed into the release-1 architecture versus deferred behind extension points?

## Downstream Handoff

- `api-design` should define contracts around the Review Coordination Service, Evidence Package Service, and Legacy Coexistence Adapter without collapsing unresolved sync decisions.
- `data-modeling` should focus on audit/evidence integrity and compatibility boundaries rather than assuming full legacy data migration.
- `task-breakdown` should sequence work around reversible seams, not around a replacement-only plan.
