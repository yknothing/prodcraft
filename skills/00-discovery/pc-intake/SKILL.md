---
name: pc-intake
description: 'The mandatory gateway for all new engineering work. Triage and route new products, apps, features, migrations, tech-debt, or any ''not sure where to start'' request to the correct lifecycle path. Use before starting design or implementation. Do not use for ongoing tasks, specific debugging, or PR reviews.'
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
---

# Intake

> The mandatory entry point for all work. No downstream execution without an approved intake decision.

## Context

Intake is the control plane for all engineering work in Prodcraft. Every piece of work — feature, bug fix, refactoring, migration, or research — enters the lifecycle through intake. Its job is to classify the work type, route to the correct lifecycle phase and methodology, and produce the `intake-brief` that anchors every downstream skill. It is triage, not a design session.

## Inputs

- **user-request** -- the raw description of the work to be done
- **existing-context** -- project documentation, recent commits, open issues (read silently before asking questions)

## Outputs

- **intake-brief** -- structured routing record: request summary, `source_language`, `artifact_record_language`, `user_presentation_locale`, intake mode, work type, entry phase, `quality_target_context`, workflow metadata (`workflow_primary` when governance is explicit, `workflow_overlays` when an overlay is active), next skill, routing rationale, key risks
- **phase-recommendation** -- the lifecycle phase where work should begin
- **workflow-recommendation** -- the methodology best suited to the work
- **route-decision** -- optional strict-mode approved route, workflow focus, obligations, revision, and operator-pinned digest
- **execution-state** -- optional strict-mode initial routed state bound to that route decision

## Quality Gate

- [ ] Intake brief produced and approved (blocking confirmation, or notify-and-proceed for `micro`), covering work type, entry phase, any explicit workflow metadata needed for the route, and key risks.
- [ ] Next skill to invoke is explicitly named in the brief (not a generic phase label).
- [ ] Fast-track rationale documented if intake was shortened.

## Why Intake Exists

Every piece of work -- a new feature, a bug fix, a refactoring, a migration -- enters the lifecycle somewhere. Intake determines **where** and **how** to proceed. Think of it as hospital triage for software: assess the situation, determine urgency and scope, route to the right treatment.

Without intake, teams jump straight to coding and discover mid-way that they're solving the wrong problem, using the wrong approach, or missing critical constraints. Thirty seconds of triage prevents hours of wasted effort.

Intake is the **control plane** for entry, not the full discovery workshop. Its job is to classify, route, and make the next step observable. If deeper concept shaping is needed after routing is chosen, hand off to a downstream discovery skill rather than turning intake into a long design session.

## Hard Gate

No implementation, architecture, or planning work may begin until an intake decision is complete and approved. Approval is a blocking user confirmation for `full`, `fast-track`, and `resume`; `micro` mode uses notify-and-proceed as defined below.

Use one of these intake modes:

- `full` -- new, ambiguous, risky, or high-impact work
- `fast-track` -- small and clear work where the route is obvious
- `micro` -- trivial, reversible work; compact brief, notify-and-proceed
- `resume` -- continuing an already approved route without changing the route

Trivial work is not an exception to intake. It uses a `micro` or `fast-track` intake decision instead of a full routing pass. Governance weight scales with risk; the gate itself is universal.

### Micro Mode (Tier 0)

Use `micro` only when **all** of these hold:

- the change is reversible with a single revert (no data migration, no external side effects, no new security surface)
- the blast radius is one file or a few clearly-scoped lines (typo, comment, doc wording, isolated config value)
- no new dependency, contract, schema, or public behavior change
- the route is unambiguous without asking any question

Micro mode emits the brief as one compact block (all schema-required fields, one line each) **in the same message as the work**, then proceeds immediately: notify-and-proceed instead of a blocking approval round. Record `approver` as `auto (micro policy)`. Any user objection at any point converts the route into a normal `fast-track` or `full` re-route.

Never use micro for anything irreversible or externally visible (deploy, publish, release, force-push, data deletion), for security-adjacent changes, or when any eligibility point is in doubt -- doubt means `fast-track`.

## Process

### Step 1: Explore Context (silently)

Before asking any questions, gather context:

