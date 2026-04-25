from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RuntimeFeedbackLoopContractTests(unittest.TestCase):
    def test_runtime_feedback_loop_assets_stay_aligned(self):
        workflow = (REPO_ROOT / ".github" / "workflows" / "runtime-feedback-loop.yml").read_text(encoding="utf-8")
        docs = (REPO_ROOT / "docs" / "observability" / "runtime-feedback-loop.md").read_text(encoding="utf-8")
        thresholds_path = REPO_ROOT / "rules" / "execution-observability-thresholds.yml"

        self.assertTrue(thresholds_path.exists())
        self.assertIn("scripts/summarize_execution_observability.py", workflow)
        self.assertIn("scripts/validate_execution_observability.py", workflow)
        self.assertIn("rules/execution-observability-thresholds.yml", workflow)
        self.assertIn("No observability JSONL inputs found", workflow)
        self.assertIn("exact_accounting_paths", workflow)
        self.assertIn("build/legacy-execution-observability-summary.json", workflow)
        self.assertIn("build/exact-accounting-summary.json", workflow)
        self.assertIn("Run scoped exact-accounting threshold gate", workflow)

        self.assertIn(".github/workflows/runtime-feedback-loop.yml", docs)
        self.assertIn("rules/execution-observability-thresholds.yml", docs)
        self.assertIn("explicit no-op", docs)
        self.assertIn("compatibility report without threshold failure", docs)
        self.assertIn("manual `exact_accounting_paths` input", docs)
        self.assertIn("exact token usage by runner and skill", docs)
        self.assertIn("unknown token usage", docs)
        self.assertIn("invalid token usage", docs)
        self.assertIn("exact token branch deltas", docs)
        self.assertIn("estimated token branch deltas only as advisory", docs)
        self.assertIn("usage-quality coverage", docs)
        self.assertIn("deferred byte/character ratio", docs)
        self.assertIn("provider usage without `usage_precision` as unknown", docs)
        self.assertIn("Do not call it token savings", docs)

        thresholds = thresholds_path.read_text(encoding="utf-8")
        self.assertIn("token_usage:", thresholds)
        self.assertIn("min_completed_count:", thresholds)
        self.assertIn("min_exact_coverage_ratio:", thresholds)
        self.assertIn("estimated_token_usage:", thresholds)
        self.assertIn("max_count:", thresholds)
        self.assertIn("unknown_token_usage:", thresholds)
        self.assertIn("invalid_token_usage:", thresholds)
        self.assertIn("skill_context:", thresholds)
        self.assertIn("min_measured_count:", thresholds)
        self.assertIn("min_sampling_ratio:", thresholds)


if __name__ == "__main__":
    unittest.main()
