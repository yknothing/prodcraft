# Architecture Outline: Access Review Modernization Release 1

## Internal Containers

1. **Modern Access Review Experience**
2. **Review Coordination Service**
3. **Reviewer Policy Compatibility Layer**
4. **Evidence Package Service**
5. **Legacy Coexistence Adapter**
6. **Audit Integrity Store**

## Security-Relevant Constraints

- release 1 must coexist with the legacy module during audit season
- evidence packages and audit history are compliance-sensitive assets
- tenant-specific hierarchy rules are contractual and cannot leak across tenants
- sync semantics between new and legacy flows remain unresolved
- unsupported reassignment and data-correction flows must fail safely