1. Read project documentation (CLAUDE.md, README, recent commits)
2. Identify the current project state (what exists, what's in progress)
3. Check for existing specs, architecture docs, or design decisions
4. Note the technology stack, team conventions, and constraints
5. Review any linked issues, PRs, or discussions

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

For new-work routing, use the **Entry Phase** tokens above verbatim. `cross-cutting` is the only non-lifecycle special value and is reserved for documentation-only routing. For `resume`, `entry_phase` may point to any already-active lifecycle phase that needs to continue.

Use the declared primary workflow name verbatim when recording `workflow_primary` (`agile-sprint`, `spec-driven`, or `iterative-waterfall`).

For `fast-track` and `micro`, omit `workflow_primary` when the route stays direct enough that the primary workflow does not materially change the handoff. Keep it explicit for `full` and `resume`.

Record `workflow_overlays` only when one or more overlays are active. Omit the field instead of emitting an empty list.

### Step 2A: Record the Quality Target Context

Every intake brief must include `quality_target_context`. Infer it from the repository and request when possible, and ask at most one clarifying question only when the answer would change route, risk, or review severity.

Record:

- `runtime_context`: `agent_internal_skill`, `host_runtime_tool`, `local_dev_harness`, `internal_service`, `public_service`, or `unknown`
- `exposure_profile`: `no_network_listener`, `localhost_only`, `private_network`, `public_internet`, or `unknown`
- `production_target`: the real thing being shipped or reviewed
- `non_targets`: important things this work is not trying to become
- `evidence_refs`: concrete artifacts or user statements that support the classification

This context must calibrate quality and security handoff. An agent-internal skill, host runtime tool, or local harness may still need rigorous QA, but it should not inherit public service controls such as browser auth flows, public API rate limiting, or internet CORS policy unless the target actually exposes that surface. A public service, multi-user API, or internet-exposed component keeps the full service-style quality and security posture.

If the target context is unknown, say so explicitly and do not invent a public service boundary from implementation details such as Flask, routes, HTTP clients, or a model provider adapter.

### Step 3: Ask Clarifying Questions

Ask questions **one at a time**, adapting based on answers. Start with the most important unknown.

Priority order:
1. **Goal**: What outcome does the user want? (if not obvious)
2. **Scope**: How large is this? (single file fix vs multi-service change)
3. **Urgency**: Is this blocking production? (hotfix vs normal flow)
4. **Constraints**: Time, tech, compatibility, or process constraints?
5. **Quality bar**: Production-grade or prototype? (determines methodology rigor)

Stop when you have enough. Typically 1-3 questions suffice. Never more than 5.

Default to the smallest question budget that still changes the routing decision. If the first two answers already make the path clear, stop and propose the route.

### Step 4: Propose Approach

Present a concise intake brief. Compare **path options**, not detailed implementation or architecture options:

- Use plain language and keep the brief easy to scan.
- Present user-facing output in the user's requested language or the `user_presentation_locale` recorded in the intake brief.
- Call out system shape and collaboration quality when they materially affect routing, risk, or the next handoff.

Name concrete Prodcraft skills whenever the next step is already known. Avoid generic labels like `specification`, `architecture`, `planning`, or `implementation` when a specific skill can already be named. If the exact downstream skill is still genuinely undecided, say that explicitly as an open routing question rather than pretending a generic phase label is a settled handoff target.

```
## Intake Brief

**Work type**: [classification from Step 2]
**Entry phase**: [which lifecycle phase]
**Intake mode**: [full / fast-track / micro / resume]
**workflow_primary**: [primary governance workflow, if explicit for this route]
**workflow_overlays**: [[overlay list], omit when none]
**quality_target_context**: [runtime_context, exposure_profile, production_target, non_targets, evidence_refs]
**Key skills needed**: [3-7 concrete Prodcraft skills, or clearly marked open routing questions]
**Scope assessment**: [small / medium / large / xlarge]
**routing_rationale**: [why this route wins]
**Key risks**: [1-2 biggest risks or unknowns]

### Proposed Path
1. [First skill] -- [what it produces]
2. [Second skill] -- [what it produces]
3. ...

### Alternative Approach (if applicable)
[Different path with different trade-offs]
```

Only include an alternative path when the trade-off is real and decision-relevant. One clear alternative is usually enough.

### Step 5: Get Approval

Wait for user confirmation. Accept:
- **Approval** -> proceed with proposed path
- **Adjustment** -> modify and re-present
- **"Skip to X"** -> translate into a reviewed `fast-track` or `resume` intake decision, then log any skipped gates as tech debt

Exception: `micro` mode uses notify-and-proceed (see Micro Mode above) -- present the compact brief and continue in the same turn instead of blocking on confirmation.

### Step 6: Handoff

Transition to the first skill in the proposed path, passing the intake brief as context.

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

Intake must leave behind a usable record of **why** the work entered the system this way.

The `intake-brief` must capture:
- `request_summary`
- `source_language` (BCP-47-style locale such as `en`, `zh-Hans`, or the explicit `mixed` sentinel) for the incoming request
- `artifact_record_language` for the canonical artifact record (`en` under current repo policy)
- `user_presentation_locale` (BCP-47-style locale) for the language used when presenting the intake result to the user
- why intake was invoked, fast-tracked, or resumed
- `intake_mode`
- `quality_target_context`, including `runtime_context`, `exposure_profile`, `production_target`, `non_targets`, and `evidence_refs`
- the key questions asked and the answers that changed routing
- `workflow_primary` when the route depends on explicit primary governance, and `workflow_overlays` when overlays are active
- the recommended path and any meaningful alternative considered
- the next skill to invoke and the reason it is next

This keeps routing decisions auditable without forcing downstream skills to reconstruct the conversation.

## Anti-Patterns

1. **Treating trivial work as "outside intake"** -- Even simple changes still need a lightweight `micro` or `fast-track` intake decision.
2. **Over-questioning** -- Intake should take 1-5 minutes, not 30. If you need 5+ questions, you're in discovery territory -- recommend moving there.
3. **Guessing the methodology** -- Don't assume agile because it's popular. Match methodology to constraints and context.
4. **Rigid phase assignment** -- The lifecycle is a guide, not a prison. A bug fix might need architecture review if it reveals a design flaw.
5. **Ignoring existing context** -- If the project has CLAUDE.md, existing specs, or established conventions, incorporate them.
6. **Turning intake into a full design session** -- Intake should decide the route. If the work needs option exploration or concept shaping, route to problem-framing instead of expanding intake indefinitely.

## Reference Material

For methodology selection signals and worked intake examples, see [routing-signals-and-examples](references/routing-signals-and-examples.md). Keep the main skill focused on routing discipline; use the reference only when a path decision needs more comparison detail.

For edge cases that commonly derail intake routing under pressure, see [Gotchas](references/gotchas.md).
