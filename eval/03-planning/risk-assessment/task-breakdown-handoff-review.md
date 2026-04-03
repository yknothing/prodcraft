# Task Breakdown to Risk Assessment Handoff Review

## Goal

Verify that `risk-assessment` is the correct routed follow-up after `task-breakdown` produces an implementation-ready plan but delivery risk still needs to alter the sequence.

## Scenario

- `access-review-modernization-risk-register`

This scenario is a brownfield planning slice where:

- release 1 must coexist with the legacy module
- sync semantics remain unresolved
- rollback and compatibility work must stay explicit
- task sequencing exists, but key delivery and dependency risks still need to change the plan

## Artifacts Reviewed

- planning inputs:
  - `fixtures/access-review-modernization-task-list.md`
  - `fixtures/access-review-modernization-dependency-graph.md`
  - `fixtures/access-review-modernization-architecture-risk-context.md`

## Review Findings

## 1. The task plan is real but not yet risk-shaped

The upstream task breakdown already creates slices and dependencies, but it does not by itself decide:

- which open questions should block later tasks
- where coexistence or rollback risk should force extra gating
- which dependencies need explicit contingency ownership

That is the correct downstream boundary for `risk-assessment`.

## 2. The register must change the plan

For this scenario, a correct `risk-assessment` output should:

- elevate unresolved sync semantics into a planning risk, not a footnote
- keep coexistence and rollback preparation visible as release-shaping risks
- attach owner and mitigation to dependency and compatibility risks
- change sequence or gating where those risks are meaningful

## 3. The route stays distinct from neighboring skills

This scenario should not go back to `task-breakdown`, because the work decomposition already exists.

It also should not jump straight into `estimation`, because the missing output is not effort confidence alone. It is a concrete risk register that changes how the plan should be executed.

The clean route is:

- `task-breakdown` produces the implementation-ready work items
- `risk-assessment` challenges the plan for delivery, dependency, and rollback risk
- downstream estimation, sprint planning, and delivery consume the resulting register

## Assertion Review

| Assertion | Review result | Notes |
|---|---|---|
| material-risks-only | pass | The scenario is dominated by coexistence, dependency, and rollback risk, not generic planning noise. |
| owner-and-mitigation-exist | pass | The register boundary is meaningful only if each major risk changes accountability. |
| risk-changes-the-plan | pass | Unresolved sync and compatibility questions should affect sequence and gating. |
| brownfield-risks-remain-explicit | pass | Coexistence and rollback are first-class planning risks here. |
| does-not-collapse-into-estimation | pass | The downstream task is risk posture, not just confidence sizing. |

## Conclusion

This first routed handoff review is enough to justify moving `risk-assessment` from `draft` to `review`.

It does not justify `tested`. The next step is an isolated benchmark on the same bounded planning slice plus a second scenario without modernization-heavy risk.
