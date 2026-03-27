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

    def test_summary_can_collect_multiple_inputs_and_apply_thresholds(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            first = root / "one.execution-observability.jsonl"
            second_dir = root / "nested"
            second_dir.mkdir(parents=True, exist_ok=True)
            second = second_dir / "two.execution-observability.jsonl"
            thresholds = root / "thresholds.yml"

            first.write_text(
                json.dumps(
                    {
                        "schema_version": "execution-event.v1",
                        "event_type": "runner_execution.failed",
                        "status": "failed",
                        "metadata": {"error_type": "timeout"},
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            second.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "runner_execution.failed",
                                "status": "failed",
                                "metadata": {"error_type": "timeout"},
                            }
                        ),
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.unavailable",
                                "status": "unavailable",
                                "metadata": {"reason": "runner stream missing usage"},
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            thresholds.write_text(
                "\n".join(
                    [
                        "recurring_failures:",
                        "  min_occurrences: 2",
                        "missing_usage:",
                        "  max_count: 0",
                        "high_risk_actions:",
                        "  max_count: 0",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            collected = module.collect_jsonl_paths([first, second_dir])
            summary = module.summarize_events(collected)
            breaches = module.evaluate_thresholds(summary, module.load_thresholds(thresholds))

        self.assertEqual(2, summary["input_count"])
        self.assertEqual(2, summary["recurring_failures"]["timeout"])
        self.assertEqual(1, summary["missing_usage"]["count"])
        self.assertIn("recurring failure 'timeout' seen 2 times", breaches)
        self.assertIn("missing usage count 1 exceeds max 0", breaches)


if __name__ == "__main__":
    unittest.main()
