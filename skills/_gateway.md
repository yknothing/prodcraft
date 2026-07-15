# Prodcraft Gateway

> The routing logic that connects user intent to the right skill at the right time.

This document defines how Prodcraft skills are discovered, selected, and composed. It is the equivalent of `using-superpowers` for the Prodcraft lifecycle system.

## Core Rule

**Every interaction starts with skill matching. No exceptions.**

Before generating any response -- even a clarifying question -- check if a Prodcraft skill applies. If one does, invoke it. If uncertain, default to `pc-intake`.

The intake decision gate is enforced in two layers:

1. **Routing policy** -- default to `pc-intake` for new work or ambiguity.
2. **Workflow contract** -- every workflow requires an approved `intake-brief` before execution, even if the intake mode is `fast-track`, `micro`, or `resume`. For `micro`, "approved" means notify-and-proceed: the brief is presented with the work and stands unless the user objects.

When intake has identified the likely lifecycle path but the problem statement or solution direction is still fuzzy, route next to `pc-problem-framing` before moving into research, specification, or architecture.

## Skill Selection Priority

When multiple skills could apply, use this priority order:

### Priority 1: Process Gates (blocking)

These skills MUST be invoked before any work begins:

| Trigger | Skill | Why |
|---------|-------|-----|
| New work of any kind | `pc-intake` | Triage and route |
| Bug, failing test, or unexpected behavior before a fix | `pc-systematic-debugging` | Root cause before code change |
| Implementation about to start | `pc-tdd` | Tests before code |
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
| Writing code or tactically executing an approved slice | 04-implementation | pc-task-execution, pc-systematic-debugging, pc-tdd, pc-feature-development, pc-refactoring |
| Reviewing/testing | 05-quality | pc-implementation-alignment-review, pc-implementation-integrity-audit, pc-code-review, pc-receiving-code-review, pc-testing-strategy, pc-security-audit |
| Deploying/releasing | 06-delivery | pc-ci-cd, pc-delivery-completion, pc-deployment-strategy, pc-release-management |
| Monitoring/responding | 07-operations | pc-monitoring-observability, pc-incident-response, pc-runbooks |
| Improving/modernizing | 08-evolution | pc-tech-debt-management, pc-migration-strategy (planned), pc-retrospective |

### Implementation Routing Quick Map

When the work is already in `04-implementation`, choose the primary skill like this:

- need a short 2-5 minute tactical batch with checkpoints or stop conditions -> `pc-task-execution`
- need root cause before any code fix -> `pc-systematic-debugging`
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

### Sequential Composition
Skills execute one after another, each consuming the previous skill's output:

```
pc-spec-writing -> pc-system-design -> pc-task-breakdown -> pc-tdd -> pc-feature-development
```

### Parallel Composition
Independent skills execute simultaneously:

```
                    ┌─> pc-api-design ────────┐
pc-system-design ──>├─> pc-data-modeling ─────>├─> pc-task-breakdown
                    └─> pc-security-design ───┘
```

### Iterative Composition
A skill repeats until its quality gate is met:

```
pc-feature-development <──> pc-code-review (loop until approved)
```

### Conditional Composition
Skills are included or skipped based on context:

```
IF regulated_industry THEN pc-security-audit
IF user_facing THEN pc-accessibility
IF multi_language THEN pc-internationalization
```

## Entry Stack Rules

Prodcraft's entry stack has two layers:

1. `pc-intake` -- classify the work, choose the phase and route, and create the `intake-brief`
2. `pc-problem-framing` -- only when the route is known but the problem or direction is still too fuzzy for clean downstream work

Use `pc-problem-framing` after intake when:
- the request is new work and still underspecified after routing
- 2-3 viable directions need comparison before requirements or research
- downstream work would otherwise start by rediscovering the problem statement

Do not use `pc-problem-framing` when:
- the route and problem are already clear enough for the next skill
- the work is already in progress
- the task is trivial enough for an intake fast-track

### Entry Stack Observability

Each entry-layer handoff must record:
- why the skill was invoked
- how many questions were asked and which answers changed the route or direction
- the primary path or direction selected
- any meaningful alternative considered
- the next skill to invoke

### Entry Stack Usability

Entry skills should minimize user burden:
- `pc-intake`: default to 1-3 questions, never more than 5
- `micro` intake asks zero questions -- if a question is needed, the work is not micro
- `pc-problem-framing`: default to 1-3 additional questions, never more than 5
- do not ask another question unless its answer could change the route, direction, or risk posture

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
2. **Document artifacts** -- Ensure all outputs are saved and accessible
3. **Brief next phase** -- Pass relevant context to the next skill
4. **Update status** -- Log the phase transition

If exit criteria are not met:
- **Option A**: Complete the remaining work in the current phase
- **Option B**: Proceed with explicit acknowledgment of skipped gates (logged as tech debt)
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
| Single-file bug fix with clear root cause | `fast-track` | Skip to implementation with pc-systematic-debugging + TDD |
| Documentation restructuring | `fast-track` | Skip to cross-cutting/pc-documentation |
| Dependency update (patch) | `fast-track` | Skip to implementation + quality |
| Configuration change with deploy impact | `fast-track` | Skip to implementation + deployment |

`micro` eligibility and its notify-and-proceed semantics are owned by the intake skill's Micro Mode section -- see `skills/00-discovery/pc-intake/SKILL.md`. Gateway summary: reversible single-revert trivia only, zero questions, never for irreversible or externally visible actions; doubt on any point means `fast-track`.

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

### Starting a Session

1. Check project context (CLAUDE.md, recent work)
2. Determine if there's an active workflow in progress
3. If new work: invoke `pc-intake`
4. If continuing work: resume at the appropriate phase/skill

Do not enter a workflow unless the `intake-brief` exists and the user has approved it.

### During a Session

1. Track which phase you're in
2. Apply the current skill's process
3. Check quality gates before transitioning
4. Invoke cross-cutting skills as needed

### Ending a Session

1. Summarize what was accomplished
2. Note the current phase and next steps
3. Document any open questions or blockers
4. If applicable, suggest the next skill to invoke

## Integration with Existing Skills

Prodcraft is designed to complement, not replace, existing skill systems. If your environment has skills like `brainstorming`, `systematic-debugging`, or `writing-plans`:

- `brainstorming` maps most closely to `pc-intake` -> `pc-problem-framing` -> discovery or specification skills
- `systematic-debugging` maps directly to repo-local `pc-systematic-debugging`
- `writing-plans` maps to phase 03 planning skills
- `executing-plans` maps most closely to repo-local `pc-task-execution` plus the downstream implementation skill for the current batch
- `requesting-code-review` maps to phase 05 quality skills
- `receiving-code-review` maps directly to repo-local `pc-receiving-code-review`
- `verification-before-completion` maps directly to repo-local `pc-verification-before-completion`
- `finishing-a-development-branch` maps most closely to repo-local `pc-delivery-completion`, with `pc-release-management` and `pc-deployment-strategy` added only when the work continues toward shipping

Use whichever skill system is more appropriate for the context. Prodcraft adds lifecycle awareness; existing skills may have deeper domain-specific guidance.

For repository-local experiments in this repo, Prodcraft may temporarily run in **repo-authoritative mode** for software-development work by installing the global `pc-prodcraft` gateway skill through `scripts/install_prodcraft_global_skill.py` and archiving conflicting global superpowers skill directories through `scripts/archive_superpowers_skills.py`. When that override is active:

- `pc-intake` becomes the mandatory first software-development entry point
- the override action and restore action must remain observable through the script's JSONL event log
- non-Prodcraft global skills are still available unless explicitly suppressed separately
