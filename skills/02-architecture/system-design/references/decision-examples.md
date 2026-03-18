# System Design Decision Examples

Use this reference when the team needs calibration for architecture trade-off writeups or ADR shape. Keep the main skill focused on the actual decision process.

## Choosing Between Monolith and Microservices

- Team of 4 developers, single product, 1-2 releases per week -> modular monolith. Low coordination overhead, simple deployment, easier debugging.
- Team of 30 across 6 squads, each owning a business domain, independent release schedules -> microservices. Team autonomy can justify the extra operational complexity.

## ADR Example

```text
# ADR-003: Use event sourcing for order processing

Status: Accepted

Context: Orders go through complex state transitions. Audit requirements demand
full history. Multiple services react to order state changes.

Decision: Implement event sourcing for the Order aggregate. Store events in
an append-only event store. Project read models for query needs.

Consequences:
+ Full audit trail without additional logging
+ Natural integration with event-driven architecture
- Increased complexity in read model projection
- Team needs training on event sourcing patterns
- Eventually consistent read models require UX consideration
```
