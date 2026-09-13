# Prodcraft Gateway

> The routing logic that connects user intent to the right skill at the right time.

This document defines how Prodcraft skills are discovered, selected, and composed. It is the equivalent of `using-superpowers` for the Prodcraft lifecycle system.

## Core Rule

**Match the work to the next unmet obligation. Reuse an approved route while it still applies.**

Start new work or a material change to outcome, scope, risk, or authority with `pc-intake`. Continue an approved route across status questions, clarifications, and skill handoffs without repeating intake or approval.

Every workflow requires an approved `intake-brief`. For `micro`, approval means notify-and-proceed unless the user objects. When the route is clear but the problem or direction is not, invoke `pc-problem-framing` next.

Match the current substantive request's language in all user-facing prose, headings, questions, human-facing tags, status labels, and completion feedback. English requests receive English; Chinese requests receive Chinese. An explicit language request takes precedence. Ignore code, paths, API names, and quoted source text when selecting the language. For mixed prose use its dominant language; retain the established presentation locale when ambiguous. Re-evaluate on a substantive follow-up, including a language switch, without restarting intake. Keep canonical machine fields/enums, skill IDs, code, commands, paths, and original diagnostics unchanged; localize their display labels and summaries. Canonical artifact records remain in English.

## Skill Selection Priority

When multiple skills could apply, use this priority order:

### Priority 1: Process Gates (blocking)

Apply each gate when its trigger is reached. A later gate is not an instruction to preload or execute the entire chain before starting:

| Trigger | Skill | Why |
|---------|-------|-----|
| New work of any kind | `pc-intake` | Triage and route |
| Bug, failing test, or unexpected behavior before a fix | `pc-debug-expert` | Root cause before code change |
| New or changed executable behavior | `pc-tdd` | Define behavioral proof before implementation; use its explicit exceptions where applicable |
| Code complete, ready for merge | `pc-code-review` | Quality gate |
| Need to verify delivered intent and scope consistency | `pc-implementation-alignment-review` | Prevent wrong-thing delivery |
| Need to audit fake-success, low-level, mock, or evidence-honesty risk | `pc-implementation-integrity-audit` | Prevent deceptive implementation |
| About to claim "done" | `pc-verification-before-completion` | Verify claims |

### Priority 2: Phase-Specific Skills (contextual)

Match based on what phase the work is currently in:

| Current Activity | Phase | Likely Skills |
|------------------|-------|---------------|
| Exploring a new idea | 00-discovery | pc-problem-framing, pc-market-analysis, pc-user-research, pc-feasibility-study |
| Defining requirements | 01-specification | pc-requirements-engineering, pc-spec-writing, pc-domain-modeling |
| Designing system structure | 02-architecture | pc-system-design, pc-api-design, pc-data-modeling, pc-security-design, pc-tech-selection |
| Breaking down work | 03-planning | pc-task-breakdown, pc-estimation, pc-risk-assessment, pc-sprint-planning |
| Writing code or tactically executing an approved slice | 04-implementation | pc-task-execution, pc-debug-expert, pc-tdd, pc-feature-development, pc-refactoring |
| Reviewing/testing | 05-quality | pc-implementation-alignment-review, pc-implementation-integrity-audit, pc-code-review, pc-receiving-code-review, pc-testing-strategy, pc-security-audit |
| Deploying/releasing | 06-delivery | pc-ci-cd, pc-delivery-completion, pc-deployment-strategy, pc-release-management |
| Monitoring/responding | 07-operations | pc-monitoring-observability, pc-incident-response, pc-runbooks |
| Improving/modernizing | 08-evolution | pc-tech-debt-management, pc-migration-strategy (planned), pc-retrospective |

### Implementation Routing Quick Map

When the work is already in `04-implementation`, choose the primary skill like this:

- need a short 2-5 minute tactical batch with checkpoints or stop conditions -> `pc-task-execution`
- need root cause for code, runtime, or skill-loading failures -> `pc-debug-expert`
- need a failing test first for new or changed behavior -> `pc-tdd`
- need to land the already-tested slice as code -> `pc-feature-development`
- need structural cleanup with protected behavior -> `pc-refactoring`

Do **not** start with `pc-task-execution` when the primary implementation discipline is already obvious and no tactical batching problem exists. It is an optional tactical wrapper, not the default producer of code.

### Priority 3: Cross-Cutting Skills (always applicable)

These can be invoked at any phase:

- `pc-documentation` -- when documentation is needed
- `pc-observability` -- when instrumenting code
- `pc-accessibility` -- when building UI
- `pc-internationalization` -- when handling user-facing text
- `pc-compliance` -- when regulatory requirements apply

### Select the Smallest Sufficient Route

Choose one primary skill for the decision or deliverable. Add skills only for required outputs, distinct risks, or unmet approved gates; phase membership and `methodologies: all` are not execution orders.

Check the next skill's input contract. Reuse current accepted artifacts by path and section. Route missing required inputs to their producer and contradictory inputs through a course correction. Never fabricate documents to fill a template.

