from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_ROOT = REPO_ROOT / "eval" / "cross-cutting" / "documentation"


class DocumentationReviewStatusTests(unittest.TestCase):
    def test_manifest_registers_documentation_as_tested_routed(self):
        import yaml

        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        entries = {entry["name"]: entry for entry in manifest["skills"]}
        entry = entries["documentation"]

        self.assertEqual("cross-cutting", entry["phase"])
        self.assertEqual("tested", entry["status"])
        self.assertEqual("standard", entry["qa_tier"])
        self.assertEqual("routed", entry["evaluation_mode"])

        qa = entry["qa"]
        self.assertIn("structure_validation_path", qa)
        self.assertIn("eval_strategy_path", qa)
        self.assertIn("benchmark_plan_path", qa)
        self.assertIn("benchmark_results_path", qa)
        self.assertIn("findings_path", qa)
        self.assertIn("manual_review_path", qa)

    def test_tested_packet_files_exist(self):
        targets = [
            DOC_ROOT / "evals" / "eval-strategy.md",
            DOC_ROOT / "findings.md",
            DOC_ROOT / "isolated-benchmark.json",
            DOC_ROOT / "isolated-benchmark-plan.md",
            DOC_ROOT / "isolated-benchmark-review.md",
            DOC_ROOT / "documentation-handoff-review.md",
            DOC_ROOT / "fixtures" / "maturity-wave-request.md",
            DOC_ROOT / "fixtures" / "public-lifecycle-summary.md",
            DOC_ROOT / "fixtures" / "maintainer-audience.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_tested_packet_is_maintainer_facing_and_constrained(self):
        eval_strategy = (DOC_ROOT / "evals" / "eval-strategy.md").read_text(encoding="utf-8")
        findings = (DOC_ROOT / "findings.md").read_text(encoding="utf-8")
        benchmark_review = (DOC_ROOT / "isolated-benchmark-review.md").read_text(encoding="utf-8")
        plan = (DOC_ROOT / "isolated-benchmark-plan.md").read_text(encoding="utf-8")
        handoff = (DOC_ROOT / "documentation-handoff-review.md").read_text(encoding="utf-8")
        request = (DOC_ROOT / "fixtures" / "maturity-wave-request.md").read_text(encoding="utf-8")
        audience = (DOC_ROOT / "fixtures" / "maintainer-audience.md").read_text(encoding="utf-8")

        self.assertIn("Manual routed handoff review", eval_strategy)
        self.assertIn("maintainer-facing", eval_strategy)
        self.assertIn("Current status: `tested`", findings)
        self.assertIn("runner-backed benchmark", findings)
        self.assertIn("Recommended status: `tested`", benchmark_review)
        self.assertIn("Why This Plan Stays Light", plan)
        self.assertIn("when a change creates durable knowledge, where should", handoff)
        self.assertIn("Do not write a changelog entry", request)
        self.assertIn("repository maintainer or contributor", audience)


if __name__ == "__main__":
    unittest.main()
