# Prodcraft Maturity Hardening Plan

> Status: proposed execution plan for delegated implementation.

> Intended execution model: Gemini implements in small slices; Codex reviews and accepts or rejects each slice against this document.

**Goal:** Turn Prodcraft from a structurally consistent beta framework into a maturity-aware repository where the default execution path is both machine-enforced and honest about what is production-ready versus merely planned.

**Architecture:** Preserve the existing control plane (`intake -> gateway -> workflow -> skill -> evidence`). Do not redesign the lifecycle. Instead, tighten the maturity contract around that lifecycle so default routes no longer rely on hidden draft capabilities, the core spine can graduate with real evidence, and the public install surface says exactly what the repository can currently stand behind.

**Tech Stack:** Markdown, YAML, JSON, Python validator/tests, repo-local eval evidence, curated skill export.

---

## Fast-Track Intake Brief

**Work type**: Enhancement  
**Entry phase**: 03-planning  
**Intake mode**: fast-track  
**Key skills needed**: `task-breakdown`, `documentation`, `verification-before-completion`  
**Scope assessment**: large  
**routing_rationale**: The repository shape and the target outcome are already clear. The right next step is a concrete execution plan plus machine-verifiable acceptance criteria, not more discovery.  
**Key risks**:
- promoting maturity in prose without promoting it in evidence
- adding governance complexity that the validator cannot actually enforce

### Proposed Path
1. `task-breakdown` -- turn the audit findings into implementation slices with reversible sequencing
2. `documentation` -- write the repository plan and handoff contract
3. `verification-before-completion` -- require validation and evidence before status or readiness claims change

---

## Why This Iteration Exists

The current repository is already coherent and test-backed, but it has a maturity mismatch:

- the repository validates and tests successfully
- the control-plane concepts are strong
- many default workflows and cross-cutting rules still rely on skills that remain `draft`
- the public install surface is deliberately beta and manually allowlisted

That means the next high-leverage move is not "add more skills." It is to make the maturity boundary explicit and enforceable.

---

## Target Outcomes

This iteration is successful only if all of the following become true:

1. Prodcraft has at least one documented and machine-defended default path from entry to delivery that does not silently rely on `draft` skills.
2. Any remaining draft dependency is explicit, intentionally downgraded, or isolated behind a clearly named experimental/planned contract.
3. Status promotion rules are evidence-driven rather than prose-driven.
4. Public docs and public install metadata describe the repository's maturity honestly.

---

## Scope

### In Scope

- maturity-aware validation for workflow and cross-cutting dependencies
- default-path hardening for the core spine
- clearer policy for `draft` versus `review/tested/secure/production`
- doc and public-surface alignment with actual maturity
- delegated execution and review protocol using a repo-local handoff directory

### Explicitly Out of Scope

- redesigning the lifecycle model
- deleting phases, workflows, or personas wholesale
- inventing benchmark or security evidence that does not exist
- promoting every skill in the repository during this iteration
- changing the curated install shape beyond what is required for honest maturity signaling

---

## Workstream A: Maturity-Aware Dependency Contract

### Problem

Workflows and the cross-cutting matrix currently act as if many draft skills are usable default dependencies. That weakens the repository's truthfulness even if the structure remains valid.

### Desired End State

- machine-readable enforcement exists for maturity-sensitive dependency references
- default-required paths cannot silently depend on `draft` skills
- draft references remain possible only when explicitly marked as planned or experimental

### Files Likely Involved

- `manifest.yml`
- `rules/cross-cutting-matrix.yml`
- `workflows/*.md`
- `skills/_gateway.md`
- `scripts/validate_prodcraft.py`
- `tests/test_cross_cutting_matrix.py`
- `tests/test_workflow_composability.py`
- one or more new maturity-specific tests

### Tasks

#### Task A1: Define the maturity policy

- Choose the minimum policy model needed to enforce truthfulness.
- Recommended rule:
  - `must_consider` and `must_produce` may reference only non-draft skills
  - default workflow skill references may reference draft skills only when explicitly marked as planned/experimental
  - routed examples may mention draft skills, but only with visible maturity labeling

#### Task A2: Encode the policy

- Add validator logic that compares referenced skill names to manifest status.
- Add tests for both valid and invalid cases.
- Prefer a narrow enforcement model over a clever one.

#### Task A3: Reconcile repository content

- Update the cross-cutting matrix to stop defaulting to draft dependencies.
- Update workflows so any remaining draft references are visibly labeled and non-default.
- Keep wording consistent across gateway, workflows, and docs.

### Acceptance Criteria

- `python3 scripts/validate_prodcraft.py` fails when a default-required dependency references a `draft` skill without an explicit allowed pattern.
- `pytest -q` includes coverage for the new maturity rule.
- No unconditional `must_consider` or `must_produce` reference points to a `draft` skill.
- Workflow prose no longer presents draft skills as default-ready capabilities without labeling.

---

## Workstream B: Core Spine Graduation

### Problem

Prodcraft's strongest value is in its control plane and default engineering spine, but that spine is still mostly at `review` status. The repo needs one path it can genuinely stand behind.

### Target Spine

Use this exact spine as the graduation candidate unless implementation evidence proves a narrower subset is necessary:

- `intake`
- `problem-framing`
- `requirements-engineering`
- `system-design`
- `task-breakdown`
- `tdd`
- `feature-development`
- `code-review`
- `ci-cd`
- `deployment-strategy`
- `verification-before-completion`

### Desired End State

