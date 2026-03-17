# Persona Schema

This document defines the required format for all persona files in the `personas/` directory.

## Frontmatter (YAML)

Every persona file MUST begin with YAML frontmatter containing these fields:

```yaml
---
name: kebab-case-name           # Unique identifier, matches filename without extension
description: "Short sentence"   # What this persona does, in quotes
leads:                          # Phases where this persona is the primary driver
  - "01-specification"
  - "02-architecture"
advises:                        # Phases where this persona provides input but doesn't own
  - "03-planning"
  - "04-implementation"
---
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Kebab-case identifier matching filename |
| `description` | string | yes | One-line summary of what this persona owns |
| `leads` | list | yes | Phases this persona drives and is accountable for |
| `advises` | list | yes | Phases this persona contributes to without owning |

## Body Structure

### Role Definition

A concise description of the persona's purpose, mindset, and value to the team. This is not a job description -- it captures the *perspective* this persona brings to product development.

### Core Responsibilities

Bulleted list of what this persona is accountable for. Focus on outcomes, not tasks. Each responsibility should be something you could verify was done or not done.

### Decision Authority

What decisions this persona can make unilaterally, what requires consultation, and what requires consensus. Be specific -- vague authority creates conflict.

### Interaction Patterns

How this persona collaborates with other personas:

- **Works with [persona]** on [topic] -- describe the nature of the collaboration
- **Receives from [persona]** -- what inputs this persona depends on
- **Provides to [persona]** -- what outputs other personas depend on

### Quality Criteria

The quality lens this persona applies. When reviewing work, what questions does this persona ask? What standards do they enforce? This section defines the persona's unique contribution to overall quality.

## Key Principle: Personas Are PERSPECTIVES

Personas represent a point of view, not a set of instructions. They define *how someone thinks about the work*, not step-by-step procedures for doing the work.

One person may embody multiple personas (a solo developer is PM + architect + developer + DevOps). A persona may be shared by multiple people (a review committee shares the reviewer persona).

Personas help answer: "What lens should I apply right now?" not "What steps should I follow?"
