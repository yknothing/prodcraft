# Domain Modeling Eval Strategy

## Goal

Evaluate whether `domain-modeling` turns reviewed requirements into a shared domain model with clear entities, relationships, bounded contexts, and ubiquitous language.

## Why Routed Review First

This skill sits between requirements and architecture. Review should verify that it improves business-language clarity without turning into schema design or API design. The important question is whether the model makes the problem easier to talk about.

## Scenarios

Use two review scenarios:

1. A requirements set with ambiguous nouns or synonyms that different teams might interpret differently.
2. A more complex system where multiple bounded contexts are plausible and the skill must decide whether they are needed.

## Assertions

1. Core entities and relationships are identified from the requirements, not invented from the solution.
2. A glossary resolves ambiguous terms and synonyms.
3. Bounded contexts are introduced only when the domain complexity justifies them.
4. The model is validated against real scenarios from the requirements.
5. The output does not collapse into database or API design.
6. The model gives downstream skills a stable shared vocabulary.

## Method

Review a baseline domain summary without the skill and then a skill-assisted summary on the same requirements. Compare for:

- terminology precision
- relationship clarity
- bounded-context judgment
- whether business language became easier to use

## Exit Criteria

The skill can move to `review` when a reviewer can see that the domain model reduces ambiguity and supports `data-modeling` and `api-design`. If it merely restates nouns from the requirements, it is not ready.
