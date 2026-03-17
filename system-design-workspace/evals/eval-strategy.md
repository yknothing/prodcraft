# System Design QA Strategy

## Goal

Evaluate whether `system-design` is useful as a routed architecture skill that consumes reviewed requirements and preserves upstream boundaries instead of silently inventing architecture facts.

## Why Start with Routed Handoff

`system-design` sits on the core lifecycle spine:

- `requirements-engineering` defines what must be preserved
- `system-design` decides the high-level structure
- downstream skills such as `api-design` and `task-breakdown` inherit its choices

Because of that position, the first QA question is not trigger discoverability. The first QA question is whether architecture handoff preserves:

- phase boundaries
- brownfield coexistence constraints
- unresolved upstream questions
- downstream handoff readiness

## Initial Evaluation Mode

The first evaluation is a **manual routed handoff review** using a brownfield modernization scenario.

Why manual first:

- the user explicitly requested evaluation without relying on `claude` CLI
- the highest-risk failure here is contract drift between requirements and architecture, which can be reviewed directly

This manual evidence is supplemental. It does not replace future isolated automated benchmarks.

## Scenario

- `access-review-modernization-requirements-handoff`

Input artifact:

- reviewed requirements document for a brownfield access-review modernization effort

## Assertions

1. **stays-in-architecture-phase**
   - output remains at component boundaries, architectural style, interaction patterns, and ADR-level decisions
   - it does not collapse into API schema, implementation tasks, or rollout choreography

2. **preserves-brownfield-coexistence**
   - release 1 coexistence with the legacy module is preserved as an architectural constraint
   - the design does not assume a big bang rewrite or same-day cutover

3. **preserves-upstream-open-questions**
   - unresolved tenant-contract, history-retention, and sync-semantics questions remain visible as architectural questions or assumptions

4. **maps-drivers-to-structure**
   - component boundaries and communication patterns can be traced back to requirements or architectural drivers

5. **prepares-downstream-handoff**
   - the output is shaped for `api-design`, `data-modeling`, or `task-breakdown`

## Pass Standard

Treat a run as strong evidence if:

- it passes all five assertions, or
- it clearly outperforms a generic baseline on brownfield boundary preservation, unresolved-question handling, and downstream handoff shape

## Next QA Step

After this manual review:

- add an isolated explicit benchmark for the same scenario
- add at least one spec-driven scenario where `spec-doc` and `domain-model` are present
