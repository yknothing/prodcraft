# Risk Assessment Evaluation Strategy

## Goal

Evaluate whether `risk-assessment` turns a reviewed task plan into a concrete, prioritized risk register that changes sequencing, scope, or mitigation instead of becoming generic planning paperwork.

## Why This Skill Matters

`task-breakdown` produces the work plan. `risk-assessment` should challenge that plan before execution starts, especially when brownfield coexistence, rollback, or dependency uncertainty could change the sequence.

The key question is whether the skill:

- identifies only material delivery risks
- ties each risk to mitigation, owner, or contingency
- changes the plan where risk is meaningful
- stays distinct from architecture and estimation

## Initial Evaluation Mode

The first evaluation is a **manual routed handoff review** from reviewed task breakdown into a bounded brownfield risk register.

This is review-stage evidence only. It does not replace future isolated automated benchmarks or execution-based planning evidence.

## Scenario

- `access-review-modernization-risk-register`

Inputs:

- task list
- dependency graph
- architecture risk context

## Assertions

1. **material-risks-only**
   - the output focuses on risks that can change sequence, scope, or release posture

2. **owner-and-mitigation-exist**
   - each significant risk has mitigation, contingency, or explicit ownership

3. **risk-changes-the-plan**
   - the register changes order, scope, or gating rather than documenting risk passively

4. **brownfield-risks-remain-explicit**
   - coexistence, rollback, migration, and dependency risks stay visible

5. **does-not-collapse-into-estimation**
   - the output stays on risk posture instead of turning into effort sizing

## Pass Standard

Treat the skill as strong review-stage evidence if the handoff artifact shows a clear risk-register boundary downstream of planning.

## Next QA Step

- add an isolated benchmark comparing generic planning risk notes against the same bounded scenario
- add a second scenario without brownfield coexistence pressure
