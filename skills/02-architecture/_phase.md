# Phase 02: Architecture

## Purpose

Design the system structure that satisfies the specification. Architecture decisions are the hardest to reverse, so invest in getting the big choices right: boundaries, data flow, integration points, and technology selection.

## When to Enter

- Specification is signed off by engineering lead and product owner.
- Requirements and domain model are stable enough to design against.

## Entry Criteria

- Spec document exists and has been reviewed.
- Domain model is documented with entity relationships.
- Non-functional requirements (performance, scale, security) are quantified.

## Exit Criteria (Quality Gate)

Architecture review passed. The review confirms: all functional requirements are addressable, non-functional requirements have a credible strategy, integration points are identified, and deployment topology is defined.

## Key Skills

| Skill | Purpose | Effort |
|---|---|---|
| system-design | Define component boundaries and interactions | large |
| api-design | Specify contracts between components and external consumers | medium |
| data-modeling | Design storage schemas and data flow | medium |
| security-design | Threat model and define security controls | medium |
| tech-selection | Choose languages, frameworks, and infrastructure | medium |

## Typical Duration

- Small feature (within existing architecture): 1-3 days
- Medium feature (new component): 1-2 weeks
- Large initiative (new system): 2-4 weeks
- Platform rewrite: 4-8 weeks

## Skill Sequence

```
system-design ──┬──> api-design
                ├──> data-modeling
                ├──> security-design
                └──> tech-selection
```

System design establishes the high-level structure. The remaining skills can proceed in parallel, feeding back into system design as constraints emerge.

## Anti-Patterns

- **Astronaut architecture.** Over-engineering for hypothetical future requirements. Design for current needs with extension points, not speculative abstractions.
- **Resume-driven development.** Choosing technology because it is trendy rather than appropriate. Every technology choice must justify itself against the requirements.
- **Architecture without operators.** Designing systems without considering who runs them, how they are deployed, or how they fail. Include operations perspective early.
- **Ignoring existing systems.** Designing in a vacuum without mapping integration points to the current landscape. Architecture lives in context.
- **Big bang architecture.** Attempting to define everything upfront. Use iterative architecture: decide what must be decided now, defer what can be deferred.
