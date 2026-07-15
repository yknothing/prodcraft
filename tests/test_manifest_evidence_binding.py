from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_prodcraft.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_prodcraft_evidence", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def skill_text(
    *,
    process: str = "Do the work.",
    note: str = "Background note.",
    description: str = "Use when the demo contract must be exercised.",
    iron_law: str = "Never skip the proof.",
    duplicate_process: bool = False,
) -> str:
    duplicate = "\n## Process\n\nA hidden second process.\n" if duplicate_process else ""
    return f"""---
name: pc-demo
description: {description}
metadata:
  phase: 04-implementation
  inputs: []
  outputs: []
  prerequisites: []
  roles: [developer]
  methodologies: [all]
---

# Demo

## Context

{note}

## The Iron Law

{iron_law}

## Inputs

None.

## Process

{process}
{duplicate}

## Outputs

None.

## Quality Gate

- [ ] The work is verified.
"""


class ManifestEvidenceBindingTests(unittest.TestCase):
    def test_contract_digest_changes_for_process_edits_but_not_context_typos(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_path = Path(tmpdir) / "SKILL.md"
            skill_path.write_text(skill_text(), encoding="utf-8")
            original = validator.compute_skill_contract_digest(skill_path)

            skill_path.write_text(skill_text(note="Background note corrected."), encoding="utf-8")
            self.assertEqual(original, validator.compute_skill_contract_digest(skill_path))

            skill_path.write_text(skill_text(process="Do the safer work."), encoding="utf-8")
            self.assertNotEqual(original, validator.compute_skill_contract_digest(skill_path))

            skill_path.write_text(skill_text(iron_law="Never skip fresh proof."), encoding="utf-8")
            self.assertNotEqual(original, validator.compute_skill_contract_digest(skill_path))

            skill_path.write_text(
                skill_text(description="Use when the changed demo contract must be exercised."),
                encoding="utf-8",
            )
            self.assertNotEqual(original, validator.compute_skill_contract_digest(skill_path))

    def test_contract_digest_rejects_duplicate_h2_contract_sections(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_path = Path(tmpdir) / "SKILL.md"
            skill_path.write_text(skill_text(duplicate_process=True), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "duplicate H2 heading `Process`"):
                validator.compute_skill_contract_digest(skill_path)

    def test_tested_skill_requires_current_contract_digest(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            skill_path = root / "skills" / "04-implementation" / "pc-demo" / "SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_path.write_text(skill_text(), encoding="utf-8")
            entry = {
                "name": "pc-demo",
                "phase": "04-implementation",
                "file": "skills/04-implementation/pc-demo/SKILL.md",
                "status": "tested",
            }

            errors: list[str] = []
            with mock.patch.object(validator, "ROOT", root):
                validator.validate_manifest_evidence_bindings({"skills": [entry]}, errors)
            self.assertTrue(any("missing `evidence_verified_against`" in error for error in errors))

            entry["evidence_verified_against"] = "contract-sha256:" + "0" * 64
            errors = []
            with mock.patch.object(validator, "ROOT", root):
                validator.validate_manifest_evidence_bindings({"skills": [entry]}, errors)
            self.assertTrue(any("stale QA evidence binding" in error for error in errors))

            entry["evidence_verified_against"] = validator.compute_skill_contract_digest(skill_path)
            errors = []
            with mock.patch.object(validator, "ROOT", root):
                validator.validate_manifest_evidence_bindings({"skills": [entry]}, errors)
            self.assertTrue(any("evidence binding record is missing" in error for error in errors))

            evidence_path = root / "eval" / "04-implementation" / "pc-demo" / "review.md"
            evidence_path.parent.mkdir(parents=True)
            evidence_path.write_text("# Current review\n", encoding="utf-8")
            record_path = root / "eval" / "meta" / "skill-evidence-bindings.yml"
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                "\n".join(
                    (
                        "schema_version: skill-evidence-bindings.v1",
                        "algorithm: contract-projection.v2",
                        "bindings:",
                        "- skill: pc-demo",
                        f"  evidence_verified_against: {entry['evidence_verified_against']}",
                        "  verified_at: '2026-07-16'",
                        "  evidence_paths:",
                        "  - eval/04-implementation/pc-demo/review.md",
                        "",
                    )
                ),
                encoding="utf-8",
            )
            errors = []
            with mock.patch.object(validator, "ROOT", root):
                validator.validate_manifest_evidence_bindings({"skills": [entry]}, errors)
            self.assertEqual([], errors)

    def test_review_skill_requires_current_contract_digest(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            skill_path = root / "skills" / "04-implementation" / "pc-demo" / "SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_path.write_text(skill_text(), encoding="utf-8")
            entry = {
                "name": "pc-demo",
                "phase": "04-implementation",
                "file": "skills/04-implementation/pc-demo/SKILL.md",
                "status": "review",
            }

            errors: list[str] = []
            with mock.patch.object(validator, "ROOT", root):
                validator.validate_manifest_evidence_bindings({"skills": [entry]}, errors)
            self.assertTrue(any("missing `evidence_verified_against`" in error for error in errors))

            digest = validator.compute_skill_contract_digest(skill_path)
            entry["evidence_verified_against"] = digest
            evidence_path = root / "eval" / "04-implementation" / "pc-demo" / "review.md"
            evidence_path.parent.mkdir(parents=True)
            evidence_path.write_text("# Review\n", encoding="utf-8")
            record_path = root / "eval" / "meta" / "skill-evidence-bindings.yml"
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                "\n".join(
                    (
                        "schema_version: skill-evidence-bindings.v1",
                        "algorithm: contract-projection.v2",
                        "bindings:",
                        "- skill: pc-demo",
                        f"  evidence_verified_against: {digest}",
                        "  verified_at: '2026-07-16'",
                        "  evidence_paths:",
                        "  - eval/04-implementation/pc-demo/review.md",
                        "",
                    )
                ),
                encoding="utf-8",
            )
            errors = []
            with mock.patch.object(validator, "ROOT", root):
                validator.validate_manifest_evidence_bindings({"skills": [entry]}, errors)
            self.assertEqual([], errors)

            skill_path.write_text(skill_text(process="Changed review contract."), encoding="utf-8")
            errors = []
            with mock.patch.object(validator, "ROOT", root):
                validator.validate_manifest_evidence_bindings({"skills": [entry]}, errors)
            self.assertTrue(any("stale QA evidence binding" in error for error in errors))

    def test_draft_skill_does_not_require_evidence_binding(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            skill_path = root / "skills" / "04-implementation" / "pc-demo" / "SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_path.write_text(skill_text(), encoding="utf-8")
            entry = {
                "name": "pc-demo",
                "phase": "04-implementation",
                "file": "skills/04-implementation/pc-demo/SKILL.md",
                "status": "draft",
            }

            errors: list[str] = []
            with mock.patch.object(validator, "ROOT", root):
                validator.validate_manifest_evidence_bindings({"skills": [entry]}, errors)

            self.assertEqual([], errors)

    def test_repository_backfills_every_review_skill(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        record = yaml.safe_load(
            (REPO_ROOT / "eval" / "meta" / "skill-evidence-bindings.yml").read_text(
                encoding="utf-8"
            )
        )
        review_entries = {
            entry["name"]: entry
            for entry in manifest["skills"]
            if entry.get("status") == "review"
        }
        record_names = {entry["skill"] for entry in record["bindings"]}

        self.assertTrue(review_entries)
        self.assertEqual(
            set(review_entries),
            {name for name in review_entries if "evidence_verified_against" in review_entries[name]},
        )
        self.assertLessEqual(set(review_entries), record_names)

    def test_evidence_paths_must_be_unique(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            skill_path = root / "skills" / "04-implementation" / "pc-demo" / "SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_path.write_text(skill_text(), encoding="utf-8")
            evidence_path = root / "eval" / "04-implementation" / "pc-demo" / "review.md"
            evidence_path.parent.mkdir(parents=True)
            evidence_path.write_text("# Review\n", encoding="utf-8")
            digest = validator.compute_skill_contract_digest(skill_path)
            entry = {
                "name": "pc-demo",
                "phase": "04-implementation",
                "file": "skills/04-implementation/pc-demo/SKILL.md",
                "status": "tested",
                "evidence_verified_against": digest,
            }
            record_path = root / "eval" / "meta" / "skill-evidence-bindings.yml"
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                "\n".join(
                    (
                        "schema_version: skill-evidence-bindings.v1",
                        "algorithm: contract-projection.v2",
                        "bindings:",
                        "- skill: pc-demo",
                        f"  evidence_verified_against: {digest}",
                        "  verified_at: '2026-07-16'",
                        "  evidence_paths:",
                        "  - eval/04-implementation/pc-demo/review.md",
                        "  - eval/04-implementation/pc-demo/review.md",
                        "",
                    )
                ),
                encoding="utf-8",
            )

            errors: list[str] = []
            with mock.patch.object(validator, "ROOT", root):
                validator.validate_manifest_evidence_bindings({"skills": [entry]}, errors)

            self.assertTrue(any("duplicate evidence path" in error for error in errors))

    def test_evidence_path_cannot_escape_through_symlinked_parent(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmpdir, tempfile.TemporaryDirectory() as external_dir:
            root = Path(tmpdir)
            skill_path = root / "skills" / "04-implementation" / "pc-demo" / "SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_path.write_text(skill_text(), encoding="utf-8")
            external_evidence = Path(external_dir) / "review.md"
            external_evidence.write_text("# External review\n", encoding="utf-8")
            linked_eval = root / "eval" / "04-implementation" / "pc-demo"
            linked_eval.parent.mkdir(parents=True)
            linked_eval.symlink_to(Path(external_dir), target_is_directory=True)
            digest = validator.compute_skill_contract_digest(skill_path)
            entry = {
                "name": "pc-demo",
                "phase": "04-implementation",
                "file": "skills/04-implementation/pc-demo/SKILL.md",
                "status": "tested",
                "evidence_verified_against": digest,
            }
            record_path = root / "eval" / "meta" / "skill-evidence-bindings.yml"
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                "\n".join(
                    (
                        "schema_version: skill-evidence-bindings.v1",
                        "algorithm: contract-projection.v2",
                        "bindings:",
                        "- skill: pc-demo",
                        f"  evidence_verified_against: {digest}",
                        "  verified_at: '2026-07-16'",
                        "  evidence_paths:",
                        "  - eval/04-implementation/pc-demo/review.md",
                        "",
                    )
                ),
                encoding="utf-8",
            )

            errors: list[str] = []
            with mock.patch.object(validator, "ROOT", root):
                validator.validate_manifest_evidence_bindings({"skills": [entry]}, errors)

            self.assertTrue(any("unsafe evidence path" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