Preserve workflow gates and artifact obligations. Reuse requires the same quality boundary and authority; strict-mode obligation changes require an approved route revision and new operator pin.

### Load Context at the Point of Use

Read the selected skill and required I/O contract first, then methods for the active step and gotchas on their trigger. Keep unchanged material available; defer unrelated bodies, examples, background, and workflows. References retain their authority.

Handoff: outcome, approved scope and authority, artifact paths/revisions, gaps, next skill, and acceptance condition. Use relevant sections rather than the session transcript. This convention adds no artifact type or execution authority.

### Compose Reviews by Question

| Skill | Distinct question |
|-------|-------------------|
| `pc-implementation-alignment-review` | Does the delivered behavior satisfy the approved intent and scope? |
| `pc-code-review` | Does the changed implementation contain a concrete defect or policy violation? |
| `pc-implementation-integrity-audit` | Can fake success, substituted dependencies, or misleading evidence conceal a failure? |
| `pc-verification-before-completion` | Does current evidence support the exact completion claim? |

Use the dimensions required by the route and observed risks. Several skills may contribute named sections to one review report. Preserve each required conclusion and its evidence; do not count the same finding repeatedly or call one agent with several personas independent reviewers.

## Workflow Selection

Once intake determines the work type, select the route in three layers:

```
Is production on fire?
  YES -> add hotfix overlay
  NO  -> continue

Is this a brand new project?
  YES -> add greenfield overlay
  NO  -> continue

Is this modernizing a legacy system?
  YES -> add brownfield overlay
  NO  -> continue

What's the project methodology?
  Formal specs required    -> workflow_primary = spec-driven
  Sprint-based team        -> workflow_primary = agile-sprint
  Phase-gated enterprise   -> workflow_primary = iterative-waterfall
  Unknown/flexible         -> workflow_primary = agile-sprint (default)
```

The `intake-brief` should record:

- `workflow_primary` when the approved route needs explicit primary governance
- `workflow_overlays` when one or more overlays are active

Examples:

- `workflow_primary=agile-sprint`, `workflow_overlays=[brownfield]`
- `workflow_primary=agile-sprint`, `workflow_overlays=[brownfield, hotfix]`
- `workflow_primary=spec-driven`, `workflow_overlays=[greenfield]`

## Skill Composition Patterns

- **Sequential**: invoke a producer before its consumer, such as `pc-spec-writing -> pc-system-design -> pc-task-breakdown` when those outputs are required.
- **Parallel**: run independent work only when coordination costs less than waiting; API, data, and security design may share accepted architecture without waiting on each other.
- **Iterative**: repeat implementation/review for unresolved findings, checking changed behavior and affected boundaries. A recurring blocker without new evidence needs diagnosis or upstream correction, not another approval loop.
- **Conditional**: add accessibility for user-facing UI, internationalization for multiple languages, and security/compliance work according to actual exposure and policy.

## Entry Stack Rules

`pc-intake` owns classification, route selection, and the `intake-brief`. Add `pc-problem-framing` only when downstream work would otherwise rediscover an unresolved problem or compare viable directions. Clear, continuing, and trivial work needs no framing detour.

### Entry Stack Observability

Record the invocation reason, questions asked, answers that changed the route, selected path, meaningful alternatives, and next skill.

### Entry Stack Usability

Ask only questions that can change route, direction, or risk. Zero is valid with sufficient context and mandatory for `micro`. Otherwise each entry skill defaults to 1-3 questions, never more than 5.

## Quality Target Context Gate

Before entering any `05-quality` skill, confirm the approved `intake-brief` includes `quality_target_context`:

- `runtime_context`
- `exposure_profile`
- `production_target`
- `non_targets`
- `evidence_refs`

Do not assume public HTTP service from implementation details such as Flask routes, HTTP clients, CORS configuration, model provider adapters, or API-shaped filenames. A codebase can use HTTP internally while the reviewed product target is an agent-internal skill, host runtime tool, or local harness.

If the target context is missing or contradictory, ask one clarifying question when it can change review severity. If the mismatch is discovered after implementation, produce a `course-correction-note` instead of continuing the quality chain. Do not run `pc-security-audit`, `pc-testing-strategy`, or `pc-e2e-scenario-design` as a service-style sequence until the quality target context is explicit.

Use this calibration:

- `agent_internal_skill`, `host_runtime_tool`, or `local_dev_harness`: focus review on skill contract, trigger behavior, prompt injection, command safety, tool/file/network side effects, secrets and PII in artifacts, dependency execution risk, schema validators, curated export, and runtime portability probes.
- `internal_service`: check service boundaries, private-network exposure, authentication or caller assumptions, logs, dependency risk, and integration contracts that actually exist.
- `public_service` or `public_internet`: keep full public service review. CORS, public auth, rate limiting, browser-facing behavior, OpenAPI contracts, and abuse controls may be blocking when evidence supports that exposure.
- `unknown`: record uncertainty, avoid invented release blockers, and route to the smallest clarification or upstream context artifact that can settle the boundary.

