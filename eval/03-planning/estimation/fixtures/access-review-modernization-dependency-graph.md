# Dependency Graph

- contract tests must land before the supported reassignment handler is considered done
- coexistence-boundary work must stay aligned with the supported handler, not trail behind it
- rollback-oriented delivery checks depend on the supported handler and coexistence boundary being explicit
- the sync-semantics decision gate must remain open until implementation evidence shows whether async behavior is still required
