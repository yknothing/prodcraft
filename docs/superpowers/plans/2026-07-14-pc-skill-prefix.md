# `pc-` Skill Identity Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `pc-` part of every Prodcraft skill's canonical, governed, runtime, and public identity without leaving ambiguous unprefixed packages.

**Architecture:** Rename the lifecycle authoring and mirrored QA trees first, then update every repository-owned identity registry and reference to the same mapping. Enforce the invariant in the existing validator and exporter. Treat installed legacy gateways as a migration boundary: automatically remove only a locator-proven same-repository install and fail clearly for unowned conflicts.

**Tech Stack:** Python 3, YAML/JSON registries, Markdown Agent Skills packages, `unittest`, repository validators, Git.

---

### Task 1: Define the canonical prefix contract with failing tests

**Files:**
- Create: `tests/test_skill_identity_prefix.py`
- Modify: `tests/test_curated_distribution_surface.py`
- Modify: `tests/test_manifest_governance.py`
- Modify: `tests/test_prodcraft_gateway_locator_contract.py`

- [ ] **Step 1: Write the failing identity tests**

Add tests that enumerate source `SKILL.md` files, manifest implemented and
planned entries, distribution registries, curated index entries, curated
directories, and mirrored eval directories. Assert that every skill identity
starts with `pc-`, frontmatter matches its parent directory, and no unprefixed
curated package remains.

```python
def test_authored_skill_names_are_pc_prefixed_and_match_directories(self):
    for skill_path in authored_skill_paths():
        frontmatter = load_frontmatter(skill_path)
        self.assertTrue(frontmatter["name"].startswith("pc-"), skill_path)
        self.assertEqual(skill_path.parent.name, frontmatter["name"], skill_path)
```

Update gateway and curated expectations from `prodcraft`, `intake`, and other
old identifiers to `pc-prodcraft`, `pc-intake`, and their `pc-*` equivalents.

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python3 -m unittest \
  tests.test_skill_identity_prefix \
  tests.test_manifest_governance \
  tests.test_curated_distribution_surface \
  tests.test_prodcraft_gateway_locator_contract -v
