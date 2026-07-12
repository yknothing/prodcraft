# ADR-004: Direction 2 Adoption Boundary

## Status

Proposed — 2026-07-12

This ADR is approved in direction and awaits written design review of [`2026-07-12-direction2-adoption-architecture.md`](../architecture/2026-07-12-direction2-adoption-architecture.md).

It may move to Accepted only in the same documentation batch that labels the existing Direction 3 event/CAS/idempotency details proposed and non-normative and passes cross-document consistency validation.

## Context

ADR-003 established repository-owned route/execution snapshots, dual external pins, deterministic work identity, and strict terminal authorization. The implementation validates authority but does not provide a complete authoring path. Users or host adapters must currently construct append-only records and derived digests manually.

The final adversarial review identified six adoption/evolution questions: authoring ergonomics, state capacity, worktree scope, terminal repinning, machine-result versioning, and module size. Treating all six as immediate implementation would create a large refactor and prematurely import Direction 3 concerns. Treating none as immediate leaves strict mode difficult to adopt and encourages divergent host writers.

## Decision Drivers

- authoring must not weaken or absorb the operator authority boundary;
- protocol-derived values should have one repository-owned implementation;
- existing text, unversioned JSON, schemas, and legacy consumers must remain compatible;
- the system needs evidence about usability and state growth before versioning lifecycle storage;
- full-worktree identity and terminal repinning remain the strongest proven integrity choices;
- new responsibilities should not deepen the existing validator module's coupling;
- future runtime mechanics must remain deferred until requirements exist.

## Options Considered

### Option A: Keep verifier-only Direction 2

Rejected. Templates do not make coupled sequence, digest, binding, retry, and reroute mutations correct by construction. Host-specific writers would become a second, weaker source of protocol semantics.

### Option B: Add a separate adoption layer and evidence-gated evolution

Selected. Add pure authoring transformations, a thin atomic-write CLI, additive versioned authority/authoring results, and capacity telemetry. Retain current authority semantics and defer rollover, scoped snapshots, repin relaxation, and Direction 3.

### Option C: Replace Direction 2 with a Direction 3 runtime

Rejected. There is no approved requirement for a database, service, scheduler, authenticated identity, tenancy, distributed concurrency, or recovery topology.

## Decision

Adopt Option B.

1. Authoring is a separate module and CLI. It may construct artifacts, compute candidates, and consume a separately supplied explicit pin as a validation precondition. It cannot designate its own candidate as approved, persist a pin, or auto-forward a candidate into authorization.
2. Canonical projection helpers remain the single source of digest semantics. Schema/registry/composed validation moves from the validation CLI into a focused repository service consumed by both CLIs; neither CLI imports the other or copies the rules.
3. Existing validation `text` and `json` outputs remain compatible. New authority and authoring `json-v1` results are separately schema-versioned; authority v1 distinguishes `approval-required` from invalidity.
4. Every authored candidate reports exact serialized capacity. The 16 MiB hard limit remains; 12 MiB stops rollout and triggers a new rollover ADR.
5. Full-worktree identity and `verified -> completed` repinning remain unchanged in v1.
6. New validation, authoring, and result responsibilities enter focused modules. The existing execution semantics module is not split solely to reduce line count.
7. Direction 3 event/CAS/idempotency details are proposed, non-normative hypotheses. Runtime implementation requires a new intake and ADR set.
8. A per-work local advisory lock covers recovery, read, revision check, candidate validation, raw-digest recheck, and replacement for cooperating authoring processes. It does not claim distributed CAS or protect against direct writers that ignore the lock.
9. Completion/retry authoring is the core adoption closure. Reroute journal/recovery is a separately accepted optional iteration and does not block the core gray rollout.

## Consequences

### Positive

- valid Direction 2 artifacts become constructible without manual derived-field repair;
- host adapters can invoke one repository-owned writer instead of reimplementing the protocol;
- authority remains external to the writer;
- machine consumers gain explicit result versions and an approval-required authority state;
- capacity and adoption decisions become evidence-led;
- future refactoring follows real dependency pressure.

### Negative

- the repository gains three focused modules, one CLI, a protocol-result registry with two schemas, and new tests;
- the authoring CLI supports a larger operation surface than a template-only workflow;
- a local lock plus expected revision/raw-digest recheck serializes cooperating writers but does not provide multi-host or hostile-writer linearizability;
- reroute needs a small recoverable local journal because its immutable archive, route, and selector cannot be committed by one filesystem replacement;
- legacy and versioned JSON outputs must coexist;
- state rollover remains intentionally unavailable until a trigger is observed.

## Trust And Authority Boundary

An authored artifact is not approved merely because the authoring CLI produced it. Route and completion pins cross an explicit external input boundary and are never stored in the writable bundle. A candidate digest is review input, not authority, and the CLI never auto-forwards it into a later authorization. `gate-authorized` and `terminal-authorized` remain outputs of the existing validator only. Direction 2 does not authenticate the actor who re-supplies a pin; an actor controlling both artifacts and pins can still self-approve under this trust model.

## Reversibility

The adoption layer is additive. Removing the authoring CLI and `json-v1` leaves ADR-003 artifacts and the existing validator usable. Each result schema is immutable after acceptance; later output evolution uses a new explicit version. No v1 state history is truncated or rewritten.

## Fitness Functions

- normal, block/resume, and reject/retry workflows complete without manual edits to derived fields;
- authoring without separately supplied explicit required pins never obtains authority and never auto-forwards its candidate;
- lock-cooperating invalid or stale mutations leave canonical bytes unchanged, and observed external raw-digest changes fail before replacement;
- authored candidates pass the shared schema/registry, bundle-closure, and semantic service without copying validation rules;
- existing text and four-field JSON golden tests remain unchanged;
- authority and authoring `json-v1` results validate against their schemas for every status;
- exact capacity warning/rejection boundaries are tested;
- full-worktree and completion-repin negative fixtures remain green;
- gray adoption reaches no unresolved P0/P1 before opt-in readiness.

## Deferred Decisions

- rollover, archival, compaction, or history segmentation;
- work-item-scoped snapshot providers;
- terminal projection changes that remove repinning;
- broad decomposition of `tools/execution_state.py`;
- Direction 3 event store, identity, scheduler, API, tenancy, retention, and recovery.

Each deferred item has an explicit evidence trigger in the linked architecture document and requires a new reviewed decision before implementation.
