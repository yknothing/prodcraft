# Prodcraft Gateway

> The routing logic that connects user intent to the right skill at the right time.

This document defines how Prodcraft skills are discovered, selected, and composed. It is the equivalent of `using-superpowers` for the Prodcraft lifecycle system.

## Core Rule

**Every interaction starts with skill matching. No exceptions.**

Before generating any response -- even a clarifying question -- check if a Prodcraft skill applies. If one does, invoke it. If uncertain, default to `intake`.

The intake hard gate is enforced in two layers:

1. **Routing policy** -- default to `intake` for new work or ambiguity.
2. **Workflow contract** -- every workflow requires an approved `intake-brief` before execution.

## Skill Selection Priority

When multiple skills could apply, use this priority order:

### Priority 1: Process Gates (blocking)

These skills MUST be invoked before any work begins:

| Trigger | Skill | Why |
|---------|-------|-----|
| New work of any kind | `intake` | Triage and route |
| Implementation about to start | `tdd` | Tests before code |
| Code complete, ready for merge | `code-review` | Quality gate |
| About to claim "done" | `verification-before-completion` | Verify claims |

### Priority 2: Phase-Specific Skills (contextual)

Match based on what phase the work is currently in:

| Current Activity | Phase | Likely Skills |
|------------------|-------|---------------|
| Exploring a new idea | 00-discovery | market-analysis, user-research, feasibility-study |
| Defining requirements | 01-specification | requirements-engineering, spec-writing, domain-modeling |
| Designing system structure | 02-architecture | system-design, api-design, data-modeling, security-design |
| Breaking down work | 03-planning | task-breakdown, estimation, risk-assessment |
| Writing code | 04-implementation | tdd, feature-development, refactoring |
| Reviewing/testing | 05-quality | code-review, testing-strategy, security-audit |
| Deploying/releasing | 06-delivery | ci-cd, deployment-strategy, release-management |
| Monitoring/responding | 07-operations | monitoring-observability, incident-response |
| Improving/modernizing | 08-evolution | tech-debt-management, migration-strategy, retrospective |

### Priority 3: Cross-Cutting Skills (always applicable)

These can be invoked at any phase:

- `documentation` -- when documentation is needed
- `observability` -- when instrumenting code
- `accessibility` -- when building UI
- `internationalization` -- when handling user-facing text
- `compliance` -- when regulatory requirements apply

## Workflow Selection

Once intake determines the work type, select the appropriate workflow:

```
Is production on fire?
  YES -> hotfix workflow
  NO  -> continue

Is this a brand new project?
  YES -> greenfield workflow
  NO  -> continue

Is this modernizing a legacy system?
  YES -> brownfield workflow
  NO  -> continue

What's the project methodology?
  Formal specs required    -> spec-driven workflow
  Sprint-based team        -> agile-sprint workflow
  Phase-gated enterprise   -> iterative-waterfall workflow
  Unknown/flexible         -> agile-sprint workflow (default)
```

## Skill Composition Patterns

### Sequential Composition
Skills execute one after another, each consuming the previous skill's output:

```
spec-writing -> system-design -> task-breakdown -> tdd -> feature-development
```

### Parallel Composition
Independent skills execute simultaneously:

```
                 ┌─> api-design ────────┐
system-design ──>├─> data-modeling ─────>├─> task-breakdown
                 └─> security-design ───┘
```

### Iterative Composition
A skill repeats until its quality gate is met:

```
feature-development <──> code-review (loop until approved)
```

### Conditional Composition
Skills are included or skipped based on context:

```
IF regulated_industry THEN security-audit
IF user_facing THEN accessibility
IF multi_language THEN internationalization
```

## Phase Transition Protocol

When transitioning between phases:

1. **Verify exit criteria** -- Check the current phase's quality gate
2. **Document artifacts** -- Ensure all outputs are saved and accessible
3. **Brief next phase** -- Pass relevant context to the next skill
4. **Update status** -- Log the phase transition

If exit criteria are not met:
- **Option A**: Complete the remaining work in the current phase
- **Option B**: Proceed with explicit acknowledgment of skipped gates (logged as tech debt)
- **Option C**: Escalate to tech-lead for decision

## Fast-Track Rules

Not every task needs the full lifecycle. Fast-track criteria:

| Condition | Allowed Shortcut |
|-----------|-----------------|
| Typo fix, comment update | Skip directly to implementation, minimal review |
| Single-file bug fix with clear root cause | Skip to implementation with TDD |
| Documentation-only change | Skip to cross-cutting/documentation |
| Dependency update (patch) | Skip to implementation + quality |
| Configuration change | Skip to implementation + deployment |

Fast-track still requires:
- The user explicitly confirms the fast-track
- A brief rationale is documented
- Quality gates for implementation and delivery still apply

## Interaction Protocol

### Starting a Session

1. Check project context (CLAUDE.md, recent work)
2. Determine if there's an active workflow in progress
3. If new work: invoke `intake`
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

- `brainstorming` maps to `intake` + phase 00 skills
- `systematic-debugging` maps to phase 04 implementation (debugging variant)
- `writing-plans` maps to phase 03 planning skills
- `executing-plans` maps to phase 04 implementation skills
- `requesting-code-review` maps to phase 05 quality skills
- `verification-before-completion` remains as a cross-cutting gate

Use whichever skill system is more appropriate for the context. Prodcraft adds lifecycle awareness; existing skills may have deeper domain-specific guidance.
