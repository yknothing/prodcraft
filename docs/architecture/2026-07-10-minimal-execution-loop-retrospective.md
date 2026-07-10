# Minimal Execution Loop Engineering Retrospective

> Status: accepted process record — 2026-07-10
>
> Scope: Direction 2 design, implementation, P2 hardening, commits, and adversarial acceptance

## Verdict

Direction 2 is the right-sized architecture, but the delivery process was not clean end to end. The initial implementation was committed as one already-published 69-file change with a vague subject. The first P2 design then introduced an unnecessary external-skill document layer, and the first post-P2 acceptance missed three entry-path defects. The defects were reproducible rather than theoretical, so acceptance was reopened and corrected.

The final implementation remains intentionally simple: a repository-owned protocol and validator, a fixed 300-second Git liveness guard, bounded strict authority documents, streaming bulk hashing, and optional machine-readable output. No resource-profile matrix or Direction 3 runtime was added.

## Process Timeline And Corrections

| Stage | What happened | Assessment | Correction |
|---|---|---|---|
| Initial Direction 2 delivery | Commit `aaabff0` mixed 69 files, 7,094 insertions, and 120 deletions under `Improve prodcraft delivery flow and supporting implementation`. It was already published on `origin/main`. | The implementation may be coherent, but the commit is not an atomic review or rollback unit and its subject does not expose architectural intent. | Do not rewrite published history without explicit authorization. Subsequent work uses bounded, single-purpose commits and staged-diff checks. |
| Initial P2 proposal | Resource profiles and a five-second fail-closed timeout were considered. | The profile matrix solved a hypothetical policy problem and the timeout would reject merely slow repositories. | Use one 300-second final liveness guard and allow large repositories to take longer. |
| P2 implementation | Strict authority JSON became bounded; evidence/worktree hashing became streaming; structured output was added. | Core direction was correct and digest/text/exit compatibility was preserved. | Keep these mechanics; do not add adaptive budgets or host overrides. |
| First P2 review | Three independent reviews returned FAIL because generic strict inspection used a different, TOCTOU-prone first-read path from authority validation, invalid bundles could expose a completion candidate, and `.git/info/exclude` had a post-`lstat` FIFO swap window. | Acceptance was declared too early from helper-level and happy-path evidence. | Reproduce at public entry points, fix the safe-reader and candidate projection, close the metadata race, add regression tests, and require fresh second-pass review. |
| First correction review | Applying the strict 16 MiB limit to every generic artifact fixed one entry path but rejected a previously valid 16 MiB-plus legacy `intake-brief.v1`; candidate text also remained in shared errors. | The correction confused safe descriptor semantics with strict size policy and hid only the structured candidate field. | Keep generic legacy reads safe but uncapped, keep strict authority bounded, and defer every candidate representation until all bundle/freshness checks finish. |
| Documentation review | `docs/superpowers/` declared external skills as required and duplicated the repository truth surface. | This violated the local integration rule and contradicted the user's simplicity constraint. | Remove the duplicate layer; keep the closure in the existing local implementation plan and this retrospective. |

## Adversarial Review Consensus

The architecture, implementation-integrity, and compatibility reviewers agreed on these points:

1. Direction 2 is a local truth and authority surface, not an orchestration service. Direction 3 should remain an extension seam until concurrency, identity, scheduling, or durable recovery is an observed requirement.
2. The route/state split and independent route/completion pins are necessary when the bundle writer is not the approver.
3. A fixed 300-second timeout is a last-resort liveness bound, not a performance threshold. Streaming is the correct response to large raw files; named resource profiles are unnecessary.
4. A candidate digest is safe only when the entire bundle is valid except for the missing completion pin. Generic inspection and authority validation share safe descriptor semantics, but only strict authority adopts the new 16 MiB limit so legacy inputs remain compatible.
5. The initial mega-commit and the external-skill P2 document layer were process errors. Clear later commit subjects do not retroactively make the first delivery atomic.
6. Direction 2 should remain opt-in until real authoring and gray-run evidence proves that teams can produce valid bundles without bypassing the protocol.

## Material Disagreements Still Open

| Question | Positions | Current decision and trigger |
|---|---|---|
| Is a route/state authoring command required now? | One view treats templates as sufficient for a verifier-first Direction 2; another treats the absence of safe init/transition/digest helpers as an adoption blocker. | Do not expand this correction slice. Before any strict-default rollout, run a separate intake for authoring ergonomics and require a human or agent to complete a bundle without hand-editing derived digests. |
| How should the 16 MiB append-only state limit age? | The hard bound protects memory and protocol intent; long-running append-only arrays may eventually exceed it. Reviewers did not agree on rollover, archival, or compaction semantics. | Keep the limit and fail clearly. Before a workload approaches 12 MiB or strict mode becomes long-lived, define a versioned archival/rollover contract with replay continuity tests. |
| Should work identity cover the full repository or only the work item? | Full-worktree scope is honest and simple but can create unrelated-change coupling; narrower scope improves concurrency but introduces exclusion-policy risk. | Retain full-worktree identity in Direction 2. Revisit only through the documented `WorkSnapshotProvider` seam with explicit scope evidence and negative exclusion tests. |
| Must `verified -> completed` require a new completion pin? | Repinning is explicit and catches terminal timestamp/state changes; it may be operationally heavy when the transition carries no new semantic work. | Retain repinning in v1. Reconsider only with adoption data and a separately versioned authority projection. |
| Is the four-field JSON object a durable API? | It is useful for current automation, but it has no `schema_version`, and `argparse` failures occur before JSON rendering. | Treat it as a local CLI projection only. A Direction 3 adapter must add explicit versioning, status vocabulary, and parse-error semantics rather than silently extending these four fields. |
| Should the 2,000-line execution module be split now? | Splitting could improve ownership and test locality; doing it during a correctness repair risks a large mechanical refactor. | Defer. Split by parser/path, state replay, completion authority, and Git provider only when the next semantic/provider change crosses those boundaries. |

## Agreed Process Changes

| Action | Owner | When | Success signal |
|---|---|---|---|
| Re-read repository intake and integration rules before introducing planning or skill dependencies. | Change author | Every new slice | No external skill is declared as an implicit repository dependency. |
| Test the public CLI entry path, not only helpers, for every resource and authority boundary. | Implementer and reviewer | Before acceptance | Each claimed boundary has a subprocess-level negative regression. |
| Inspect staged scope and subject before each commit. | Commit author | Every commit | One reversible purpose per commit; message names the behavioral intent. |
| Reopen acceptance whenever a fresh reviewer reproduces a P0/P1. | Acceptance owner | Before delivery | Final record names the failed pass, correction, and fresh rerun rather than hiding the failure. |
| Gate strict-default adoption on authoring usability and state-growth evidence. | Maintainer | Before rollout | A documented gray run completes without manual derived-digest repair and records state-size headroom. |

## Direction 3 Extension Boundary

Direction 3 may replace filesystem projections and the Git snapshot adapter, but it must preserve the Direction 2 domain invariants: explicit route authority, replayable lifecycle/phase ordering, obligation satisfaction, attempt-scoped completion, evidence freshness, and non-self-issued terminal approval. Storage, scheduling, identity, and concurrency mechanisms are replaceable; those invariants are not.
