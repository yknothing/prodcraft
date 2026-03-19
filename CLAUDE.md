# Prodcraft - Claude Code Integration

## Project Overview

Prodcraft is a lifecycle-aware skills system for production-grade software development. It organizes skills by development phase (00-discovery through 08-evolution), defines methodology-specific workflows (spec-driven, agile, waterfall), and provides AI agent personas for multi-agent collaboration.

## MANDATORY ENTRY POINT

**Every new piece of work MUST begin with the `intake` skill** (`skills/00-discovery/intake/SKILL.md`).

Intake triages the work, determines the lifecycle phase and methodology, and routes to the correct skill sequence. This is a hard gate -- no implementation, architecture, or planning work may begin until intake is complete and the user approves the proposed path.

If intake identifies the route but the problem statement or solution direction is still too fuzzy for clean downstream work, hand off to `skills/00-discovery/problem-framing/SKILL.md` before moving deeper into the lifecycle. Keep intake concise; do not turn it into a full design workshop.

The routing logic is defined in `skills/_gateway.md`, which maps user intent to skill sequences, handles workflow selection, and defines fast-track rules for trivial changes.

Exceptions: if the user explicitly requests to skip intake for trivial work (typo fixes, comment updates), produce a 2-3 sentence intake summary and confirm.

## Key Concepts

- **Gateway** (`skills/_gateway.md`) is the routing logic that connects user intent to the right skill sequence
- **Intake** (`skills/00-discovery/intake/SKILL.md`) is the mandatory first skill -- triage, classify, route
- **Skills** (`skills/`) are atomic units of development practice. Each has frontmatter declaring its phase, inputs, outputs, prerequisites, and quality gate.
- **Workflows** (`workflows/`) orchestrate skills into methodology-specific sequences. Same skills, different composition.
- **Personas** (`personas/`) define AI agent roles with specific responsibilities and perspectives.
- **Rules** (`rules/`) define quality criteria applied at different phases.
- **Templates** (`templates/`) provide starting structures for key documents.

## File Conventions

- Skill files: `skills/{phase}/{skill-name}/SKILL.md` with Anthropic runtime frontmatter plus Prodcraft `metadata`
- Phase overview files: `skills/{phase}/_phase.md` describing entry/exit criteria
- Schema files: `skills/_schema.md`, `workflows/_schema.md`, `personas/_schema.md`
- QA evidence: `eval/{phase}/{skill-name}/` mirrors the `skills/` directory tree; each directory holds eval sets, fixtures, benchmark results, and findings for one skill
- All file names use kebab-case
- All content in English

## Working with This Project

When editing skills:
- Maintain the frontmatter schema: top-level `name` and `description`, with Prodcraft lifecycle fields under `metadata`
- Ensure inputs reference outputs from earlier-phase skills
- Ensure quality gates are measurable and verifiable
- Cross-reference related skills using canonical `SKILL.md` links; from a skill body, same-phase links look like `[skill-name](../skill-name/SKILL.md)` and cross-phase links look like `[skill-name](../../phase/skill-name/SKILL.md)`

When editing workflows:
- Workflows compose skills, they do not duplicate skill content
- Each workflow step references a skill by name
- Quality gates in workflows must match skill-level gates

When editing personas:
- Personas define perspective and judgment criteria, not step-by-step instructions
- Each persona declares which phases it leads and which it advises on

## Skill Quality Assurance

**Every new or modified skill MUST go through the skill-creator QA pipeline** before being marked as production-ready. See `skills/_quality-assurance.md` for the full process.

Key checkpoints:
1. **Structure validation**: Use `/skill-creator` to validate format and frontmatter
2. **Trigger accuracy**: Run `/skill-creator eval` to test triggering precision
3. **Performance benchmarking**: Run `/skill-creator benchmark` for variance analysis
4. **Description optimization**: Run `/skill-creator optimize` for trigger accuracy
5. **Security review**: Complete the security checklist (prompt injection, command safety, data protection, scope limitation, supply chain safety)

Skills move through statuses: draft -> review -> tested -> secure -> production.

## Build & Validation

No build system. This is a documentation/configuration project. Validation is structural:
- Every skill referenced in a workflow must exist in `skills/`
- Every persona referenced in a skill must exist in `personas/`
- Input/output chains must be acyclic (no circular dependencies between phases)
- Every skill must pass skill-creator evaluation before production status

For local QA/test/eval execution in this repository, prefer the installed `gemini` CLI. Do not use Claude CLI for routine reruns here; treat any remaining Claude-specific helpers as legacy until they are migrated.

## Style Guide

- Skills should be actionable (focus on what to do, not theory)
- Use imperative mood for instructions ("Write the test first", not "The test should be written first")
- Keep skills focused -- if a skill covers more than one concern, split it
- Prefer concrete examples over abstract principles
- Include anti-patterns alongside best practices
