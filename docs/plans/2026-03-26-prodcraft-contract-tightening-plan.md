# Prodcraft Contract Tightening Implementation Plan

> Status: historical implementation plan. The scoped contract-hardening work in this document has been implemented; use current repo contracts and pressure-test summaries for the latest operating state.

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Tighten Prodcraft's highest-value contracts so the repo's claimed rigor is machine-enforced in the places that matter most, while deferring deletion decisions that require real usage data.

**Architecture:** Treat this as a contract-hardening pass, not a redesign. Keep the existing control plane (`intake -> gateway -> workflow -> skill`) intact, close the biggest schema and distribution gaps, clarify obligation semantics, and add just enough measurement to support future subtractive governance.

**Tech Stack:** Markdown, YAML, JSON Schema, Python validator/tests, repo-local eval artifacts

**Design Doc:** N/A

---

## Scope

### In Scope for This Iteration

- tighten routing-critical schemas so invalid values fail validation
- make `.curated/` parity enforceable instead of trust-based
- separate cross-cutting obligation semantics from unconditional execution semantics
- define `qa_tier` behavior policy beyond evidence-path presence
- add a pressure-test protocol that can produce deletion candidates from real runs

### Explicitly Out of Scope for This Iteration

- deleting skills, workflows, or personas before pressure-test data exists
- introducing public semver/version-locking for the curated install surface
- redesigning the lifecycle model or removing the mandatory `intake` gate
- broad language-boundary schema changes before the contract-hardening pass lands

### Sequencing Rules

1. Land P0 contract fixes first.
2. Only then clarify policy semantics (`cross-cutting`, `qa_tier`).
3. Only after those land, add measurement for future subtraction.
4. Treat language-boundary work as a follow-on task unless it blocks an earlier contract.

## Success Criteria

- `python3 scripts/validate_prodcraft.py` passes after each task batch.
- Invalid `work_type`, `entry_phase`, `workflow_primary`, and unapproved course-correction jumps fail tests.
- Fresh curated export matches checked-in `skills/.curated/` byte-for-byte.
- Fast-track behavior for documentation obligation is defined in machine-readable form.
- `qa_tier` differences are documented and validated, not inferred.
- A repo-checked-in pressure-test protocol exists with measurable outputs.

## Task 1: Tighten `intake-brief` Semantic Contract

**Files:**
- Modify: `schemas/artifacts/intake-brief.schema.json`
- Modify: `skills/00-discovery/intake/SKILL.md`
- Modify: `scripts/validate_prodcraft.py`
- Modify: `tests/test_artifact_schema_registry.py`
- Add: `tests/test_intake_schema_semantics.py`

**Step 1: Encode routing-critical enums**

- Add explicit enums for `work_type`, `entry_phase`, and `workflow_primary`.
- Change `additionalProperties` from `true` to the narrowest safe setting. Prefer `false` unless a specific extension mechanism is needed.

**Step 2: Keep schema and prose in sync**

- Update the `intake` skill table if enum names change.
- Ensure the schema and `intake` taxonomy describe the same work types with the same spelling.

**Step 3: Add validator coverage**

- Extend `validate_prodcraft.py` so it checks:
  - `entry_phase` enum matches manifest phase IDs
  - `workflow_primary` enum matches declared primary workflows
  - `work_type` enum matches the intake taxonomy

**Step 4: Add negative tests**

- Add tests proving that invalid routing values are rejected.
- Keep one test focused on schema structure and one on semantic parity with repo sources.

**Run:**

```bash
python3 -m unittest tests/test_artifact_schema_registry.py tests/test_intake_schema_semantics.py -v
python3 scripts/validate_prodcraft.py
```

**Expected:**

- schema tests pass
- validator passes
- hand-edited invalid routing values are rejected

## Task 2: Close the `course-correction-note` ADR/Schema Gap

**Files:**
- Modify: `schemas/artifacts/course-correction-note.schema.json`
- Modify: `docs/adr/ADR-002-cross-phase-course-corrections.md`
- Modify: `skills/_gateway.md`
- Modify: `scripts/validate_prodcraft.py`
- Modify: `tests/test_course_correction_contract.py`

**Step 1: Encode approved jump pairs**

- Represent the eight approved source/target pairs directly in the schema.
- Use the smallest readable mechanism available, for example `anyOf` over approved pairs.

**Step 2: Make one source authoritative**

- Keep ADR and gateway text aligned with the same approved pair set.
- Add validator logic that compares the documented pairs against the schema pairs.

**Step 3: Add failure tests**

- Add tests that reject an unapproved jump such as `03-planning -> 00-discovery`.
- Keep an approval-path test for one valid implementation jump and one valid operations jump.

**Run:**

```bash
python3 -m unittest tests/test_course_correction_contract.py -v
python3 scripts/validate_prodcraft.py
```

**Expected:**

- valid jump pairs pass
- invalid jump pairs fail
- ADR, gateway, and schema no longer drift silently

## Task 3: Enforce `.curated/` Parity

**Files:**
- Modify: `scripts/validate_prodcraft.py`
- Modify: `tests/test_curated_distribution_surface.py`
- Modify: `docs/distribution/public-skill-lifecycle.md`

**Step 1: Add parity check to validation**

- Export the curated surface to a temporary directory.
- Compare it against checked-in `skills/.curated/`.
- Fail validation if any file content or bundle structure differs.

**Step 2: Keep the existing static checks**

- Preserve current checks for missing files and dangling bundled resources.
- Treat parity as an additional gate, not a replacement.

