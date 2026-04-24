# AR-01 Enforcement Promotion Matrix

> Date: 2026-04-24
>
> Status: provisional planning artifact; not canonical architecture policy; not an ADR; not an enforcement contract.
>
> Parent plan:
> [`2026-04-24-connected-architecture-evolution-plan.md`](./2026-04-24-connected-architecture-evolution-plan.md)
>
> Measurement protocol:
> [`ar-01-enforcement-promotion-measurement-protocol.md`](../../architecture/ar-01-enforcement-promotion-measurement-protocol.md)

## Source Documents

- `docs/architecture/2026-04-18-prodcraft-architecture-state-bundle.md`
- `docs/architecture/2026-04-17-architecture-review-action-register.md`
- `docs/architecture/ar-01-enforcement-promotion-measurement-protocol.md`
- `docs/plans/architecture-evolution/2026-04-24-connected-architecture-evolution-plan.md`
- `schemas/artifacts/registry.yml`
- `schemas/distribution/public-skill-registry.json`
- `schemas/distribution/public-skill-portability.json`
- `scripts/validate_prodcraft.py`
- `tests/`
- `manifest.yml`
- `skills/_quality-assurance.md`
- `rules/security.yml`

## Scope

This matrix converts AR-01 from a measurement protocol into an initial set of
candidate promotion decisions. It is a reviewable planning artifact, not a rule
source. It does not make any control executable by itself, and it does not assert
that any control proves semantic adequacy.

A row becomes authoritative only after the corresponding control lands in an
accepted schema, registry, validator, workflow contract, rule source, CI check,
manifest artifact flow, or ADR.

## Non-Goals

- Do not infer that `repo-native enforcement` rows already prove route quality.
- Do not treat host approval behavior as repository policy.
- Do not promote broad prompt-injection, command-safety, secret, PII, or
  semantic-review claims from keyword scans.
- Do not use this matrix as public export policy; public distribution remains
  governed by the distribution registries and curated export checks.

## Authority Boundary

This file recommends where each candidate should go next. It is below accepted
schemas, validators, workflow contracts, artifact registries, rules, ADRs, and
the canonical architecture state bundle. If this file conflicts with any of
those sources, the executable or canonical source wins.

## Validation Expectations

While provisional, this file should be protected only by lightweight structural
tests:

- every Decision Index ID has one matching measurement record
- each record carries the AR-01 measurement fields
- each record states a semantic boundary
- status and non-claims remain explicit

It should not be wired into `scripts/validate_prodcraft.py` until a specific row
graduates into an executable repository contract.

## Sample Window

Unless a row states otherwise, the sample window is the checked-in Prodcraft
repository baseline on 2026-04-24, with emphasis on:

- `docs/architecture/`
- `docs/plans/architecture-evolution/`
- `schemas/artifacts/`
- `schemas/distribution/`
- `scripts/validate_prodcraft.py`
- `tests/`
- `manifest.yml`
- `rules/cross-cutting-matrix.yml`
- `rules/security.yml`
- `.githooks/pre-commit`
- `scripts/hooks/no_magic_values_scan.py`
- `skills/`

The default review date for initial rows is 2026-07-24 unless a row is promoted,
rejected, or superseded earlier.

## Decision Index

