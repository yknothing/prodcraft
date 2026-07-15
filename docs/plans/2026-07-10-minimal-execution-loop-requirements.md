# Minimal Execution Loop Requirements

## Required Artifact

- artifact: `requirements-doc`
- schema_version: `requirements-doc.v1`
- status: `approved`
- source_language: `zh-Hans`
- artifact_record_language: `en`
- user_presentation_locale: `zh-Hans`

## Source Context

- primary upstream artifact: approved Direction 2 problem frame from the 2026-07-10 repository review
- supporting upstream artifacts:
  - `README.md`
  - `docs/architecture/2026-04-18-prodcraft-architecture-state-bundle.md`
  - `docs/architecture/2026-04-17-architecture-review-action-register.md`
  - `docs/plans/architecture-evolution/2026-04-24-ar-01-enforcement-promotion-matrix.md`
- approved direction: strengthen the repository-owned downstream execution loop with a minimal, host-agnostic state and evidence contract
- extension constraint: preserve a credible path toward a future standalone runtime without implementing that runtime in this slice
- quality constraint: use adversarial peer review and fresh repository evidence before completion is claimed

## Problem Statement

Prodcraft can validate repository structure, skill metadata, workflow entry rules, artifact schemas, and public export parity, but it does not yet have one repository-owned artifact that binds a real work item to its approved route, current execution state, required artifacts, completion claim, and accepted verification evidence.

As a result, the repository governance loop can be green while the downstream execution loop remains incomplete. A host or agent can lose route state, reuse stale evidence, skip a required artifact, or claim completion without a route-bound proof record. The first implementation slice must close that gap without pretending to automate semantic engineering judgment or creating a standalone orchestrator.

## Users And Needs

| User | Need |
|---|---|
| Engineering operator | Know whether a work item is routed, executing, blocked, verified, or complete and why. |
| Agent runtime adapter | Consume one host-agnostic contract instead of reconstructing lifecycle state from conversation text. |
| Reviewer or approver | Reject illegal transitions, missing gate artifacts, stale evidence, and premature completion claims. |
| Prodcraft maintainer | Evolve schemas and validators without breaking existing `verification-record.v1` consumers. |
| Public skill consumer | Understand which guarantees survive a curated-only install and which still require repository context. |

## Requirements

