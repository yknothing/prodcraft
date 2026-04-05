# Risk Assessment Isolated Benchmark Review

## Scope

This note reviews the first isolated explicit-invocation benchmark for `risk-assessment`.

The benchmark uses one brownfield planning slice and compares:

1. a generic baseline prompt
2. the same prompt with explicit `risk-assessment` skill invocation

Runner: `copilot`
Run: `eval/03-planning/risk-assessment/run-2026-04-03-copilot-brownfield-minimal`

## Scenario: Brownfield Planning Risk Register

### Baseline

The baseline was competent. It identified major delivery and dependency risks, kept rollback and coexistence visible, and proposed release gates.

That means this benchmark is not a blowout. The baseline already understands the shape of a decent risk register.

### With-Skill

The skill-applied branch was still better on the contract that matters here:

- it stayed tightly focused on material delivery risk rather than drifting into adjacent planning work
- it paired each major risk with explicit owner and mitigation language
- it surfaced more concrete planning adjustments and gating changes
- it kept brownfield coexistence, rollback, and contract-test-first constraints explicit

The improvement is moderate rather than dramatic, but it is visible and directionally correct on the skill's core job.

## Judgment

This is still a narrow evidence base, but it is now stronger than routed review alone:

- routed handoff review proves the lifecycle boundary
- one isolated benchmark shows the skill produces a more explicit and action-shaping risk register than baseline

Current limits remain:

- only one scenario exists
- the benchmark is brownfield-only
- there is no downstream delivery evidence yet showing later work consumed this register

Those gaps should be addressed in follow-up coverage, but they no longer justify keeping the skill at `review` when a clean isolated run now exists and shows measurable improvement.

## Status Recommendation

- Recommended status: `tested`
