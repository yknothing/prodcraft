# Prodcraft

A lifecycle-aware skills system for building and maintaining production-grade software products.

Prodcraft organizes the entire software development lifecycle into composable, methodology-agnostic skills with explicit input/output contracts, quality gates, and multi-agent collaboration patterns.

## How It Works

Every piece of work enters through the **intake** skill -- a mandatory triage that explores context, classifies the work type, determines which lifecycle phase to start at, and recommends a workflow. Think of it as a hospital triage for software development: assess first, then route.

When intake identifies the route but the problem statement or solution direction is still fuzzy, Prodcraft uses a second entry-layer skill, `problem-framing`, before deeper discovery, specification, or architecture work begins.

This hard gate is not meant to depend only on skill discoverability. Prodcraft enforces it through workflow contracts and validation: workflows declare `entry_skill: intake`, require an `intake-brief`, and CI checks those invariants.

```
User Request
    │
    ▼
┌─────────┐    ┌──────────┐    ┌───────────┐    ┌────────────┐
│ Intake   │───>│ Gateway   │───>│ Workflow   │───>│ Skills     │
│ (triage) │    │ (routing) │    │ (compose)  │    │ (execute)  │
└─────────┘    └──────────┘    └───────────┘    └────────────┘
```

The **gateway** routes to the right workflow (agile, spec-driven, waterfall, hotfix...), and the workflow composes the right skills in the right order with quality gates between phases.

## Why Prodcraft

Most development skill systems are flat collections -- useful individually but lacking the connective tissue that turns good practices into great outcomes. Prodcraft adds four structural innovations:

1. **Intake-first design** -- Every interaction starts with triage. The `intake` skill classifies work, explores context, and proposes a path before any implementation begins. If the route is clear but the concept is not, `problem-framing` compares directions and hands off a cleaner problem statement. Inspired by the brainstorming hard-gate pattern: design before code.
2. **Phase-aware skills** -- Each skill knows where it sits in the lifecycle (discovery through evolution), what it needs as input, and what it produces as output.
3. **Methodology adapters** -- The same skills can be orchestrated differently for spec-driven, agile, or iterative-waterfall development. Skills are methodology-agnostic; workflows are methodology-specific.
4. **Quality gates** -- Phase transitions have explicit entry/exit criteria. You cannot proceed to implementation without architecture review; you cannot deploy without quality verification.

## Intake Hard Gate

Prodcraft treats `intake` as a system rule, not just a trigger hint:

- New work should route through `skills/00-discovery/intake/SKILL.md`
- Every workflow requires an approved `intake-brief`
- Entry-layer decisions should stay observable through `intake-brief` and, when used, `problem-frame`
- CI validates workflow entry rules so the gate cannot silently drift out of sync

Use the validator locally:

```bash
python scripts/validate_prodcraft.py \
  --check skill-frontmatter \
  --check workflow-frontmatter \
  --check workflow-entry-gate
```

For local QA/test/eval runs in this repository, prefer the locally installed `gemini` CLI. Do not use Claude CLI for routine reruns here; its cost is too high for this project. The one exception is Anthropic-specific trigger-discoverability evaluation, which should run only through the vendored harness in `tools/anthropic_trigger_eval/` when you explicitly need official Claude trigger behavior.

## Project Structure

```
prodcraft/
  skills/                    # Core: lifecycle-organized skill definitions
    00-discovery/            # Market research, feasibility, concept validation
    01-specification/        # Requirements, specs, domain modeling, acceptance criteria
    02-architecture/         # System design, API design, data modeling, security
    03-planning/             # Task breakdown, estimation, risk assessment, sprint planning
    04-implementation/       # TDD, feature dev, refactoring, pair programming
    05-quality/              # Code review, testing, security audit, performance audit
    06-delivery/             # CI/CD, deployment, release management, feature flags
    07-operations/           # Monitoring, incident response, runbooks, capacity
    08-evolution/            # Tech debt, migration, deprecation, retrospective
    cross-cutting/           # Documentation, observability, accessibility, compliance
  eval/                      # Per-skill QA evidence, mirroring the skills/ phase structure
    00-discovery/            # Eval artifacts for discovery-phase skills
    01-specification/        # ...and so on through 08-evolution
  workflows/                 # Methodology-specific orchestrations
  personas/                  # AI agent role definitions
  rules/                     # Quality rules engine (YAML)
  templates/                 # Document templates (PRD, TDD, ADR, RFC, postmortem)
  examples/                  # Real-world usage examples
  scripts/                   # Structural validator and benchmark runner
  manifest.yml               # QA state index: skill status and evidence paths
```

## Skill Format

Every skill follows Anthropic's `SKILL.md` package shape. The runtime-discoverable fields stay at the top level, and Prodcraft lifecycle data lives under `metadata`:

```yaml
---
name: skill-name
description: "Design the system structure and major component boundaries for a scoped feature or product. Use when requirements are clear enough to choose components, interfaces, and quality-attribute trade-offs before planning or implementation."
metadata:
  phase: "02-architecture"
  inputs: ["requirements-doc", "domain-model"]
  outputs: ["system-architecture-doc", "component-diagram"]
  prerequisites: ["spec-writing", "domain-modeling"]
  quality_gate: "Architecture review approved by tech lead"
  roles: ["architect", "tech-lead"]
  methodologies: ["all"]
  effort: "medium"
---
```

- `name` / `description` -- Anthropic runtime discovery fields; keep them focused and distinctive
- `metadata.inputs` / `metadata.outputs` -- Artifacts this skill consumes and produces, forming the dependency graph
- `metadata.prerequisites` -- Other skills that should complete first
- `metadata.quality_gate` -- Exit criteria before downstream skills proceed
- `metadata.roles` -- Which personas are best suited to execute this skill
- `metadata.methodologies` -- Which workflow families or explicit workflows include this skill (`all`, `agile`, `spec-driven`, `waterfall`, `greenfield`, `brownfield`, `hotfix`)
- `metadata.effort` -- Relative effort: `small` (<1h), `medium` (1-4h), `large` (4h-2d), `xlarge` (2d+)

## Workflows

Three methodology adapters compose the same skills differently:

| Workflow | Cadence | Planning Depth | Documentation | Best For |
|----------|---------|----------------|---------------|----------|
| **Spec-Driven** | Milestone-based | Deep upfront | Comprehensive | Regulated, safety-critical, contractual |
| **Agile Sprint** | 1-2 week sprints | Just enough | Living docs | Product teams, SaaS, rapid iteration |
| **Iterative Waterfall** | Phase-gated | Phase-complete | Phase deliverables | Enterprise, large teams, compliance |

Additional workflows: `hotfix` (emergency path), `greenfield` (new project bootstrap), `brownfield` (legacy modernization).

## Personas

AI agent roles that collaborate across the lifecycle:

| Persona | Primary Phases | Core Responsibility |
|---------|----------------|---------------------|
| Product Manager | Discovery, Specification | Requirements, prioritization, stakeholder alignment |
| Architect | Architecture, Planning | System design, tech decisions, quality attributes |
| Developer | Implementation | Code, tests, incremental delivery |
| Reviewer | Quality | Code review, design review, knowledge sharing |
| QA Engineer | Quality, Delivery | Test strategy, automation, regression |
| DevOps Engineer | Delivery, Operations | CI/CD, infrastructure, reliability |
| Tech Lead | All phases | Coordination, mentoring, technical decisions |

## Quality Gates

Phase transitions are guarded by explicit criteria:

```
Discovery ──[Feasibility approved]──> Specification
Specification ──[Spec reviewed & signed off]──> Architecture
Architecture ──[Design review passed]──> Planning
Planning ──[Tasks estimated & assigned]──> Implementation
Implementation ──[All tests pass, code reviewed]──> Quality
Quality ──[QA sign-off, security cleared]──> Delivery
Delivery ──[Deployment verified, rollback tested]──> Operations
Operations ──[SLOs met, runbooks validated]──> Evolution
Evolution ──[Retrospective complete]──> Discovery (next cycle)
```

## Quick Start

### Using with Claude Code

1. Symlink or copy skills to your Claude skills directory:
   ```bash
   ln -s /path/to/prodcraft/skills ~/.claude/skills/prodcraft
   ```

2. Start new work through the intake skill and follow the routed workflow:
   - open `skills/00-discovery/intake/SKILL.md`
   - produce an `intake-brief`
   - use `skills/_gateway.md` plus the selected file in `workflows/` to choose the next skills

3. Invoke individual skills by loading their `SKILL.md` packages in context. For example:
   - `skills/04-implementation/tdd/SKILL.md`
   - `skills/05-quality/code-review/SKILL.md`
   - `skills/06-delivery/ci-cd/SKILL.md`

Prodcraft does **not** ship a standalone `/orchestrator` command. The orchestration layer is defined by the checked-in skill packages, gateway rules, workflow files, and validator.

### Standalone Usage

Each skill is a self-contained Anthropic skill package. Read and apply the guidance directly:
```bash
cat skills/04-implementation/tdd/SKILL.md
```

## Design Principles

1. **Skills are atomic** -- Each skill does one thing well and can be used independently.
2. **Workflows are compositions** -- Methodologies differ in how they compose skills, not which skills exist.
3. **Contracts are explicit** -- Every skill declares its inputs, outputs, and quality gate.
4. **Phases are permeable** -- Quality gates exist but can be bypassed with explicit justification (documented as technical debt).
5. **Personas are advisors** -- Each role brings a perspective; the developer makes the final call.
6. **Rules are tiered** -- Must (blocking), Should (advisory), May (informational).
7. **Evolution is built-in** -- Every cycle ends with retrospective that feeds the next discovery phase.

## Contributing

1. Follow the skill schema defined in `skills/_schema.md`
2. Every new skill needs: clear trigger conditions, input/output contracts, and quality gate
3. Test skills in real projects before submitting
4. Workflows should compose existing skills, not duplicate them

## License

MIT