| ID | Rule or discipline name | Recommended next move | Recommended surface |
|---|---|---|---|
| AR01-C01 | Workflow entry declares required `intake-brief` | Keep existing entry-gate check as baseline | repo-native enforcement |
| AR01-C02 | Intake route metadata remains schema-closed | Keep existing schema and validator contract | protocol and repo-native enforcement |
| AR01-C03 | Direct phase jumps require `course-correction-note` | Keep existing schema, ADR, and gateway alignment | protocol and repo-native enforcement |
| AR01-C04 | Completion claims require accepted verification proof shape | Prototype route-level validator usage | repo-native enforcement |
| AR01-C05 | Verification evidence binds to current work state | Prototype freshness check | repo-native enforcement |
| AR01-C06 | Artifact schemas and templates stay synchronized | Keep existing registry check as baseline | repo-native enforcement |
| AR01-C07 | Manifest artifact flow matches skill inputs and outputs | Keep existing artifact-flow check as baseline | repo-native enforcement |
| AR01-C08 | Default workflows do not silently depend on draft skills | Keep existing workflow maturity check as baseline | repo-native enforcement |
| AR01-C09 | Public export requires portability metadata and no blocked exports | Keep existing curated-surface check as baseline | repo-native enforcement |
| AR01-C10 | Localized or public docs cannot override canonical contracts | Keep existing documentation contract | repo-native enforcement |
| AR01-C11 | External skill ideas must be re-expressed as local contracts | Collect bounded evidence before enforcement expansion | protocol |
| AR01-C12 | Skill discovery metadata resists minimal injection payloads | Keep minimal scanner; collect misses | repo-native enforcement |
| AR01-C13 | Command safety requires explicit scope and approval basis | Keep protocol-led; defer host adapter | protocol |
| AR01-C14 | Prompt injection authority boundaries are explicit | Collect evidence before enforcement | protocol and evidence only |
| AR01-C15 | Secrets and PII must not leak into artifacts or logs | Collect evidence; prototype narrow scanner later | protocol and CI candidate |
| AR01-C16 | Magic values and hardcoded configuration are review-blocking | Collect scanner evidence before CI promotion | hook and CI candidate |
| AR01-C17 | Dynamic remote instruction imports are prohibited unless reviewed locally | Inventory checked-in references before enforcement | protocol and evidence only |

## Measurement Records

### AR01-C01: Workflow entry declares required `intake-brief`

- Rule or discipline name: Workflow entry declares required `intake-brief`.
- Current home: `workflow`, `validator`.
- Failure mode: A workflow presents itself as a valid Prodcraft route without
  declaring `intake` as the entry skill or requiring an `intake-brief`.
- Observed evidence source: `scripts/validate_prodcraft.py`
  `workflow-entry-gate`; workflow frontmatter in `workflows/*.md`.
- Failure frequency estimate: none observed in current validation.
- Cost if missed: high; downstream work can begin without route state,
  approval context, or required artifacts.
- Checkability: high for declaration shape; low for the semantic validity of a
  particular intake instance.
- Goodhart risk: low for the entry declaration; medium if the declaration is
  treated as proof that intake judgment was correct.
- Recommended next move: keep existing entry-gate check as baseline.
- Recommended surface: `repo-native enforcement`.
- Owner: maintainers.
- Evidence source class: `validator result`.
- Sample window: 2026-04-24 checked-in workflows and validator implementation.
- False-positive risk: low; valid workflows should declare the same entry
  contract.
- False-negative risk: medium; a valid entry shape does not prove route
  quality.
- Friction cost: low; workflow declarations are stable.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: proves declared workflow entry shape only; does not prove
  that any concrete `intake-brief` instance is valid or sufficient.

### AR01-C02: Intake route metadata remains schema-closed

- Rule or discipline name: Intake route metadata remains schema-closed.
- Current home: `schema`, `validator`, `template`, `test`.
- Failure mode: Intake records drift into open-ended prose, invalid work types,
  invalid phases, or ambiguous language-boundary fields.
- Observed evidence source: `schemas/artifacts/intake-brief.schema.json`;
  `templates/intake-brief.md`; `validate_intake_brief_schema_contract`;
  `tests/test_intake_schema_semantics.py`;
  `tests/test_artifact_schema_registry.py`.
- Failure frequency estimate: none observed in current validation.
- Cost if missed: high; route state becomes hard to replay across sessions and
  host runtimes.
- Checkability: high for field shape and enum alignment; low for route judgment
  quality.
- Goodhart risk: low for closed fields; medium if treated as proof that routing
  was correct.
