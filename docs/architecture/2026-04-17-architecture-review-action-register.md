# Supporting Register: Prodcraft Architecture Review Action Register

> Date: 2026-04-17
>
> Status: execution support document, subordinate to the canonical architecture state bundle.
>
> Canonical architecture state now lives in:
> [`2026-04-18-prodcraft-architecture-state-bundle.md`](./2026-04-18-prodcraft-architecture-state-bundle.md)
>
> Historical synthesis source remains:
> [`2026-04-17-prodcraft-architecture-evolution-basis.md`](./2026-04-17-prodcraft-architecture-evolution-basis.md)
>
> Role of this document: translate the canonical state and historical review into sequenced implementation work without pretending that the whole review has already become accepted ADR policy.

## Why This Register Exists

The architecture state bundle and the historical review basis together established enough stable signal to stop debating in the abstract.
What remained was an execution problem:

- which work moves first
- which work must wait
- which work deserves a future ADR
- which work should be explicitly rejected or deferred

This register answers that execution question.

## Review-Derived Execution Principles

The following rules came directly out of the architecture review and govern this register:

1. Prefer **repo-native enforcement** before host-native enforcement.
2. Do not collapse high-semantic engineering judgment into cheap predicates.
3. Treat `Protocol/State` as a first-class asset, not as documentation overhead by default.
4. Distinguish repository governance improvements from downstream execution control improvements.
5. Use narrower future ADRs only when a concrete implementation move needs a durable contract.

## Current Topline Judgment

Prodcraft's highest-leverage weakness is not more skill authoring.
It is the weakness of the **downstream execution loop** relative to the strength of the **repository governance loop**.

That means the first work should not be:

- another broad architecture review
- a mass rewrite of `SKILL.md` files
- a host-specific hook-first implementation
- a public-surface redesign before the core control plane is clearer

The first work should be:

- identify which execution-critical rules can be promoted safely
- harden them first in repository-owned enforcement
- then bind that contract into host runtimes
- then reassess public export against the hardened core

## Action Register

| ID | Action | Why now | Output | Priority | ADR expectation |
|---|---|---|---|---|---|
| AR-01 | Build an enforcement promotion matrix for execution-critical rules | turns abstract agreement into a finite decision list; avoids blind hookification | one checked-in matrix mapping rules to signal quality, failure frequency, control surface, and recommended next mechanism | P0 | no ADR yet |
| AR-02 | Harden the first repo-native downstream execution checks | strongest architecture gap is the weak downstream execution loop | a small set of repository-owned checks covering the highest-signal execution-critical rules | P0 | maybe, if a new durable contract is introduced |
| AR-03 | Define host-binding adapter policy | prevents runtime-specific drift after repo-native hardening begins | a narrow design note or ADR describing how Claude/Codex/Gemini bindings relate to repo-owned contracts | P1 | likely yes |
| AR-04 | Review `.curated/` export through the four-layer lens | public skills may lose protocol/enforcement context in transit | a compatibility review of exported skills with downgrade, keep, or require-context decisions | P1 | maybe, if public export policy changes |
| AR-05 | Audit protocol artifacts for essential vs accidental complexity | first-class protocol/state does not mean every artifact is justified | a keep/simplify/remove review of current artifact contracts | P2 | no, unless a core artifact contract changes |

## Workstream 1: Enforcement Promotion Matrix

### Goal

Create a repository-owned decision table that answers:

- which rules fail often enough to matter
- which rules are materially costly when missed
- which rules can be checked mechanically with acceptable signal quality
- which rules must remain skill/review/evidence-led

### Why This Is First

Without this matrix, the team will oscillate between:

- over-hardening low-signal proxies
- under-hardening repeat offenders

The matrix is the concrete form of the control promotion law.

The measurement protocol for this workstream is defined in
[`ar-01-enforcement-promotion-measurement-protocol.md`](./ar-01-enforcement-promotion-measurement-protocol.md).
That companion document is governance guidance for building the matrix; it is
not a claim that any listed control has already been enforced.

### Required Fields

Each candidate rule should record at least:

- rule or discipline name
- current home (`skill`, `workflow`, `rule`, `validator`, `hook`, `CI`, `evidence`)
- failure mode
- observed evidence source
- failure frequency estimate
- cost if missed
- checkability (`high`, `medium`, `low`)
- Goodhart risk (`high`, `medium`, `low`)
- recommended next move
- recommended surface (`protocol`, `repo-native enforcement`, `host-native adapter`, `evidence only`)
- owner

AR-01 measurement must also record:

- evidence source class
- sample window
- false-positive risk
- false-negative risk
- friction cost
- decision owner
- review date

### Initial Candidate Set

The first candidate set should include at least:

- workflow entry requires valid `intake-brief`
- completion claims require fresh verification evidence
- mandatory route changes preserve explicit state handoff
- unsupported-flow and release-safety structural checks
- TDD-adjacent checks that are structural but not semantic
- review-adjacent checks that are structural but not semantic
- agent security controls: prompt injection, command safety, external reference trust, dynamic remote instruction prohibition, and secret/PII exposure

Expected evidence inputs for this first pass should come from real repository traces where possible, including:

- routed benchmark reviews and current-evidence snapshots under `eval/`
- skill findings documents
- execution observability summaries
- validator failures and existing repo-native guardrail hits

