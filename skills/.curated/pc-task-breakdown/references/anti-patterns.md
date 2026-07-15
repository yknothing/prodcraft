# Anti-Pattern Notes

1. **Horizontal slicing** -- "Build all the database layer, then all the API layer, then all the UI." Vertical slices (one feature end-to-end) deliver value faster.
2. **Mega-tasks** -- "Implement authentication" is not a task. Break into: registration, login, password reset, session management, etc.
3. **No dependencies mapped** -- Developers blocked waiting for other tasks creates idle time and frustration.
4. **Over-decomposition** -- Tasks smaller than 2 hours create overhead. Find the sweet spot.
5. **Planning as rewrite fantasy** -- Turning a coexistence architecture into a replacement-only task plan that ignores rollback and compatibility work.
