# Input and Output Contract Notes

## Inputs

- **task-list** -- Required candidate tasks, goal, dependency constraints, and acceptance conditions.
- **estimate-set** -- Required current ranges or relative sizes with confidence and assumptions. Unknown items cannot silently become committed capacity.
- **risk-register** -- Conditional input; reuse current risk notes unless the approved workflow requires a standalone register.
- **Capacity and ownership** -- Required for a commitment, including known availability, review/integration, operational load, and constrained environments. Missing capacity or ownership permits only a clearly provisional plan.

## Outputs

- **sprint-plan** -- The execution team consumes the goal, horizon, capacity basis, selected task references, dependency order, confirmed or proposed owners, acceptance/handoff points, exclusions, and replan triggers. Distinguish commitment from stretch, deferred, blocked, and provisional work. A proposal does not create user or team approval.

A solo task can use a short plan section. Parallel agents sharing one integration environment still share that constraint; the plan must not count it as independent capacity for each agent.