### Explicit Non-Goal

Do **not** pretend this matrix proves semantic adequacy.
Its purpose is to separate what can be hardened safely from what must remain judgment-heavy.

## Workstream 2: First Repo-Native Downstream Checks

### Goal

After the promotion matrix exists, implement the first small wave of repo-native checks that strengthen the downstream execution loop without triggering proxy gaming.

### Candidate First Wave

Only move rules from the matrix if they satisfy all three conditions:

- frequent enough to matter
- costly enough to justify friction
- checkable with acceptable signal quality

The likely first wave is:

1. workflow and handoff artifact presence checks
2. completion-claim freshness and proof-shape checks
3. a narrow set of structural release-safety checks

### Explicit Exclusions

This first wave should **not** attempt to enforce:

- "real TDD" as a semantic claim
- "real code review quality" as a semantic claim
- "good architecture" as a semantic claim

Those remain in the skill/review/evidence domain unless a much higher-signal mechanism appears later.

### Success Criteria

- the new checks reduce obvious false-completion or false-entry failures
- they do not create obvious busywork-only compliance
- they remain repository-owned and host-portable

## Workstream 3: Host-Native Adapter Policy

### Goal

Make it explicit how host-native bindings relate to repository-owned contracts.

The provisional policy is recorded in
[`ar-03-host-adapter-policy.md`](./ar-03-host-adapter-policy.md).
It is a design note, not an accepted ADR.

### Why This Is Not First

If host bindings are defined before the repo-native contract is clear, the repository will optimize around the first runtime it happens to integrate with.
That is architectural capture by the host.

### Questions The Policy Must Answer

- which repository contracts deserve a host-native adapter
- when should Claude hooks be used versus repo-native checks versus CI
- what is the equivalent adapter story for Codex and Gemini
- what behavior is allowed to remain host-specific
- what evidence must exist before a host-specific rule becomes part of the recommended path

### Expected Output

One of:

- a narrow design note if the policy remains provisional
- a narrow ADR if the adapter boundary becomes a durable repository contract

## Workstream 4: Public Surface Compatibility Review

### Goal

Establish a public portability landing zone, then review the current
`.curated/` surface skill by skill.

The coarse classification is now recorded in
[`schemas/distribution/public-skill-portability.json`](../../schemas/distribution/public-skill-portability.json).
The initial static review is recorded in
[`2026-04-24-curated-portability-review.md`](../distribution/2026-04-24-curated-portability-review.md).
Future live and skill-by-skill reviews should use the companion registry as the
landing zone for:

1. portable as-is
2. portable with explicit protocol/context caveats
3. should not be publicly exported in current form

### Sequencing

The landing zone and initial static review may proceed after the first
repo-native check proves the repository-owned path is viable.

Final public export decisions still depend on understanding which capabilities
are:

- pure knowledge units
- partial protocol units
- tightly coupled to repo-native enforcement or evidence scaffolding

If the hardened control plane is still unclear, a full skill-by-skill export
review will be noisy and unstable.

### Review Lens

For each exported skill:

- what value survives outside the full Prodcraft repository
- what hidden dependency on routing, state, or evidence is currently implied
- whether the current description overstates standalone robustness

## Workstream 5: Protocol/State Audit

### Goal

Protect the value of protocol/state without treating every artifact as sacred.

### Questions

- which artifacts are essential to cross-session continuity
- which artifacts merely mirror information already carried elsewhere
- which schemas are still contract-bearing
- which artifacts introduce governance overhead without corresponding decision value

### Expected Output

A keep/simplify/remove review for:

- artifact schemas
- templates
- workflow-required artifacts
- handoff contracts

## Deferred And Rejected Moves

### Deferred

- umbrella ADR for the entire architecture review
- major public surface redesign before core control hardening
- broad rewrite of lifecycle skills before control surfaces are clearer

### Rejected

- treating distribution as a fifth ontology layer
- replacing most skills with hooks/rules
- using cheap proxies as proof of semantic engineering quality
- assuming repository governance maturity equals downstream execution control

## Proposed Sequence

### Phase A — Decision Table

- complete `AR-01`
- confirm the first wave candidates

### Phase B — First Hardening Wave

- execute `AR-02`
- measure false-positive risk and compliance quality

### Phase C — Adapter Boundary

- execute `AR-03`
- keep repo-native contracts authoritative

### Phase D — Export Review

- execute `AR-04`
- classify `.curated/` skills by portability and hidden dependency

### Phase E — Protocol Simplification

- execute `AR-05`
- remove accidental complexity without deleting real state value

## What Future ADRs Should Capture

If future work reveals a durable contract change, the ADR should be narrow.

Likely future ADR candidates:

- enforcement promotion matrix becomes part of repository governance
- host-binding adapter boundary becomes a formal contract
- public export policy changes for protocol-dependent skills
- a core artifact contract is materially tightened or simplified

These should be independent ADRs.
They should not be backfilled into a giant philosophy ADR after the fact.

## Final Execution Judgment

The correct next move after the architecture review is not more model refinement.
It is to move from broad agreement to a controlled first hardening wave.

If this register is followed in order, Prodcraft should gain:

- stronger downstream execution control
- less host-specific architectural drift
- cleaner future ADR boundaries
- a more honest public export story
