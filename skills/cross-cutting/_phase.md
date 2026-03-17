# Cross-Cutting Concerns

## Purpose

Skills that span the entire lifecycle and apply at every phase. These are not sequential -- they are continuous practices woven into all work.

## When to Apply

Cross-cutting skills are triggered by context, not by phase transitions:
- Building UI? Apply accessibility.
- User-facing text? Apply internationalization.
- Any code change? Apply observability (structured logging, metrics).
- Any project? Apply documentation.
- Regulated industry? Apply compliance.

## Key Skills

| Skill | Applies When | Effort |
|---|---|---|
| documentation | Any phase produces artifacts worth documenting | small-medium |
| observability | Any code is instrumented for debugging and monitoring | small |
| accessibility | Any user interface is built or modified | small-medium |
| internationalization | Any user-facing text is created | medium |
| compliance | Regulatory or legal requirements apply | large |

## Integration Pattern

Cross-cutting skills are incorporated into the Definition of Done for each phase:
- Code review checks for observability (logging, metrics)
- PR checklists include accessibility verification
- Sprint definition of done includes documentation updates
- Release checklists include compliance verification