- Recommended next move: keep existing schema and validator contract.
- Recommended surface: `protocol` and `repo-native enforcement`.
- Owner: maintainers.
- Evidence source class: `validator result`.
- Sample window: 2026-04-24 checked-in intake schema, template, registry, and
  tests.
- False-positive risk: low; invalid enum or missing-field failures are
  concrete.
- False-negative risk: medium; valid fields can still carry weak rationale.
- Friction cost: low; writers already produce the artifact.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: proves intake artifact shape and allowed values only; does
  not prove that the selected route is strategically right.

### AR01-C03: Direct phase jumps require `course-correction-note`

- Rule or discipline name: Direct phase jumps require `course-correction-note`.
- Current home: `ADR`, `gateway`, `schema`, `validator`, `template`, `test`.
- Failure mode: A later phase jumps back across the lifecycle without
  preserving trigger, evidence, blocked artifact, constraints, and reapproval
  requirement.
- Observed evidence source:
  `docs/adr/ADR-002-cross-phase-course-corrections.md`; `skills/_gateway.md`;
  `schemas/artifacts/course-correction-note.schema.json`;
  `validate_course_correction_schema_contract`;
  `tests/test_course_correction_contract.py`.
- Failure frequency estimate: none observed in current validation.
- Cost if missed: high; cross-phase corrections lose state and can restart work
  under false assumptions.
- Checkability: high for approved jump pairs and required fields; medium for
  evidence adequacy.
- Goodhart risk: medium; teams can fill the form without preserving real
  decision value.
- Recommended next move: keep existing schema, ADR, and gateway alignment.
- Recommended surface: `protocol` and `repo-native enforcement`.
- Owner: maintainers.
- Evidence source class: `validator result`.
- Sample window: 2026-04-24 checked-in ADR-002, gateway, schema, template, and
  tests.
- False-positive risk: low for invalid jump pairs; medium when a legitimate
  urgent correction has incomplete evidence.
- False-negative risk: medium; a valid note may still omit important context in
  prose fields.
- Friction cost: medium; direct jumps are exceptional but require structured
  evidence.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: proves that direct-jump state has a required carrier; does
  not prove that the correction decision was optimal.

### AR01-C04: Completion claims require accepted verification proof shape

- Rule or discipline name: Completion claims require accepted verification proof
  shape.
- Current home: `schema`, `validator`, `template`, `skill`,
  `manifest artifact_flow`, `test`.
- Failure mode: A delivery or completion statement claims work is done while
  verification status is draft or rejected, checks are skipped, failures remain,
  or unverified scope remains.
- Observed evidence source:
  `schemas/artifacts/verification-record.schema.json`;
  `templates/verification-record.md`;
  `skills/cross-cutting/verification-before-completion/SKILL.md`;
  `skills/06-delivery/delivery-completion/SKILL.md`;
  `validate_verification_record_schema_contract`;
  `tests/test_artifact_schema_registry.py`; `manifest.yml`.
- Failure frequency estimate: recent architecture hardening identified false
  completion claims as high-cost; no row-level route sample has been counted
  yet.
- Cost if missed: high; false completion claims undermine downstream execution
  trust.
- Checkability: high for proof shape; low for semantic completeness of the
  checked work.
- Goodhart risk: medium; teams may optimize for passing checks instead of
  meaningful verification.
- Recommended next move: prototype route-level validator usage.
- Recommended surface: `repo-native enforcement`.
- Owner: maintainers.
- Evidence source class: `validator result`.
- Sample window: 2026-04-24 checked-in `verification-record.v1` schema,
  template, manifest artifact flow, skills, and tests.
- False-positive risk: low for impossible status/proof combinations.
- False-negative risk: medium; stale or irrelevant evidence can still satisfy
  shape.
- Friction cost: medium; completion claims need explicit evidence references.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: proves proof-shape eligibility for a claim; does not prove
  the claimed work is complete, current, or strategically sufficient.

