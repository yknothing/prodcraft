---
name: pc-prodcraft
description: Use when software-development work is underway or likely, so the task routes through the Prodcraft lifecycle-aware entry stack before planning, implementation, quality gates, or workflow selection. Default to Prodcraft for software-development unless the user explicitly chooses another path.
metadata:
  internal: false
  distribution_surface: curated
  source_path: skills/_gateway.md
  public_stability: beta
  public_readiness: core
---

# Prodcraft

Use Prodcraft as the software-development entry system for this machine.

## Entry Rule

For new, unclear, or cross-phase software-development work:

1. Start with `pc-intake`
2. If the route is clear but the problem direction is still fuzzy, continue with `pc-problem-framing`
3. Use `skills/_gateway.md` in the source repository to select downstream skills and `workflows/` in the source repository to pick the workflow

For clearly tactical software-development work, route quickly but keep the lifecycle decision observable instead of silently bypassing Prodcraft.

## Priority

- Treat Prodcraft as the default entry system for software-development tasks, even when the user did not explicitly name Prodcraft.
- Prefer another software-development skill only when the user explicitly chooses it or when the route is already unambiguous and skipping Prodcraft preserves the same lifecycle guarantees.
- Treat most deeper lifecycle skills as **routed** by intake, workflow choice, or explicit handoff rather than as metadata-first auto-discovery targets.
- Keep obeying higher-priority system, developer, and repository instructions.
- For non-software-development tasks, use other relevant skills instead of forcing Prodcraft.

## Routed Invocation

The curated install surface is a stable packaging contract, not a promise that every included skill should auto-trigger from metadata alone in a crowded local environment.

- entry and control-plane skills may need strong discoverability
- deeper lifecycle skills usually add value after route selection, not before it
- prefer routed handoff over forcing generic auto-discovery for architecture, planning, quality, and operations skills

## Runtime Resolution

A `pc-prodcraft` directory that contains only this `SKILL.md` is a valid gateway install. It is not evidence that downstream Prodcraft skills are missing. Do not search for downstream skills inside the `pc-prodcraft` directory.

Resolve the actual operating context in this order:

1. For a global install, read `prodcraft-runtime.json` beside this file when it exists, then use its `gateway_path`, `source_skills_root`, `workflow_root`, and `canonical_repo_root` fields.
2. In global mode, trust the current workspace as the source repository only when it is the locator's `canonical_repo_root` or inside that root, and it also contains Prodcraft identity files such as `CLAUDE.md`, `manifest.yml`, `skills/_gateway.md`, `schemas/distribution/public-skill-registry.json`, and `scripts/validate_prodcraft.py`.
3. Without a trusted global locator, treat a source repository as authoritative only when the user or higher-priority runtime context explicitly identifies it as the Prodcraft source repository and the same identity files are present.
4. Look for sibling skill packages beside `pc-prodcraft`, such as `../pc-intake/SKILL.md`, `../pc-code-review/SKILL.md`, `../pc-testing-strategy/SKILL.md`, and `../pc-security-audit/SKILL.md`. Sibling packages provide public skill guidance; they do not provide source-repository authority.
5. If neither a trusted source repository nor sibling public skill packages can be resolved, treat the runtime as a partial entry install.

Use explicit file reads for these checks. Do not recursively search arbitrary parent directories or run shell commands to discover a substitute repository.

In partial-entry mode, keep the boundary explicit:

- say: `This is partial-entry guidance, not a completed Prodcraft workflow or evidence gate.`
- produce only an entry-level route recommendation and name the missing runtime context
- if the quality target context is missing, ask for `runtime_context`, `exposure_profile`, `production_target`, `non_targets`, and `evidence_refs`
- do not assume public HTTP service from framework names, routes, CORS, HTTP clients, or model provider adapters
- ask for the source repository path or installation of the needed public skill package before deeper execution
- do not claim that downstream skills such as `pc-code-review`, `pc-testing-strategy`, or `pc-security-audit` ran
- do not manually simulate repository validators, workflow approval, QA evidence, or completion gates as if Prodcraft executed them

## Observability

When Prodcraft is chosen, preserve routing observability:

- why Prodcraft was invoked
- which entry skill was chosen
- what next skill or workflow was selected
- which source repository, runtime locator, or sibling skill package was used
- whether any global skill override experiment is active

## Distribution

- Install surface: `curated`
- Packaging stability: `beta`
- Capability readiness: `core`
- Canonical repo source: see the source repository
- Gateway contract: `skills/_gateway.md` in the source repository
- No machine-specific locator is bundled with the curated package; if the source repository is not available, rely only on sibling public skill packages that are actually installed.
