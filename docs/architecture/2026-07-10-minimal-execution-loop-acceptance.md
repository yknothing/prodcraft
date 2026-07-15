# Minimal Execution Loop Acceptance Record

> Status: Accepted after corrective adversarial review — 2026-07-10
>
> Scope: Direction 2 repository-owned strict execution loop

## Verdict

Direction 2 is accepted with no unresolved P0/P1 findings. The delivered contract is additive and opt-in: generic artifact inspection remains structural-only; gate authority requires the canonical live state and an operator-held route pin; terminal authority additionally requires an operator-held completion pin over the final authority projection and fresh evidence/work validation.

Direction 3 remains architecture only. This change does not introduce a service, database, queue, scheduler, network API, identity provider, or multi-writer runtime.

The delivery/process review, including consensus and unresolved design disagreements, is recorded in [`2026-07-10-minimal-execution-loop-retrospective.md`](./2026-07-10-minimal-execution-loop-retrospective.md).

## Intent And Acceptance Coverage

| Acceptance area | Evidence | Result |
|---|---|---|
| MEL-AC-01..05 route/state authority | Schema contracts, route pin, canonical selector, global lifecycle/phase/binding replay, obligation and reroute tests | Pass |
| MEL-AC-06..09 completion integrity | Verification commitment, claim/basis freeze, exact terminal records, external completion pin, retry freshness, work/evidence closure | Pass |
| MEL-AC-10..12 compatibility and portability | Additive v1 artifacts, unchanged `verification-record.v1` semantics, safe local refs, deterministic Git snapshot, flattened curated reference/loadability checks | Pass |
| MEL-AC-13 truth surface | Structural inspection emits no authority; strict CLI exits zero only for `gate-authorized` or `terminal-authorized`; missing completion pin reports a candidate only | Pass |
| MEL-AC-14..15 contract alignment and evolution | Registry, manifest, templates, skills, exporter, schemas, README, ADR, threat model, and Direction 3 ports/event semantics agree | Pass |
| MEL-AC-16 verification depth | Focused and full suites on Python 3.12 and 3.11, canonical validator, Ruff, mypy for the new execution engine, diff hygiene, and independent adversarial reviews | Pass |

## Adversarial Review Dispositions

| Severity | Finding | Disposition |
|---|---|---|
| P0 | A writable bundle could coordinate verification, claim, basis, binding, and digest rewrites. | Added the externally approved `terminal_authority.v1` completion pin and a coordinated-rewrite regression. |
| P1 | `updated_at` was outside the terminal projection and `verified -> completed` repinning lacked a dedicated regression. | Added `updated_at` to the projection and a test proving both timestamp mutation and lifecycle advancement invalidate the old pin. |
| P1 | Generic JSON inspection, Git metadata, or a local config include could block on a FIFO. | Added nonblocking regular-file reads, Git metadata checks, and a bounded fail-closed Git-command policy with real FIFO regression coverage. |
| P1 | Git config, replace refs, alternate index state, or submodule settings/index flags could change or hide snapshot identity. | Fixed relevant Git settings, disabled replace refs, rejected unverifiable index states, and recursively validates submodule content independently of status-hiding config. |
| P1 | Separate digest and semantic reads allowed an A-digest/B-semantics race. | Strict JSON is hashed and parsed from one descriptor snapshot; Schema and terminal semantics reuse that payload; authority performs a final control-bundle/freshness capture. |
| P1 | Canonical/historical route-state selection, reroute replay, and generic structural semantics had incomplete negative coverage. | Enforced canonical filenames/selectors, content-addressed history, predecessor replay, and structural-only generic validation. |
| P1 | Generic artifact inspection performed a TOCTOU-prone first read; the first correction then applied the strict 16 MiB cap to all legacy artifacts. | Unified safe descriptor semantics, retained the cap on strict authority inputs, and added a schema-valid 16 MiB-plus legacy compatibility regression. |
| P1 | A globally invalid terminal bundle could still expose a completion candidate in JSON errors or text. | Deferred every candidate field/message until final bundle and freshness checks pass; invalid-bundle regressions cover both renderers. |
| P1 | `.git/info/exclude` could be replaced with a FIFO after an outer `lstat`, leaving validation blocked outside the Git timeout. | Read Git metadata through the same nonblocking regular-file descriptor snapshot and reproduced the swap as fail-fast. |
| P2 | `./x`, `x/`, and `a//b` were normalized before local-ref validation. | Closed in this slice: runtime and both schemas now reject noncanonical raw segments. |

The first post-P2 review returned FAIL and acceptance was reopened. After two corrective implementation commits, fresh architecture/process, implementation-integrity, and compatibility reviewers reran the original reproductions and returned PASS with no unresolved P0/P1.

## Verification Evidence

The final governed state is accepted only when these commands pass on the same work snapshot:

```bash
python3 -m unittest discover -s tests
UV_CACHE_DIR=/tmp/uv-cache-prodcraft uv run --python 3.11 --with pyyaml --with jsonschema python -m unittest discover -s tests
python3 scripts/validate_prodcraft.py
ruff check tools/execution_state.py scripts/validate_prodcraft.py scripts/export_curated_skills.py tests/test_execution_state_*.py tests/test_curated_distribution_surface.py
mypy tools/execution_state.py
git diff --check
```

The self-hosted acceptance bundle lives at the intentionally ignored canonical locator `.prodcraft/artifacts/prodcraft-direction2/execution-state.json`. It binds this final work snapshot and review/test evidence. Running strict authority without a completion pin must return a non-authoritative candidate digest; rerunning with the separately retained route and completion pins must return `terminal-authorized`.

## Residual P2 And Direction 3 Triggers

- Approval identity, trusted time, malicious races around both captures, multi-writer concurrency, durable recovery, and CAS/idempotency remain explicit Direction 3 concerns.

These are not silent guarantees: none is upgraded to terminal authority by Direction 2, and each has a documented migration seam in the architecture.

The strict-authority whole-file memory-pressure issue is closed by bounded control JSON plus streaming evidence/worktree hashing. Generic legacy artifact inspection intentionally retains whole-document parsing for backward compatibility, but uses the same nonblocking regular-file descriptor safety. The former five-second Git timeout is now a fixed 300-second liveness guard: large repositories may run slowly, while blocking Git config/FIFO input still fails eventually. Direct package-module CLI tests and the current machine-readable candidate output are also covered by the final P2 regression suite.
