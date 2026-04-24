# Architecture State Bundle

## Part 1: Intent And Constraints

> This section is for top-level routing and automated acceptance-test design.
> It must not encode concrete implementation mechanics.

- Core Objective: Prodcraft's highest-value role is to move critical production-engineering discipline from model self-discipline into externalized, auditable, host-portable governance. Any sufficiently capable agent runtime should be constrained by the same repository-owned engineering protocols, while knowledge, state, constraints, and evidence move across consumer surfaces with minimal distortion.

```text
CANONICAL_OBJECTIVE :=
  GOVERN_PRODUCTION_ENGINEERING(
    host_agnostic = true,
    externalized_state = true,
    auditable = true,
    resistant_to_model_drift = true
  )
```

- Immutable Constraints:
  - Execution-critical claims must not rely on model self-discipline alone. Any rule that controls whether work may start, skip phases, or claim completion cannot live only in prompt text or skill prose.
  - Cross-phase and cross-session state must be externalized. Route choices, key assumptions, blockers, correction reasons, and verification boundaries cannot exist only in chat history or short-term model memory.
  - Repository-owned contracts remain sovereign. Claude, Codex, Gemini, and other host bindings may only adapt repository contracts; they must not become the only authoritative execution surface.
  - Low-fidelity proxy metrics must not masquerade as high-semantic engineering truth. A test file does not prove TDD; a review artifact does not prove high-quality review.
  - Public exported capability must not overclaim. Any capability that depends on internal protocol, enforcement, or evidence must not be presented as independently complete outside that context.
  - Accepted narrow decisions keep their anchor role. A broad architecture model must not overwrite narrower accepted ADRs unless a later, narrower, implementation-backed decision supersedes them.

```text
assert EXECUTION_CRITICAL_CLAIM != MODEL_SELF_DISCIPLINE_ONLY
assert CROSS_SESSION_CONTINUITY == EXTERNALIZED_STATE_REQUIRED
assert REPO_CONTRACT.authority == true
assert HOST_BINDING.authority == adapter_only
assert SEMANTIC_QUALITY != PROVEN_BY(cheap_proxy_only)
assert EXPORTED_CAPABILITY.must_match(actual_portability)
```

- Acceptance Assertions:
  - If new engineering work enters Prodcraft, then the system must form an explicit route decision and the minimum required protocol artifact before downstream execution begins.
  - If someone claims work is complete or directly jumps back across phases, then the system must require a valid state handoff and fresh evidence; otherwise the claim is not authoritative.
  - If a capability is exported to the public install surface, then its public shape must accurately describe the value that survives outside internal protocol and enforcement; otherwise it must be downgraded, caveated, or blocked from export.

## Part 2: Domain Topology And State Flow

> This section is for architecture, implementation planning, and future schema design.
> It is a logical model. A state or contract below is executable only after it is represented in repository-owned schemas, validators, workflow contracts, or manifest artifact flow.

- Core Domain Entities:
  - `WorkItem`: The engineering unit being governed. Lifecycle: `received -> routed -> gated -> executing -> completion_claimed -> verified -> completed`, with rejection or reroute as non-completion alternatives. `verified` confirms the completion claim against required artifacts and evidence; `completed` is the terminal operational and accounting state after verification has been accepted for the current route.
  - `RouteDecision`: The explicit decision about entry phase, recommended path, approval requirements, and required artifacts for a `WorkItem`. Lifecycle: `proposed -> approved -> active -> superseded`.
  - `ProtocolArtifact`: An externalized carrier of engineering state, such as `intake-brief`, `course-correction-note`, or `verification-record`. Lifecycle: `required -> drafted -> validated | rejected`; validated artifacts may become `consumed -> archived` or `superseded`, while rejected artifacts must be revised or superseded before they can satisfy a route.
  - `ControlRule`: An engineering discipline or boundary that may need system support. Lifecycle: `soft_guidance -> observed_failure -> promotion_candidate -> protocolized | repo_enforced | host_adapted | evidence_only`.
  - `EvidenceRecord`: Proof or challenge material for execution, verification, failure modes, or observed behavior. Lifecycle: `expected -> collected -> validated -> accepted | contested | stale`.
  - `ExportedCapability`: A public capability unit exposed through the install surface. Lifecycle: `internal_only -> export_evaluated -> portable_as_is | portable_with_caveat | blocked`.
  - `ConsumerSurface`: A system consumption surface. Current fixed set: `repo_internal`, `host_runtime`, `public_export`.
  - `ControlLoop`: A system control loop. Current fixed set: `repo_governance`, `downstream_execution`.

