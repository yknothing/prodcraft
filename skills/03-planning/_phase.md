# Phase 03: Planning

## Purpose

Break the architecture into actionable, estimable, assignable work units. Planning bridges the gap between design and execution by making the work visible, sequenced, and resourced.

## When to Enter

- Architecture review has passed.
- Technical approach and component boundaries are defined.
- Major coexistence or compatibility boundaries are visible enough to sequence work safely.

## Entry Criteria

- Architecture documents are approved.
- API contracts are reviewed when the work depends on external or inter-service interfaces.
- Team capacity and availability are known for the planning horizon.
- Dependencies on external teams or systems are identified.

## Exit Criteria (Quality Gate)

All tasks are estimated, assigned, and sequenced. Dependencies are mapped. Risks are documented with mitigations. The team agrees the plan is achievable within the stated timeline.

## Key Skills

| Skill | Purpose | Effort |
|---|---|---|
| task-breakdown | Decompose architecture into implementable work items | medium |
| sprint-planning | Organize work into iteration-sized chunks | small |
| estimation | Size work items with calibrated confidence | medium |
| risk-assessment | Identify and mitigate delivery risks | medium |

## Typical Duration

- Small feature: half day to 1 day
- Medium feature: 1-2 days
- Large initiative: 3-5 days
- Multi-team program: 1-2 weeks

## Skill Sequence

```
task-breakdown ──> estimation ──> sprint-planning
                       │
risk-assessment ───────┘
```

Break down tasks first, then estimate. Risk assessment informs estimation (add buffers for risky items). Sprint planning uses estimates and risk data to sequence work.

In brownfield programs, planning should preserve reversible seams and coexistence work instead of flattening the roadmap into replacement-only implementation.

## Anti-Patterns

- **Planning theater.** Spending more time planning than building. Plans are a tool, not a deliverable. Keep planning proportional to the work.
- **No buffer for unknowns.** Plans that assume everything goes perfectly. Add explicit contingency for integration, testing, and unknowns.
- **Individual hero plans.** Assigning critical-path work to a single person with no backup. Identify bus-factor risks and cross-train.
- **Ignoring dependencies.** Planning in isolation without confirming external team availability or API readiness. Map dependencies and get commitments.
- **Estimate as commitment.** Treating estimates as deadlines. Estimates are probabilistic; communicate ranges and confidence levels.