### AR01-C05: Verification evidence binds to current work state

- Rule or discipline name: Verification evidence binds to current work state.
- Current home: `schema`, `skill`, `planning buffer`.
- Failure mode: Old or unrelated verification evidence is reused against a
  changed work state and creates a false proof of completion.
- Observed evidence source: `verification-record.v1` `work_state_ref`;
  architecture state bundle evidence-freshness debt; this connected plan.
- Failure frequency estimate: risk identified by architecture review; no
  bounded failure count yet.
- Cost if missed: high; the system can falsely close work after code, docs, or
  generated artifacts change.
- Checkability: medium; work-state identity can be checked structurally, but
  semantic freshness needs route-specific review.
- Goodhart risk: medium; shallow `work_state_ref` values can become ceremony.
- Recommended next move: prototype freshness check.
- Recommended surface: `repo-native enforcement`.
- Owner: maintainers.
- Evidence source class: `repository trace`.
- Sample window: 2026-04-24 checked-in verification-record contract and
  architecture planning docs.
- False-positive risk: medium; legitimate evidence can be hard to bind when the
  work state is multi-file or non-code.
- False-negative risk: medium; a syntactically current reference can still point
  to inadequate evidence.
- Friction cost: medium; contributors must identify the work state they
  verified.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: can prove explicit work-state binding only; cannot prove
  that the selected state reference captures every relevant change.

### AR01-C06: Artifact schemas and templates stay synchronized

- Rule or discipline name: Artifact schemas and templates stay synchronized.
- Current home: `schema`, `template`, `validator`, `test`.
- Failure mode: A required artifact field exists in schema but not in the
  template, so humans and agents produce incomplete records.
- Observed evidence source: `schemas/artifacts/registry.yml`;
  `validate_artifact_schema_registry`; `tests/test_artifact_schema_registry.py`.
- Failure frequency estimate: none observed in current validation.
- Cost if missed: medium; artifact records become non-conforming or force
  contributors to reconstruct hidden requirements.
- Checkability: high.
- Goodhart risk: low; this checks contract presence, not semantic adequacy.
- Recommended next move: keep existing registry check as baseline.
- Recommended surface: `repo-native enforcement`.
- Owner: maintainers.
- Evidence source class: `validator result`.
- Sample window: 2026-04-24 checked-in artifact registry, schemas, templates,
  and tests.
- False-positive risk: low.
- False-negative risk: low for required field markers; high for semantic
  adequacy of guidance text.
- Friction cost: low.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: proves schema-template field alignment only; does not prove
  that template prose teaches high-quality artifact authoring.

### AR01-C07: Manifest artifact flow matches skill inputs and outputs

- Rule or discipline name: Manifest artifact flow matches skill inputs and
  outputs.
- Current home: `manifest`, `skill metadata`, `validator`, `test`.
- Failure mode: A skill declares inputs or outputs that are not represented in
  manifest artifact flow, weakening cross-skill state continuity.
- Observed evidence source: `manifest.yml`; lifecycle skill frontmatter;
  `validate_artifact_flow`; `tests/test_p0_execution_gap_skills.py`.
- Failure frequency estimate: none observed in current validation.
- Cost if missed: medium; handoff expectations drift away from the repository's
  artifact graph.
- Checkability: high for declared metadata; medium for artifacts not yet
  governed by schema.
- Goodhart risk: low.
- Recommended next move: keep existing artifact-flow check as baseline.
- Recommended surface: `repo-native enforcement`.
- Owner: maintainers.
- Evidence source class: `validator result`.
- Sample window: 2026-04-24 checked-in manifest and lifecycle skill
  frontmatter.
- False-positive risk: low.
- False-negative risk: medium; manifest alignment does not prove artifact
  quality.
- Friction cost: low.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: proves declared metadata and manifest flow alignment only;
  does not prove that handoffs preserve all needed context.