```

Expected: failures show current unprefixed source, manifest, curated, and
gateway names.

### Task 2: Migrate canonical authoring and governance identities

**Files:**
- Rename: `skills/{phase}/{name}/` to `skills/{phase}/pc-{name}/` for all 46 authored skills
- Rename: `eval/{phase}/{name}/` to `eval/{phase}/pc-{name}/` for each authored skill mirror
- Modify: all renamed `SKILL.md` frontmatter and cross-skill links
- Modify: `manifest.yml`
- Modify: `skills/_gateway.md`
- Modify: `rules/cross-cutting-matrix.yml`
- Modify: `skills/*/_phase.md`
- Modify: `workflows/*.md`
- Modify: active schemas, examples, rules, tests, and documentation that reference canonical skill identities or paths
- Modify: `scripts/validate_prodcraft.py`

- [ ] **Step 1: Rename source and eval directories with Git history preserved**

Derive the mapping from the 46 source frontmatter names and execute `git mv`
for source and matching eval directories. Do not rename unrelated eval fixtures
such as `xcuitest-webview-e2e` or protocol/product files that merely contain the
word Prodcraft.

- [ ] **Step 2: Rewrite governed identity references**

Apply the exact mapping to frontmatter names, prerequisite/related-skill
metadata, manifest names and paths, artifact producer/consumer references,
manifest iterative feedback edges, workflow and gateway identifiers, matrix entries, Markdown skill links, public
registry source paths, and test expectations. Preserve non-skill artifact IDs
such as `intake-brief` and protocol IDs such as
`prodcraft-runtime-locator.v1`.

- [ ] **Step 3: Enforce the prefix in repository validation**

Extend `validate_skill_file` and `validate_manifest` so source directory,
frontmatter name, Agent Skills syntax, and `pc-` prefix mismatches produce
explicit errors. Extend curated validation so public and portability registry
entries without `pc-` fail instead of being silently exported.

```python
if not name.startswith("pc-"):
    errors.append(f"{path}: skill name `{name}` must start with `pc-`")
```

- [ ] **Step 4: Run the narrow identity and governance tests**

Run:

```bash
python3 -m unittest \
  tests.test_skill_identity_prefix \
  tests.test_manifest_governance \
  tests.test_workflow_composability -v
python3 scripts/validate_prodcraft.py \
  --check skill-frontmatter \
  --check manifest-files \
  --check manifest-skill-status \
  --check workflow-skill-refs \
  --check cross-cutting-matrix
```

Expected: PASS.

### Task 3: Migrate public export and gateway runtime behavior

**Files:**
- Modify: `schemas/distribution/public-skill-registry.json`
- Modify: `schemas/distribution/public-skill-portability.json`
- Modify: `scripts/export_curated_skills.py`
- Modify: `scripts/prodcraft_gateway_skill.py`
- Modify: `scripts/install_prodcraft_global_skill.py`
- Modify: `tests/test_curated_distribution_surface.py`
- Modify: `tests/test_prodcraft_gateway_locator_contract.py`
- Modify: `tests/test_install_prodcraft_global_skill.py`
- Regenerate: `skills/.curated/`

- [ ] **Step 1: Make the exporter reject non-prefixed packages**

Validate public registry names and generated package frontmatter before writing
the curated output. The generated gateway package is `pc-prodcraft`; all
flattened cross-skill links resolve to `../pc-*/SKILL.md`.

- [ ] **Step 2: Add safe legacy gateway migration tests**

Cover three cases with temporary target roots:

1. fresh install writes `pc-prodcraft` and locator `skill_name: pc-prodcraft`;
2. locator-owned legacy `prodcraft` is removed during install;
3. unowned legacy `prodcraft` causes a clear conflict and is left untouched.

- [ ] **Step 3: Implement the minimum installer migration**

Use `SKILL_NAME = "pc-prodcraft"` and
`LEGACY_SKILL_NAME = "prodcraft"`. Prove ownership by parsing the legacy
runtime locator and matching its canonical repository root before deletion.
Never infer ownership from directory name alone.

- [ ] **Step 4: Regenerate and verify the curated surface**

Run:

```bash
python3 scripts/export_curated_skills.py
python3 -m unittest \
  tests.test_curated_distribution_surface \
  tests.test_prodcraft_gateway_locator_contract -v
python3 scripts/validate_prodcraft.py --check curated-surface
```

Expected: PASS and `skills/.curated/` contains only `pc-*` package directories.

### Task 4: Document upgrade behavior and close QA

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `docs/distribution/npx-skills-compat.md`
- Modify: `docs/distribution/public-skill-lifecycle.md`
- Modify: `CLAUDE.md`
- Modify: tests that assert public installation and gateway documentation

- [ ] **Step 1: Document the canonical naming rule and breaking upgrade**

State that all user-visible skill identifiers use `pc-`. Explain that flat
installers may retain removed package directories and therefore users upgrading
from the unprefixed beta must remove the old packages before reinstalling or
updating the curated surface. Do not claim that `npx skills update` removes
renamed packages unless verified.

- [ ] **Step 2: Scan for stale active identities and broken paths**

Use the pre-migration mapping to find exact old identifiers in active
governance, distribution, runtime, test, and documentation contexts. Review
each hit instead of globally replacing generic words such as documentation,
compliance, or accessibility.

- [ ] **Step 3: Run full repository QA**

Run:

```bash
python3 scripts/validate_prodcraft.py
python3 -m unittest discover -s tests -v
git diff --check
```

Also run a dedicated loadability probe over every source and curated
`SKILL.md`: parse YAML, enforce the Agent Skills name grammar and 1024-character
description limit, match directory to frontmatter, and resolve relative
references.

- [ ] **Step 4: Perform adversarial review**

Challenge the migration for stale aliases, partial renames, unsafe legacy
deletion, curated/source divergence, broken cross-skill links, accidental
artifact renames, and false-green tests. Fix all P0/P1 findings and record any
accepted lower-priority residual risk in the final handoff.

- [ ] **Step 5: Commit, merge, and push**

Keep architecture/design, identity migration, runtime/distribution migration,
and documentation/QA changes in reviewable commits where the tree is green at
every implementation commit. Merge `codex/pc-skill-prefix` into `main`, rerun
the full QA command on `main`, and push `main` only after fresh verification.