| ID | Priority | Requirement | Source | Acceptance criteria |
|---|---|---|---|---|
| MEL-P0-01 | P0 | The system shall define separate, versioned `route-decision` and `execution-state` artifacts. The declared approved route decision is the authority for route identity, declared route revision, workflow composition, non-empty focus sequence whose first phase equals `entry_phase`, and complete reviewer-declared obligations for each lifecycle transition or workflow-phase checkpoint; mutable execution state may bind evidence but may not redefine those obligations. Each obligation declares whether it requires presence, structural validation, or explicit approval assurance. Gate authority requires the canonical current execution-state locator and an operator-supplied pinned route digest outside the writable control bundle. Strict terminal authority additionally requires an operator-pinned digest of the final completion projection. Historical snapshots may validate structurally but cannot authorize current completion. | Direction 2; adversarial review | MEL-AC-01, MEL-AC-02, MEL-AC-03, MEL-AC-05 |
| MEL-P0-02 | P0 | The system shall encode one canonical work-item transition matrix: `received -> routed -> gated -> executing`; `executing -> blocked | completion_claimed | rerouted`; `blocked -> executing | rerouted`; `completion_claimed -> verified | rejected`; `rejected -> gated | rerouted`; `verified -> completed`. `completed` and `rerouted` are terminal for a route revision. | Architecture state bundle; blocked-state requirement | MEL-AC-04 |
| MEL-P0-03 | P0 | The system shall reject execution state whose route ID, route revision, route digest, workflow composition, or artifact-obligation bindings are missing, stale, or inconsistent with the referenced approved route decision and operator pin. Deleting an obligation from mutable execution state must never make a gate pass. Every authoritative lifecycle or phase gate advancement, not only completion, requires pin equality; no-pin validation is structural-only. | Gate-bypass threat | MEL-AC-03, MEL-AC-05 |
| MEL-P0-04 | P0 | The system shall model lifecycle state and workflow position as a product automaton. Execution state carries lifecycle transitions, phase events with explicit `entered`/`exited` checkpoints, and artifact-binding activations in one contiguous global `recorded_sequence`; current state revision equals the highest sequence. Replaying from lifecycle `received` at sequence 0 derives the state before each record. Routed/gated/new-reroute states may have no phase events and no cursor; once the first phase event exists, the cursor is required and derived. Phase events are legal only when the immediately preceding derived lifecycle state is `executing`; the first phase entry occurs after `gated -> executing`, phase movement pauses while blocked, and no phase event is legal before execution, after completion claim, during rejection/gating, or after a terminal state. Final-phase exit is representable without an out-of-range cursor and is required before `executing -> completion_claimed`. Route obligations must activate before their gate sequence. | Intake, workflow, product-order, and phase-gate contracts | MEL-AC-04, MEL-AC-05 |
| MEL-P0-05 | P0 | The system shall model append-only completion attempts. Each attempt freezes an immutable claim payload, claim cut sequence, claim digest, preterminal as-of projection digest, work ID, route ID/revision/digest, content-addressed Git work snapshot, and a preclaim verification commitment containing the verification-record and evidence snapshot digests. Claim digest is computed from a projection excluding both derived digests; the completion basis is computed afterward and may contain the claim digest while excluding its own field. A completion binding copies the commitment and adds the exact allowed terminal transition records. A rejected attempt remains reconstructable by cut sequence, and a later attempt receives a new revision and fresh verification/evidence identities after the lifecycle returns through `gated -> executing`. The binding must not reinterpret legacy `claim_scope` as route identity. | Completion-integrity, ordering, retry, and compatibility requirements | MEL-AC-06, MEL-AC-08 |
| MEL-P0-06 | P0 | Strict validation shall invalidate prior completion authority after route revision, reroute, source revision, governed work-content digest, completion-attempt payload, preterminal execution projection, referenced verification-record content, authorization-affecting approval/validator evidence content, or other execution payload changes. Every authorization-affecting file excluded from the governed work digest must be covered by a content digest, and the final attempt/commitment/binding/terminal-record projection must match an operator-supplied completion digest outside the writable bundle. The additive completion envelope shall bind every verification evidence ID to a local content snapshot without reinterpreting legacy `verification-record.v1` Git refs, opaque evidence descriptions, or evidence-ID fields as paths. Advancing from `verified` to `completed` changes the terminal projection and requires a new completion pin. Validation shall enforce the declared `work captured <= evidence captured <= verified` ordering, while documenting that self-reported timestamps are not trusted clocks, and shall compare the bound work snapshot with the live repository state when authorizing completion. | Replay, freshness, retry, circularity, and compatibility threats | MEL-AC-07, MEL-AC-08 |
| MEL-P0-07 | P0 | The system shall preserve existing `verification-record.v1`, workflow, and public-skill consumers; stricter route and execution validation must be additive and explicitly invoked rather than silently changing legacy semantics. | Compatibility constraint | MEL-AC-08 |
| MEL-P0-08 | P0 | The contract and validator shall remain host-agnostic, deterministic, local, and free of network, model, database, or external-skill dependencies. Strict artifacts shall use one reserved, non-symlink canonical control root inside the governed Git root; strict validation shall reject terminal authority from other locations. The versioned work-snapshot algorithm shall use config-independent canonical path/type/mode/content records, hash symlink targets without following them, reject blocking or unsupported special files, fail closed on dirty/unverifiable submodules, and identify its algorithm and scope policy. Files under the reserved control root are not governed implementation content and every authorization-affecting control file is separately content-bound. | Prodcraft architecture, path, and self-hash boundary | MEL-AC-09 |
| MEL-P0-09 | P0 | Repository and public documentation shall distinguish repository structural guarantees, strict execution-state guarantees, semantic review, and curated-only guidance so that no surface overclaims a closed execution loop. | Public-export truth boundary | MEL-AC-10 |
| MEL-P0-10 | P0 | The architecture shall preserve an extension seam for a future standalone runtime to persist state, append versioned events, schedule work, and enforce approvals without changing the core lifecycle vocabulary or evidence semantics. | Approved Direction 3 constraint | MEL-AC-11 |
| MEL-P0-11 | P0 | The completed slice shall receive independent adversarial review covering architecture, implementation integrity, compatibility, silent failure, security, and evidence honesty, with no unresolved P0/P1 findings. | User acceptance constraint | MEL-AC-12 |
| MEL-P1-01 | P1 | The canonical validator shall validate route-decision and execution-state shape/structural semantics from the existing artifact-instance surface and shall provide a distinct execution-authorization mode requiring the canonical state path and operator route pin. Terminal mode additionally requires the operator completion pin; without it a valid terminal bundle may report only a non-authoritative candidate digest. Authority mode exits zero only for machine-distinct `gate-authorized` or `terminal-authorized` outcomes; structural-only, candidate-only, missing-pin, historical, non-canonical, and invalid results exit non-zero. | Operator usability and silent-failure boundary | MEL-AC-13 |
| MEL-P1-02 | P1 | The artifact registry, manifest artifact flow, templates, relevant skills, and tests shall describe one consistent producer/consumer and lifecycle contract. | Repository governance | MEL-AC-14 |
| MEL-P1-03 | P1 | Documentation shall include a migration and versioning policy that explains legacy mode, strict execution-state mode, and the boundary at which a future runtime would take ownership. | Compatibility and Direction 3 | MEL-AC-15 |
| MEL-P1-04 | P1 | Verification shall include focused schema/contract tests, obligation-deletion, same-ID/new-revision, invalid-transition, post-verification mutation, reroute replay, mismatched-evidence, curated-surface checks when affected, and the full repository validator/test suite. | Acceptance depth | MEL-AC-16 |
| MEL-P1-05 | P1 | Public export validation shall prove installed runtime loadability, not only metadata parity: every flattened skill must retain valid frontmatter and description bounds, and every packaged relative reference must resolve after export. Existing broken cross-phase references discovered during this review are in scope for repair. | Public compatibility and silent-failure evidence | MEL-AC-10, MEL-AC-14, MEL-AC-16 |

