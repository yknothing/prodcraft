from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class DeliveryCompletionSkillTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

    def test_delivery_completion_skill_files_exist(self):
        targets = [
            REPO_ROOT / "skills" / "06-delivery" / "delivery-completion" / "SKILL.md",
            REPO_ROOT / "skills" / "06-delivery" / "delivery-completion" / "references" / "gotchas.md",
        ]
        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_manifest_and_artifact_flow_register_delivery_completion(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}
        artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}

        entry = entries["delivery-completion"]
        self.assertEqual("06-delivery", entry["phase"])
        self.assertEqual("draft", entry["status"])
        self.assertEqual("critical", entry["qa_tier"])

        self.assertIn("delivery-completion", artifact_flow["verification-record"]["consumed_by"])
        self.assertIn("delivery-completion", artifact_flow["execution-checkpoint"]["consumed_by"])
        self.assertEqual("delivery-completion", artifact_flow["delivery-decision-record"]["produced_by"])
        self.assertIn("release-management", artifact_flow["delivery-decision-record"]["consumed_by"])

    def test_gateway_phase_and_skill_contract_keep_delivery_completion_thin(self):
        skill_text = (
            REPO_ROOT / "skills" / "06-delivery" / "delivery-completion" / "SKILL.md"
        ).read_text(encoding="utf-8")
        phase_text = (REPO_ROOT / "skills" / "06-delivery" / "_phase.md").read_text(encoding="utf-8")
        gateway_text = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")

        self.assertIn("Present these four outcomes", skill_text)
        self.assertIn("typed `discard` confirmation", skill_text)
        self.assertIn("does **not** replace release management or deployment strategy", skill_text)
        self.assertIn("delivery-completion", phase_text)
        self.assertIn("delivery-completion", gateway_text)
        self.assertIn("finishing-a-development-branch", gateway_text)


if __name__ == "__main__":
    unittest.main()
