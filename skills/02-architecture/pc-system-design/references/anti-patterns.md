# Anti-Pattern Notes

1. **Resume-Driven Architecture** -- Choosing technologies because they look impressive rather than because they solve the problem. Always start from drivers, not from tools.
2. **Big Design Up Front** -- Trying to nail every detail before writing code. Design to the level of certainty you have; mark unknowns as spikes for validation during implementation.
3. **Distributed Monolith** -- Splitting into microservices without achieving independent deployability. If services must deploy together, they are not separate services.
4. **Ignoring the "-ilities"** -- Focusing only on functional requirements. Non-functional requirements (scalability, observability, security) are architectural concerns -- they rarely emerge from good intentions alone.
5. **Architecture Astronautics** -- Over-abstracting and over-generalizing for hypothetical future needs. Design for today's known requirements with extension points for likely changes.
6. **Closing open questions by accident** -- Turning unresolved compatibility, synchronization, or rollout questions into assumed architecture facts without labeling them as assumptions or follow-up decisions.
7. **Irreversible bets without an exit story** -- Choosing a platform, decomposition, or migration path that is expensive to unwind without documenting why the lock-in is acceptable and how failure would be detected.
