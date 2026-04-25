# Prodcraft

Prodcraft is a lifecycle-aware skills system for production-grade software development. It turns engineering discipline into repository-owned skills, workflows, artifact contracts, validators, and evidence records that can survive across agent runtimes.

This English README is the canonical project overview. A non-authoritative Chinese reader guide is available at [README.zh-CN.md](README.zh-CN.md).

## Current State

As of 2026-04-25, the checked-in system contains:

- 44 lifecycle skill packages in `skills/00-discovery/` through `skills/cross-cutting/`
- authored-skill maturity in `manifest.yml`: 6 `production`, 32 `tested`, 6 `review`, 0 `draft`
- 6 workflow files: 3 primary methodology workflows and 3 overlays
- 7 advisory personas
- 6 registered protocol artifact schemas
- 40 generated public skills in `skills/.curated/`

The current canonical architecture state is [Architecture State Bundle](docs/architecture/2026-04-18-prodcraft-architecture-state-bundle.md). Its core position is that Prodcraft is not just a skill library. It is a host-agnostic governance system for production engineering, with repository-owned contracts as the authority and host bindings as adapters.

The current architecture model uses four content layers:

| Layer | Role |
|---|---|
| Knowledge | Teaches judgment, patterns, and trade-offs. It does not prove compliance by itself. |
| Protocol | Preserves state and contract shape through artifacts such as `intake-brief`, `course-correction-note`, and `verification-record`. |
| Enforcement | Blocks, validates, warns, or checks repository-owned contracts. |
| Evidence | Proves or challenges real execution behavior, including verification results, findings, benchmarks, and audit traces. |

Those layers are evaluated across three consumer surfaces: `repo_internal`, `host_runtime`, and `public_export`.

## Guarantees And Limits

Prodcraft can currently enforce and validate structural contracts such as workflow entry gates, artifact schema shape, curated-surface parity, portability metadata, and security-minimal checks.

Prodcraft does not claim that structural checks prove semantic engineering quality. A valid schema does not prove a good requirement, a passing review template does not prove high-quality review, and `verification-record.v1` does not by itself prove route-level completion. Judgment-heavy work still needs bounded evidence, review, and route-specific acceptance.

The downstream execution loop is still being hardened. AR-01, AR-02, AR-03, and the public portability review are active governance workstreams, not proof that every execution-critical rule is already enforced.

## How It Works

Every piece of engineering work starts with `intake`, the mandatory triage skill. Intake classifies the request, chooses the lifecycle entry point, records the route decision, and hands off to the next skill or workflow.

If the route is clear but the problem statement or solution direction is still fuzzy, `problem-framing` runs before deeper discovery, specification, or architecture work begins.

```text
User request
  -> intake
  -> gateway
  -> workflow
  -> routed skills
  -> artifact contracts
  -> validation and evidence
```

The gateway in `skills/_gateway.md` connects the route decision to one of the workflows in `workflows/`. Workflows compose existing skills; they do not duplicate skill content.

## Why Prodcraft

Most development skill systems are flat collections. Prodcraft adds the control plane around those skills:

1. **Intake-first routing** -- new work records an explicit route before execution begins.
2. **Phase-aware skills** -- every skill declares where it sits in the lifecycle, what it consumes, and what it produces.
3. **Methodology adapters** -- the same skills can run through agile, spec-driven, or iterative-waterfall workflows.
4. **Protocol artifacts** -- route, correction, requirement, review, and verification state can be externalized instead of living only in chat history.
5. **Repo-native validation** -- the repository validates the contract shape that should not depend on model self-discipline.
6. **Evidence-led hardening** -- new controls should be promoted only when evidence supports the friction and signal quality.

## Intake Hard Gate

Prodcraft treats `intake` as a system rule, not just a trigger hint:

- New work should route through `skills/00-discovery/intake/SKILL.md`.
- Every workflow declares `entry_skill: intake`.
- Every workflow requires an `intake-brief`.
- Entry-layer decisions should stay observable through `intake-brief` and, when needed, `problem-frame`.
- CI and local validators check workflow entry rules so the gate cannot silently drift.

Use the validator locally:

```bash
python scripts/validate_prodcraft.py \
  --check skill-frontmatter \
  --check workflow-frontmatter \
  --check workflow-entry-gate
```

For full local QA on this repository, prefer Python 3.11 through `uv` because some tests use modern Python syntax:

```bash
UV_CACHE_DIR=/tmp/uv-cache-prodcraft uv run --python 3.11 --with pyyaml --with jsonschema python -m unittest discover tests
UV_CACHE_DIR=/tmp/uv-cache-prodcraft uv run --python 3.11 --with pyyaml --with jsonschema python scripts/validate_prodcraft.py
```

For local QA, test, and eval execution, prefer the installed `gemini` CLI. Do not use Claude CLI for routine reruns here. The exception is Anthropic-specific trigger-discoverability evaluation, which should run only through the vendored harness in `tools/anthropic_trigger_eval/`.

## Artifact Contracts

Protocol artifacts are registered in `schemas/artifacts/registry.yml` and backed by schemas and templates. Current registered artifacts include:

- `intake-brief`
- `problem-frame`
- `requirements-doc`
- `course-correction-note`
- `review-report`
- `verification-record`

`verification-record.v1` is the first repo-native foothold for completion-claim proof shape. It requires evidence references, checks run, pass/fail lists, remaining unverified scope, and `claim_may_be_made` alignment. A completion claim may be made only when the record is accepted, checks are passed, and no failed or unverified items remain.

This is intentionally narrow. `verification-record.v1` validates proof shape; route-level acceptance and semantic adequacy still require workflow rules, artifact-flow checks, and human or agent review for the specific route.

## Routed vs Discoverability

Prodcraft does **not** assume every skill should be found from metadata alone.

- **discoverability-first** skills are the small control-plane set whose value depends on being surfaced directly from a user request.
- **routed** skills are the majority of the lifecycle spine and are usually invoked by `intake`, workflow selection, or explicit handoff from an upstream skill.

This means:

- the public install surface in `skills/.curated/` is an install and upgrade contract, not a promise that every skill should auto-trigger in a crowded environment
- review or benchmark evidence for routed skills matters more than raw trigger recall
- if a deeper lifecycle skill adds value mainly after handoff, Prodcraft treats routed invocation as the primary contract
- repository maturity and public installability are separate signals; a skill can be `tested` in `manifest.yml` without being part of the public install surface
- moving a skill to `tested` does **not** automatically publish it to `npx`; public export still happens through `schemas/distribution/public-skill-registry.json`
- public registry entries separate **packaging stability** from **capability readiness**

## Public Install Surface

Prodcraft supports the public Agent Skills install flow:

```bash
npx skills add <repo-url>
npx skills add <repo-url> --skill intake
npx skills update
```

The canonical public beta install surface is `skills/.curated/`. It is generated from repository registries and should not be edited by hand.

Public export is governed by two registries:

- `schemas/distribution/public-skill-registry.json` answers which skills are packaged.
- `schemas/distribution/public-skill-portability.json` answers what value survives outside the full repository control plane.

Portability classifications are:

- `portable_as_is`: the exported skill does not depend on hidden repository protocol, validation, or evidence context.
- `portable_with_caveat`: the skill remains useful as portable guidance, but full governance guarantees require named repository context.
- `blocked`: the skill must not be exported in its current form.

Current public skills are conservatively classified as `portable_with_caveat`. The generated `skills/.curated/index.json` exposes only public-safe portability fields: `portability` and, when needed, `public_caveat_text`. Hidden dependency notes stay in the repository registry.

Regenerate and validate the curated surface:

```bash
python scripts/export_curated_skills.py
python scripts/validate_prodcraft.py --check curated-surface
```

## External Skill Integration Boundary

Prodcraft can absorb ideas from other skill systems and can extend itself through plugin-like or delegation-style boundaries.

- absorb methods, guardrails, and workflow patterns from external skills or skills projects when they improve Prodcraft
- integrate external capability through explicit plugin, wrapper, adapter, or delegation boundaries
- do not directly reference external skills at the source-code level
- do not make external skills an implicit runtime dependency of this repository
- when importing an idea, restate it as a local Prodcraft contract, artifact, workflow rule, or skill so validation and QA remain owned here