## Acceptance Criteria Set

### MEL-AC-01 — An approved route is independently authoritative

Given an approved route decision, when it is read without execution state, then it exposes the work ID, route ID, declared revision, canonical content digest, workflow composition, and complete reviewer-declared artifact obligations keyed by lifecycle transition or phase checkpoint with an explicit assurance level. Every strict gate requires an operator-supplied pinned digest equal to the route digest; changing obligations and recomputing the writable route file cannot preserve authority without that external pin. Terminal authority additionally depends on the completion pin defined by MEL-AC-06.

### MEL-AC-02 — Valid execution state is representable and inspectable

Given a routed work item with a valid approved route decision, when the conforming execution state at the canonical current locator is validated and read without conversation history, then the validator accepts it and the work identifier, route binding, workflow cursor/checkpoint, lifecycle state, artifact bindings, lifecycle history, phase-event history, block reason if any, completion attempts, and current completion boundary are explicit. An archived state can be inspected but cannot authorize a current terminal claim.

### MEL-AC-03 — Mutable state cannot weaken its approved route

Given the canonical current execution-state instance omits an approved obligation, changes the workflow, uses an old route revision or digest, reuses state after reroute, references a route whose recomputed digest differs from the operator pin, or attempts any authoritative gate advancement without the pin, when strict validation runs, then validation fails or returns structural-only without advancement authority. An empty or reduced mutable obligation list cannot pass by construction. Direct validation of an internally consistent historical pair is reported as historical structural validity, never as current gate or terminal authority.

### MEL-AC-04 — The canonical state machine is enforced

Given a routed or gated state before workflow focus begins, then an empty phase-event list with no cursor is valid. Given lifecycle transitions, phase events, and artifact-binding activations whose combined `recorded_sequence` has a duplicate, gap, reordering, current-revision mismatch, cursor contradiction, or invalid product-state window, validation fails. Phase events before `gated -> executing`, while blocked/rejected/gated, after completion claim, or after terminal state fail; phase events may resume only after `blocked -> executing`. Exiting the final phase is valid and leaves the cursor at that phase with checkpoint `exited`; every required binding must have a lower sequence than the gate it authorizes.

### MEL-AC-05 — Unsatisfied route obligations cannot be crossed

Given a route-decision obligation required for a traversed lifecycle transition or reached phase checkpoint, when its execution-state binding is absent, points to the wrong artifact type, references a missing artifact, or does not meet the declared assurance level, then execution-state validation fails and identifies the obligation and gate. `structural_valid` requires a recorded validator identity/version/check set plus a successful result/evidence reference and revalidation now; `approval_accepted` additionally requires an accepted approval reference bound to the subject and approval-record digests. The validator recomputes every referenced digest but does not claim that structural validity proves semantic quality or that an approval is authentic outside the pinned route boundary, repository review, and source control.

