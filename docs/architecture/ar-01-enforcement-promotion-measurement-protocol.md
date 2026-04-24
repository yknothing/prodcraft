# AR-01 Enforcement Promotion Measurement Protocol

> Status: provisional architecture/governance protocol.
>
> Parent register:
> [`2026-04-17-architecture-review-action-register.md`](./2026-04-17-architecture-review-action-register.md)
>
> Scope: defines how AR-01 should measure candidate controls before any rule is
> promoted to protocol, repository-native enforcement, host-native adapter, CI,
> or evidence-only governance.

## Purpose

AR-01 exists to prevent two failure modes:

- promoting low-signal checks into hard enforcement because they are easy to
  automate
- leaving recurring, high-cost failures as reviewer memory because they are
  inconvenient to measure

This protocol defines the minimum evidence shape for the enforcement promotion
matrix. It does not assert that any listed control is already implemented,
complete, or semantically adequate.

## Measurement Record

Each candidate control should have one row in the promotion matrix. A row should
capture both the existing action-register fields and the additional measurement
fields below.

| Field | Purpose | Expected values |
|---|---|---|
| Rule or discipline name | Names the behavior under consideration. | Short control name. |
| Current home | Shows where the rule currently lives. | `skill`, `workflow`, `rule`, `validator`, `hook`, `CI`, `evidence`, or `none`. |
| Failure mode | Describes the specific miss the control is meant to catch. | Concrete failure statement. |
| Observed evidence source | Points to the actual trace or artifact used for the row. | Repository path, review note, benchmark output, validator result, or issue reference. |
| Failure frequency estimate | Estimates how often the failure appears in the sample. | `none observed`, `rare`, `occasional`, `recurring`, or a count. |
| Cost if missed | Captures downstream damage if the failure escapes. | `low`, `medium`, `high`, with a short rationale. |
| Checkability | Rates whether a mechanical check can detect the failure. | `high`, `medium`, or `low`. |
| Goodhart risk | Rates whether hardening the check would invite shallow compliance. | `high`, `medium`, or `low`. |
| Recommended next move | States the proposed governance action. | Keep, revise wording, collect evidence, prototype check, promote, or reject. |
| Recommended surface | Identifies the next control plane. | `protocol`, `repo-native enforcement`, `host-native adapter`, `CI`, or `evidence only`. |
| Owner | Names the person or role accountable for the candidate. | Role or named maintainer. |
| Evidence source class | Classifies the kind of evidence behind the row. | `repository trace`, `validator result`, `benchmark/eval`, `security review`, `incident/near miss`, `manual audit`, or `external reference`. |
| Sample window | Defines the evidence period or artifact set. | Date range, commit range, release window, or named corpus. |
| False-positive risk | Estimates how often valid work would be blocked or burdened. | `low`, `medium`, or `high`, with a short rationale. |
| False-negative risk | Estimates how often bad work would still pass. | `low`, `medium`, or `high`, with a short rationale. |
| Friction cost | Estimates cost imposed on normal contributors. | `low`, `medium`, or `high`, with the likely workflow impact. |
| Decision owner | Names who can approve promotion or rejection. | Role or named maintainer. |
| Review date | Sets when the row should be revisited. | ISO date. |

## Evidence Protocol

Use current repository evidence where possible before relying on general
security doctrine or agent folklore.

Evidence source classes should be interpreted as follows:

| Evidence source class | Meaning |
|---|---|
| `repository trace` | Existing skills, workflows, architecture docs, state bundles, or handoff artifacts show the rule in use or being missed. |
| `validator result` | A repository-owned validator, schema check, or guardrail reports a pass/fail signal. |
| `benchmark/eval` | Evaluation outputs, benchmark reviews, or routed test corpora expose repeated behavior. |
| `security review` | A human security review identifies a control need or classifies control risk. |
| `incident/near miss` | A real or near-real execution failure shows material impact. |
| `manual audit` | A bounded human audit samples documents, skills, or workflows for the candidate failure mode. |
| `external reference` | External guidance informs the row, but does not by itself justify enforcement promotion. |

Sample windows must be bounded. Acceptable windows include:

- a date range such as `2026-04-01..2026-04-24`
- a commit range
- a named artifact set such as `skills/cross-cutting/*` or `eval/current-evidence-snapshots`
- a specific review bundle

Rows with no bounded sample window should remain `evidence only` or
`collect evidence` until the sample is defined.

## Promotion Guidance

A candidate is eligible for repository-native enforcement only when:

- evidence shows a recurring or high-cost failure mode
- false-positive risk is acceptable for the proposed surface
- friction cost is lower than the expected review or failure cost
- the check detects structure or evidence shape rather than pretending to prove
  semantic quality
- the decision owner accepts the trade-off and sets a review date

A candidate should remain review-led or evidence-only when:

- checkability is low and Goodhart risk is medium or high
- the likely enforcement would reward shallow compliance
- the sample window is too thin to estimate false positives or false negatives
- the rule expresses professional judgment rather than a concrete artifact
  contract

## Initial Agent Security Controls Candidate Set

These rows are the starting candidate set for agent security controls in AR-01.
They are intentionally framed as measurement targets, not executable claims.

| Candidate control | Failure mode to measure | Evidence source class | Initial recommended surface | Measurement note |
|---|---|---|---|---|
| Prompt injection | Agent follows untrusted content that attempts to override repository, user, or system instructions. | `security review`, `manual audit`, `repository trace` | `protocol` first, possible `repo-native enforcement` for artifact boundaries | Measure where untrusted instructions can enter artifacts and whether current docs distinguish content from authority. |
| Command safety | Agent runs destructive, privileged, or broad commands without an explicit scope and approval basis. | `security review`, `incident/near miss`, `manual audit` | `protocol` plus possible `host-native adapter` | Measure approval clarity, command scope, and whether repository docs create expectations beyond host policy. |
| External reference trust | Agent treats external skill systems, web pages, package docs, or generated outputs as repository-owned authority. | `repository trace`, `manual audit`, `external reference` | `protocol` | Measure whether external inputs are re-expressed as local contracts before use. |
| Dynamic remote instruction prohibition | Agent imports or obeys mutable remote instructions during work without repository review. | `security review`, `manual audit` | `protocol`, possible `repo-native enforcement` for checked-in references | Measure whether workflows allow remote instruction drift or unreviewed runtime dependency on external guidance. |
| Secret/PII exposure | Agent stores, prints, or propagates secrets or personal data in artifacts, logs, examples, or evaluation outputs. | `security review`, `validator result`, `manual audit`, `incident/near miss` | `protocol` plus possible `repo-native enforcement` or `CI` | Measure existing artifact patterns, validator feasibility, false positives on examples, and contributor friction. |

## Decision Cadence

Each AR-01 row should have a decision owner and review date before promotion.
The default review date should be no later than one quarter after the row is
created. High-friction or host-binding candidates should be reviewed earlier.

Promotion decisions should record one of:

- `promote to protocol`
- `prototype repo-native check`
- `prototype host-native adapter`
- `move to CI`
- `keep evidence-only`
- `collect more evidence`
- `reject as low-signal enforcement`

This keeps AR-01 aligned with the architecture review intent: promote controls
only when measurement supports the trade-off, and preserve judgment-heavy work
as judgment-heavy work.