### AR01-C08: Default workflows do not silently depend on draft skills

- Rule or discipline name: Default workflows do not silently depend on draft
  skills.
- Current home: `manifest`, `workflow`, `validator`, `test`.
- Failure mode: A workflow presents a route as ready while depending on skills
  that remain `draft`.
- Observed evidence source: `manifest.yml`; workflow Markdown;
  `validate_workflow_skill_references`; `tests/test_workflow_composability.py`.
- Failure frequency estimate: none observed in current validation.
- Cost if missed: high; public or default routes overstate repository maturity.
- Checkability: high for explicit workflow references.
- Goodhart risk: low; this is a maturity-label consistency check.
- Recommended next move: keep existing workflow maturity check as baseline.
- Recommended surface: `repo-native enforcement`.
- Owner: maintainers.
- Evidence source class: `validator result`.
- Sample window: 2026-04-24 checked-in workflows and manifest.
- False-positive risk: low; draft dependencies can still appear when explicitly
  marked experimental or planned.
- False-negative risk: medium; prose can imply readiness without using explicit
  skill references.
- Friction cost: low.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: proves explicit workflow-reference maturity only; does not
  prove the workflow is complete or operationally sufficient.

### AR01-C09: Public export requires portability metadata and no blocked exports

- Rule or discipline name: Public export requires portability metadata and no
  blocked exports.
- Current home: `distribution registry`, `portability registry`, `exporter`,
  `validator`, `test`.
- Failure mode: A public skill is exported without caveats, hidden-dependency
  classification, or with a blocked portability state.
- Observed evidence source:
  `schemas/distribution/public-skill-registry.json`;
  `schemas/distribution/public-skill-portability.json`;
  `scripts/export_curated_skills.py`; `validate_curated_surface`;
  `tests/test_manifest_governance.py`;
  `tests/test_curated_distribution_surface.py`.
- Failure frequency estimate: none observed in current validation; the current
  public surface is conservatively classified.
- Cost if missed: high; public users may infer full governance guarantees from a
  portable package.
- Checkability: high for metadata presence and blocked-export prevention.
- Goodhart risk: medium; metadata can be filled without live portability
  evidence.
- Recommended next move: keep existing curated-surface check as baseline.
- Recommended surface: `repo-native enforcement`.
- Owner: maintainers.
- Evidence source class: `validator result`.
- Sample window: 2026-04-24 checked-in distribution registries, exporter,
  curated index, and tests.
- False-positive risk: low.
- False-negative risk: medium; `portable_with_caveat` truth still needs live
  full-repo versus curated-only benchmark evidence.
- Friction cost: low.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: proves portability metadata and export blocking only; does
  not prove that a curated-only user preserves route quality.

### AR01-C10: Localized or public docs cannot override canonical contracts

- Rule or discipline name: Localized or public docs cannot override canonical
  contracts.
- Current home: `README`, `CLAUDE.md`, `test`.
- Failure mode: A localized reader guide or public-facing doc becomes a hidden
  source of repository policy.
- Observed evidence source: `README.md`; `README.zh-CN.md`; `CLAUDE.md`;
  `tests/test_readme_contract.py`; `tests/test_public_skill_positioning.py`.
- Failure frequency estimate: none observed after the language-policy update;
  risk is structurally likely when localized or public docs exist.
- Cost if missed: medium; users can follow a non-canonical policy that conflicts
  with schemas, validators, or architecture state.
- Checkability: medium; tests can constrain locations and disclaimers, but not
  every possible overclaim.
- Goodhart risk: medium; disclaimers can exist while prose still overstates
  authority.
- Recommended next move: keep existing documentation contract.
- Recommended surface: `repo-native enforcement`.
- Owner: maintainers.
- Evidence source class: `repository trace`.
- Sample window: 2026-04-24 checked-in README files, CLAUDE policy, public-skill
  positioning checks, and README contract tests.
