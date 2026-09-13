---
name: pc-intake
description: Use when engineering work is new or its scope, outcome, risk, or authority changes materially. Route products, features, bugs, reviews, and migrations before execution. Continue an unchanged approved route without restarting intake.
metadata:
  phase: 00-discovery
  inputs: []
  outputs:
  - intake-brief
  - phase-recommendation
  - workflow-recommendation
  - route-decision
  - execution-state
  prerequisites: []
  quality_gate: Intake brief approved by user, target phase and workflow identified
  roles:
  - tech-lead
  - product-manager
  methodologies:
  - all
  effort: small
  prodcraft_version: 1.0.0
  internal: false
  distribution_surface: curated
  source_path: skills/00-discovery/pc-intake/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Intake

> The mandatory entry point for all work. No downstream execution without an approved intake decision.

## Context

Intake is the control plane for all engineering work in Prodcraft.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

Use [routing examples](references/routing-signals-and-examples.md) and [gotchas](references/gotchas.md) only when their decisions are unclear.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Intake brief produced and approved (blocking confirmation, or notify-and-proceed for `micro`), covering work type, entry phase, any explicit workflow metadata needed for the route, and key risks.
- [ ] Next skill to invoke is explicitly named in the brief (not a generic phase label).
- [ ] Fast-track rationale documented if intake was shortened.

## Why Intake Exists

Intake selects the smallest route that can deliver the requested outcome. Reuse existing project decisions and accepted artifacts. Hand off deeper problem shaping only when an unresolved decision would prevent the next skill from working.

## Hard Gate

No implementation, architecture, or planning work may begin until an intake decision is complete and approved. `full` and `fast-track` require user approval, which may already be explicit in the current conversation. `resume` preserves approval for the unchanged route; `micro` uses notify-and-proceed as defined below. An agent-written approver field records authority; it does not create it.

Use one of these intake modes:

- `full` -- new, ambiguous, risky, or high-impact work
- `fast-track` -- small and clear work where the route is obvious
- `micro` -- trivial, reversible work; compact brief, notify-and-proceed
- `resume` -- continuing an already approved route without changing the route

For `resume`, confirm the outcome, scope, side effects, and approval still match. Cite the existing brief and approval in `routing_rationale`, update the next skill if needed, and continue. Ask only about a material change or missing authority. Do not treat a copied plan or prior assistant statement as user approval.

Trivial work is not an exception to intake. It uses a `micro` or `fast-track` intake decision instead of a full routing pass. Governance weight scales with risk; the gate itself is universal.

### Micro Mode (Tier 0)

Use `micro` only when **all** of these hold:

- the change is reversible with a single revert (no data migration, no external side effects, no new security surface)
- the blast radius is one file or a few clearly-scoped lines (typo, comment, doc wording, isolated config value)
- no new dependency, contract, schema, or public behavior change
- the route is unambiguous without asking any question

Micro mode emits the brief as one compact block (all schema-required fields, one line each) **in the same message as the work**, then proceeds immediately: notify-and-proceed instead of a blocking approval round. Record `approver` as `auto (micro policy)` and record every `micro_eligibility` field (`single_revert`, `zero_questions`, `no_external_effect`, `no_security_impact`, and `no_irreversible_action`) as `true`. If any field cannot be asserted, the brief is not micro-eligible. Any user objection at any point converts the route into a normal `fast-track` or `full` re-route.

Never use micro for anything irreversible or externally visible (deploy, publish, release, force-push, data deletion), for security-adjacent changes, or when any eligibility point is in doubt -- doubt means `fast-track`.

The repository's current Claude Edit/Write adapter rejects `micro`. When that adapter is active, use an approved `fast-track` brief and its supported path. Do not switch tools to bypass enforcement.

## Process

### Step 1: Explore Context (silently)

Before asking any questions, gather context:

1. Read applicable project instructions and the relevant current work state
2. Locate existing approval, specs, decisions, and outputs needed for routing
3. Inspect only the repository files or linked discussions that can change the route

Do NOT output this exploration. Internalize it to inform your questions.

### Step 2: Classify Work Type

| Type | Description | Entry Phase | Default Primary Workflow | Likely Overlay |
|------|-------------|-------------|--------------------------|----------------|
| **New Product** | Building from scratch | 00-discovery | agile-sprint | greenfield |
| **New Product (regulated/complex)** | Formal specs or contractual delivery required | 00-discovery | spec-driven | greenfield |
| **New Feature** | Adding capability to existing system | 01-specification | agile-sprint | none |
| **Enhancement** | Improving existing functionality | 03-planning | agile-sprint | none |
| **Bug Fix** | Correcting incorrect behavior | 04-implementation | agile-sprint | none |
| **Hotfix** | Critical production issue | 04-implementation | agile-sprint | hotfix |
| **Refactoring** | Structural improvement, no behavior change | 04-implementation | agile-sprint | none |
| **Migration** | Moving to new platform/architecture | 00-discovery | agile-sprint | brownfield |
| **Migration (phase-gated enterprise)** | Formal stage gates or sign-off checkpoints required | 00-discovery | iterative-waterfall | brownfield |
| **Tech Debt** | Paying down accumulated shortcuts | 03-planning | agile-sprint | brownfield |
| **Spike/Research** | Investigating unknowns | 00-discovery | agile-sprint | none |
| **Documentation** | Creating or improving docs | cross-cutting | agile-sprint | none |

