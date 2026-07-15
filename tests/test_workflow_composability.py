from __future__ import annotations

import unittest
from pathlib import Path
import tempfile
from copy import deepcopy
from unittest import mock

import yaml

from scripts import validate_prodcraft as validator
from tools.workflow_contract import validate_workflow_contract, workflow_skill_references


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS_DIR = REPO_ROOT / "workflows"
PRIMARY_WORKFLOWS = {"agile-sprint", "spec-driven", "iterative-waterfall"}
OVERLAY_WORKFLOWS = {"greenfield", "brownfield", "hotfix"}


def load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    _, frontmatter, _ = text.split("---\n", 2)
    return yaml.safe_load(frontmatter)


def minimal_workflow_contract(*, workflow_kind: str = "primary") -> dict:
    contract = {
        "version": "workflow.v2",
        "overview": {
            "summary": "A compact workflow contract used by the composability tests.",
            "distinctive": "The contract remains machine-readable instead of relying on narrative headings.",
        },
        "entry_gate": {
            "summary": "Start only after intake approval.",
            "artifact": "intake-brief",
            "approval_required": True,
            "fast_track_rule": "Only an intake-approved route may shorten the phase sequence.",
        },
        "phase_sequence": [
            {
                "id": "04-implementation",
                "name": "Implementation",
                "purpose": "Build the approved slice.",
                "skills": ["pc-tdd"],
                "inputs": ["approved task slice"],
                "outputs": ["tested implementation"],
                "duration": "one iteration",
            }
        ],
        "quality_gates": [
            {
                "name": "Implementation complete",
                "after": "04-implementation",
                "criteria": ["The focused test suite passes."],
                "approvers": ["tech lead"],
                "enforcement": "blocking",
            }
        ],
    }
    if workflow_kind == "overlay":
        contract["overlay_delta"] = {
            "applies_to": ["agile-sprint"],
            "changes": [
                {
                    "dimension": "implementation",
                    "effect": "Narrow the implementation sequence without replacing primary governance.",
                }
            ],
        }
    return {
        "name": "example-primary" if workflow_kind == "primary" else "example-overlay",
        "description": "Compact test workflow",
        "cadence": "on demand",
        "workflow_kind": workflow_kind,
        "composes_with": ["greenfield"] if workflow_kind == "primary" else ["agile-sprint"],
        "entry_skill": "pc-intake",
        "required_artifacts": ["intake-brief"],
        "best_for": ["contract-tests"],
        "phases_included": ["04-implementation"],
        "contract": contract,
    }


def write_workflow(path: Path, frontmatter: dict, body: str | None = None) -> None:
    payload = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=False)
    path.write_text(
        f"---\n{payload}---\n\n# Example Workflow\n\n"
        + (body if body is not None else "## Adaptation Notes\n\n- Keep the test route intentionally small.\n"),
        encoding="utf-8",
    )


