# Tech Selection Evaluation Strategy

## Goal

Evaluate whether `tech-selection` turns a reviewed architecture into explicit stack decisions with real trade-offs instead of leaving technology choices to ad hoc implementation drift.

## Why This Skill Matters

`system-design` defines the structure and constraints. `tech-selection` should decide the concrete stack inside those constraints without reopening architecture or pretending every technology question is still open.

The key question is whether the skill:

- keeps decisions tied to architecture drivers
- chooses only the technology categories that actually need a decision now
- records rejected alternatives and trade-offs
- stays distinct from architecture design and implementation planning

## Initial Evaluation Mode

The first evaluation is a **manual routed handoff review** from reviewed system design into a bounded brownfield technology decision.

This is review-stage evidence only. It does not replace future isolated automated benchmarks or deeper multi-option evaluation.

## Scenario

- `access-review-modernization-tech-selection`

Inputs:

- requirements summary
- architecture summary

## Assertions

1. **stays-on-real-decision-surface**
   - the output only chooses technologies that remain unresolved after architecture

2. **maps-choices-to-drivers**
   - selected technologies are justified against coexistence, operational burden, and reversibility drivers

3. **records-trade-offs**
   - alternatives and rejected costs are visible rather than implied

4. **chooses-minimum-stack**
   - the plan avoids unnecessary platform sprawl

5. **does-not-reopen-architecture**
   - the output does not replace structural design with a new architecture pass

## Pass Standard

Treat the skill as strong review-stage evidence if the handoff artifact shows a clear technology-decision boundary downstream of architecture.

## Next QA Step

- add an isolated benchmark comparing generic stack advice against the same architecture slice
- add a second scenario with a different operational profile so the skill is not overfit to one brownfield modernization case
