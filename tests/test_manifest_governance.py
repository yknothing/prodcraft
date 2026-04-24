from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SKILL_REGISTRY_PATH = REPO_ROOT / "schemas" / "distribution" / "public-skill-registry.json"
PUBLIC_SKILL_PORTABILITY_PATH = REPO_ROOT / "schemas" / "distribution" / "public-skill-portability.json"


class ManifestGovernanceTests(unittest.TestCase):
    def test_distribution_registry_declares_public_readiness(self):
        registry = json.loads(PUBLIC_SKILL_REGISTRY_PATH.read_text(encoding="utf-8"))

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
        registry = json.loads(PUBLIC_SKILL_REGISTRY_PATH.read_text(encoding="utf-8"))
        public_names = {entry["name"] for entry in registry["public_skills"]}

        self.assertIn("prodcraft", public_names)
        self.assertIn("intake", public_names)
        self.assertIn("tdd", public_names)
        self.assertIn("incident-response", public_names)

    def test_public_registry_covers_manifest_tested_or_better_skills(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        registry = json.loads(PUBLIC_SKILL_REGISTRY_PATH.read_text(encoding="utf-8"))

        public_names = {entry["name"] for entry in registry["public_skills"]}
        tested_or_better = {
            skill["name"]
            for skill in manifest["skills"]
            if skill["status"] in {"tested", "secure", "production"}
        }

        self.assertEqual(set(), tested_or_better - public_names)

    def test_public_registry_only_keeps_one_below_tested_exception(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        registry = json.loads(PUBLIC_SKILL_REGISTRY_PATH.read_text(encoding="utf-8"))

        statuses = {skill["name"]: skill["status"] for skill in manifest["skills"]}
        below_tested = {
            entry["name"]
            for entry in registry["public_skills"]
            if statuses.get(entry["name"]) not in {None, "tested", "secure", "production"}
        }

        self.assertEqual({"system-design"}, below_tested)

    def test_public_portability_registry_covers_exported_public_skills(self):
        registry = json.loads(PUBLIC_SKILL_REGISTRY_PATH.read_text(encoding="utf-8"))
        portability = json.loads(PUBLIC_SKILL_PORTABILITY_PATH.read_text(encoding="utf-8"))

        self.assertEqual("public-skill-portability.v1", portability["schema_version"])
        public_names = {entry["name"] for entry in registry["public_skills"]}
        portability_entries = {entry["name"]: entry for entry in portability["skills"]}

        self.assertEqual(public_names, set(portability_entries))

        valid_portability = {"portable_as_is", "portable_with_caveat", "blocked"}
        for name, entry in portability_entries.items():
            self.assertIn(entry["portability"], valid_portability, name)
            self.assertIn("hidden_dependencies", entry, name)
            self.assertIsInstance(entry["hidden_dependencies"], list, name)
            self.assertIn("required_context", entry, name)
            self.assertIn("public_caveat_text", entry, name)

            if entry["portability"] == "portable_as_is":
                self.assertEqual([], entry["hidden_dependencies"], name)
                self.assertEqual("", entry["public_caveat_text"], name)
            if entry["portability"] == "portable_with_caveat":
                self.assertGreater(len(entry["required_context"]), 0, name)
                self.assertGreater(len(entry["public_caveat_text"]), 0, name)

        blocked_public = {
            name
            for name in public_names
            if portability_entries[name]["portability"] == "blocked"
        }
        self.assertEqual(set(), blocked_public)


if __name__ == "__main__":
    unittest.main()