## Architecture Governance

Current architecture governance is split deliberately:

- Canonical current state: [Architecture State Bundle](docs/architecture/2026-04-18-prodcraft-architecture-state-bundle.md)
- Historical synthesis source: [Architecture Evolution Basis](docs/architecture/2026-04-17-prodcraft-architecture-evolution-basis.md)
- Execution support register: [Architecture Review Action Register](docs/architecture/2026-04-17-architecture-review-action-register.md)
- AR-01 measurement protocol: [Enforcement Promotion Measurement Protocol](docs/architecture/ar-01-enforcement-promotion-measurement-protocol.md)
- Provisional AR-03 host policy: [Host Adapter Policy](docs/architecture/ar-03-host-adapter-policy.md)

The current action sequence is:

1. Treat the AR-01 provisional enforcement promotion matrix as the current planning input, not as canonical architecture policy.
2. Run AR-02 first repo-native downstream execution checks on a small execution-critical slice.
3. Formalize or implement AR-03 host adapters only after repository-owned contracts are clear.
4. Extend AR-04 `.curated/` portability review from the initial static review to live full-repo versus curated-only task runs.
5. Audit AR-05 protocol artifacts for essential versus accidental complexity.

Do not treat conceptual contracts in the architecture bundle as executable API definitions until they are represented in schemas, validators, workflow contracts, manifest artifact flow, or generated public artifacts.

## Project Structure

```text
prodcraft/
  skills/
    00-discovery/            # Intake, research, framing, feasibility
    01-specification/        # Requirements, specs, domain modeling, acceptance criteria
    02-architecture/         # System design, API design, data modeling, security
    03-planning/             # Task breakdown, estimation, risk, sprint planning
    04-implementation/       # TDD, feature development, refactoring
    05-quality/              # Review, testing, audit, performance
    06-delivery/             # CI/CD, deployment, release, verification
    07-operations/           # Monitoring, incidents, runbooks, capacity
    08-evolution/            # Tech debt, migration, deprecation, retrospectives
    cross-cutting/           # Documentation, observability, accessibility, compliance
    .curated/                # Generated public install surface
  workflows/                 # Primary methodology workflows and overlays
  personas/                  # Advisory agent roles
  schemas/
    artifacts/               # Protocol artifact schemas and registry
    distribution/            # Public export and portability registries
  templates/                 # Artifact templates
  rules/                     # Structural quality and governance rules
  docs/                      # Architecture, ADR, distribution, observability, and plans
  eval/                      # Per-skill QA evidence
  tests/                     # Structural and contract tests
  scripts/                   # Validators, exporters, benchmark runners, cutover tools
  manifest.yml               # Skill maturity and evidence index
```

## Skill Format

Every skill follows Anthropic's `SKILL.md` package shape. Runtime-discoverable fields stay at the top level, and Prodcraft lifecycle data lives under `metadata`:

```yaml
---
name: skill-name
description: "Use when requirements are clear enough to choose components, interfaces, and quality-attribute trade-offs before planning or implementation."
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

Important fields:

- `name` and `description`: runtime discovery fields; keep them focused and distinctive
- `metadata.inputs` and `metadata.outputs`: artifact contracts that form the dependency graph
- `metadata.prerequisites`: skills that should complete first
- `metadata.quality_gate`: exit criteria before downstream work proceeds
- `metadata.roles`: advisory personas suited to the skill
- `metadata.methodologies`: workflow families or explicit workflows that include the skill
- `metadata.effort`: relative execution effort

## Workflows

Three primary workflows compose the same skills differently:

| Workflow | Cadence | Planning depth | Documentation | Best for |
|---|---|---|---|---|
| Spec-driven | Milestone-based | Deep upfront | Comprehensive | Regulated, safety-critical, contractual work |
| Agile sprint | 1-2 week sprints | Just enough | Living docs | Product teams, SaaS, rapid iteration |
| Iterative waterfall | Phase-gated | Phase-complete | Phase deliverables | Enterprise, large-team, compliance-heavy work |

Three overlays adapt the primary workflows:

- `hotfix`: emergency path
- `greenfield`: new project bootstrap
- `brownfield`: legacy modernization and coexistence

## Personas

Personas are advisory collaboration lenses, not autonomous authorities.

| Persona | Primary phases | Core responsibility |
|---|---|---|
| Product Manager | Discovery, Specification | Requirements, prioritization, stakeholder alignment |
| Architect | Architecture, Planning | System design, technical decisions, quality attributes |
| Developer | Implementation | Code, tests, incremental delivery |
| Reviewer | Quality | Code review, design review, knowledge sharing |
| QA Engineer | Quality, Delivery | Test strategy, automation, regression |
| DevOps Engineer | Delivery, Operations | CI/CD, infrastructure, reliability |
| Tech Lead | All phases | Coordination, mentoring, technical decisions |

## Quality Gates

Phase transitions are guarded by explicit criteria:

```text
Discovery      -> Specification  [feasibility approved]
Specification  -> Architecture   [spec reviewed and signed off]
Architecture   -> Planning       [design review passed]
Planning       -> Implementation [tasks estimated and assigned]
Implementation -> Quality        [tests pass and code reviewed]
Quality        -> Delivery       [QA and security cleared]
Delivery       -> Operations     [deployment verified]
Operations     -> Evolution      [SLOs and runbooks validated]
Evolution      -> Discovery      [retrospective informs next cycle]
```

Quality gates are not magic. They are useful only when the required state, artifact, or evidence is explicit enough to be reviewed or validated.

## Quick Start

### Work from the repository

1. Read `CLAUDE.md` for mandatory project rules.
2. Start through `skills/00-discovery/intake/SKILL.md`.
3. Use `skills/_gateway.md` and the selected file in `workflows/` to route the next skills.
4. Produce the required protocol artifacts from `templates/`.
5. Run validators before claiming completion.

### Use the public skill surface

```bash
npx skills add <repo-url> --skill prodcraft
```

The public surface is useful for portable guidance and entry routing. Full governance guarantees require the source repository contracts, schemas, validators, and evidence paths.

### Standalone usage

Each skill package can still be read directly:

```bash
cat skills/04-implementation/tdd/SKILL.md
```

Prodcraft does **not** ship a standalone `/orchestrator` command. The orchestration layer is defined by checked-in skill packages, gateway rules, workflow files, validators, and artifact registries.

## Operator Notes

For gray-rollout or production cutovers where Prodcraft should become the default software-development entry system, use `scripts/install_prodcraft_global_skill.py` to manage the global `~/.agents/skills/prodcraft` gateway and `scripts/archive_superpowers_skills.py` to archive or restore conflicting global superpowers skills. Both scripts write reversible state and event logs under `build/`, which is gitignored.

For routine local QA, prefer the installed `gemini` CLI where this repository asks for model-backed evals. Use the vendored Anthropic trigger harness only when official Claude trigger behavior is the object under test.

## Design Principles

1. **Repository-owned contracts are sovereign** -- host integrations adapt the repo contract; they do not replace it.
2. **Skills are atomic** -- each skill should do one thing well and compose through workflows.
3. **Workflows are compositions** -- methodologies differ in sequencing and gates, not by duplicating skill content.
4. **State must survive handoff** -- route decisions, assumptions, blockers, corrections, and verification boundaries need artifacts.
5. **Cheap checks do not prove semantic quality** -- validation can enforce shape, but judgment-heavy work still needs review and evidence.
6. **Public export must not overclaim** -- the curated surface must say what survives outside repository context.
7. **Evolution is evidence-led** -- repeated friction can justify simplification or hardening; instinct alone should not.

## Contributing

1. Start with `intake`, even for small work. Use fast-track only when the route is clear.
2. Keep canonical repository artifacts in English.
3. Put user-facing localized guidance in explicitly named companion docs only when needed.
4. Follow `skills/_schema.md` and the relevant artifact schemas.
5. Update tests or validators when a claim becomes a repository contract.
6. Run `scripts/validate_prodcraft.py` and the focused unit tests for the touched surface.
7. Do not manually edit `skills/.curated/`; regenerate it from the export script.

## License

MIT