- one end-to-end spine is documented as the default path
- every skill on that spine has the evidence required for its claimed status
- no status is promoted without matching manifest, tests, and evidence

### Files Likely Involved

- `manifest.yml`
- `eval/**` for the target skills
- `skills/.curated/**`
- `schemas/distribution/public-skill-registry.json`
- `README.md`
- `docs/distribution/public-skill-lifecycle.md`
- possibly selected skill docs if evidence expectations need clarification

### Tasks

#### Task B1: Define graduation gates

- Write down what `review -> tested -> secure -> production` means for the target spine in repository terms.
- Reuse existing QA policy where possible; only add contract if a real gap exists.

#### Task B2: Fill evidence gaps for the target spine

- Do not fabricate evidence.
- If a skill cannot honestly graduate in this iteration, leave it at the appropriate lower status and document why.
- Prefer promoting fewer skills honestly over promoting many skills vaguely.

#### Task B3: Make the default path explicit

- Update docs so the repository clearly identifies:
  - the default hardened spine
  - the review-grade adjacent skills
  - the planned or experimental outer ring

### Acceptance Criteria

- At least one documented default path from entry to delivery is free of hidden draft dependency.
- Any promoted status in `manifest.yml` has matching evidence paths and passing tests.
- Public docs distinguish hardened spine versus planned outer ring.
- Curated/public metadata does not imply broader maturity than the repo can support.

---

## Workstream C: Public Surface Truthfulness

### Problem

The repository already has a curated install surface, but the public story is still closer to "beta capability set" than "explicit maturity map."

### Desired End State

- the public surface stays beta where appropriate
- the docs say exactly why it is beta
- stable names and install contract remain intact
- users can tell which parts are core, which are adjacent, and which are not yet ready

### Files Likely Involved

- `README.md`
- `docs/distribution/npx-skills-compat.md`
- `docs/distribution/public-skill-lifecycle.md`
- `schemas/distribution/public-skill-registry.json`
- `skills/.curated/index.json`

### Tasks

#### Task C1: Tighten wording

- Replace any implication that full lifecycle maturity already exists.
- State clearly that the curated surface is a stable packaging contract, not a blanket production-readiness claim.

#### Task C2: Align registry semantics

- Keep `manual_allowlist` and `beta` only where they remain justified.
- If any curated skill becomes strong enough for a higher maturity claim, update the registry and docs together.

### Acceptance Criteria

- README and distribution docs describe the same maturity story.
- Public registry entries do not conflict with repo status and evidence posture.
- `python3 scripts/validate_prodcraft.py --check curated-surface` still passes.

---

## Workstream D: Delegated Execution and Review Protocol

### Objective

Gemini should be able to execute without reconstructing intent from chat history, and Codex should be able to review without guessing what "done" means.

### Working Directory

Use:

`build/gemini-handoff/2026-04-01-prodcraft-maturity-hardening/`

This directory is temporary, local, and review-oriented. It is the handoff and evidence buffer for this iteration.

### Required Handoff Files

- `README.md` -- execution contract
- `STATUS.md` -- slice-by-slice progress log
- `QUESTIONS.md` -- blockers and decision requests
- `VALIDATION.md` -- commands run and results

### Slice Protocol

For each implementation slice:

1. Claim the slice in `STATUS.md`.
2. Make only the files needed for that slice.
3. Run targeted tests first, then full repo validation before claiming completion.
4. Record exact commands and outcomes in `VALIDATION.md`.
5. If blocked, stop and write the blocker in `QUESTIONS.md` instead of guessing.

### Review Protocol

Codex review should reject a slice if:

- status claims exceed evidence
- a validator/test rule is missing for a new contract
- docs and machine checks disagree
- draft capability is relabeled as ready without explicit graduation evidence
- the implementation expands scope beyond the active workstream

---

## Development Principles

1. Preserve the control plane. Do not redesign `intake`, lifecycle phases, or workflow architecture unless a contract bug makes it unavoidable.
2. Prefer machine-enforced truth over narrative truth. If a rule matters, encode it in validator/tests.
3. Do not fabricate maturity. A skill stays `draft` or `review` unless evidence justifies promotion.
4. Promote the spine before the perimeter. Default-path honesty matters more than outer-ring completeness.
5. Keep slices reversible. Each task should be reviewable and backout-friendly.
6. Keep content English inside repo artifacts unless an existing file establishes a different norm.
7. Do not widen the curated/public surface just because a skill exists.
8. When a draft dependency must remain, label it explicitly rather than hiding it in prose.
9. Update docs and enforcement together. No contract prose without a matching check when the rule is important.
10. Use the handoff directory as the operational record instead of burying decisions in chat.

---

## Global Acceptance Standard

The iteration is acceptable only when all of the following are true:

- `python3 scripts/validate_prodcraft.py` passes
- `pytest -q` passes
- any new contract rule has at least one negative test
- default-required routes no longer silently rely on `draft` skills
- docs, manifest, registry, and curated surface tell a consistent maturity story
- handoff files under `build/gemini-handoff/2026-04-01-prodcraft-maturity-hardening/` are updated and readable

---

## Recommended Execution Order

1. Workstream A -- enforce the maturity boundary first
2. Workstream C -- align narrative and public surface with the new contract
3. Workstream B -- promote the hardened spine only after the contract boundary is trustworthy
4. Final verification pass -- full validation, full test run, handoff log completion

This order prevents a false win where statuses improve before the repository can actually enforce what those statuses mean.
