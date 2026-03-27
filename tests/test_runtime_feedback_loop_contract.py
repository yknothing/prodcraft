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
        self.assertIn("rules/execution-observability-thresholds.yml", workflow)
        self.assertIn("No observability JSONL inputs found", workflow)

        self.assertIn(".github/workflows/runtime-feedback-loop.yml", docs)
        self.assertIn("rules/execution-observability-thresholds.yml", docs)
        self.assertIn("explicit no-op", docs)


if __name__ == "__main__":
    unittest.main()
