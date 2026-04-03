from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class ManifestGovernanceTests(unittest.TestCase):
    def test_distribution_registry_declares_public_readiness(self):
        registry = json.loads((REPO_ROOT / "schemas" / "distribution" / "public-skill-registry.json").read_text(encoding="utf-8"))

        for entry in registry["public_skills"]:
            self.assertIn("stability", entry, entry["name"])
            self.assertIn(entry["stability"], {"beta", "stable"}, entry["name"])
            self.assertIn("readiness", entry, entry["name"])
            self.assertIn(entry["readiness"], {"core", "beta", "experimental"}, entry["name"])

    def test_every_skill_declares_qa_tier(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        for skill in manifest["skills"]:
            self.assertIn("qa_tier", skill, skill["name"])
            self.assertIn(skill["qa_tier"], {"critical", "standard"})

    def test_non_draft_skills_have_minimum_review_artifacts(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        for skill in manifest["skills"]:
            if skill["status"] == "draft":
                continue
            qa = skill.get("qa", {})
            self.assertIn("structure_validation_path", qa, skill["name"])
            self.assertIn("eval_strategy_path", qa, skill["name"])

    def test_critical_review_skills_have_findings_and_review_depth_evidence(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        review_depth_paths = {
            "benchmark_plan_path",
            "benchmark_results_path",
            "security_check_path",
            "trigger_eval_results_path",
        }

        for skill in manifest["skills"]:
            if skill["qa_tier"] != "critical" or skill["status"] != "review":
                continue
            qa = skill.get("qa", {})
            self.assertIn("findings_path", qa, skill["name"])
            self.assertTrue(any(path in qa for path in review_depth_paths), skill["name"])

    def test_distribution_registry_exists_and_names_curated_public_skills(self):
        registry = json.loads((REPO_ROOT / "schemas" / "distribution" / "public-skill-registry.json").read_text(encoding="utf-8"))
        public_names = {entry["name"] for entry in registry["public_skills"]}

        self.assertIn("prodcraft", public_names)
        self.assertIn("intake", public_names)
        self.assertIn("tdd", public_names)
        self.assertIn("incident-response", public_names)


if __name__ == "__main__":
    unittest.main()