```text
LAYER := {Knowledge, Protocol, Enforcement, Evidence}
SURFACE := {repo_internal, host_runtime, public_export}
LOOP := {repo_governance, downstream_execution}

AUTHORITY:
  Knowledge      -> teaches judgment, does not prove compliance
  Protocol       -> preserves state and contract shape
  Enforcement    -> blocks, warns, or validates mechanically
  Evidence       -> proves or disproves real-world behavior

SHARED_INTERFACE_RULE:
  some_protocol_specs (for example schema contracts)
    are defined by Protocol
    consumed by Enforcement
    judged for adequacy by Evidence

EXAMPLE:
  intake_brief_schema      -> Protocol spec
  schema_validator_check   -> Enforcement mechanism
  routed_eval_and_findings -> Evidence of semantic adequacy
```

- State Transition Matrix:

```text
WorkItem:
  received -> routed
  routed -> gated
  gated -> executing
  executing -> completion_claimed | rerouted
  completion_claimed -> verified | rejected
  verified -> completed
  rejected -> gated | rerouted

RouteDecision:
  proposed -> approved
  approved -> active
  active -> superseded

ProtocolArtifact:
  required -> drafted
  drafted -> validated | rejected
  rejected -> drafted | superseded
  validated -> consumed | superseded
  consumed -> archived

ControlRule:
  soft_guidance -> observed_failure
  observed_failure -> promotion_candidate
  promotion_candidate -> protocolized
  promotion_candidate -> repo_enforced
  promotion_candidate -> evidence_only
  repo_enforced -> host_adapted(optional)

EvidenceRecord:
  expected -> collected
  collected -> validated | contested
  validated -> accepted | stale

ExportedCapability:
  internal_only -> export_evaluated
  export_evaluated -> portable_as_is
  export_evaluated -> portable_with_caveat
  export_evaluated -> blocked
```

- Conceptual Contract Candidates:

> The following blocks are architecture candidates, not executable API definitions.
> They are authoritative only as design intent until a follow-up change lands the relevant schema, registry entry, validator rule, workflow rule, or manifest artifact-flow update.

```text
Candidate: route_work(work_item)
input:
  - work_type
  - urgency
  - ambiguity_level
  - requested_surface
output:
  - route_id
  - entry_phase
  - required_artifacts[]
  - approval_required
rule:
  - NO_DOWNSTREAM_EXECUTION until route_id exists and required_artifacts are satisfied
repo-owned contract status:
  - partially represented today by intake-brief schema, workflow entry gates, and validator checks
```

```text
Candidate: submit_protocol_artifact(artifact)
input:
  - artifact_type
  - schema_version
  - payload
  - route_id
  - prior_artifact_refs[]
output:
  - schema_valid
  - missing_fields[]
  - semantic_review_required
rule:
  - schema_valid is necessary but not sufficient for semantic adequacy
repo-owned contract status:
  - represented only for artifacts registered in schemas/artifacts/registry.yml
```

```text
Candidate: claim_completion(work_item)
input:
  - work_id
  - route_id
  - artifact_refs[]
  - evidence_refs[]
  - claim_scope
output:
  - accepted | rejected
  - rejection_reasons[]
rule:
  - ACCEPT only if required protocol artifacts exist and fresh evidence is attached
  - Schema-level status alignment is necessary but not sufficient for route-level acceptance
repo-owned contract status:
  - verification-record.v1 now represents the first protocol foothold for completion-claim proof shape, including accepted/rejected status alignment
  - route-level acceptance or rejection remains future work until backed by workflow rules, artifact-flow checks, and semantic review for the specific route
```

```text
Candidate: promote_control_rule(rule)
input:
  - rule_id
  - failure_frequency
  - miss_cost
  - checkability
  - goodhart_risk
output:
  - stay_soft
  - add_protocol_contract
  - add_repo_enforcement
  - add_host_adapter
  - keep_evidence_only
rule:
  - REPO_ENFORCEMENT precedes HOST_ADAPTER whenever host-agnostic enforcement is possible
  - HIGH_GOODHART_RISK forbids cheap proxy hardening as proof of semantic quality
repo-owned contract status:
  - AR-01 now has a repository-owned measurement protocol; the executable decision matrix remains future work
```

```text
Candidate: classify_exported_capability(capability)
input:
  - capability_id
  - standalone_value
  - hidden_dependencies[]
  - required_context
output:
  - portable_as_is
  - portable_with_caveat
  - blocked
rule:
  - public description MUST NOT overstate robustness beyond surviving context
repo-owned contract status:
  - represented by schemas/distribution/public-skill-portability.json as the companion classification registry for the public export allowlist
  - skill-by-skill portability review remains future work beyond the initial landing zone
```