- False-positive risk: low for CJK boundary checks; medium for wording checks.
- False-negative risk: medium; English public docs can still overclaim without
  violating CJK checks.
- Friction cost: low.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: proves documented authority disclaimers and language
  boundaries only; does not prove every public sentence is free of overclaim.

### AR01-C11: External skill ideas must be re-expressed as local contracts

- Rule or discipline name: External skill ideas must be re-expressed as local
  contracts.
- Current home: `CLAUDE.md`, `README.md`, `test`.
- Failure mode: External skill systems, web guidance, or package docs become
  implicit runtime dependencies or repository authority without local contract
  expression.
- Observed evidence source: `CLAUDE.md`; `README.md`;
  `tests/test_external_skill_integration_boundary.py`.
- Failure frequency estimate: none observed in current tests.
- Cost if missed: medium; authority moves outside the repository and undermines
  host-portable governance.
- Checkability: medium for explicit source-level references; low for conceptual
  borrowing.
- Goodhart risk: medium; a ban on references can discourage useful attribution
  without improving governance.
- Recommended next move: collect bounded evidence before enforcement expansion.
- Recommended surface: `protocol`.
- Owner: maintainers.
- Evidence source class: `repository trace`.
- Sample window: 2026-04-24 checked-in integration-boundary docs and tests.
- False-positive risk: medium; not every external mention is a dependency.
- False-negative risk: medium; implicit dependency can exist without a direct
  text reference.
- Friction cost: low if kept as protocol guidance.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: can govern explicit authority claims and checked-in
  dependencies only; cannot detect every conceptual influence.

### AR01-C12: Skill discovery metadata resists minimal injection payloads

- Rule or discipline name: Skill discovery metadata resists minimal injection
  payloads.
- Current home: `validator`.
- Failure mode: Skill descriptions contain hidden characters, shell-pipe
  injection patterns, or homoglyph substitutions that can influence discovery or
  execution.
- Observed evidence source: `validate_skill_security_minimal` and related
  scanner constants in `scripts/validate_prodcraft.py`.
- Failure frequency estimate: none observed in current validation.
- Cost if missed: medium; malicious or ambiguous metadata can alter skill
  discovery and trust.
- Checkability: high for current minimal patterns; low for broader
  prompt-injection classes.
- Goodhart risk: medium; narrow scanners can create false confidence.
- Recommended next move: keep minimal scanner; collect misses.
- Recommended surface: `repo-native enforcement`.
- Owner: maintainers.
- Evidence source class: `validator result`.
- Sample window: 2026-04-24 checked-in lifecycle skill descriptions.
- False-positive risk: low for hidden characters and obvious pipe patterns.
- False-negative risk: high for semantic prompt injection beyond these patterns.
- Friction cost: low.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: proves only the narrow metadata patterns currently
  scanned; does not prove prompt-injection resistance.

### AR01-C13: Command safety requires explicit scope and approval basis

- Rule or discipline name: Command safety requires explicit scope and approval
  basis.
- Current home: `host policy`, `skill guidance`, `architecture protocol
  candidate`.
- Failure mode: An agent runs destructive, privileged, broad, or externally
  side-effectful commands without clear scope or approval basis.
- Observed evidence source: current agent runtime approval policy;
  command-safety expectations in quality skills; AR-01 security control
  candidate.
- Failure frequency estimate: no repository-owned incident sample in this
  matrix.
- Cost if missed: high; unsafe commands can destroy data or bypass user intent.
- Checkability: low in repository-only checks; medium in host adapters after
  repository policy is explicit.
- Goodhart risk: high; static command-name lists overblock legitimate work and
  miss context-dependent danger.
- Recommended next move: keep protocol-led; defer host adapter.
- Recommended surface: `protocol`.
- Owner: maintainers with host adapter reviewers.
- Evidence source class: `manual audit`.
- Sample window: 2026-04-24 checked-in repository docs plus current host approval
  model.