class WorkflowComposabilityTests(unittest.TestCase):
    def test_workflow_frontmatter_declares_kind_and_composition(self):
        for path in sorted(WORKFLOWS_DIR.glob("*.md")):
            if path.name.startswith("_"):
                continue
            frontmatter = load_frontmatter(path)
            self.assertIn("workflow_kind", frontmatter)
            self.assertIn("composes_with", frontmatter)
            self.assertIsInstance(frontmatter["composes_with"], list)

    def test_primary_and_overlay_sets_match_contract(self):
        for path in sorted(WORKFLOWS_DIR.glob("*.md")):
            if path.name.startswith("_"):
                continue
            frontmatter = load_frontmatter(path)
            name = frontmatter["name"]
            if name in PRIMARY_WORKFLOWS:
                self.assertEqual("primary", frontmatter["workflow_kind"])
            if name in OVERLAY_WORKFLOWS:
                self.assertEqual("overlay", frontmatter["workflow_kind"])

    def test_intake_template_and_skill_use_primary_plus_overlays(self):
        intake_template = (REPO_ROOT / "templates" / "intake-brief.md").read_text(encoding="utf-8")
        intake_skill = (REPO_ROOT / "skills" / "00-discovery" / "pc-intake" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("workflow_primary", intake_template)
        self.assertIn("workflow_overlays", intake_template)
        self.assertIn("workflow_primary", intake_skill)
        self.assertIn("workflow_overlays", intake_skill)

    def test_workflow_no_silent_draft_dependencies(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        draft_skills = {skill["name"] for skill in manifest.get("skills", []) if skill.get("status") == "draft"}

        for path in sorted(WORKFLOWS_DIR.glob("*.md")):
            if path.name.startswith("_"):
                continue
            refs = workflow_skill_references(load_frontmatter(path))
            self.assertTrue(draft_skills.isdisjoint(refs), f"{path.name} depends on a draft skill")

    def test_workflow_status_labels_match_manifest(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        skill_status = {skill["name"]: skill["status"] for skill in manifest.get("skills", [])}

        for path in sorted(WORKFLOWS_DIR.glob("*.md")):
            if path.name.startswith("_"):
                continue
            for ref in workflow_skill_references(load_frontmatter(path)):
                self.assertIn(ref, skill_status, f"{path.name} references unregistered skill {ref}")
                self.assertNotEqual("draft", skill_status[ref], f"{path.name} references draft skill {ref}")

    def assert_workflows_use_structured_contract(self, names: set[str]) -> None:
        for name in sorted(names):
            path = WORKFLOWS_DIR / f"{name}.md"
            self.assertEqual([], validate_workflow_contract(path), path.name)
            frontmatter = load_frontmatter(path)
            self.assertTrue(workflow_skill_references(frontmatter), path.name)

    def test_primary_workflows_use_the_structured_contract(self):
        self.assert_workflows_use_structured_contract(PRIMARY_WORKFLOWS)

    def test_overlay_workflows_use_the_structured_contract(self):
        self.assert_workflows_use_structured_contract(OVERLAY_WORKFLOWS)

    def test_narrative_headings_without_structured_semantics_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty-headings.md"
            frontmatter = minimal_workflow_contract()
            frontmatter.pop("contract")
            write_workflow(
                path,
                frontmatter,
                "## Entry Gate\n\n## Overview\n\n## Phase Sequence\n\n## Quality Gates\n\n## Adaptation Notes\n",
            )
            errors = validate_workflow_contract(path)
            self.assertTrue(any("contract" in error for error in errors), errors)

    def test_each_structured_semantic_is_independently_required(self):
        mutations = {
            "phase": lambda data: data["contract"].pop("phase_sequence"),
            "skill": lambda data: data["contract"]["phase_sequence"][0].update(skills=[]),
            "gate": lambda data: data["contract"].pop("quality_gates"),
            "artifact": lambda data: data["contract"]["entry_gate"].pop("artifact"),
            "approval": lambda data: data["contract"]["quality_gates"][0].update(approvers=[]),
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for label, mutate in mutations.items():
                with self.subTest(label=label):
                    frontmatter = minimal_workflow_contract()
                    mutate(frontmatter)
                    path = root / f"missing-{label}.md"
                    write_workflow(path, frontmatter)
                    self.assertTrue(validate_workflow_contract(path), label)

    def test_overlay_delta_is_required_only_for_overlays(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            missing_delta = minimal_workflow_contract(workflow_kind="overlay")
            missing_delta["contract"].pop("overlay_delta")
            missing_path = root / "missing-overlay-delta.md"
            write_workflow(missing_path, missing_delta)
            errors = validate_workflow_contract(missing_path)
            self.assertTrue(any("overlay_delta" in error for error in errors), errors)

            invalid_primary = minimal_workflow_contract()
            invalid_primary["contract"]["overlay_delta"] = deepcopy(
                minimal_workflow_contract(workflow_kind="overlay")["contract"]["overlay_delta"]
            )
            invalid_path = root / "primary-with-overlay-delta.md"
            write_workflow(invalid_path, invalid_primary)
            errors = validate_workflow_contract(invalid_path)
            self.assertTrue(any("overlay_delta" in error for error in errors), errors)

    def test_adaptation_notes_must_contain_guidance(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty-adaptation.md"
            write_workflow(path, minimal_workflow_contract(), "## Adaptation Notes\n")
            errors = validate_workflow_contract(path)
            self.assertTrue(any("Adaptation Notes" in error for error in errors), errors)

    def test_workflow_name_must_match_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "expected-name.md"
            write_workflow(path, minimal_workflow_contract())
            errors = validate_workflow_contract(path)
            self.assertTrue(any("must match filename" in error for error in errors), errors)

    def test_repository_validator_rejects_heading_only_legacy_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "legacy.md"
            frontmatter = minimal_workflow_contract()
            frontmatter.pop("contract")
            write_workflow(
                path,
                frontmatter,
                "## Overview\n\npc-intake intake-brief\n\n## Entry Gate\n\npc-intake intake-brief\n\n"
                "## Phase Sequence\n\n## Quality Gates\n\n## Adaptation Notes\n\n- Placeholder.\n",
            )
            errors: list[str] = []
            validator.validate_workflow_file(
                path,
                errors,
                {"workflow-frontmatter", "workflow-entry-gate"},
            )
            self.assertTrue(any("contract" in error for error in errors), errors)

    def test_repository_validator_reads_structured_skill_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            frontmatter = minimal_workflow_contract()
            frontmatter["contract"]["phase_sequence"][0]["skills"] = ["pc-not-registered"]
            path = root / "structured-reference.md"
            write_workflow(path, frontmatter)
            errors: list[str] = []
            manifest = {
                "skills": [],
                "planned_skills": [],
                "workflows": [{"name": "example-primary"}],
            }
            with (
                mock.patch.object(validator, "WORKFLOWS_DIR", root),
                mock.patch.object(validator, "validate_gateway_phase_skill_references"),
            ):
                validator.validate_workflow_skill_references(manifest, errors)
            self.assertTrue(any("pc-not-registered" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
