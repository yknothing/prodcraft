# Input and Output Contract Notes

## Inputs

- **requirements-doc** -- Minimum required input. Functional and non-functional requirements with priority rankings, scope boundaries, and unresolved questions. Pay special attention to quality attributes (latency, throughput, availability, consistency) and brownfield coexistence constraints.
- **spec-doc** -- Optional amplifying input when spec-driven or waterfall work produces a detailed specification.
- **domain-model** -- Optional amplifying input when the problem has enough domain complexity that entity boundaries or ubiquitous language should shape component boundaries.

## Outputs

- **architecture-doc** -- The decision, ranked drivers, affected responsibilities and interfaces, actual runtime topology, significant ADRs, and relevant fitness functions. Reuse accepted context and keep detail proportional to the change. Must be understandable by a developer joining the work.
- **component-diagram** -- A version-controlled diagram of the affected boundary and interactions. Use C4 levels only where they clarify the decision; a local module or skill need not invent deployable containers. Mermaid, PlantUML, or Structurizr DSL are options, not mandatory dependencies.
