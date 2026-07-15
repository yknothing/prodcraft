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
