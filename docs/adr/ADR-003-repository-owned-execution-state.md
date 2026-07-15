# ADR-003: Repository-Owned Route And Execution State

## Status

Accepted — 2026-07-10

Implementation, focused adversarial fixtures, both supported Python suites, public flattened-reference validation, and fresh independent alignment, integrity, and compatibility reviews passed with no unresolved P0/P1 findings. Evidence and residual risks are recorded in [`2026-07-10-minimal-execution-loop-acceptance.md`](../architecture/2026-07-10-minimal-execution-loop-acceptance.md).

## Context

Prodcraft can validate repository structure and completion proof shape, but it does not yet bind an approved route, current execution state, gate obligations, frozen completion basis, and live governed work into one terminal authorization decision.

`verification-record.v1` intentionally keeps `claim_scope` as free text. Reinterpreting it as route identity would be a breaking change. A single mutable execution artifact would also be able to remove its own unmet obligations. A route file with only a self-declared digest is still writable by the executing agent and cannot independently anchor approval.

## Decision Drivers

- current authority must be distinguishable from historical structural validity;
- route obligations must remain independent of mutable execution bindings;
- gate authorization must use an out-of-band route pin, and terminal authorization must also pin the final completion projection;
- evidence and governed work must be content-bound without self-hash cycles;
- current artifacts and `verification-record.v1` semantics must remain compatible;
- semantic quality and actor authenticity must not be overstated;
- a future runtime must have a clean event-authority migration path.

## Options Considered

### Option A: One mutable execution-state artifact

Rejected. The same file would define and satisfy obligations, so deletion could self-authorize progress.

### Option B: Redefine `verification-record.v1`

Rejected. Existing free-text claim scope and current consumers do not provide route identity or revision.

### Option C: Separate route and execution snapshots, but trust the route file digest

Rejected for terminal authority. The same writer can weaken route obligations and recompute every in-bundle digest.

### Option D: Separate snapshots plus canonical live locator and operator-pinned route/completion digests

Recommended. The route owns reviewer-declared obligations; live execution satisfies them; an out-of-band route pin anchors gate authority and a separately approved completion pin anchors the reviewed terminal attempt/evidence projection. Frozen completion and work/evidence digests make stale or partial mutation detectable, while the completion pin prevents coordinated in-bundle recomputation from preserving terminal authority.

### Option E: Build a standalone event-driven runtime now

Deferred. It would force persistence, API, identity, scheduler, tenancy, and operational decisions before Direction 2 has adoption evidence.

## Proposed Decision

Add `route-decision.v1` and `execution-state.v1` as opt-in repository artifacts. Keep the existing artifact-instance CLI for structural inspection and add a distinct execution-authorization mode requiring an approved-route digest for gates and an approved-completion digest for terminal state; authority mode exits zero only for gate- or terminal-authorized current state.

- Canonical live state is `<git-root>/.prodcraft/artifacts/<work_id>/execution-state.json`.
- Route revisions are immutable snapshots with predecessor bindings; the live state selects the current route.
- Gate authorization requires the recomputed route digest to equal an operator-supplied pin; terminal authorization additionally requires the final `terminal_authority.v1` digest to equal a second operator-supplied pin.
- Lifecycle transitions and route-specific workflow focus events are independent histories.
- Reached obligations use explicit presence, structural, or declared-approval assurance.
- Completion attempts freeze a canonical preterminal basis and verification commitment; the final attempt/binding/terminal records are externally pinned.
- `git-worktree-content-v1` captures governed work deterministically and excludes only a closed, separately content-bound control root.
- Legacy artifacts and `verification-record.v1.claim_scope` keep their current meaning.
- Strict mode remains optional in this change.
- The curated exporter rewrites and validates references for the flattened install layout.

## Consequences

### Positive

- historical validity is no longer confused with current terminal authority;
- route weakening inside the writable bundle conflicts with the external pin;
- completion retries, rejection, replay, and allowed terminal projection have explicit semantics;
- post-verification evidence or source mutation is mechanically detectable;
- local users, CI, and agent hosts share one repository-owned contract;
- Direction 3 can replace storage mechanics without capturing authority in one host.

### Negative

- strict mode requires multiple artifacts, a canonical directory, a route pin, and explicit terminal completion approval;
- full worktree hashing adds I/O;
- approval identity and trusted time remain outside Direction 2;
- source-control review remains the historical monotonicity anchor;
- legacy users remain guidance-led until they opt in.

## Trust Boundary

The decision detects partial/stale mutation and prevents a writable bundle from silently overriding unchanged route or completion pins. It does not resist an actor that controls repository history and both pins, and it does not authenticate approvers.

## Reversibility

The change is additive. Existing consumers remain in legacy mode, and strict artifacts can be deprecated through normal schema versioning. A future event runtime imports Direction 2 with an explicit genesis event and preserves v1 compatibility semantics behind versioned upcasters and projections.

## Fitness Functions

- route obligation deletion plus digest recomputation fails against the pinned digest;
- coordinated verification-commitment, claim, basis, binding, and in-bundle digest rewrites fail against the original completion pin, while a missing completion pin never authorizes a terminal state;
- rerouted old state cannot authorize current completion when governed work is unchanged;
- frozen execution, verification, approval, and validator evidence mutations fail;
- rejected attempt 1 cannot authorize attempt 2;
- final phase exit and repeated focus phases are representable;
- Git config changes do not change the content digest;
- unsafe paths, symlinks, special files, and dirty submodules fail closed;
- existing legacy behavior remains green;
- flattened public packages load and all relative references resolve.

## Follow-Up

- implement schemas, templates, validator, exporter, and tests;
- record a threat model and adversarial review dispositions;
- change this ADR to Accepted only after final evidence and reviews pass;
- treat any event store, scheduler, identity provider, or host adapter as separate approved work.
