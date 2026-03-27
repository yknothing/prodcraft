# Task Execution QA Strategy

## Goal

Evaluate whether `task-execution` turns an approved implementation slice into a short, verifiable tactical batch without duplicating planning or implementation skills.

## Why This Skill Matters

The remaining execution gap is not just "a plan exists." It is whether the approved slice becomes:

- a short executable batch
- routed to the correct implementation discipline
- governed by explicit stop conditions
- summarized in a handoff-friendly checkpoint

## Initial Evaluation Mode

The first evaluation is a routed manual review using two scenarios:

1. a normal feature slice that should route through `tdd`
2. a bug-fix slice that should route through `systematic-debugging` before code changes

## Assertions

1. **tactical-not-strategic**
   - the output produces 2-5 minute batch steps instead of repeating 1-3 day planning

2. **routes-to-real-discipline**
   - the skill hands work to `systematic-debugging`, `tdd`, or `feature-development` instead of swallowing their role

3. **stop-conditions-explicit**
   - blockers and pause conditions are clearly named

4. **checkpoint-honest**
   - the output records what changed, what was verified, and what remains open

## Pass Standard

Treat the skill as strong review-stage evidence if it improves tactical execution discipline without duplicating `task-breakdown` or `feature-development`.
