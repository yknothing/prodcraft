from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class SpecificationAndArchitectureTestedPromotionsWaveTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        self.entries = {entry["name"]: entry for entry in self.manifest["skills"]}
        self.artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}

    def test_manifest_distinguishes_revised_spec_from_unchanged_tested_skills(self):
        targets = {
            "pc-spec-writing": "01-specification",
            "pc-domain-modeling": "01-specification",
            "pc-data-modeling": "02-architecture",
            "pc-security-design": "02-architecture",
        }

        for name, phase in targets.items():
            with self.subTest(skill=name):
                entry = self.entries[name]
                self.assertEqual(phase, entry["phase"])
                self.assertEqual("review" if name == "pc-spec-writing" else "tested", entry["status"])
                self.assertEqual("standard", entry["qa_tier"])
                self.assertEqual("routed", entry["evaluation_mode"])

                qa = entry["qa"]
                self.assertIn("benchmark_plan_path", qa)
                self.assertIn("benchmark_results_path", qa)
                self.assertIn("findings_path", qa)
                self.assertIn("integration_test_path", qa)

                self.assertTrue((REPO_ROOT / qa["benchmark_plan_path"]).exists())
                self.assertTrue((REPO_ROOT / qa["benchmark_results_path"]).exists())
                self.assertTrue((REPO_ROOT / qa["findings_path"]).exists())
                self.assertTrue((REPO_ROOT / qa["integration_test_path"]).exists())

    def test_manual_branch_pair_artifacts_exist(self):
        targets = [
            REPO_ROOT / "eval" / "01-specification" / "pc-domain-modeling" / "manual-run-2026-04-10-access-review" / "eval-1-access-review-modernization-domain-model" / "without_skill" / "response.md",
            REPO_ROOT / "eval" / "01-specification" / "pc-domain-modeling" / "manual-run-2026-04-10-access-review" / "eval-1-access-review-modernization-domain-model" / "with_skill" / "response.md",
            REPO_ROOT / "eval" / "01-specification" / "pc-spec-writing" / "manual-run-2026-04-10-access-review" / "eval-1-access-review-modernization-spec" / "without_skill" / "response.md",
            REPO_ROOT / "eval" / "01-specification" / "pc-spec-writing" / "manual-run-2026-04-10-access-review" / "eval-1-access-review-modernization-spec" / "with_skill" / "response.md",
            REPO_ROOT / "eval" / "02-architecture" / "pc-data-modeling" / "manual-run-2026-04-10-access-review" / "eval-1-access-review-modernization-data-model" / "without_skill" / "response.md",
            REPO_ROOT / "eval" / "02-architecture" / "pc-data-modeling" / "manual-run-2026-04-10-access-review" / "eval-1-access-review-modernization-data-model" / "with_skill" / "response.md",
            REPO_ROOT / "eval" / "02-architecture" / "pc-security-design" / "manual-run-2026-04-10-access-review" / "eval-1-access-review-modernization-security-design" / "without_skill" / "response.md",
            REPO_ROOT / "eval" / "02-architecture" / "pc-security-design" / "manual-run-2026-04-10-access-review" / "eval-1-access-review-modernization-security-design" / "with_skill" / "response.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_historical_findings_and_current_artifact_flow_remain_available(self):
        expectations = {
            "pc-domain-modeling": ("domain-model", "pc-spec-writing"),
            "pc-spec-writing": ("spec-doc", "pc-api-design"),
            "pc-data-modeling": ("data-schema", "pc-feature-development"),
            "pc-security-design": ("threat-model", "pc-security-audit"),
        }

        for skill_name, (artifact_name, downstream_consumer) in expectations.items():
            with self.subTest(skill=skill_name):
                qa = self.entries[skill_name]["qa"]
                findings_path = REPO_ROOT / qa.get("historical_findings_path", qa["findings_path"])
                if skill_name == "pc-spec-writing":
                    self.assertNotEqual(qa["historical_findings_path"], qa["findings_path"])
                    self.assertTrue((REPO_ROOT / qa["revalidation_plan_path"]).is_file())
                findings = findings_path.read_text(encoding="utf-8")

                self.assertIn("Current status: `tested`", findings)
                self.assertEqual(skill_name, self.artifact_flow[artifact_name]["produced_by"])
                self.assertIn(downstream_consumer, self.artifact_flow[artifact_name]["consumed_by"])


if __name__ == "__main__":
    unittest.main()
