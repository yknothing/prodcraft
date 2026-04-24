# Historical Source: Prodcraft Architecture Evolution Basis

> Date: 2026-04-17
>
> Status: retained as a historical source record, not the highest-level canonical architecture definition.
>
> Canonical architecture state now lives in:
> [`2026-04-18-prodcraft-architecture-state-bundle.md`](./2026-04-18-prodcraft-architecture-state-bundle.md)
>
> Role of this document: preserve the longer review synthesis, debate lineage, ADR process framing, and convergence path that fed the canonical state bundle.
> It is **not** itself an ADR, and it is no longer the top-level source of truth for architecture state.

## Purpose

Prodcraft has reached a point where local fixes are no longer enough.
The repository already contains:

- a lifecycle skill tree
- artifact schemas and workflow entry contracts
- repo-owned validators and QA evidence
- a public `.curated/` install surface
- explicit pressure to align better with modern harness engineering practice

That created a real architecture review question:

> What is Prodcraft actually becoming, where are its real control surfaces, and which parts now need stronger separation or stronger enforcement?

This document exists to answer that question with enough rigor to guide the next implementation phase.

## What This Document Is And Is Not

This document **is**:

- a review-grade synthesis of the multi-round architecture discussion
- a record of competing positions, corrections, and convergence
- the decision basis for prioritizing follow-on architecture work
- the place where the ADR process surrounding this discussion is made explicit

This document is **not**:

- a replacement for accepted ADRs
- a new accepted ADR
- a full implementation plan
- a claim that every statement below has already been converted into repository policy

The execution handoff from this historical review is tracked separately in:

- [`2026-04-17-architecture-review-action-register.md`](./2026-04-17-architecture-review-action-register.md)
- [`2026-04-18-prodcraft-architecture-state-bundle.md`](./2026-04-18-prodcraft-architecture-state-bundle.md)

## Review Method

The conclusions below were not derived from opinion alone.
They were grounded in:

- direct inspection of repository structure, validators, hooks, tests, and public export machinery
- inspection of local Claude Code package/runtime behavior
- review of current primary-source platform guidance from OpenAI, Anthropic, Claude Code, Cursor, and Windsurf
- repeated adversarial critique and correction rather than one-pass synthesis

## Repository Facts That Matter

As of this review:

- source lifecycle skills: `44`
- curated public install skills: `40`
- workflows: `6`
- personas: `7`
- rules files: `7`
- tests: `49`
- all active manifest skills use `evaluation_mode: routed`

Important context-economics distinction:

- repository total volume is **not** the same thing as runtime injected volume
- Anthropic's current skill guidance distinguishes metadata that is pre-loaded from `SKILL.md` and supporting files that are read on demand
- the real pressure point for Prodcraft is therefore not raw repository size alone, but the cumulative load of the entry path and downstream path a task actually activates

Key repository artifacts repeatedly referenced in the review:

- entry contract: [`CLAUDE.md`](../../CLAUDE.md)
- routing contract: [`skills/_gateway.md`](../../skills/_gateway.md)
- QA contract: [`skills/_quality-assurance.md`](../../skills/_quality-assurance.md)
- structural validator: [`scripts/validate_prodcraft.py`](../../scripts/validate_prodcraft.py)
- repo-native blocking guardrail: [`.githooks/pre-commit`](../../.githooks/pre-commit)
- repo-native scanner: [`scripts/hooks/no_magic_values_scan.py`](../../scripts/hooks/no_magic_values_scan.py)
- execution summary tooling: [`scripts/summarize_execution_observability.py`](../../scripts/summarize_execution_observability.py)
- runtime feedback loop: [`docs/observability/runtime-feedback-loop.md`](../observability/runtime-feedback-loop.md), [`.github/workflows/runtime-feedback-loop.yml`](../../.github/workflows/runtime-feedback-loop.yml)
- public distribution contract: [`schemas/distribution/public-skill-registry.json`](../../schemas/distribution/public-skill-registry.json), [`docs/distribution/public-skill-lifecycle.md`](../distribution/public-skill-lifecycle.md)

## External Inputs That Shaped The Review

The review repeatedly grounded itself in these primary external references:

