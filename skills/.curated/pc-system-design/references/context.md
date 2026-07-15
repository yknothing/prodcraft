# Context Notes

System design translates requirements and domain knowledge into a technical blueprint. A well-designed architecture absorbs change gracefully -- poor design decisions compound over time and become exponentially expensive to reverse. Invest here before writing code. Every subsequent skill in the architecture and implementation phases depends on the decisions made here.

In spec-driven work, system design often starts from a reviewed spec package. In agile and brownfield work, it may start from a reviewed requirements document with open questions still visible. Do not silently "fix" requirement ambiguity inside the architecture. Preserve unresolved scope, compatibility, and quality-bound questions as design constraints or architectural open questions.

## Reference Material

For worked architecture-style comparisons and an ADR example, see [decision-examples](decision-examples.md). Keep the core skill focused on drivers, boundaries, and trade-offs; use the reference when the team needs examples to calibrate the artifact shape.
