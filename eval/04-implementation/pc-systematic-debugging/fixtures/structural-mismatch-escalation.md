# Structural Mismatch Escalation Record

## Failure Boundary

- Scenario id: `structural-mismatch-escalation`
- The order workflow requires `PaymentAuthorized` to be durably observable before `OrderConfirmed` is published.
- The current architecture publishes those events from separate services with no shared transaction, durable outbox, or ordering coordinator.
- Under a broker partition, `OrderConfirmed` can become visible first.

## Three Failed Local Fixes

1. Handler retry: retried `PaymentAuthorized` publication in the payment handler. The same ordering failure remained when the order service recovered first.
2. Consumer delay: added a fixed delay before consuming `OrderConfirmed`. The same failure remained under a longer partition and introduced latency.
3. In-memory flag: blocked confirmation while a process-local payment flag was false. The same failure returned after either service restarted.

All three attempted fixes changed handler-local behavior while the violated invariant spans two independently committed services.

## Structural Evidence and Constraints

- The same failure persists after three local fixes; a fourth handler patch cannot establish cross-service atomic ordering.
- The implementation artifact `order-confirmation-handler` is blocked pending an architecture decision.
- Preserve backward compatibility for existing event consumers.
- Preserve the current incident containment flag; it may remain enabled while architecture is corrected.
- Do not weaken the payment-before-confirmation invariant.
- Required route: `04-implementation` to `02-architecture` through `pc-system-design`, with user reapproval because the delivery boundary changes.
