# Input and Output Contract Notes

## Inputs

- **task-list** -- Required accepted task references, scope, dependencies, and acceptance conditions. Use the existing reviewed plan rather than duplicating it.
- **risk-register** -- Conditional source of known risks. Current task risk notes may suffice unless a standalone register is required by the workflow.
- **Calibration context** -- Comparable completed work and known execution/review constraints when available. Missing history is uncertainty, not permission to invent velocity or agent throughput.

## Outputs

- **estimate-set** -- `pc-sprint-planning` consumes task reference, unit, range/size or explicit unknown, confidence, evidence, assumptions, waiting/dependency constraints, and re-estimation trigger. Reuse a table in the current plan where permitted.

A known implementation task and an unknown vendor wait are different planning signals. Record the active-work estimate separately and leave vendor timing unresolved until evidence exists; do not sum incompatible units or report the result as a promised completion date.