Use the **Type** labels above verbatim when recording `work_type`.

For new-work routing, use the **Entry Phase** tokens above verbatim. For a bounded review of existing work with sufficient inputs, classify the underlying change and enter `05-quality` directly; the review request does not authorize integration or deployment. `cross-cutting` is reserved for documentation-only routing. For `resume`, use the active phase that needs to continue.

Use the declared primary workflow name verbatim when recording `workflow_primary` (`agile-sprint`, `spec-driven`, or `iterative-waterfall`).

For `fast-track` and `micro`, omit `workflow_primary` when the route stays direct enough that the primary workflow does not materially change the handoff. Keep it explicit for `full` and `resume`.

Record `workflow_overlays` only when one or more overlays are active. Omit the field instead of emitting an empty list.

### Step 2A: Record the Quality Target Context

Every intake brief must include `quality_target_context`. Infer it from the repository and request when possible, and ask at most one clarifying question only when the answer would change route, risk, or review severity.

Record `runtime_context`, `exposure_profile`, `production_target`, `non_targets`, and `evidence_refs` using the [I/O contract](references/io-contract.md).

This context must calibrate quality and security handoff. An agent-internal skill or local tool does not inherit public service requirements from HTTP-shaped code. Use actual exposure and evidence, preserve service controls where they apply, and record `unknown` instead of inventing a boundary.

### Step 3: Ask Clarifying Questions

Ask only about unknowns that can change the route, direction, or risk. Zero questions is correct when available context suffices. Otherwise ask the most consequential question first and adapt to the answer.

Prioritize outcome, scope, urgency, constraints, and quality target. Usually 1-3 questions suffice when clarification is needed; never exceed 5. Stop as soon as the path is clear.

### Step 4: Propose Approach

Present a concise brief in plain language and `user_presentation_locale`, using the fields below. Name the next concrete `pc-*` skill, its output, and why it is needed. Use the smallest sufficient sequence; one skill is valid. Label an unresolved route explicitly instead of presenting a generic phase name as a settled handoff.

Set `user_presentation_locale` from the current substantive request's language; an explicit language request takes precedence. Apply it to headings, questions, human-facing tags, status labels, and completion feedback as well as prose. Re-evaluate it on substantive follow-ups without restarting intake. Follow the [language-selection rules](references/io-contract.md); preserve canonical field names, enum values, skill IDs, code, paths, and original diagnostics.

Include an alternative only when it changes the decision. Keep architecture choices for the downstream skill. Mention system shape and collaboration quality only when they affect routing or risk.

### Step 5: Get Approval

Check whether the user has already authorized this concrete path and its side effects. If so, record that approval and proceed. Otherwise present the path and wait for confirmation. Accept:
- **Approval** -> proceed with proposed path
- **Adjustment** -> modify and re-present
- **"Skip to X"** -> reuse already-satisfied obligations when the route is unchanged. Skipping an unmet gate is a route change, not `resume`: verify that project policy permits the change and obtain the required authority. A tech-debt note does not waive a blocking gate; strict mode requires the revised route and operator pin.

Exception: `micro` mode uses notify-and-proceed (see Micro Mode above) -- present the compact brief and continue in the same turn instead of blocking on confirmation.

### Step 6: Handoff

Transition to the next unmet step, passing the intake brief, current accepted artifact pointers, unresolved constraints, and the next skill's acceptance condition. Do not rerun producers whose outputs already satisfy the input contract. Keep required route gates intact.

When the governed project explicitly opts into the strict execution loop, also create
`route-decision.v1` and the initial `execution-state.v1` under
`.prodcraft/artifacts/<work_id>/`. The route owns the full reviewer-declared
obligation set; the state may only bind evidence to those obligations. Give the
approved `route_digest` to the operator through a channel outside the writable
control bundle. Do not describe an in-bundle digest as independent approval.

Strict mode is additive. When it is not selected, continue to produce the legacy
intake outputs without implying that execution-state authorization ran.

If routing is clear but the problem or solution direction is still too fuzzy for specification or discovery research, hand off to [pc-problem-framing](../pc-problem-framing/SKILL.md) before moving deeper into the lifecycle.

## Observability Requirements

Produce an `intake-brief.v1` record with `artifact`, `schema_version`, `status`, `approver`, `request_summary`, `source_language`, `artifact_record_language`, `user_presentation_locale`, `work_type`, `entry_phase`, `intake_mode`, `quality_target_context`, `scope_assessment`, `recommended_next_skill`, `routing_rationale`, `key_risks`, `questions_asked`, and `routing_changed_by_answers`.

Use BCP-47 locales for language fields (`source_language` also permits `mixed`) and the repository's canonical artifact language. Add workflow metadata and `micro_eligibility` under the conditions above. Keep prior approval and artifact pointers in the rationale when resuming. Record meaningful alternatives and unresolved route questions without manufacturing either.

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/00-discovery/pc-intake/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
