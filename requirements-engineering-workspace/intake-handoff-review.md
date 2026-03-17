# Intake-to-Requirements Handoff Review

## Goal

Verify that `requirements-engineering` preserves an approved `intake-brief` when entering the `01-specification` phase.

## Artifacts Reviewed

- Initial long-prompt handoff run: `intake-handoff-run-2026-03-16-approvals`
- Optimized context-file handoff run: `intake-handoff-run-2026-03-16-approvals-rerun`
- Pending brownfield modernization run: `intake-handoff-run-2026-03-17-modernization`

## What Changed Between Runs

The initial handoff benchmark inlined the full intake brief and discovery notes into the prompt. That made the benchmark expensive and the with-skill branch timed out.

The rerun moved the handoff artifacts into separate context files and shortened the prompt. This better matches how skills are supposed to load context progressively and eliminated the timeout.

## Initial Run Findings

- Baseline produced a usable requirements document.
- With-skill timed out.
- Because the prompt was unnecessarily long, this run is useful mainly as a benchmark-design lesson, not as the main evidence artifact.

## Rerun Findings

### Baseline

Baseline preserved many handoff constraints, but it drifted on an important scope boundary:

- it promoted department-specific thresholds into release-1 in-scope requirements
- it did not preserve downstream handoff notes as explicitly
- it preserved open questions reasonably well

### With Skill

The with-skill output showed stronger handoff fidelity:

- kept the work clearly in the requirements layer
- preserved intake risks as explicit `Risks`
- preserved intake open questions as unresolved `Open Questions`
- respected the "no invented precision" constraint by leaving `near-instant` as an open question rather than fabricating a latency target
- preserved downstream handoff intent (`spec-writing`, `acceptance-criteria`) explicitly
- correctly treated department-specific thresholds as **out of scope for release 1**, matching the intended scope boundary better than baseline

## Assertion Review

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| stays in specification phase | pass | pass | Neither output jumped into API or schema design. |
| preserves intake risks | partial | pass | Baseline captured some ambiguity, but with-skill preserved intake risks more explicitly. |
| preserves intake open questions | pass | pass | With-skill structured them more cleanly. |
| respects no invented precision | pass | pass | With-skill explicitly reinforced the open-question treatment of `near-instant`. |
| prepares downstream handoff | partial | pass | With-skill named downstream handoff expectations more clearly. |

## Conclusion

This is the first good evidence that `requirements-engineering` is not just a useful standalone skill, but also a useful **workflow skill** inside Prodcraft.

The skill improves:

- scope-boundary preservation
- risk carry-through
- open-question preservation
- downstream handoff readiness

These are exactly the dimensions that matter in a lifecycle-aware system.

## Remaining Limits

- This handoff evidence is one scenario only.
- It does not resolve the weak trigger-discoverability result.
- It should increase confidence in the skill as a routed/core workflow skill, not as an auto-discoverable skill.

## Brownfield Modernization Scenario

To test whether handoff quality generalizes beyond a net-new feature flow, a second routed handoff scenario was added:

- `access-review-modernization-handoff`

This scenario stresses:

- brownfield coexistence constraints
- incomplete contractual compatibility knowledge
- open questions around migration boundaries
- qualitative NFR pressure without approved numeric targets

### First Execution Attempt

The first official execution artifact exists at `intake-handoff-run-2026-03-17-modernization`, but it did **not** yield model outputs.

Both branches failed before response generation with the local CLI message:

`Not logged in · Please run /login`

Interpretation:

- this is a local harness precondition failure, not evidence against the skill
- the new scenario is now part of the checked-in QA corpus
- the scenario must be rerun once the local Claude CLI authentication state is restored

Until that rerun exists, the approvals scenario remains the only completed routed handoff evidence artifact.

## Manual Brownfield Evaluation

Because a non-CLI evaluation was explicitly requested, a supplemental manual review was added at:

- `intake-handoff-manual-run-2026-03-17-modernization`

This manual evaluation includes both:

- a generic baseline response without the skill
- a skill-applied response using `requirements-engineering`

Important limitation:

- this is **not** an isolated automated benchmark
- both branches were authored under one reviewer context
- treat it as supplemental evidence about likely handoff behavior, not as a replacement for isolated benchmark evidence

### Manual Baseline Findings

The baseline response is competent, but it drifts on several points that matter in a lifecycle-aware system:

- it keeps the work in the requirements layer
- it preserves the high-level coexistence constraint
- it fails to keep the read-only historical-campaign boundary as an explicit requirement
- it turns `same-day sync` into a requirement instead of preserving the intake ambiguity cleanly
- it pulls data-correction and reviewer reassignment into release 1 requirements without clearly marking the scope uncertainty
- it is less explicit about downstream handoff shape

### Manual With-Skill Findings

The skill-applied response is materially stronger on the handoff dimensions that matter here:

- it stays in the requirements layer
- it preserves the brownfield coexistence boundary as an explicit release-1 requirement
- it keeps historical legacy read-only treatment visible as a scope boundary instead of silently collapsing it
- it preserves unresolved contractual and synchronization questions as open questions
- it converts unsupported precision into requirement direction plus explicit uncertainty
- it distinguishes release-1 obligations from out-of-scope rewrite and cutover work
- it prepares the artifact for downstream `system-design` and `acceptance-criteria`

### Manual Assertion Review

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| stays in specification phase | pass | pass | Neither branch jumps into architecture or migration sequencing. |
| preserves brownfield boundary | partial | pass | Baseline mentions coexistence but is weaker on legacy-read-only and release boundary handling. |
| preserves intake risks | partial | pass | With-skill keeps contractual ambiguity and scope pressure more explicitly. |
| preserves intake open questions | partial | pass | Baseline keeps some questions, but with-skill protects them more clearly. |
| respects no invented precision | partial | pass | Baseline turns `same-day sync` into a requirement; with-skill leaves the bound unresolved. |
| prepares downstream handoff | partial | pass | With-skill makes downstream constraints and handoff intent explicit. |

### Manual Conclusion

This supplemental manual review supports the same emerging conclusion as the approvals scenario:

- `requirements-engineering` is more valuable as a **routed workflow skill** than as an auto-discoverable skill
- its value is strongest where scope boundaries, open questions, and brownfield constraints must survive handoff
- the handoff-quality signal now appears in both a feature scenario and a brownfield modernization scenario, although only one of them has completed isolated benchmark evidence so far
