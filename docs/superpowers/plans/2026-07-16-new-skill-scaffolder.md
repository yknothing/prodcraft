# New Skill Scaffolder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a draft-only `scripts/new_skill.py <phase> <name>` command that creates the three authoring surfaces, validates the complete candidate repository, and leaves the repository byte-identical after any failure.

**Architecture:** Build all changes in a temporary repository copy and invoke the candidate copy's repository validator before touching the source repository. After validation, commit the two new package directories with atomic no-replace moves and commit the surgically updated manifest with an atomic exchange whose displaced bytes must match the validated baseline. On failure, remove only unchanged transaction-owned files and preserve concurrent owner content. Distribution registries, the cross-cutting matrix, workflows, and `artifact_flow` remain promotion-time concerns and are never mutated by this command.

**Tech Stack:** Python 3 standard library, PyYAML, `unittest`.

---

### Task 1: Specify the draft authoring transaction

**Files:**
- Create: `tests/test_new_skill_scaffold.py`

- [ ] Write a temporary-repository fixture with a lifecycle phase, manifest sections, distribution registry, cross-cutting matrix, and an executable validator boundary.
- [ ] Write a happy-path test asserting creation of only `SKILL.md`, `eval-strategy.md`, and a draft manifest entry; assert empty inputs/outputs add no `artifact_flow` entry.
- [ ] Write a planned-skill conversion test asserting the matching same-phase planned entry is removed exactly once.
- [ ] Write collision tests for implemented, phase-mismatched planned, public, filesystem, invalid phase, and unsafe name cases.
- [ ] Write idempotence tests proving a second invocation fails without changing bytes or duplicating manifest entries.
- [ ] Write failure tests for validator rejection and each commit replacement step; compare the full repository snapshot before and after.
- [ ] Run `python -m unittest tests.test_new_skill_scaffold` and observe RED because `scripts/new_skill.py` does not exist.

### Task 2: Implement candidate generation and validation

**Files:**
- Create: `scripts/new_skill.py`
- Test: `tests/test_new_skill_scaffold.py`

- [ ] Validate the canonical phase allowlist and `pc-` skill-name grammar before deriving paths.
- [ ] Load manifest and public registry data to reject implemented/public/filesystem collisions and accept only a matching planned entry.
- [ ] Render an English Agent Skills-compatible `SKILL.md` with empty inputs/outputs and a draft eval strategy.
- [ ] Splice a draft skill entry before `planned_skills:` and remove the matching planned block without rewriting unrelated manifest bytes.
- [ ] Copy the repository to a temporary candidate root, apply all candidate changes there, and call an injectable validator callback; the default callback runs `scripts/validate_prodcraft.py` from the candidate root.
- [ ] Run the focused tests and confirm happy-path and validation-boundary tests are GREEN.

### Task 3: Implement guarded commit and rollback

**Files:**
- Modify: `scripts/new_skill.py`
- Test: `tests/test_new_skill_scaffold.py`

- [ ] Recheck the source manifest bytes and destination absence immediately before commit to reject concurrent drift.
- [ ] Stage the two validated directories and manifest beside the source repository.
- [ ] Move the skill and eval directories with no-replace semantics, then atomically exchange the manifest and verify the displaced baseline bytes.
- [ ] On any exception, exchange the manifest back when needed and remove only unchanged transaction-owned files; preserve concurrent owner content.
- [ ] Run all injected-failure tests and confirm every repository snapshot is byte-identical after failure.

### Task 4: Document authoring and verify repository boundaries

**Files:**
- Modify: `skills/_schema.md`
- Test: `tests/test_new_skill_scaffold.py`

- [ ] Document the command, its draft-only three-surface output, candidate validation, planned-entry conversion, and failure rollback.
- [ ] State explicitly that distribution registries, portability, curated output, workflows, cross-cutting policy, and artifact flow are promotion-time/manual review surfaces.
- [ ] Run `python -m unittest tests.test_new_skill_scaffold`.
- [ ] Run `python scripts/validate_prodcraft.py --check skill-frontmatter --check manifest-skill-status --check curated-surface` without invoking the scaffolder against the shared working tree.
- [ ] Run `git diff --check` and inspect `git status --short` to confirm no protected surface was modified by Task 6.
