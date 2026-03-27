# Delivery Completion QA Strategy

## Goal

Evaluate whether `delivery-completion` turns verified work into an explicit integration outcome without duplicating `release-management` or `deployment-strategy`.

## Why This Skill Matters

The remaining delivery-side gap is not deployment mechanics alone. It is whether verified work has a clear fate:

- land now
- push and open a PR
- keep for later
- discard deliberately

The key question is whether Prodcraft can make that choice explicit and auditable instead of relying on implied "done" states.

## Initial Evaluation Mode

The first evaluation is a routed manual review using two scenarios:

1. a verified feature branch that should become a PR handoff
2. a verified local change that should be preserved or discarded deliberately

## Assertions

1. **four-outcomes-explicit**
   - the output presents a bounded set of completion outcomes instead of vague next-step prompts

2. **verification-gate-preserved**
   - the skill refuses completion options when verification evidence is stale

3. **discard-safety**
   - destructive cleanup requires typed confirmation

4. **thin-delivery-boundary**
   - the skill hands off to `release-management` for coordinated shipping instead of swallowing release planning

## Pass Standard

Treat the skill as strong review-stage evidence if it improves completion clarity and safety without duplicating release coordination or rollout design.

## Next QA Step

- add an isolated benchmark for PR, keep, and discard variants
- compare against a generic branch-finish baseline