### MEL-AC-06 — Completion requires an explicit additive binding

Given an execution state declared as `verified` or `completed`, when its current immutable completion attempt, verification commitment, claim cut sequence, reconstructed as-of basis digest, completion binding, verification-record digest, terminal-transition record digests, operator completion pin, or referenced `verification-record.v1` is absent, rejected, authorizes no completion claim, contains failed checks, retains unverified scope, or disagrees with the bound claim/work/route/revision/digest, then validation fails. A rejected attempt remains reconstructable history and cannot be overwritten by a retry. Validation does not derive route identity from `claim_scope`, and a binding authorizes no terminal metadata mutation beyond the operator-pinned projection.

### MEL-AC-07 — Replay and post-verification mutation are detected

Given previously accepted completion evidence, when the route revision or pinned route digest changes, the work item is rerouted, the Git revision or governed content digest changes, the current attempt or its preterminal execution projection changes, the verification/approval/validator evidence content snapshot changes, coordinated in-bundle digests are recomputed, another execution payload changes, or declared evidence timestamps predate the work snapshot, then the original completion pin no longer authorizes the result. Every verification evidence ID has exactly one additive local snapshot binding. Advancing from `verified` to `completed` requires approval of the new final projection. A later retry uses a new attempt revision, verification record identity, evidence IDs, and completion pin.

### MEL-AC-08 — Existing consumers remain valid

Given an existing valid `verification-record.v1` instance and existing workflow files, when the current legacy validators run without route-decision or execution-state instances, then their previous valid behavior remains valid and `claim_scope` retains its existing free-text meaning.

### MEL-AC-09 — Validation is portable and deterministic

Given the checked-in repository and its documented Python dependencies, when strict validation runs twice against the same canonical control bundle, operator route pin, terminal-only completion pin, and live Git work state, then it produces the same result without network, model, database, or host-specific calls. Moving the current execution state outside its canonical control locator removes terminal authority. Top-level, intermediate, final, POSIX, Windows-drive, UNC, backslash, symlink, special-file, file-mode, Git environment/config/index, and submodule cases have deterministic fail-closed outcomes, and control-artifact writes do not create a work-digest self-cycle.

Given route revision `N` ends in `rerouted`, when revision `N+1` becomes current, then the prior state is content-addressed under the canonical history locator, the new route binds its predecessor, the replacement live state binds the archived rerouted state and begins a new route-scoped `received -> routed` history, selector replacement is same-filesystem atomic, and a new operator pin is required. The archived pair remains inspectable but never gate- or terminal-authoritative.

### MEL-AC-10 — Guarantee levels are honest

Given the README, architecture document, relevant skill guidance, curated metadata, and a freshly generated flattened install, when reviewed and validated together, then they do not imply that schema validity proves semantic quality, that legacy mode has strict execution guarantees, or that curated-only guidance provides repository enforcement; every exported skill frontmatter loads and every packaged relative reference resolves.

### MEL-AC-11 — Direction 3 remains possible without premature implementation

Given the architecture document, then it explicitly defines snapshot versus event-log authority, a versioned future event envelope, monotonic aggregate revision, idempotency key and optimistic-concurrency boundary, ports for persistence/event append/scheduling/approval/host integration, stable Direction 2 contracts, deferred Direction 3 decisions, and the rule for rebuilding snapshots from events. Runtime services, databases, daemons, and public APIs remain deferred.

### MEL-AC-12 — Adversarial review is dispositioned

Given the final diff and fresh verification evidence, when independent reviewers attempt to falsify architecture consistency, obligation completeness, compatibility, failure behavior, security, and completion claims, then all P0/P1 findings are fixed or explicitly block completion.

### MEL-AC-13 — Invalid instances are actionable

Given an invalid route-decision or execution-state JSON file, when `python scripts/validate_prodcraft.py --artifact-instance <path>` runs, then it exits non-zero and reports the artifact path plus a specific schema or structural-replay violation. Given a structurally valid but non-authoritative state, generic artifact inspection may succeed but emits no authority result; `--authorize-execution-state` exits non-zero. Only current route-pinned state can return `gate-authorized`, and only a terminal state matching both pins can return `terminal-authorized`.

