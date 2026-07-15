# Anti-Pattern Notes

1. **Solution masquerading as requirement** -- "Use Redis for caching" is a solution, not a requirement. The requirement is "cache frequently accessed data to achieve < 50ms read latency."
2. **Vague requirements** -- "The system should be fast" is untestable. Quantify everything.
3. **Invented precision** -- Turning "must remain responsive" into "p99 < 800ms" without a source or approved assumption creates false certainty. Mark unknown bounds as open questions.
4. **Requirements by committee** -- Too many stakeholders without a single owner leads to bloat. One person owns the requirements doc.
5. **Scope creep via "just one more"** -- Each new requirement has a cost. Evaluate against the backlog, don't just add.
