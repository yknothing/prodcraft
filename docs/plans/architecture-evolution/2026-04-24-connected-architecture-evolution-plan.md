# Connected Architecture Evolution Plan

> Date: 2026-04-24
>
> Status: active planning buffer, not canonical architecture policy.
>
> Location decision: use `docs/plans/architecture-evolution/` for tracked,
> temporary architecture-evolution planning artifacts.

## Route Record

- Intake mode: `resume`
- Work type: `Documentation`
- Entry phase: `cross-cutting`
- Primary workflow: lightweight agile planning over the existing architecture
  action register
- Key skills: `documentation`, `risk-assessment`, `task-breakdown`,
  `code-review`, `verification-before-completion`
- Routing rationale: the canonical architecture state already exists; the next
  need is connected execution planning without turning active planning notes
  into canonical architecture.

## Source Documents

- `docs/architecture/2026-04-18-prodcraft-architecture-state-bundle.md`
- `docs/architecture/2026-04-17-prodcraft-architecture-evolution-basis.md`
- `docs/architecture/2026-04-17-architecture-review-action-register.md`
- `docs/architecture/ar-01-enforcement-promotion-measurement-protocol.md`
- `docs/architecture/ar-03-host-adapter-policy.md`
- `docs/distribution/2026-04-24-curated-portability-review.md`
- `schemas/artifacts/verification-record.schema.json`
- `schemas/distribution/public-skill-portability.json`

## Placement Decision

Use `docs/plans/architecture-evolution/`.

Rationale:

- `docs/architecture/` should remain reserved for canonical state, historical
  source records, supporting registers, and provisional architecture design
  notes.
- `docs/plans/` already holds execution plans and temporary roadmap material.
- A dedicated subdirectory keeps active architecture-evolution planning from
  mixing with skill-maturity plans.
- `build/` is appropriate for local handoff logs, but not for documents that
  should be reviewed, staged, or temporarily committed.
- `docs/adr/` is too authoritative until a narrow, accepted decision exists.

Rejected alternatives:

| Location | Why rejected |
|---|---|
| `docs/architecture/working/` | Too close to canonical architecture state; invites scratchpad drift in the architecture source area. |
| `docs/architecture/evolution/` | Makes planning artifacts look like architecture authority. |
| `docs/plans/` root | Keeps temporary architecture plans mixed with release and skill-maturity plans. |
| `build/architecture-evolution/` | Good for local handoff logs, but not for tracked planning that needs review. |
| `.tmp/architecture-evolution/` | Too invisible for a repository planning artifact. |

## Current Architecture Baseline

The architecture bundle has already converged on these durable constraints:

- repository-owned contracts remain sovereign
- host bindings adapt repository contracts rather than replacing them
- public export must not overclaim what survives outside repository context
- protocol/state is valuable only when it preserves decision state, not when it
  creates ceremonial paperwork
- low-signal checks must not masquerade as proof of semantic quality

The open debt is now execution sequencing:

- AR-01 now has a provisional enforcement promotion matrix; individual rows
  still need to graduate through narrow repository-owned contracts before they
  become executable
- AR-02 has its first small repo-native downstream execution hardening slice
  landed: `verification-record.v1` now carries structured work-state and
  evidence bindings plus validator coverage for stale or mismatched completion
  proof
- AR-03 exists as a provisional host adapter policy, but is not an ADR and has
  no implemented adapters
- AR-04 has a portability landing zone and initial static review, but no live
  full-repo versus curated-only benchmark
- AR-05 still needs an essential-versus-accidental protocol audit

## Evolution Principles

1. Start with repo-native contracts before host adapters.
2. Promote controls only from bounded evidence, not from architectural taste.
3. Harden proof shape and artifact presence before claiming semantic quality.
4. Keep public export caveats visible until curated-only task runs show the
   same route quality and handoff preservation as full-repo runs.
5. Give every temporary plan a graduation path into an ADR, architecture note,
   schema, validator, workflow contract, rule, test, or historical record.
6. Keep the canonical architecture bundle stable unless a real contract change
   or accepted narrow decision requires an update.

## Connected Workstreams

### Phase 0: Planning Containment

Goal: establish a tracked planning buffer that prevents active work from
polluting canonical architecture state.

Output:

- `docs/plans/architecture-evolution/README.md`
- this connected plan

Acceptance:

- the directory states that it is non-canonical
- the plan names source documents and graduation paths
- canonical docs remain unchanged unless the planning boundary itself changes

### Phase 1: AR-01 Enforcement Promotion Matrix

Goal: turn the measurement protocol into a concrete decision table without
claiming enforcement before implementation.

Current artifact:

- `docs/plans/architecture-evolution/2026-04-24-ar-01-enforcement-promotion-matrix.md`

Status on 2026-04-24: initial provisional matrix exists. It remains a planning
artifact until individual controls graduate into schemas, validators, workflow
contracts, rules, tests, CI, manifest artifact flow, or a narrow ADR.

Minimum rows:

- workflow entry requires valid `intake-brief`
- completion claims require fresh verification evidence
- mandatory route changes preserve explicit state handoff
- unsupported-flow and release-safety structural checks
- TDD-adjacent structural checks
- review-adjacent structural checks
- agent security controls named by AR-01

Acceptance:

- every row includes evidence source class, sample window,
  false-positive risk, false-negative risk, friction cost, decision owner, and
  review date
- rows with thin evidence remain `collect evidence` or `evidence only`
- no row claims semantic adequacy from cheap structural signals

Graduation path:

- matrix stays in this directory while provisional
- individual controls graduate into `rules/`, `schemas/`, `scripts/`,
  workflows, tests, or a narrow ADR only after evidence supports the trade-off

### Phase 2: AR-02 First Repo-Native Hardening Wave

Goal: implement one small downstream execution check that strengthens completion
honesty without creating proxy compliance.

Status: first hardening slice landed.

Landed slice:

- use AR01-C04 and AR01-C05 from the promotion matrix to extend
  `verification-record.v1` from proof-shape schema into a practical
  completion-claim validator path
- represent `work_state_ref` as a structured current-work-state object rather
  than a free-form string
- represent `evidence_refs` as structured evidence objects with ids,
  timestamps, and explicit work-state bindings
- require each `checks_run` item to bind back to both an evidence id and the
  current work-state id
- add validator coverage for accepted records whose evidence is older than the
  work-state capture, references undeclared evidence, or binds evidence to a
  different work state

Current check shape:

- accepted verification records must bind to the current work state
- `claim_may_be_made=true` remains valid only when status is accepted, checks
  passed, failed list is empty, and remaining unverified list is empty
- freshness must be represented by an explicit work-state reference or evidence
  reference, not by prose
- instance validation checks evidence/check alignment that portable JSON Schema
  cannot express by itself

Acceptance for this slice:

- at least one negative test covers stale or mismatched completion proof
- the validator reports a concrete failure reason
- the check remains repository-owned and host-portable
- the implementation does not claim to prove real TDD, real review quality, or
  good architecture

Boundary:

- this slice validates artifact shape, current work-state binding, evidence
  timestamp freshness, and evidence/check alignment only
- it does not prove that the named command was sufficient, that TDD happened,
  that review was high quality, or that the architecture is semantically sound

Graduation path:

- executable contract lands in schema, validator, tests, and any required
  workflow/artifact-flow documentation
- if the new contract changes completion semantics materially, open a narrow ADR

### Phase 3: AR-03 Host Adapter Formalization

Goal: decide whether the provisional host adapter policy should remain a design
note, become an ADR, or drive a concrete adapter implementation.

Do not begin implementation until Phase 2 produces at least one repo-native
contract worth mirroring.

Acceptance:

- every proposed host adapter names the exact repository source it mirrors
- no adapter adds stronger authority than the repository contract
- host-specific behavior is explicitly marked as adapter behavior

Graduation path:

- keep `ar-03-host-adapter-policy.md` as a design note if no durable contract
  exists
- create an ADR only if the adapter boundary becomes stable policy
- create host-specific files only after the repository-native source exists

### Phase 4: AR-04 Public Export Live Portability Review

Goal: move beyond the initial static portability review by comparing full-repo
and curated-only execution on the same probes.

Recommended artifact:

- `docs/plans/architecture-evolution/2026-04-25-ar-04-live-portability-benchmark-plan.md`

Required probe fields:

- model and host runtime
- prompt
- full-repo output
- curated-only output
- overclaim finding
- handoff preservation score
- route correctness score
- caveat sufficiency decision

Acceptance:

- no skill is promoted to `portable_as_is` without live curated-only evidence
- blocked or caveated decisions update `schemas/distribution/public-skill-portability.json`
- public docs and generated curated index remain consistent

Graduation path:

- stable policy changes land in `docs/distribution/`
- registry changes land in `schemas/distribution/`
- generated surface changes land through `scripts/export_curated_skills.py`

### Phase 5: AR-05 Protocol Essentiality Audit

Goal: protect first-class protocol/state while removing accidental governance
overhead.

Recommended artifact:

- `docs/plans/architecture-evolution/2026-04-24-ar-05-protocol-essentiality-audit.md`

Audit each artifact against:

- decision value
- cross-session continuity value
- validation value
- duplication with another artifact
- contributor friction
- downstream evidence value

Acceptance:

- each artifact receives `keep`, `simplify`, `merge`, `defer`, or `remove`
- removals do not break accepted ADRs, schema contracts, or workflow entry gates
- simplification proposals name the exact schema/template/workflow diffs needed

Graduation path:

- durable changes land in schemas, templates, workflows, validators, and tests
- historical reasoning remains in the audit file

## Immediate Next Slice

Create the AR-01 enforcement promotion matrix as the next planning artifact.
Keep it provisional and evidence-first.

Suggested next-row decision:

- `completion claims require fresh verification evidence`
- Current home: `verification-before-completion`, `delivery-completion`,
  `verification-record.v1`, validator schema contract
- Initial surface: `repo-native enforcement`
- Initial landed move: validator coverage only for proof freshness, status
  alignment, work-state binding, and evidence/check alignment; leave semantic
  completion judgment review-led

## Validation Expectations

For planning-only changes:

```bash
python scripts/validate_prodcraft.py
git diff --check
rg -n "[\u4e00-\u9fff]" docs/plans/architecture-evolution
```

For any executable contract change:

```bash
UV_CACHE_DIR=/tmp/uv-cache-prodcraft uv run --python 3.11 --with pyyaml --with jsonschema python -m unittest discover tests
UV_CACHE_DIR=/tmp/uv-cache-prodcraft uv run --python 3.11 --with pyyaml --with jsonschema python scripts/validate_prodcraft.py
```

## Open Questions

1. Should the accepted AR-01 matrix eventually live as a Markdown governance
   table, a YAML rule source, or both?
2. What is the minimum work-state identity needed for verification-record
   freshness without creating a full work-item database?
3. Which live portability probes should become regression fixtures rather than
   one-off review evidence?
4. What retirement cadence should apply to temporary architecture-evolution
   plans after their workstream graduates or is rejected?