### MEL-AC-14 — Repository contracts stay aligned

Given the artifact registry, manifest, templates, skills, exporter, curated tree, and validator, when repository contract tests run, then all surfaces agree on artifact names, schema versions, producers, consumers, required fields, state vocabulary, transition matrix, validation command, flattened relative references, and installed runtime loadability.

### MEL-AC-15 — Compatibility modes are documented

Given an existing adopter, a strict-mode adopter, and a future runtime implementer, when each reads the architecture document, then each can determine which guarantees apply, what changes are required, and which compatibility boundary must not be crossed silently.

### MEL-AC-16 — Verification is proportional and complete

Given the final implementation, when acceptance runs, then focused route/execution tests, both authority-pin mismatches, a missing terminal completion pin, a coordinated verification-commitment/claim/basis/binding rewrite against the original completion pin, digest/semantic single-snapshot consistency, obligation deletion, frozen-field mutation, retry, path/symlink/mode/special-file/submodule, Git-config/replace-ref independence, bounded Git-command failure, artifact registry, manifest/workflow, flattened curated reference/loadability, canonical validator, and the full discovered unit test suite all pass on the final work state.

## Non-Functional Requirements

- **Compatibility:** No existing artifact schema version is redefined incompatibly. New strict guarantees use additive artifacts and explicit validation paths.
- **Determinism:** Identical local inputs produce identical validation outcomes.
- **Failure semantics:** Missing, malformed, stale, mismatched, replayed, or rejected route/evidence state must not be converted into warnings for gated or terminal transitions.
- **Integrity boundary:** A digest and canonical current locator detect accidental, partial, or stale mutation but are not authenticity or anti-tamper mechanisms against an actor that can rewrite the entire control bundle and its repository history. Approval authenticity and historical monotonicity remain repository review and source-control responsibilities in Direction 2.
- **Security:** The top-level strict artifact and every reference are confined by canonical realpath to the governed Git/control roots. Validation rejects URLs, absolute POSIX paths, Windows drive/UNC forms, backslashes, traversal, symlink components/targets, unsupported special files, and referenced commands; it never fetches or executes evidence.
- **Usability:** Error messages identify the file and violated invariant rather than returning a generic invalid result.
- **Maintainability:** Lifecycle vocabulary, phase-event rules, obligation assurance levels, and transition rules have one canonical definition that tests and validators consume or verify for parity.

## Assumptions Requiring Review

- The first slice will use checked-in JSON route-decision and execution-state artifacts plus the local validator as its authoritative implementation surface.
- The route-decision snapshot is authoritative in Direction 2. Execution state carries an append-only transition history inside a revisioned snapshot; a separate event store remains Direction 3.
- The canonical current execution-state path acts as Direction 2's current-authority selector. A single snapshot cannot cryptographically prove that prior revisions were never rewritten; Git review remains the historical anchor.
- Workflow phase events advance independently while the work-item lifecycle remains `executing`; explicit enter/exit checkpoints do not create self-loop lifecycle transitions.
- Strict-mode control files live under `.prodcraft/artifacts/<work_id>/`; governed source or deliverable content placed there is outside the work snapshot by policy and must not be treated as implementation evidence.
- Direction 2 can prove an approval binding is explicit and content-bound, but approval authenticity and semantic adequacy remain repository review responsibilities.
- Git work-snapshot identity consists of the current revision plus a deterministic content digest when the worktree is dirty. The exact canonicalization algorithm is an architecture decision and must include relevant untracked artifacts or declare their exclusion explicitly.
- Semantic adequacy remains review-led. The validator enforces bindings, transition integrity, and evidence shape only.
- Strict mode is opt-in for existing consumers until a separately approved migration changes workflow entry requirements.

## Preserved Non-Goals

- No standalone service, daemon, database, scheduler, queue, public API, or web UI.
- No attempt to mechanically prove good architecture, real TDD, or high-quality review.
- No mass rewrite or re-benchmarking of unrelated skills.
- No host-specific hook as the sole source of authority.
- No breaking redefinition of `verification-record.v1`.

## Downstream Consumers

- `system-design`
- `security-design`
- `task-breakdown`
- `tdd`
- `feature-development`
- `implementation-alignment-review`
- `implementation-integrity-audit`
- `testing-strategy`
- `verification-before-completion`
