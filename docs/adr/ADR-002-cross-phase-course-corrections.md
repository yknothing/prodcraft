# ADR-002: Standardize Cross-Phase Course Corrections

**Date**: 2026-03-26
**Status**: Accepted
**Deciders**: tech lead, architect, developer

## Context

Prodcraft already models iterative feedback, but the repository has mostly local loops and phase-adjacent handoffs. Real projects often discover higher-order mismatches later:

- implementation reveals a requirements ambiguity
- quality review reveals an architectural flaw
- operations reveals a deployment or architecture boundary problem

Without a standard artifact and routing rule, these course corrections become ad hoc and expensive to audit.

## Decision

We introduce `course-correction-note` as the canonical artifact for direct jumps across `2-3` lifecycle phases.

Approved direct jumps:

- `04-implementation -> 01-specification`
- `04-implementation -> 02-architecture`
- `05-quality -> 02-architecture`
- `07-operations -> 02-architecture`
- `07-operations -> 03-planning`
- `08-evolution -> 01-specification`
- `08-evolution -> 02-architecture`
- `08-evolution -> 03-planning`

Every direct jump must preserve:

- the evidence that triggered the jump
- the blocked artifact or decision
- the constraints that remain true
- the recommended next skill
- whether the user must re-approve the route

## Consequences

### Positive

- Mid-cycle discoveries become auditable instead of conversational folklore.
- Downstream skills receive a stable artifact instead of reconstructing the failure from chat history.
- Reviewers can distinguish a legitimate course correction from scope drift.

### Negative

- The repository owns one more artifact schema and template.
- Teams must learn when to produce a course correction instead of silently rewriting upstream assumptions.

## References

- `schemas/artifacts/course-correction-note.schema.json`
- `templates/course-correction-note.md`
- `skills/_gateway.md`
