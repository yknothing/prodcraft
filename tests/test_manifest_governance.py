from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class ManifestGovernanceTests(unittest.TestCase):
    def test_every_skill_declares_qa_tier(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        for skill in manifest["skills"]:
            self.assertIn("qa_tier", skill, skill["name"])
            self.assertIn(skill["qa_tier"], {"critical", "standard"})

    def test_distribution_registry_exists_and_names_curated_public_skills(self):
        registry = json.loads((REPO_ROOT / "schemas" / "distribution" / "public-skill-registry.json").read_text(encoding="utf-8"))
        public_names = {entry["name"] for entry in registry["public_skills"]}

        self.assertIn("prodcraft", public_names)
        self.assertIn("intake", public_names)
        self.assertIn("tdd", public_names)
        self.assertIn("incident-response", public_names)


if __name__ == "__main__":
    unittest.main()
