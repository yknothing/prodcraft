# Code Review Gotchas

## Gotchas

### Heuristic scanners flag idiomatic literals
- Trigger: A lightweight hook or regex flags `0`, `1`, `""`, or `[]` in tests, indexing, or standard library patterns.
- Failure mode: Review time burns on false positives, or teams disable the gate to "make CI green".
- What to do: Confirm which scanner and policy apply. Under the Prodcraft scanner policy, use `ALLOW_MAGIC_NUMBER: reason, ticket` for a justified local exception. Otherwise follow project conventions. Extract constants only when they represent a shared concept, not merely to silence an inapplicable checklist.
- Escalate when: The flagged literal is part of a language/framework contract and cannot be expressed cleanly without harming readability.

### Exceptions without traceability
- Trigger: A reviewer accepts a magic value "just this once" without a ticket-backed rationale.
- Failure mode: The exception becomes permanent tribal knowledge and spreads as copy-paste.
- What to do: If the project requires ticket-backed scanner exceptions, block on that explicit policy and cite it. Use `ALLOW_MAGIC_NUMBER: reason, ticket` in the Prodcraft source repository. Without that policy, evaluate the actual correctness or maintenance risk instead of inventing a required token.
- Escalate when: The same exception pattern repeats across files in one changeset (signals a missing shared constant or configuration surface).

### Hardcoding disguised as configuration
- Trigger: Values move from inline literals into ad-hoc local variables without a stable configuration boundary.
- Failure mode: The code looks "clean" but still embeds environment-specific behavior in source.
- What to do: Treat that as hardcoding unless the value is sourced from configuration, build-time injection, or a clearly owned constants module with a single source of truth.
- Escalate when: The value varies per environment, tenant, or deployment region but remains in repository source.
