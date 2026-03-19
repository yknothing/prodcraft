---
name: intake
description: 'Route new engineering work before execution. Use when a user wants to build a new product, app, or internal tool, start from scratch, plan a migration, run a multi-sprint tech-debt or documentation effort, or says they are not sure where to start. Also use when a feature, refactor, or hotfix needs scope triage before implementation. Do not use for ongoing work, concrete debugging, trivial edits, direct commands, PR review, or pure questions.'
metadata:
  phase: 00-discovery
  inputs: []
  outputs:
  - intake-brief
  - phase-recommendation
  - workflow-recommendation
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

> The mandatory entry point for all work. No implementation without intake. No exceptions.

## Why Intake Exists

Every piece of work -- a new feature, a bug fix, a refactoring, a migration -- enters the lifecycle somewhere. Intake determines **where** and **how** to proceed. Think of it as hospital triage for software: assess the situation, determine urgency and scope, route to the right treatment.

Without intake, teams jump straight to coding and discover mid-way that they're solving the wrong problem, using the wrong approach, or missing critical constraints. Thirty seconds of triage prevents hours of wasted effort.

Intake is the **control plane** for entry, not the full discovery workshop. Its job is to classify, route, and make the next step observable. If deeper concept shaping is needed after routing is chosen, hand off to a downstream discovery skill rather than turning intake into a long design session.

## Hard Gate

No implementation, architecture, or planning work may begin until intake is complete and the user approves the proposed path.

**Fast-track exception**: if the user explicitly states they want to skip intake for trivial work (typo fix, comment update), produce a 2-3 sentence intake summary and confirm before proceeding.

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

| Type | Description | Entry Phase | Default Workflow |
|------|-------------|-------------|------------------|
| **New Product** | Building from scratch | 00-discovery | greenfield |
| **New Feature** | Adding capability to existing system | 01-specification | agile-sprint |
| **Enhancement** | Improving existing functionality | 03-planning | agile-sprint |
| **Bug Fix** | Correcting incorrect behavior | 04-implementation | agile-sprint |
| **Hotfix** | Critical production issue | 04-implementation | hotfix |
| **Refactoring** | Structural improvement, no behavior change | 04-implementation | agile-sprint |
| **Migration** | Moving to new platform/architecture | 00-discovery | brownfield |
| **Tech Debt** | Paying down accumulated shortcuts | 03-planning | agile-sprint |
| **Spike/Research** | Investigating unknowns | 00-discovery | agile-sprint |
| **Documentation** | Creating or improving docs | cross-cutting | agile-sprint |

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

Name concrete Prodcraft skills whenever the next step is already known. Avoid generic labels like `specification`, `architecture`, `planning`, or `implementation` when a specific skill can already be named. If the exact downstream skill is still genuinely undecided, say that explicitly as an open routing question rather than pretending a generic phase label is a settled handoff target.

```
## Intake Brief

**Work type**: [classification from Step 2]
**Entry phase**: [which lifecycle phase]
**Recommended workflow**: [methodology]
**Key skills needed**: [3-7 concrete Prodcraft skills, or clearly marked open routing questions]
**Scope assessment**: [small / medium / large / xlarge]
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
- **"Skip to X"** -> jump to specified phase (log skipped gates as tech debt)

### Step 6: Handoff

Transition to the first skill in the proposed path, passing the intake brief as context.

If routing is clear but the problem or solution direction is still too fuzzy for specification or discovery research, hand off to [problem-framing](../problem-framing/SKILL.md) before moving deeper into the lifecycle.

## Observability Requirements

Intake must leave behind a usable record of **why** the work entered the system this way.

The `intake-brief` must capture:
- why intake was invoked or fast-tracked
- the key questions asked and the answers that changed routing
- the recommended path and any meaningful alternative considered
- the next skill to invoke and the reason it is next

This keeps routing decisions auditable without forcing downstream skills to reconstruct the conversation.

## Anti-Patterns

1. **Skipping intake for "obvious" tasks** -- Even simple changes benefit from 30 seconds of context. The fast-track exists for truly trivial work.
2. **Over-questioning** -- Intake should take 1-5 minutes, not 30. If you need 5+ questions, you're in discovery territory -- recommend moving there.
3. **Guessing the methodology** -- Don't assume agile because it's popular. Match methodology to constraints and context.
4. **Rigid phase assignment** -- The lifecycle is a guide, not a prison. A bug fix might need architecture review if it reveals a design flaw.
5. **Ignoring existing context** -- If the project has CLAUDE.md, existing specs, or established conventions, incorporate them.
6. **Turning intake into a full design session** -- Intake should decide the route. If the work needs option exploration or concept shaping, route to problem-framing instead of expanding intake indefinitely.

## Reference Material

For methodology selection signals and worked intake examples, see [routing-signals-and-examples](references/routing-signals-and-examples.md). Keep the main skill focused on routing discipline; use the reference only when a path decision needs more comparison detail.
