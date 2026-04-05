# Feasibility Study Eval Strategy

## Goal

Evaluate whether `feasibility-study` converts a narrowed idea into a defensible go/no-go, pivot, or scope-down recommendation across technical, economic, operational, and timeline dimensions.

## Why Routed Review First

This skill is a decision gate, not a research note. Review should confirm that it uses the evidence from market and user discovery to make a concrete viability call instead of re-asking upstream questions or sliding into requirements.

## Scenarios

Use two review scenarios:

1. A product concept with one dominant technical risk, such as a feature that depends on a hard integration or data constraint.
2. A scope-sensitive idea where the main question is operational or economic viability rather than technical possibility.

## Assertions

1. All four feasibility dimensions are covered.
2. The highest-risk technical assumption is explicitly validated by research or a small proof-of-concept.
3. Cost, revenue, and break-even assumptions are documented, not implied.
4. Operational burden is discussed as a real ownership issue, not a footnote.
5. The recommendation is explicitly one of go, no-go, or pivot/scope-down.
6. The output identifies the simplest viable version if the full idea is not justified.

## Method

Review a baseline feasibility memo without the skill, then a second pass with `feasibility-study` invoked on the same idea packet. Compare the two outputs for:

- whether the recommendation is actually decision-ready
- whether the riskiest assumption is made visible
- whether the output stays at viability level rather than drifting into spec or architecture

## Exit Criteria

The skill can move to `review` when a reviewer can read the report and answer: should we proceed, narrow, or stop? If the report still reads like exploratory brainstorming, it is not ready.