- False-positive risk: high for broad static enforcement.
- False-negative risk: high without host-runtime context.
- Friction cost: high if enforced too early.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: can require explicit scope and approval records; cannot
  decide command safety without runtime context.

### AR01-C14: Prompt injection authority boundaries are explicit

- Rule or discipline name: Prompt injection authority boundaries are explicit.
- Current home: `protocol`, `skill guidance`, `architecture protocol
  candidate`.
- Failure mode: Untrusted artifact, web, package, or generated content is
  treated as instructions that override repository, user, system, or developer
  authority.
- Observed evidence source: AR-01 initial security candidate set; external-skill
  boundary docs; architecture state bundle authority rules;
  `skills/_quality-assurance.md`.
- Failure frequency estimate: no bounded repository failure count yet.
- Cost if missed: high; untrusted text can redirect execution or corrupt
  artifacts.
- Checkability: low for semantic instruction-following; medium for explicit
  artifact authority labels.
- Goodhart risk: high; keyword filters can miss real attacks and block harmless
  examples.
- Recommended next move: collect evidence before enforcement.
- Recommended surface: `protocol` and `evidence only`.
- Owner: maintainers.
- Evidence source class: `security review`.
- Sample window: 2026-04-24 checked-in architecture docs, boundary tests, and
  quality-assurance guidance.
- False-positive risk: high for content scanners.
- False-negative risk: high for semantic attacks.
- Friction cost: medium if kept in protocol; high if statically enforced.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: can label trusted and untrusted authority surfaces; cannot
  prove an agent will resist prompt injection.

### AR01-C15: Secrets and PII must not leak into artifacts or logs

- Rule or discipline name: Secrets and PII must not leak into artifacts or logs.
- Current home: `skill guidance`, `security review`, `CI candidate`.
- Failure mode: Secrets, credentials, personal data, or sensitive customer
  context are stored in docs, examples, eval output, logs, or generated
  artifacts.
- Observed evidence source: AR-01 security candidate set; `rules/security.yml`;
  `skills/05-quality/code-review/SKILL.md`; `skills/05-quality/security-audit/SKILL.md`;
  current validator has no broad secret scanner.
- Failure frequency estimate: no bounded repository failure count in this
  matrix.
- Cost if missed: high; exposure can create security, privacy, and compliance
  incidents.
- Checkability: medium for common secret patterns; low for contextual PII.
- Goodhart risk: medium; scanners can produce noisy false positives and still
  miss real secrets.
- Recommended next move: collect evidence; prototype narrow scanner later.
- Recommended surface: `protocol` and `CI candidate`.
- Owner: maintainers with security reviewer.
- Evidence source class: `security review`.
- Sample window: 2026-04-24 checked-in security guidance and repository
  validation gaps.
- False-positive risk: medium for secret scanners; high for PII scanners.
- False-negative risk: medium for secrets; high for contextual PII.
- Friction cost: medium.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: can target narrow secret-pattern leakage later; cannot
  statically prove absence of contextual PII or sensitive business context.

### AR01-C16: Magic values and hardcoded configuration are review-blocking

- Rule or discipline name: Magic values and hardcoded configuration are
  review-blocking.
- Current home: `skill`, `hook`, `script`, `docs`.
- Failure mode: Domain thresholds, hardcoded hosts, IDs, URLs, emails, ports, or
  long string identifiers enter source without a named constant, configuration
  boundary, or approved exception.
- Observed evidence source: `skills/05-quality/code-review/SKILL.md`;
  `.githooks/pre-commit`; `scripts/hooks/no_magic_values_scan.py`;
  `docs/quality/magic-value-governance.md`.
- Failure frequency estimate: no current scanner-result sample is included in
  this matrix.
- Cost if missed: medium; environment-specific configuration or hidden policy
  thresholds become brittle.
- Checkability: medium; heuristic scanning catches common cases but cannot prove
  domain intent.
