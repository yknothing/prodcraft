# Estimation QA Strategy

## Goal/Objective

Evaluate whether `estimation` turns reviewed task lists and risk context into realistic planning signals with explicit assumptions, confidence, and coordination cost.

## Why Routed Review First

`estimation` is a routed planning skill. Its quality is not whether it gets discovered, but whether it helps a planner make a believable commitment from actual work decomposition.

The review question is whether the skill sizes work with enough honesty that sprint or milestone planning can use the result without quietly converting uncertainty into false precision.

## Scenario(s)

1. `access-review-modernization-estimation`
   - a brownfield task list with rollout, coexistence, and dependency risk
   - used to test whether the skill inflates confidence or surfaces uncertainty properly

2. `feature-slice-estimation`
   - a simpler non-brownfield task list
   - used to confirm the skill still produces useful estimates when migration risk is low

## Assertions

1. `uses-a-consistent-estimation-unit`
   - the plan picks a coherent sizing unit and keeps it stable
   - the output is not a mix of incompatible sizing styles

2. `estimates-task-by-task`
   - each task receives a size or range
   - no planned task is left implicitly unestimated

3. `makes-assumptions-and-uncertainty-explicit`
   - blockers, dependencies, and open questions are recorded
   - low-confidence work is clearly marked as such

4. `accounts-for-risk-and-coordination-cost`
   - novelty, integration, review, and waiting time influence the estimate
   - brownfield or rollout complexity increases the estimate where appropriate

5. `prepares-downstream-handoff`
   - the output is usable by `sprint-planning` without translating the estimate set first

## Method

1. Produce a baseline estimate set from the same task list and risk context without the skill.
2. Produce a second estimate set while explicitly using `estimation`.
3. Compare both outputs for realism, uncertainty handling, and planning usability.
4. Record whether the skill improves decision quality enough to justify review status.

## Exit Criteria for Review Stage

- Every task is sized with visible uncertainty or confidence
- The output avoids single-number theater and hidden assumptions
- Risk meaningfully changes the estimate where it should
- The result is directly consumable by planning without rework
- A benchmark can be added later without changing the review contract
