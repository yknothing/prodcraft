# Problem Framing Eval Strategy

`problem-framing` is an **entry-stack routed skill**. Its value is not mainly whether metadata wins discovery on its own. Its value is whether, after `intake` has already chosen the route, the skill sharpens the problem and direction without turning entry into a heavyweight workshop.

QA should therefore focus on three questions:

1. **Usability**: does the skill keep the additional question load low?
2. **Observability**: does it produce artifacts that explain why a direction was chosen?
3. **Execution quality**: does it produce cleaner downstream handoff than a baseline conversation?

## Evaluation Mode

- `evaluation_mode`: `routed`
- trigger eval: optional and secondary
- primary evidence: explicit invocation review + intake handoff review

## Assertions to Test

### 1. Boundary discipline

The skill should:
- stay after intake, not repeat full triage
- stay before requirements or architecture, not drift into implementation detail
- compare solution directions, not workflow-routing paths

### 2. Low user burden

The skill should:
- usually add no more than 1-3 new questions
- justify any case that exceeds 3
- avoid restating questions already settled in the intake brief

### 3. Output observability

The framing output should make it easy for reviewers to see:
- why `problem-framing` was invoked
- which answers materially changed the direction
- what options were considered
- why the recommended direction won
- what skill should consume the output next

### 4. Downstream usefulness

The output should help downstream work start cleanly by:
- sharpening the problem statement
- preserving constraints and non-goals
- keeping unresolved items visible instead of silently resolving them
- naming a clear next lifecycle destination

## First Review Scenarios

### Scenario A: Non-brownfield feature direction

Use a new-product or new-feature request where intake can route to specification, but the delivery direction is still fuzzy.

Fixture:
- `fixtures/team-invite-product-intake-brief.md`

Why this matters:
- checks that the skill is not overfit to modernization work
- checks whether the skill can compare directions without inheriting brownfield assumptions

### Scenario B: Brownfield modernization direction

Use a modernization request where coexistence constraints are known, but the release-1 direction remains fuzzy.

Fixture:
- `fixtures/access-review-modernization-intake-brief.md`

Why this matters:
- checks whether the skill preserves coexistence and release boundaries
- checks whether it leaves architecture and migration sequencing to downstream skills

## Review Standard for First Pass

For `problem-framing` to stay in `review` with credible momentum, the first manual evaluation should show:

- a bounded question budget
- a visible `problem-frame`
- at least 2 viable directions compared
- a justified recommended direction
- a clean next handoff to `requirements-engineering`, `market-analysis`, `user-research`, or `feasibility-study`

Do not promote the skill beyond `review` until there is at least one manual or isolated benchmark review showing that the output is materially stronger than a no-skill baseline.
