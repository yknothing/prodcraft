from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "summarize_execution_observability.py"


def load_module():
    spec = importlib.util.spec_from_file_location("summarize_execution_observability", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ExecutionObservabilitySummaryTests(unittest.TestCase):
    def test_summary_groups_recurring_failures_missing_usage_and_high_risk_actions(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            jsonl_path = Path(tmpdir) / "execution-observability.jsonl"
            jsonl_path.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "runner_execution.failed",
                                "status": "failed",
                                "runner": "gemini",
                                "skill_name": "intake",
                                "workflow": "agile-sprint",
                                "metadata": {"error_type": "timeout", "command": "python3 scripts/run_explicit_skill_benchmark.py"},
                            }
                        ),
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.unavailable",
                                "status": "unavailable",
                                "runner": "claude",
                                "skill_name": "intake",
                                "workflow": "discoverability-eval",
                                "metadata": {"reason": "runner stream missing usage"},
                            }
                        ),
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "skill_invocation.failed",
                                "status": "failed",
                                "runner": "gemini",
                                "skill_name": "deployment-strategy",
                                "workflow": "hotfix",
                                "metadata": {"error_type": "unsafe_action", "action": "force push"},
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = module.summarize_events(jsonl_path)

        self.assertIn("timeout", summary["recurring_failures"])
        self.assertEqual(1, summary["missing_usage"]["count"])
        self.assertIn("force push", summary["high_risk_actions"])


if __name__ == "__main__":
    unittest.main()
