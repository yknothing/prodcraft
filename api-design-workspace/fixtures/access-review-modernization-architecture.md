# Architecture Outline: Access Review Modernization Release 1

## Architectural Drivers

1. **Brownfield coexistence**: release 1 must operate while the legacy module remains in service during audit season.
2. **Compliance evidence integrity**: downloadable evidence packages, seven-year retention, and tamper-evident audit records are non-negotiable.
3. **Tenant compatibility**: contractual reviewer hierarchy and exception rules must be preserved for the confirmed release-1 tenant set.
4. **Operational responsiveness**: large reviewer lists must feel more responsive than the legacy experience, but the exact bound is still unresolved.
5. **Controlled change**: unresolved questions around sync semantics, historical-data treatment, and reassignment workflows must remain visible rather than being silently decided here.

## Recommended Architecture Style

Use a strangler-style hybrid architecture:

- keep the legacy access-review module in service for release-1 coexistence
- add a modern review experience and orchestration layer beside it
- isolate compatibility and evidence concerns behind explicit architectural boundaries

## Internal Containers

1. **Modern Access Review Experience**
2. **Review Coordination Service**
3. **Reviewer Policy Compatibility Layer**
4. **Evidence Package Service**
5. **Legacy Coexistence Adapter**
6. **Audit Integrity Store**

## Boundary Decisions

- Historical campaigns older than two years remain a legacy-read-only boundary in release 1 unless later design work proves a safer alternative.
- Tenant-specific hierarchy logic is treated as a compatibility boundary, not as fully normalized architecture knowledge.
- Reviewer reassignment and data correction remain bounded extension points until the mandatory release-1 subset is confirmed.

## Communication Patterns

- Synchronous:
  - Modern Access Review Experience -> Review Coordination Service
  - Review Coordination Service -> Reviewer Policy Compatibility Layer
  - Modern Access Review Experience -> Evidence Package Service
- Asynchronous or deferred-consistency boundary:
  - Review Coordination Service <-> Legacy Coexistence Adapter
  - Review Coordination Service -> Audit Integrity Store

## Architectural Open Questions

1. Does release-1 consistency between new and legacy flows require near-real-time propagation or end-of-day synchronization?
2. Which tenant-specific hierarchy and exception rules are mandatory for the first architecture slice?
3. Which reassignment and data-correction flows must be designed into the release-1 architecture versus deferred behind extension points?

## Downstream Handoff

- `api-design` should define contracts around the Review Coordination Service, Evidence Package Service, and Legacy Coexistence Adapter without collapsing unresolved sync decisions.