- OpenAI: [Harness engineering](https://openai.com/index/harness-engineering/)
- OpenAI: [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- Anthropic: [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- Anthropic: [Skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Claude Code: [Hooks](https://code.claude.com/docs/en/hooks)
- Claude Code: [Memory / CLAUDE.md behavior](https://code.claude.com/docs/en/memory)
- Cursor: [Rules](https://docs.cursor.com/en/context/rules)
- Windsurf: [Cascade skills](https://docs.windsurf.com/windsurf/cascade/skills)

## Architecture Review Summary

### What Prodcraft Actually Is

Prodcraft is not best understood as only:

- a skill library
- a runtime harness
- a workflow engine
- a governance document set

The strongest current description is:

> Prodcraft is a mixed engineering-control system that co-locates knowledge, externalized protocol/state, enforcement mechanisms, and evidence contracts inside one repository.

That mixed nature is not itself the bug.
The real architecture pressure comes from two problems:

- the content types are not yet cleanly separated enough
- the consumer surfaces do not all receive the same level of protocol and enforcement support

The deeper form of that pressure is:

> Prodcraft's central architecture challenge is to let knowledge, state, constraints, and evidence move across different consumer surfaces with as little distortion as possible.

### Why The Debate Mattered

Early positions got important things right but still missed the architecture center of gravity.

- one side correctly saw that critical constraints cannot stay purely probabilistic
- another side correctly saw that not all engineering judgment can be safely reduced into runtime predicates
- the key missing insight was that Prodcraft's distinctive value is not only guidance, but also externalized engineering state and handoff structure

The debate therefore shifted from:

- `skills vs hooks`
- `knowledge vs harness`

to a more accurate question:

> Which kinds of content live in Prodcraft, which mechanisms should deliver them, and where are the control loops actually weak?

## Debate Process Overview

The discussion produced value because each round corrected a real overreach from the previous one.

### Debate Sequence

1. **Broad initial analysis**
   - identified layered design pressure
   - correctly emphasized deterministic guardrails
   - did not yet isolate the repository's deepest tension

2. **First hard critique**
   - correctly pushed the runtime enforcement problem much harder
   - correctly raised context economics and open-loop control risk
   - overreached by collapsing too much of the system toward hooks/rules

3. **First synthesis**
   - recovered the missing `Protocol/State` layer
   - introduced Goodhart risk as the hard boundary on enforcement expansion
   - reframed the problem as a multi-layer control system

4. **Second critique**
   - correctly separated repository governance from downstream execution
   - correctly surfaced public distribution as a real consumer tension
   - overreached by promoting distribution into a new ontology layer

5. **Second synthesis**
   - corrected distribution into a cross-cutting consumer-surface concern
   - clarified the dual-loop control problem
   - risked drifting into meta-analysis overhead

6. **Final convergence**
   - produced stable common ground strong enough to guide implementation
   - reduced the remaining disagreement to scope, sequencing, and boundary precision rather than first-principles conflict

## Existing ADR Lineage

This architecture review builds on existing accepted ADRs.
It does not replace them.

### ADR-001

[`ADR-001`](../adr/ADR-001-execution-observability-envelope.md) established execution observability as a first-class cross-cutting contract.

In the architecture model used by this review, `ADR-001` primarily strengthens:

- `Evidence`
- the repository governance loop

### ADR-002

[`ADR-002`](../adr/ADR-002-cross-phase-course-corrections.md) established `course-correction-note` as the canonical cross-phase correction artifact.

In the architecture model used by this review, `ADR-002` primarily strengthens:

- `Protocol/State`
- cross-session and cross-phase continuity

### ADR Process Status For This Review

This review produced architecture conclusions that are strong enough to shape implementation.
It did **not** automatically promote those conclusions into a new accepted ADR.

That distinction is deliberate.

- `ADR-001` and `ADR-002` remain accepted repository commitments.
- The conclusions in this document are architecture basis statements.
- Any future ADR derived from this review should be narrower and implementation-backed, not a bulk restatement of the whole debate.

### Decision Candidates Produced By This Review

The following candidate decisions were explicitly evaluated during the review.

| Candidate | Current status in this review | Why |
|---|---|---|
| Use `Knowledge / Protocol / Enforcement / Evidence` as the main explanatory model | **Accepted as architecture basis** | strong enough to guide follow-on work, but still a basis statement rather than a new umbrella ADR |
| Distinguish repository governance loop from downstream execution loop | **Accepted as architecture basis** | materially changes prioritization and avoids a false sense of control |
| Treat distribution as a fifth ontology layer | **Rejected** | distribution is a consumer-surface concern, not a content type |
| Bulk-convert most disciplines into hooks/rules | **Rejected** | Goodhart risk and semantic loss make this unsafe as a general rule |
| Use repo-native enforcement as the first hardening layer, with host-native bindings as adapters | **Accepted as architecture basis** | best fit for portability and repository-owned control |
| Create a new umbrella ADR that restates the full review | **Rejected for now** | too broad, too early, and not implementation-backed |
| Create narrower ADRs once concrete hardening moves are selected | **Deferred / future ADR path** | appropriate once individual implementation moves are specified and evidenced |

## Stable Architecture Conclusions

The following conclusions are strong enough to treat as current architecture basis.

### 1. Prodcraft Is A Mixed System

Prodcraft mixes multiple kinds of engineering control in one repository:

- knowledge
- protocol/state
- enforcement
- evidence

This is the right starting point for all future refactoring discussions.

### 2. Four Content Layers Best Explain The Repository

The least misleading current content model is:

#### Knowledge

Methods, heuristics, anti-patterns, and judgment frameworks.

Examples:

- `tdd`
- `systematic-debugging`
- `code-review`
- gotchas and supporting references

#### Protocol

Externalized state, handoff objects, artifact contracts, and workflow routing contracts.

Examples:

- `intake-brief`
- `course-correction-note`
- `verification-record`
- workflow entry requirements
- artifact and handoff contracts

#### Enforcement

Mechanisms that can mechanically block, warn, validate, or reject.

Examples:

- `validate_prodcraft.py`
- `.githooks/pre-commit`
- `no_magic_values_scan.py`
- repo-native checks
- future host-native bindings

#### Evidence

Artifacts that prove, challenge, or revise the system's claims after execution.

Examples:

- isolated benchmarks
- routed handoff reviews
- findings notes
- execution observability summaries
- pressure-test artifacts

### 3. Distribution Is A Cross-Cutting Consumer-Surface Concern

Distribution matters, but not as a content layer.

The right question is not "what new layer is distribution?"
The right question is:

> which consumer surfaces receive which parts of the system, and what gets lost in transit?

Current relevant surfaces are:

- repository-internal authoring and governance
- runtime execution in a host environment
- external install and upgrade through `.curated/`

This matters because a skill can remain valuable as a knowledge unit outside the full repository while losing protocol and enforcement context.

### 4. Protocol/State Is A First-Class Asset

Prodcraft's distinctive value does not come only from instructions.
It also comes from recording engineering state outside the model:

- chosen route
- open assumptions
- correction triggers
- verification boundaries
- downstream consumer intent

Without this layer, the system collapses toward:

- transient model memory
- transcript archaeology
- ad hoc reconstruction of past reasoning

For production-grade multi-step work, that is not robust enough.

### 5. Enforcement Must Expand Selectively, Not Blindly

The review converged on a usable promotion rule:

> frequent failure + meaningful cost + stable checkability -> stronger protocol and/or stronger enforcement

This is the working **control promotion law**.

But the review also established an equally important negative rule:

- not every valuable engineering discipline can be reduced safely into a cheap predicate
- weak proxies create Goodhart drift

So the goal is not maximal hookification.
The goal is selective hardening without destroying semantic quality.

### 6. Prodcraft Has Two Distinct Control Loops

#### Repository governance loop

This loop governs Prodcraft itself.

Current state: **weak closed loop**

Evidence includes:

- structural validation
- curated parity validation
- repo-native pre-commit blocking
- benchmark and findings discipline
- monthly runtime observability summary path

#### Downstream execution loop

This loop governs the engineering work Prodcraft is trying to shape.

Current state: **near-open loop**

Evidence includes:

- intake, TDD, and verification disciplines still depend primarily on skill text and workflow contracts
- hard runtime blocking remains narrow
- host-native hooks are not yet a meaningful part of the operational control plane

This distinction is critical.
Repository maturity must not be mistaken for downstream execution control.

### 7. Discoverability Is Internally Deprioritized But Externally Still Live

Inside Prodcraft's lifecycle spine:

- routed invocation is the primary contract
- discoverability has been intentionally downgraded as a primary maturity gate

Outside the full repository context:

- discoverability still matters
- exported skills do not bring the whole routing and enforcement plane with them
- public compatibility remains a live architecture tension

So the right conclusion is:

- discoverability is no longer the core internal control question
- discoverability remains unresolved for external consumption

## Disagreements Preserved By This Review

This document does not flatten all disagreement into fake consensus.
The following tensions remain real and should stay visible.

### 1. How Fine The Architecture Model Needs To Be

One side kept pushing toward more exact axes and finer decomposition.
Another side argued that beyond a point the analysis becomes self-consuming.

Current review judgment:

- four content layers are worth preserving
- dual-loop control is worth preserving
- distribution should be remembered as a consumer-surface concern
- further abstraction refinement is not the current bottleneck

### 2. How Strictly Protocol Should Be Separated From Enforcement

The review settled on a bounded compromise:

- protocol specs and enforcement mechanisms should not be collapsed conceptually
- some artifacts, such as JSON Schema, are intentionally shared interfaces between them

That means future design work should distinguish:

- `protocol spec` -- the object, state, or handoff contract itself
- `enforcement mechanism` -- the validator, hook, CI check, or rule runner that consumes the contract
- `semantic adequacy evidence` -- the eval, review, or findings evidence that tells us whether a valid object is actually sufficient in practice

Example:

- `schemas/artifacts/intake-brief.schema.json` expresses a `protocol spec`
- the artifact-schema checks inside `scripts/validate_prodcraft.py` are an `enforcement mechanism`
- routed benchmarks, findings, and review artifacts under `eval/00-discovery/intake/` provide `semantic adequacy evidence`

### 3. Whether More Meta-Analysis Is Still Justified

The late rounds made the diminishing-return pattern visible.

Current review judgment:

- this debate has already produced enough stable signal to guide action
- future analysis should now be implementation-coupled, not another open-ended abstract loop

## Explicitly Rejected Or Downgraded Positions

The following positions were examined and should **not** be carried forward as architecture guidance:

- "Prodcraft is just a governance framework pretending to be skills"
- "most skills should be replaced by hooks/rules"
- "distribution should become a fifth architecture layer"
- "a passing proxy check proves a high-semantic engineering discipline is satisfied"
- "repository governance maturity means downstream execution is already controlled"
- "the right next move is another round of broad abstract architecture debate"

## What This Review Makes Mature Enough For Action

The following are mature enough to guide execution priority now:

### Priority 1: Strengthen the downstream execution loop with repo-native enforcement first

Start with rules that are:

- high-frequency failure points
- materially costly when missed
- stable enough to check without collapsing into fake compliance

Candidate early targets:

- required entry artifacts and workflow-gating evidence
- completion-claim evidence freshness
- a narrow set of structural safety and release-safety checks

Why repo-native first:

- more portable across host agents
- keeps the contract repository-owned
- avoids overfitting the first hardening step to one runtime

### Priority 2: Add host-native bindings as adapters, not as the source of truth

Once the strongest repo-native checks are clear, bind them into host environments such as:

- Claude Code hooks
- Codex-specific workflow controls
- future Gemini-compatible bindings

These should adapt the repository contract to the host.
They should not replace it.

### Priority 3: Reassess the public `.curated/` surface through the new architecture lens

For each exported skill, ask:

- does it retain real value when detached from the full Prodcraft protocol layer?
- is it genuinely a portable knowledge unit, or does it depend on repo-local routing and evidence structure?
- does the public description overpromise robustness that only exists inside the full repository contract?

## Questions That Must Continue To Guide Follow-On Work

1. Which currently soft rules fail often enough in real work to justify promotion into stronger enforcement?
2. Which protocol artifacts are essential for continuity, and which are governance overhead that should be simplified?
3. Which exported public skills still make sense when detached from internal routing and evidence scaffolding?
4. Where are we measuring repository hygiene but not downstream engineering behavior?
5. Which current "proof of compliance" signals are vulnerable to Goodhart drift?

## What Future ADRs Should And Should Not Do

This review intentionally stops short of creating a new umbrella ADR.

Future ADRs should be:

- narrower
- implementation-backed
- specific to one architecture move or contract change

Good future ADR candidates might include:

- a repo-native enforcement matrix for execution-critical rules
- a host-binding adapter policy for Claude/Codex/Gemini
- a public-surface compatibility rule for exported skills that depend on internal protocol/state

Future ADRs should **not** simply restate this entire review as a broad philosophy decree.

## Final Review Judgment

Prodcraft's next evolution should not be driven by a desire to become "more like a runtime" or "more like a skill pack."

It should be driven by a clearer separation of:

- knowledge
- protocol/state
- enforcement
- evidence

while preserving visibility into:

- repository governance control
- downstream execution control
- public consumer surfaces

The hard part is not writing more engineering wisdom into the system.
The hard part is preserving the integrity of that wisdom, its state objects, its constraints, and its proof signals as they move across those surfaces.

The immediate next move is not another abstract architecture round.
It is to use the control promotion law to harden the downstream execution loop without destroying the high-semantic judgment that makes Prodcraft valuable.
