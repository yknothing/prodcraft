# Input and Output Contract Notes

## Inputs

- **Approved outcome and boundary context** -- Required. Reuse the current intake decision, accepted requirements, and relevant source or document sections. A small change within established boundaries does not require a new architecture document.
- **architecture-doc** -- Required when the change introduces unresolved architecture decisions or the approved workflow explicitly requires it; otherwise reuse existing boundary references. Route missing decisions to `pc-system-design`, not already-settled context to a new document.
- **api-contract** -- Optional but strongly preferred when implementation work includes API-facing changes or compatibility surfaces.
- **spec-doc** -- Optional amplifying input for spec-driven or waterfall paths.

## Outputs

- **task-list** -- produced by this skill
- **dependency-graph** -- produced by this skill