- Goodhart risk: medium; contributors can rename literals without improving
  configuration design.
- Recommended next move: collect scanner evidence before CI promotion.
- Recommended surface: `hook` and `CI candidate`.
- Owner: maintainers.
- Evidence source class: `repository trace`.
- Sample window: 2026-04-24 checked-in hook, scanner, docs, and code-review
  skill.
- False-positive risk: medium; heuristic scanners can flag examples or protocol
  literals.
- False-negative risk: medium; semantic magic values can be hidden behind named
  variables.
- Friction cost: medium.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: can surface likely hardcoded configuration for review; does
  not prove a literal is domain-dangerous or that a named constant is well
  designed.

### AR01-C17: Dynamic remote instruction imports are prohibited unless reviewed locally

- Rule or discipline name: Dynamic remote instruction imports are prohibited
  unless reviewed locally.
- Current home: `protocol`, `skill guidance`, `security review`.
- Failure mode: A workflow, skill, or helper imports or obeys mutable remote
  instructions during work without repository review or local contract
  expression.
- Observed evidence source: AR-01 initial security candidate set;
  `skills/_quality-assurance.md` supply-chain checklist;
  `eval/05-quality/security-audit/evals/security-check-evidence.md`.
- Failure frequency estimate: no bounded repository inventory has been completed
  yet.
- Cost if missed: high; mutable remote guidance can bypass repository review and
  alter agent behavior at runtime.
- Checkability: medium for checked-in fetch-and-execute instruction patterns;
  low for live research or browser use.
- Goodhart risk: high if implemented as a URL ban; valid attribution and
  package references would be suppressed without improving runtime safety.
- Recommended next move: inventory checked-in references before enforcement.
- Recommended surface: `protocol` and `evidence only`.
- Owner: maintainers with security reviewer.
- Evidence source class: `manual audit`.
- Sample window: 2026-04-24 checked-in quality-assurance guidance and security
  audit evidence; no full repository inventory yet.
- False-positive risk: high for URL or domain bans.
- False-negative risk: medium; dynamic instruction dependency can be indirect.
- Friction cost: medium if kept as inventory; high if enforced as broad block.
- Decision owner: maintainers.
- Review date: 2026-07-24.
- Semantic boundary: can target explicit checked-in mutable instruction imports;
  cannot govern ordinary external research unless a repository-owned adapter
  contract defines that boundary.

## Promotion Groups

Keep as baseline repo-native structural checks:

- AR01-C01
- AR01-C02
- AR01-C03
- AR01-C06
- AR01-C07
- AR01-C08
- AR01-C09
- AR01-C10
- AR01-C12

Prototype next as narrow repo-native checks:

- AR01-C04
- AR01-C05

Collect evidence before CI or hook promotion:

- AR01-C16

Keep evidence-led or protocol-led for now:

- AR01-C11
- AR01-C13
- AR01-C14
- AR01-C15
- AR01-C17

## Graduation Path

This matrix remains in `docs/plans/architecture-evolution/` while provisional.
Individual rows may graduate independently:

- schema or artifact-flow controls graduate into `schemas/`, templates,
  `manifest.yml`, and tests
- repository checks graduate into `scripts/validate_prodcraft.py`, hooks, or CI
- workflow controls graduate into workflow contracts and gateway tests
- durable policy decisions graduate into a narrow ADR
- judgment-heavy or low-checkability rows remain protocol-led or evidence-only

Graduation should update or supersede the affected row rather than silently
leaving the planning matrix stale.

## Explicit Non-Claims

- This matrix does not prove semantic adequacy.
- It does not assert that any control is enforced unless an accepted schema,
  validator, workflow contract, rule, CI check, manifest artifact flow, or ADR
  also says so.
- It does not make a host adapter authoritative.
- It does not promote any public skill to `portable_as_is`.
- It does not make `verification-record.v1` a complete route-level acceptance
  system.
- It does not replace human or agent review for judgment-heavy work.
