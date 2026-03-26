from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS_DIR = REPO_ROOT / "workflows"
PRIMARY_WORKFLOWS = {"agile-sprint", "spec-driven", "iterative-waterfall"}
OVERLAY_WORKFLOWS = {"greenfield", "brownfield", "hotfix"}


def load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    _, frontmatter, _ = text.split("---\n", 2)
    return yaml.safe_load(frontmatter)


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
        intake_skill = (REPO_ROOT / "skills" / "00-discovery" / "intake" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("workflow_primary", intake_template)
        self.assertIn("workflow_overlays", intake_template)
        self.assertIn("workflow_primary", intake_skill)
        self.assertIn("workflow_overlays", intake_skill)


if __name__ == "__main__":
    unittest.main()
