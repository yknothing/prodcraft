# Input and Output Contract Notes

## Inputs

- **task-list** -- Defines the current slice, scope boundary, and success criteria.
- **test-suite** -- Gives the executable safety net that the implementation must satisfy.
- **architecture-doc** -- Provides component boundaries and constraints.
- **api-contract** -- Protects externally visible behavior when the slice changes a public or inter-service interface.

## Outputs

- **source-code** -- The implementation for the planned slice, ready for code review and downstream quality checks.
