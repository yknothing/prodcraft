# Input and Output Contract Notes

## Inputs

- **requirements-doc** -- Minimum required input. Functional and non-functional requirements with priority rankings, scope boundaries, and unresolved questions. Pay special attention to quality attributes (latency, throughput, availability, consistency) and brownfield coexistence constraints.
- **spec-doc** -- Optional amplifying input when spec-driven or waterfall work produces a detailed specification.
- **domain-model** -- Optional amplifying input when the problem has enough domain complexity that entity boundaries or ubiquitous language should shape component boundaries.

## Outputs

- **architecture-doc** -- Written document covering the ranked quality attribute table, architectural style, component boundaries, communication patterns, deployment topology, significant ADRs, and the fitness functions that will validate the most important decisions. Must be understandable by any developer joining the team.
- **component-diagram** -- C4 diagrams at context, container, and component levels. Use a tool that supports version control (Structurizr DSL, Mermaid, PlantUML).
