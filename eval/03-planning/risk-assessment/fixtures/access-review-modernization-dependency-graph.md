# Dependency Graph

- contract tests must land before implementation changes are considered complete
- coexistence checks depend on the bounded modern handler existing
- release and rollback preparation depend on the coexistence path being explicit
- sync semantics decision is a blocker for wider rollout, not for the narrow initial slice
