# Prodcraft Pressure-Test Protocol

## Goal

Run repeatable pressure tests against the current Prodcraft control plane without redesigning it. The purpose is to decide what can be simplified later based on evidence, not to add new guardrails by instinct.

## Non-Goals

- do not delete skills, workflows, or artifacts during the run
- do not reinterpret a tabletop replay as live runtime evidence
- do not change routing rules just because one scenario feels awkward

## Evidence Classes

| Class | Meaning | Eligible To Trigger Follow-On Contract Work |
|------|---------|----------------------------------------------|
| `tabletop` | repository-guided replay using the written contracts only | no |
| `live` | an actual run through intake and downstream routing with a fresh request | yes |

Only `live` pressure-test evidence can unlock follow-on contract changes such as the language-boundary task.

## Operator Checklist

1. Pick `3-5` scenarios from `eval/meta/prodcraft-pressure-tests/scenario-matrix.md`
2. Prefer at least one of:
   - `PT-04-hotfix-incident`
   - `PT-05-docs-only-change`
   - `PT-06-mixed-language-request`
3. Start from a clean request with no hidden phase context
4. Preserve the approved `intake-brief` and any `course-correction-note`
5. Record the run in `eval/meta/prodcraft-pressure-tests/templates/live-run-record.md`
6. Add the completed record under `eval/meta/prodcraft-pressure-tests/runs/`
7. Update the subtraction-candidate summary if a pattern repeats

## Review Questions

- Was the first route correct?
- Which clarification question actually changed the route?
- Which cross-cutting skill created durable value?
- Which artifact or metadata field was recorded but not materially used?
- Which friction repeated from earlier runs?
- Is the friction essential complexity or accidental complexity?

## Escalation Rule

Only escalate a deletion or schema-tightening proposal when the same low-value friction appears in at least two `live` runs or once in a high-severity operational scenario.

## Language-Boundary Trigger

The deferred language-boundary task may begin only after:

- Tasks 1-6 remain green in validation
- at least one `live` pressure test uses `PT-06-mixed-language-request` or an equivalent mixed-language scenario
- the recorded friction is about artifact/presentation language boundaries, not general prompt quality
