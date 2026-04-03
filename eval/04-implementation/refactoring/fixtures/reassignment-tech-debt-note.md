# Reassignment Tech-Debt Note

The reassignment handler currently repeats the same create-and-sync path for each supported type.

That duplication is small today, but it creates recurring change cost:

- rollout behavior must stay aligned across every supported branch
- later additions can silently diverge in sync behavior
- review effort increases because structural noise hides real behavior changes

This is a narrow implementation debt item, not a reason to reopen product scope.
