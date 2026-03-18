# User Research Semi-Isolated Benchmark Review

## Scope

This review summarizes the current **semi-isolated manual benchmark** evidence for `user-research`.

It does **not** claim automated isolated benchmark status. The run under review preserves:

- separate baseline and with-skill branches
- a copied `skill-under-test/SKILL.md`
- prompts and raw outputs per branch
- a fixed brownfield B2B/SaaS fixture

but the outputs were still authored in one reviewer context.

Important: this benchmark reviews the quality of the intermediate `research-plan` artifact. It does **not** claim that the full user-research quality gate has been satisfied or that evidence-backed personas already exist.

## Reviewed Artifact

| Artifact | Scenario | Notes |
|---|---|---|
| `problem-framing-handoff-manual-run-2026-03-17-seat-guest` | `seat-guest-management-problem-framing-handoff` | Preferred classic B2B/SaaS brownfield stress case |

## Contamination Review

This run is stronger than a loose manual review because:

- the prompts reference only the framing artifact and the skill under test
- the outputs do not reference repo structure, neighboring skills, templates, or local project instructions
- the comparison is anchored to one fixed scenario rather than a general subjective impression

This run is **not** fully isolated because the same reviewer authored both branches.

## Cross-Branch Review

| Dimension | Baseline | With skill | Judgment |
|---|---|---|---|
| discovery boundary | stays mostly in discovery, but points quickly toward requirements | keeps the work clearly in discovery and delays requirements until evidence exists | **Positive lift** |
| chosen direction | mentions guest vs seat controls, but the selected path is weakly preserved | keeps `guest-first coexistence` explicit as the thing being validated | **Positive lift** |
| non-goals | pricing and policy redesign remain mostly implicit | non-goals are explicit and govern the research scope | **Positive lift** |
| research questions | reasonable but broad | sharper, more decision-linked questions tied to coexistence and stakeholder pressure | **Positive lift** |
| evidence threshold | implied | explicit about what must be learned before `requirements-engineering` begins | **Positive lift** |

## What the Benchmark Shows

### 1. The skill adds value under deliberate routed invocation

Baseline can already produce a reasonable research plan. The with-skill delta is strongest on:

- preserving the chosen direction
- preventing brownfield scope drift
- making the evidence threshold before requirements explicit
- leaving a more auditable research plan for downstream lifecycle work

### 2. The skill is especially valuable in brownfield B2B/SaaS discovery

This scenario is harder than `team-invite` because the product already has a seat model, admin workarounds, and finance/procurement pressure. The skill helps keep the first release question narrow instead of reopening a broad admin-modernization program.

### 3. The evidence is stronger, but still not final-form

This benchmark is stronger than plain manual handoff review, but weaker than a true isolated run. It is enough to reinforce `review` status, not enough to justify `tested`.

## Current Judgment

`user-research` now has credible review-stage evidence that it is:

- stronger as a **routed discovery skill**
- particularly useful when an upstream `problem-frame` has already selected a likely direction
- valuable in classic B2B/SaaS brownfield discovery where scope drift is a real risk

## Next Required Evidence

1. run a true isolated benchmark or cross-reviewer execution drill on this same scenario
2. add downstream evidence showing how the resulting research outputs improve a later skill such as `requirements-engineering`
