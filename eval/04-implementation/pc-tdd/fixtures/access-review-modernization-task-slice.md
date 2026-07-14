# Task Slice

## Selected Tasks

- **Task 3**: Define unsupported-flow responses for non-release-1 reassignment variants.
  - Done when contract tests cover structured unsupported responses.
- **Task 10**: Implement supported reassignment flow subset.
  - Depends on task 3, task 4, and task 5.
  - Done when confirmed release-1 reassignment variants work and unsupported variants fail explicitly.

## Blockers and Constraints

- Unsupported reassignment variants must fail explicitly rather than inventing release-1 behavior.
- Final release-1 tenant compatibility set is not fully closed.
- Brownfield coexistence must remain intact.