## Phase Transition Protocol

### Optional Strict Execution Authority

Projects may opt into the repository-owned `route-decision.v1` and
`execution-state.v1` protocol. In that mode, conversation history and skill
checklists remain guidance; the canonical state, its closed local evidence bundle,
the live Git work snapshot, and operator-supplied route and terminal-completion
digests determine gate or terminal authority.

- `--artifact-instance` checks artifact shape/contract and emits no authority.
- `gate-authorized` permits a non-terminal transition or checkpoint only.
- `terminal-authorized` permits the bound completion claim only after the final
  completion projection matches the out-of-band operator completion pin.
- missing pin, stale evidence/work, non-canonical history, and structural-only
  results fail closed.

Strict mode is not mandatory for legacy workflows in this release. Hosts may adapt
the CLI, but may not replace the repository contract with host-local state.

When transitioning between phases:

1. **Verify exit criteria** -- Check the current phase's quality gate
2. **Document artifacts** -- Ensure required outputs are saved and accessible; reuse current accepted outputs
3. **Brief next phase** -- Pass relevant context to the next skill
4. **Update status** -- Log the phase transition

If exit criteria are not met:
- **Option A**: Complete the remaining work in the current phase
- **Option B**: For an advisory gate, record the gap and permitted follow-up. A blocking gate needs an authorized route change or waiver under project policy; a tech-debt note alone is not approval. Strict mode requires a new approved obligation set and operator pin.
- **Option C**: Escalate to tech-lead for decision

## Cross-Phase Course Corrections

When a later phase discovers a cross-phase contract mismatch, do not force a full loop back through discovery by default. Use a `course-correction-note` and jump directly to the most relevant upstream phase.

Approved direct jumps:

- `04-implementation -> 01-specification`
- `04-implementation -> 02-architecture`
- `05-quality -> 02-architecture`
- `07-operations -> 02-architecture`
- `07-operations -> 03-planning`
- `08-evolution -> 01-specification`
- `08-evolution -> 02-architecture`
- `08-evolution -> 03-planning`

These eight pairs are the full approved set. A `course-correction-note` outside this set is invalid and should fail schema/validator checks rather than relying on reviewer memory.

Each `course-correction-note` must capture:

- the trigger and evidence
- the blocked artifact
- the constraints that still hold
- the recommended next skill
- whether the user must re-approve the route

## Fast-Track Rules

Not every task needs the full lifecycle. Governance weight scales with the risk of the work; the intake gate itself is universal.

| Condition | Mode | Allowed Shortcut |
|-----------|------|-----------------|
| Typo fix, comment update, doc wording | `micro` | Compact brief, notify-and-proceed, straight to the change |
| Isolated reversible config value | `micro` | Compact brief, notify-and-proceed |
| Single-file bug fix with clear root cause | `fast-track` | Skip to implementation with pc-debug-expert + TDD |
| Documentation restructuring | `fast-track` | Skip to `pc-documentation` |
| Dependency update (patch) | `fast-track` | Skip to implementation + quality |
| Configuration change with deploy impact | `fast-track` | Skip to implementation + deployment |

`micro` eligibility and its notify-and-proceed semantics are owned by `pc-intake`'s Micro Mode section. Gateway summary: reversible single-revert trivia only, zero questions, never for irreversible or externally visible actions; doubt on any point means `fast-track`.

The current repository Claude Edit/Write adapter rejects `micro`. Under that adapter, use an approved `fast-track` brief; do not work around the gate with another tool. Portable guidance alone provides no host enforcement.

Fast-track still requires:
- an approved `intake-brief`
- `intake_mode=fast-track` (or `intake_mode=micro` with notify-and-proceed approval)
- a brief rationale documented
- quality gates for implementation and delivery still apply

## Cross-Cutting Injection

Cross-cutting expectations are tracked in `rules/cross-cutting-matrix.yml`.

Use the matrix to decide which skills are:

- `must_consider` for a phase
- `must_produce` as a durable output obligation
- waived in `skip_when_fast_track` when the route is explicitly fast-tracked
- `conditional` when UI, observability, historical failures, or compliance risk are in play

## Interaction Protocol

At session entry, read applicable project instructions and identify new versus continuing work. Start new work through intake; continue an approved route after checking scope, authority, and artifact freshness. During execution, apply the active skill and required gates. At handoff, report the result, remaining gaps, current phase, and next skill using artifact pointers.

## Integration with Existing Skills

External skills may provide deeper expertise when the user chooses them and the approved route permits it. Translate their outputs into local Prodcraft contracts; do not create implicit source-code or runtime dependencies on another skill system. Preserve required gates and report which system actually ran.

Installing the global `pc-prodcraft` gateway or archiving competing global skills is an explicit deployment operation, not an effect of ordinary routing. The repository-owned install/archive scripts described in CLAUDE.md provide reversible state and event logs. Keep unrelated global skills intact and record any authorized override.
