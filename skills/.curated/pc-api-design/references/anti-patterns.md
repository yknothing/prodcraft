# Anti-Pattern Notes

1. **Chatty APIs** -- Requiring 10 calls to render one page. Design for client use cases.
2. **Leaking implementation** -- Exposing internal IDs, database column names, or internal service structure.
3. **Ignoring pagination** -- Every list endpoint must paginate. No unbounded responses.
4. **Breaking changes without versioning** -- Renaming a field breaks every client. Plan for evolution.
5. **Closing architecture questions inside the API** -- Turning unresolved sync, rollout, or compatibility questions into fixed contract behavior without labeling them.
