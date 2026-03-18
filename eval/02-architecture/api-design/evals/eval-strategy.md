# API Design QA Strategy

## Goal

Evaluate whether `api-design` turns reviewed architecture and requirements into stable, bounded contracts without collapsing unresolved architecture questions into premature API behavior.

## Why Start with Routed Handoff

`api-design` sits immediately downstream of `system-design`.

The first QA question is not trigger discoverability. The first QA question is whether the skill:

- respects architecture boundaries
- preserves brownfield coexistence constraints
- avoids leaking implementation and migration decisions into the contract
- prepares clean handoff for implementation and contract testing

## Initial Evaluation Mode

The first evaluation is a **manual architecture-to-API handoff review** using the brownfield access-review modernization scenario.

This is review-stage evidence only. It does not replace future isolated automated benchmarks.

## Scenario

- `access-review-modernization-architecture-handoff`

Inputs:

- reviewed architecture outline
- supporting requirements document

## Assertions

1. **stays-in-api-contract-layer**
   - output stays at endpoint/contract/event/interface level
   - it does not collapse into implementation tasks, rollout sequencing, or detailed schema internals beyond contract scope

2. **preserves-brownfield-coexistence**
   - coexistence and compatibility boundaries remain explicit
   - the contract does not assume a big bang replacement or silently resolve legacy behavior

3. **preserves-open-questions**
   - unresolved sync semantics, tenant compatibility, and historical-read behavior remain visible as assumptions, deferred behavior, or explicit open questions

4. **defines-consistent-contract-shape**
   - operations, errors, and authorization boundaries are consistent and traceable to the architecture/requirements

5. **prepares-downstream-handoff**
   - output is shaped for implementation and contract testing

## Pass Standard

Treat a run as strong review-stage evidence if it clearly outperforms a generic baseline on:

- compatibility-boundary preservation
- unresolved-question handling
- consistency of contract shape
- downstream readiness for implementation/testing

## Next QA Step

After this manual review:

- add an isolated benchmark for the same brownfield scenario
- add one spec-driven scenario with a richer domain model and external consumer contract
