---
name: intake
description: 'Assess new engineering work before execution by classifying the work type, choosing the right lifecycle starting phase and workflow, and producing an intake brief for approval. Use when a user is starting a new product, migration, major cross-cutting initiative, multi-sprint tech debt effort, broad documentation push, or says they are unsure where to begin and need routing before implementation. Also use when a feature, refactor, or incident needs scope triage first rather than immediate execution. Do not use for tasks already in progress or already tightly scoped: specific debugging with stack traces, writing tests for a known function, running commands, trivial edits, reviewing PRs, or pure knowledge questions.'
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

### Step 4: Propose Approach

Present a concise intake brief:

```
## Intake Brief

**Work type**: [classification from Step 2]
**Entry phase**: [which lifecycle phase]
**Recommended workflow**: [methodology]
**Key skills needed**: [3-7 skills from lifecycle]
**Scope assessment**: [small / medium / large / xlarge]
**Key risks**: [1-2 biggest risks or unknowns]

### Proposed Path
1. [First skill] -- [what it produces]
2. [Second skill] -- [what it produces]
3. ...

### Alternative Approach (if applicable)
[Different path with different trade-offs]
```

### Step 5: Get Approval

Wait for user confirmation. Accept:
- **Approval** -> proceed with proposed path
- **Adjustment** -> modify and re-present
- **"Skip to X"** -> jump to specified phase (log skipped gates as tech debt)

### Step 6: Handoff

Transition to the first skill in the proposed path, passing the intake brief as context.

## Methodology Selection Signals

- **Spec-driven**: regulated industry, contractual deliverable, large team, compliance, safety-critical
- **Agile**: product iteration, startup, evolving requirements, small team, SaaS
- **Waterfall**: well-understood requirements, enterprise, distributed teams, compliance checkpoints
- **Hotfix**: production down, security vulnerability, data corruption, revenue impact
- **Greenfield**: no existing codebase, new product/service, proof of concept
- **Brownfield**: legacy system exists, migration needed, modernization goal

## Anti-Patterns

1. **Skipping intake for "obvious" tasks** -- Even simple changes benefit from 30 seconds of context. The fast-track exists for truly trivial work.
2. **Over-questioning** -- Intake should take 1-5 minutes, not 30. If you need 5+ questions, you're in discovery territory -- recommend moving there.
3. **Guessing the methodology** -- Don't assume agile because it's popular. Match methodology to constraints and context.
4. **Rigid phase assignment** -- The lifecycle is a guide, not a prison. A bug fix might need architecture review if it reveals a design flaw.
5. **Ignoring existing context** -- If the project has CLAUDE.md, existing specs, or established conventions, incorporate them.

## Examples

### Feature Request
```
User: "Add dark mode support to the settings page"

Intake Brief:
- Work type: New Feature
- Entry phase: 01-specification
- Workflow: agile-sprint
- Skills: spec-writing -> system-design -> task-breakdown -> tdd -> code-review
- Scope: medium
- Risks: CSS architecture may not support theming cleanly
```

### Production Bug
```
User: "Users are getting 500 errors on checkout"

Intake Brief:
- Work type: Hotfix
- Entry phase: 04-implementation (skip to diagnosis)
- Workflow: hotfix
- Skills: debugging -> tdd (regression test) -> code-review -> deployment
- Scope: small (hopefully)
- Risks: Root cause may be in payment provider, not our code
```

### New Project
```
User: "I want to build a CLI tool for managing database migrations"

Intake Brief:
- Work type: New Product
- Entry phase: 00-discovery
- Workflow: greenfield
- Skills: feasibility -> requirements -> system-design -> tech-selection -> tdd
- Scope: large
- Risks: Scope creep, existing tools in space
```
