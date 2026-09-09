# Input and Output Contract Notes

## Inputs

- **architecture-doc** -- Required boundary facts: callers/providers, interaction pattern, trust, and compatibility constraints. Existing code/documentation can supply these for a stable boundary; a new architecture document is not mandatory. Route material boundary changes to system design.
- **requirements-doc** -- Required behavior and constraints, supplied by approved requirements or the current accepted change scope. Clarify facts missing from both rather than guessing.
- **domain-model** -- Optional amplifying input when resource naming or entity boundaries need stronger domain vocabulary.

## Outputs

- **api-contract** -- The reviewed interface version, operation/message semantics, compatibility policy, and unresolved decisions; consumed by implementations, clients, and contract tests.
- **api-documentation** -- Consumer instructions and representative valid/error examples linked to that same contract, not a separately invented specification.
