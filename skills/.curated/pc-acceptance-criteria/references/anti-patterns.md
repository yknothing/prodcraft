# Anti-Pattern Notes

1. **Too vague** -- "System works correctly" is not acceptance criteria.
2. **Too implementation-specific** -- "Redis cache TTL is 300s" is an implementation detail, not acceptance criteria.
3. **Missing negative cases** -- Only testing the happy path. What happens when things go wrong?
4. **Criteria written after implementation** -- Write criteria BEFORE coding. They guide development, not just verify it.
