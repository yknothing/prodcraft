---
name: pc-acceptance-criteria
description: Use when defining testable criteria that determine whether a requirement is met
metadata:
  phase: 01-specification
  inputs:
  - requirements-doc
  - spec-doc
  outputs:
  - acceptance-criteria-set
  prerequisites:
  - pc-requirements-engineering
  quality_gate: Every P0/P1 requirement has at least one acceptance criterion, QA team has reviewed
  roles:
  - product-manager
  - qa-engineer
  methodologies:
  - all
  effort: medium
---

# Acceptance Criteria

> If you can't test it, you can't ship it. Acceptance criteria make requirements verifiable.

## Context

Acceptance criteria bridge the gap between "what we want" (requirements) and "how we verify it works" (tests).

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Choose a Format

Use Given-When-Then (Gherkin) for behavior-driven criteria:
```
Given [precondition]
When [action]
Then [expected result]
```

Or use checklist format for simpler requirements:
```
- [ ] User can reset password via email link
- [ ] Link expires after 24 hours
- [ ] User sees error if link is expired
```

### Step 2: Cover Happy Path and Edge Cases

For each requirement, write criteria for:
- **Happy path**: Normal, expected usage
- **Edge cases**: Boundary values, empty inputs, maximum limits
- **Error paths**: Invalid input, permission denied, network failure
- **Security paths**: Unauthorized access, injection attempts

### Step 3: Make Criteria Measurable

Bad: "Page loads quickly"
Good: "Page loads in under 2 seconds on 3G connection with 95th percentile"

Bad: "System handles many users"
Good: "System supports 500 concurrent users with < 200ms response time at p95"

### Step 4: Review with QA

QA engineers are expert at finding missing edge cases. Review criteria with them before finalizing. They should be able to write test cases directly from acceptance criteria.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Every P0/P1 requirement has at least one acceptance criterion
- [ ] Happy path, edge cases, and error paths covered for critical features
- [ ] All criteria are measurable and testable
- [ ] QA team has reviewed and approved
