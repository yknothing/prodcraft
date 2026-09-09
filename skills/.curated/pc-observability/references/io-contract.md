# Input and Output Contract Notes

## Inputs

- Current code or workflow entry points where behavior, failure, or cost must be visible
- Existing execution boundaries such as CLI runners, background jobs, request handlers, or workflow dispatchers
- Any external platform constraints on usage accounting or token reporting

## Outputs

- **observability-spec** -- Boundary, questions, source fields, privacy/cardinality constraints, consumers, and design/runtime verification status. Reuse an existing contract section where sufficient.
- **execution-event-schema** -- Applicable log/metric/trace/event definitions or a versioned change to the existing contract. Include skill/model/usage fields only for AI boundaries; downstream monitoring consumes the actual supported signals.