**Step 3: Update the contract doc**

- Change the distribution doc from a trust statement to an enforced statement.
- Document the exact validation path.

**Run:**

```bash
python3 -m unittest tests/test_curated_distribution_surface.py -v
python3 scripts/validate_prodcraft.py --check curated-surface
```

**Expected:**

- locally regenerated curated output matches repo state
- manual edits under `skills/.curated/` fail validation immediately

## Task 4: Introduce a Cross-Cutting Obligation Model

**Files:**
- Modify: `rules/cross-cutting-matrix.yml`
- Modify: `skills/cross-cutting/documentation/SKILL.md`
- Modify: `skills/_gateway.md`
- Modify: `scripts/validate_prodcraft.py`
- Modify: `tests/test_cross_cutting_matrix.py`

**Step 1: Split obligation semantics**

- Replace `required` with explicit fields such as:
  - `must_consider`
  - `must_produce`
  - `skip_when_fast_track`

**Step 2: Resolve the documentation mismatch**

- Make `documentation` a consideration obligation by default unless a phase truly requires a durable artifact.
- Define the fast-track rule explicitly instead of leaving it implicit.

**Step 3: Update gateway language**

- Align `skills/_gateway.md` with the new obligation terms.
- Avoid mixing “must think about” with “must invoke skill and produce artifact.”

**Step 4: Extend validation/tests**

- Validate presence and type of the new fields.
- Add at least one fast-track scenario test.

**Run:**

```bash
python3 -m unittest tests/test_cross_cutting_matrix.py -v
python3 scripts/validate_prodcraft.py --check cross-cutting-matrix
```

**Expected:**

- fast-track documentation behavior is defined, tested, and machine-readable
- documentation skill trigger no longer conflicts with the matrix

## Task 5: Turn `qa_tier` Into a Real Policy

**Files:**
- Modify: `skills/_quality-assurance.md`
- Modify: `scripts/validate_prodcraft.py`
- Modify: `tests/test_manifest_governance.py`
- Modify: `README.md`

**Step 1: Define concrete tier differences**

- For `critical` and `standard`, document:
  - required benchmark posture
  - required security-review depth
  - whether manual review/sign-off is required
  - minimum evidence freshness expectations

**Step 2: Encode validator rules**

- Convert the new documented policy into validator checks where feasible.
- Keep human-only policy explicit if it cannot yet be automated.

**Step 3: Add governance tests**

- Add tests for missing required QA artifacts by tier.
- Add at least one stale-or-incomplete-policy test if validator support exists.

**Run:**

```bash
python3 -m unittest tests/test_manifest_governance.py -v
python3 scripts/validate_prodcraft.py --check manifest-skill-status
```

**Expected:**

- `qa_tier` changes review behavior on paper and in validation
- repo readers no longer have to infer what `critical` means

## Task 6: Add Pressure-Test Protocol for Future Subtractive Governance

**Files:**
- Add: `docs/plans/2026-03-26-prodcraft-pressure-test-protocol.md`
- Add: `eval/meta/prodcraft-pressure-tests/README.md`
- Add: `eval/meta/prodcraft-pressure-tests/scenario-matrix.md`
- Modify: `docs/observability/runtime-feedback-loop.md`
- Modify: `README.md`

**Step 1: Define the scenario set**

- Include 3-5 representative requests:
  - new feature
  - bug fix
  - migration/brownfield
  - hotfix
  - documentation-only change

**Step 2: Define measurable outputs**

- Record:
  - first-route correctness
  - number of clarification rounds
  - cross-cutting skills actually triggered
  - artifacts produced but never consumed
  - course-correction jumps observed

**Step 3: Connect it to future deletion**

- Add a required review question: which skills, artifacts, or matrix obligations are now candidates for removal or downgrade?
- Treat this as the first data source for subtractive governance.

**Run:**

```bash
python3 scripts/validate_prodcraft.py
```

**Expected:**

- the repo contains a repeatable measurement protocol
- future deletion decisions can be evidence-backed instead of taste-backed

## Task 7: Deferred Follow-On for Language Boundary Contract

**Files:**
- Modify later: `schemas/artifacts/intake-brief.schema.json`
- Modify later: other user-facing artifact schemas
- Modify later: `CLAUDE.md`
- Add later: `tests/test_language_boundary_contract.py`

**Why Deferred:**

- the gap is real, but it is lower leverage than the P0/P1 contract closures above
- language-boundary fields should be added after the repo has a clearer policy for which artifacts are canonical English records versus localized presentation outputs

**Entry Criteria for Starting This Task:**

- Tasks 1-5 are landed
- pressure-test protocol has produced at least one real multilingual or mixed-language scenario

## Final Verification Pass

**Run:**

```bash
python3 scripts/validate_prodcraft.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

**Expected:**

- full validator passes
- full test suite passes
- no doc, schema, or curated-surface drift remains

## Execution Order

1. Task 1
2. Task 2
3. Task 3
4. Task 4
5. Task 5
6. Task 6
7. Task 7 only after the earlier work and first pressure-test data exist

## Notes for the Implementer

- Do not delete concepts just because they feel heavy; only delete after Task 6 produces evidence.
- Do tighten any contract that already claims to be machine-enforced but currently is only prose-enforced.
- Prefer improving the authority of existing files over adding new registries unless duplication becomes unavoidable.
- Keep the control-plane shape intact for this pass. This is a hardening iteration, not a philosophy rewrite.
