---
name: pc-prodcraft
description: Use when software-development work is underway or likely, so the task routes through the Prodcraft lifecycle-aware entry stack before planning, implementation, quality gates, or workflow selection. Default to Prodcraft for software-development unless the user explicitly chooses another path.
metadata:
  internal: false
  distribution_surface: curated
  source_path: skills/_gateway.md
  public_stability: beta
  public_readiness: beta
---

# Prodcraft

Use Prodcraft as the software-development entry system for this machine.

## Entry Rule

For new software-development work or a material change to scope, outcome, risk, or authority:

1. Start with `pc-intake`
2. If the route is clear but the problem direction is still fuzzy, continue with `pc-problem-framing`
3. Use the [portable routing map](references/routing-map.md) to select downstream skills and that generated routing map to pick the workflow

For clearly tactical software-development work, route quickly but keep the lifecycle decision observable instead of silently bypassing Prodcraft.

For continuing approved work, reuse the route and prior authorization while they still apply. A status question, clarification, or skill handoff does not restart intake. Select the next unmet obligation and one primary skill; reuse current accepted artifacts instead of rerunning their producers. Preserve required workflow gates and strict-mode operator pins.

Match the current substantive request's language in all user-facing prose, headings, questions, human-facing tags, status labels, and completion feedback. English requests receive English; Chinese requests receive Chinese. An explicit language request takes precedence. Ignore code, paths, API names, and quoted source text when selecting the language. For mixed prose use its dominant language; retain the established presentation locale when ambiguous. Re-evaluate on a substantive follow-up without restarting intake. Write new record prose in the requested language and record its actual locale where supported. Preserve machine fields/enums, skill IDs, code, paths, API names, diagnostics, and historical evidence. Lead with descriptive titles; show stable IDs beside their meaning only when needed for traceability.

Read only the selected skill, its required I/O contract, and references needed for the active step. Intake owns route and authority, workflows own sequencing and gates, and specialists own decisions and evidence. Carry accepted result pointers/revisions, constraints, gaps, and the next acceptance condition in the existing task record. Check freshness before reuse; return a specific missing fact to its producer and recheck only conclusions dependent on changed inputs. The routing map does not require loading every skill or executing every phase.

## Priority

Follow higher-priority system, developer, and repository instructions. Use Prodcraft as the default entry system for software-development tasks; honor explicit alternatives and use other skills for non-software tasks. Deeper lifecycle skills are routed by intake, workflow, or handoff. Curated packaging does not promise metadata-only auto-discovery.

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
- Capability readiness: `beta`
- Canonical repo source: see the generated routing map provenance
- Gateway contract: the [portable routing map](references/routing-map.md)
- No machine-specific locator is bundled with the curated package; if the source repository is not available, rely only on sibling public skill packages that are actually installed.
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
