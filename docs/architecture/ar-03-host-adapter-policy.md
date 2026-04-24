# AR-03 Host Adapter Policy

> Status: provisional architecture design note.
>
> Parent register:
> [`2026-04-17-architecture-review-action-register.md`](./2026-04-17-architecture-review-action-register.md)
>
> Scope: defines how Claude, Codex, Gemini, or other runtime bindings may attach
> to Prodcraft repository-owned contracts after the first repo-native hardening
> check exists.

## Policy Statement

Host adapters are runtime bindings. They are not the source of architectural
authority.

The repository contract comes first:

1. A rule starts as skill guidance, workflow policy, artifact schema, validator,
   manifest artifact flow, or evidence requirement.
2. AR-01 measures whether the rule is worth promotion.
3. Repo-native enforcement is preferred when the rule can be checked without
   host-specific affordances.
4. Host adapters may mirror, accelerate, or preflight a repository-owned rule.
5. A host adapter must not create a stronger claim than the repository contract
   can verify.

## Adapter Eligibility

A control is eligible for a host adapter only when all of the following are true:

- the underlying rule is already represented in a repository-owned contract or
  AR-01 measurement row
- the adapter can name the canonical source it mirrors
- the adapter failure mode is understood well enough to avoid blocking valid work
  without an escape path
- the adapter preserves user approval and sandbox boundaries for side-effectful
  actions
- the adapter produces evidence that can be inspected outside the host runtime

Controls that are mostly semantic judgment should stay in skills, review, or
evidence until a higher-signal repository contract appears.

## Adapter Map

| Host surface | Appropriate use | Forbidden use |
|---|---|---|
| Claude hooks | Preflight repository-owned checks, remind about required artifacts, block known unsafe command shapes when the repo contract is explicit. | Defining private Claude-only governance that has no schema, validator, workflow, or AR-01 row. |
| Codex instructions/tools | Preserve routing discipline, require verification before completion claims, request approval for side effects, and run repo-native validators. | Treating Codex-only behavior as evidence that other hosts will preserve the same route or handoff. |
| Gemini benchmark/eval runners | Generate evidence about skill behavior, trigger quality, or runtime drift. | Treating benchmark runner prompts as canonical workflow policy. |
| CI | Enforce repository-owned checks after code or artifact changes. | Replacing runtime judgment with low-signal pass/fail proxies for semantic quality. |

## Required Adapter Record

Every future adapter should have a small record that states:

- adapter name
- host surface
- canonical repository source
- control rule or artifact contract mirrored
- trigger condition
- action (`warn`, `block`, `suggest`, `record evidence`, or `run validator`)
- false-positive escape path
- evidence emitted
- review date

## Initial Candidates

These are eligible for adapter exploration after the current repo-native
verification-record hardening:

| Candidate | Canonical source | Host adapter posture |
|---|---|---|
| Verification before completion | `verification-record.v1`, `verification-before-completion`, artifact-flow checks | Runtime reminder or preflight validator before final completion claims. |
| Curated export portability | `public-skill-portability.v1`, curated-surface validator | Export-time check only; host runtime should display public caveats, not reinterpret hidden dependencies. |
| Course-correction routing | `course-correction-note.v1`, gateway direct-jump contract | Warn when a host conversation jumps phases without the required artifact. |
| Agent security controls | AR-01 measurement protocol | Keep as protocol/evidence first; only promote narrow command or artifact-boundary checks after measurement. |

## Anti-Capture Rule

If a host adapter discovers a useful rule that is not yet repository-owned, the
next step is not to expand the adapter. The next step is to create or update the
repository contract, then decide whether the adapter should mirror it.

This keeps Claude, Codex, Gemini, CI, and future hosts as consumers of Prodcraft
rather than competing sources of Prodcraft authority.
