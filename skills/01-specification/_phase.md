# Phase 01: Specification

## Purpose

Define precisely what to build. Specification translates validated discovery insights into unambiguous requirements and design documents that engineering can execute against. The goal is shared understanding, not exhaustive documentation.

## When to Enter

- Feasibility study is approved with a "go" decision.
- The team has a clear problem statement and target user definition from discovery.
- Or an approved `problem-frame` / `design-direction` exists and the team is ready to convert that direction into reviewed requirements.

## Entry Criteria

- Feasibility report exists with a documented go decision.
- Market research report and user personas are available.
- A product owner or sponsor is identified and available for decisions.

For lighter or routed entry paths, a reviewed `problem-frame` and approved `design-direction` may substitute for a heavier discovery packet as long as the problem statement, scope boundary, and open questions are explicit.

If implementation, quality, operations, or evolution discover that the current requirements are wrong or incomplete, route the fix back here with a `course-correction-note` instead of silently rewriting the spec.

## Exit Criteria (Quality Gate)

Spec document reviewed and signed off by engineering lead and product owner. All P0/P1 requirements have acceptance criteria. Open questions list is empty or deferred with documented rationale.

## Key Skills

| Skill | Purpose | Effort |
|---|---|---|
| [requirements-engineering](requirements-engineering/SKILL.md) | Capture and prioritize what the product must do | large |
| [spec-writing](spec-writing/SKILL.md) | Document the detailed design for engineering | large |
| [domain-modeling](domain-modeling/SKILL.md) | Establish shared language and entity relationships | medium |
| [acceptance-criteria](acceptance-criteria/SKILL.md) | Define measurable success conditions per requirement | medium |

## Typical Duration

- Small feature: 2-5 days
- Medium feature: 1-2 weeks
- Large initiative: 2-4 weeks
- Platform / infrastructure: 3-6 weeks

## Skill Sequence

```
requirements-engineering ──┬──> spec-writing
                           │
                           └──> domain-modeling ──> spec-writing
                                                        │
acceptance-criteria <───────────────────────────────────┘
```

Requirements come first. Domain modeling and spec writing can overlap. Acceptance criteria finalize after the spec stabilizes.

## Anti-Patterns

- **Waterfall spec in agile clothing.** Writing a 60-page spec and calling it a "user story." Match spec depth to methodology and risk.
- **Ambiguity as flexibility.** Vague requirements are not flexible; they are a defect. Be precise about what is decided and explicit about what is deferred.
- **No non-functional requirements.** Specifying features but ignoring performance, security, and accessibility guarantees. These surface late and cost more to fix.
- **Spec as contract, not communication.** The spec exists to create shared understanding. If engineers are confused, the spec failed regardless of its length.
- **Gold-plating.** Specifying edge cases that affect 0.1% of users at the same depth as core flows. Prioritize specification effort by impact.

## Cross-Cutting Matrix

See `rules/cross-cutting-matrix.yml` for `must_consider`, `must_produce`, `skip_when_fast_track`, and `conditional` cross-cutting obligations at this phase.