## Part 3: Evolution Log And Meta-Warnings

> This section is for code review and architecture retrospectives.
> It records trade-offs, rejected paths, and known architecture debt.

- Decision Tree:
  - Proposal A: "Prodcraft is just a governance framework disguised as skills" -> Why Not: This misidentifies the system. Prodcraft is not disguised; it is mixed. It contains knowledge, protocol state, execution constraints, and evidence contracts.
  - Proposal B: "Hooks and rules should take over most of the system, and skills should retreat" -> Why Not: Critical constraints do need externalization, but high-semantic engineering judgment cannot be safely compressed into cheap predicates. Over-hardening creates Goodhart drift.
  - Proposal C: "Distribution should become a fifth ontology layer" -> Why Not: Distribution describes who consumes the system and what they receive in transit. It is a consumer axis, not a content layer.
  - Proposal D: "Continue refining the architecture model through finer abstractions" -> Why Not: After three rounds, additional abstraction had lower expected value than converting stable agreement into enforceable work.
  - Proposal E: "Immediately create an umbrella ADR for the whole discussion" -> Why Not: That would present implementation-light, partially unsettled conclusions as accepted repository policy and dilute the narrow value of `ADR-001` and `ADR-002`.
  - Final compromise: Use `Knowledge / Protocol / Enforcement / Evidence` as the content ontology, with `ConsumerSurface` and `ControlLoop` as analysis axes. The trade-off is that some nuanced debate becomes historical source material instead of remaining in the canonical state record.
  - Review disposition: The latest Claude review was directionally right about ending open-ended meta-analysis and moving to execution. It was also right about dual loops, shared-interface schema, and distribution not being a fifth layer. However, it did not fully pin down sequencing, and `07a66673194d82c48fd6d6e71a2a18f896066c66` changed no repository files; a review session is not repository knowledge until recorded in canonical docs, checks, or ADRs.
  - ADR anchors remain: `ADR-001` remains the `Evidence / repo_governance` anchor. `ADR-002` remains the `Protocol / cross-phase continuity` anchor. This bundle does not replace them.

- Meta-Warnings:
  - Edge Case: Repository-size illusion. Total repository volume is not the same thing as runtime injected volume. Metadata is preloaded; bodies and supporting files are read on demand. The pressure point is the cumulative load of the path a task activates, not raw file count.
  - Edge Case: Review-persistence illusion. A review conversation or empty commit can make a decision feel landed. If it is not in a canonical document, repo-native check, or later ADR, it does not exist as engineering knowledge.
  - Edge Case: False-closed-loop illusion. A stronger repository authoring loop does not imply a stronger downstream execution loop. Confusing the two creates overconfidence.
  - Edge Case: Fast-track / hotfix state evaporation. Simplified entry paths can lose route decisions, constraints, and verification boundaries, making the resulting fix hard to audit.
  - Edge Case: Evidence freshness masquerade. Old verification records or benchmarks reused against new code state can create a false proof of completion. Evidence must bind to the current work state.
  - Edge Case: Host capture. If Claude, Codex, or Gemini bindings are designed before the repository contract, the system may be captured by the first host runtime's private affordances.
  - Edge Case: Public export overclaim. `.curated/` skills can lose internal protocol and enforcement context. Strong public claims must match what survives export.
  - Edge Case: Protocol bloat. Treating protocol/state as first-class does not make every artifact valuable. Artifacts that preserve format without decision value become governance noise.
  - Edge Case: Goodhart drift. Translating "real TDD", "real code review", or "real architecture quality" into low-signal checks pushes the system toward proxy optimization rather than engineering truth.
  - Edge Case: External discoverability gap. Internal routed invocation does not prove external public install users can discover and use the capabilities correctly.
  - Debt: There is no canonical enforcement promotion matrix yet, so promotion decisions still lack a unified decision table.
  - Debt: The downstream execution loop still lacks a complete first wave of repo-native constraints. `verification-record.v1` now covers proof-shape structure, but route entry and state handoff checks still need hardening.
  - Debt: A provisional host-binding adapter policy now exists, but it is not yet an accepted ADR and has no implemented adapters.
  - Debt: `.curated/` now has a portability landing zone and initial static review, but live full-repo versus curated-only benchmarking remains open.
  - Debt: Existing protocol artifacts still need an essential-vs-accidental audit; otherwise governance complexity can undermine the core value.
  - Source Lineage: Historical debate and details remain in `2026-04-17-prodcraft-architecture-evolution-basis.md`. Execution breakdown remains in `2026-04-17-architecture-review-action-register.md`. They are source and support documents, not the highest-level canonical architecture state.
