# Prodcraft - Claude Code Integration

## Project Overview

Prodcraft is a lifecycle-aware skills system for production-grade software development. It organizes skills by development phase (00-discovery through 08-evolution), defines methodology-specific workflows (spec-driven, agile, waterfall), and provides AI agent personas for multi-agent collaboration.

## MANDATORY ENTRY POINT

**Every new piece of work MUST begin with the `intake` skill** (`skills/00-discovery/intake/SKILL.md`).

Intake triages the work, determines the lifecycle phase and methodology, and routes to the correct skill sequence. This is a hard gate -- no implementation, architecture, or planning work may begin until intake is complete and the user approves the proposed path.

If intake identifies the route but the problem statement or solution direction is still too fuzzy for clean downstream work, hand off to `skills/00-discovery/problem-framing/SKILL.md` before moving deeper into the lifecycle. Keep intake concise; do not turn it into a full design workshop.

The routing logic is defined in `skills/_gateway.md`, which maps user intent to skill sequences, handles workflow selection, and defines fast-track rules for trivial changes.

Trivial work does not skip intake. Use a lightweight `fast-track` intake decision (`intake_mode=fast-track`) instead of a full routing pass.

For repository-local validation experiments that need Prodcraft to become the authoritative software-development entry system, use `scripts/install_prodcraft_global_skill.py` to install the global `prodcraft` gateway skill under `~/.agents/skills/prodcraft`, and `scripts/manage_brainstorming_gate.py` to temporarily disable or restore the global `brainstorming` skill. Both scripts write reversible state and JSONL event logs under `build/` so the experiment remains observable.

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

When producing user-facing skill outputs:
- User-facing responses default to Chinese unless the user explicitly asks for another language
- Use plain language, short sentences, and direct explanations rather than abstract or inflated wording
- Keep checking current system shape and collaboration quality when they materially affect routing, scope, risk, or handoff

When revising skills and workflows:
- Keep `description` focused on **when to use** the skill
- Keep heavyweight references in supporting files instead of overloading the main skill
- Preserve explicit approval points for risky or side-effectful actions
- Add new guardrails only when they map to real observed failure modes
- Treat personas as advisory collaboration lenses unless explicit evaluation proves runtime differentiation

When editing workflows:
- Workflows compose skills, they do not duplicate skill content
- Each workflow step references a skill by name
- Quality gates in workflows must match skill-level gates

When editing personas:
- Personas define perspective and judgment criteria, not step-by-step instructions
- Each persona declares which phases it leads and which it advises on

## Skill Quality Assurance

**Every new or modified skill MUST go through the repository QA pipeline** before being marked as production-ready. See `skills/_quality-assurance.md` for the full process.

Key checkpoints:
1. **Structure validation**: Use `/skill-creator` to validate format and frontmatter
2. **Trigger accuracy**: Run `/skill-creator eval` to test triggering precision
3. **Performance benchmarking**: Run `python3 scripts/run_explicit_skill_benchmark.py ...` for isolated variance analysis (defaults to Gemini)
4. **Description optimization**: Run `/skill-creator optimize` for trigger accuracy
5. **Security review**: Complete the security checklist (prompt injection, command safety, data protection, scope limitation, supply chain safety)

Skills move through statuses: draft -> review -> tested -> secure -> production.

## Build & Validation

No build system. This is a documentation/configuration project. Validation is structural:
- Every skill referenced in a workflow must exist in `skills/`
- Every persona referenced in a skill must exist in `personas/`
- Input/output chains must be acyclic (no circular dependencies between phases)
- Every skill must pass the documented QA checks before production status
- The public install surface in `skills/.curated/` must remain exportable for `npx skills add/update`

For local QA/test/eval execution in this repository, prefer the installed `gemini` CLI. Do not use Claude CLI for routine reruns here. The exception is Anthropic-specific trigger-discoverability evaluation, which should run only through the vendored harness in `tools/anthropic_trigger_eval/` when official Claude trigger semantics are required.

## Distribution Surface

Prodcraft now maintains two layers:

- **authoring source** -- lifecycle-organized source under `skills/00-discovery/` through `skills/cross-cutting/`
- **public install surface** -- `skills/.curated/`, exported for `npx skills add/update`

The lifecycle tree is the source of truth for design and QA. The curated tree is the stable install and upgrade contract.

## Style Guide

- Skills should be actionable (focus on what to do, not theory)
- Use imperative mood for instructions ("Write the test first", not "The test should be written first")
- Keep skills focused -- if a skill covers more than one concern, split it
- Prefer concrete examples over abstract principles
- Include anti-patterns alongside best practices
