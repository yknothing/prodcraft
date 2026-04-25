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

    def test_summary_groups_token_usage_and_skill_context_efficiency(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            jsonl_path = Path(tmpdir) / "execution-observability.jsonl"
            jsonl_path.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.completed",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": None,
                                "token_input": 100,
                                "token_output": 20,
                                "token_total": 120,
                                "token_cache_read_input": 10,
                                "token_cache_write_input": 0,
                                "usage_source": "provider",
                                "usage_precision": "exact",
                                "metadata": {"scenario_id": "demo", "branch": "without_skill"},
                            }
                        ),
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "skill_invocation.started",
                                "status": "started",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "metadata": {"scenario_id": "demo", "invocation_id": "invoke-1"},
                            }
                        ),
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "skill_invocation.completed",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "metadata": {"scenario_id": "demo", "invocation_id": "invoke-1"},
                            }
                        ),
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "skill_context.measured",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "token_input": None,
                                "token_total": None,
                                "usage_source": "unavailable",
                                "usage_precision": "unavailable",
                                "metadata": {
                                    "scenario_id": "demo",
                                    "branch": "with_skill",
                                    "loaded_context_char_count": 30,
                                    "deferred_context_char_count": 70,
                                    "available_context_char_count": 100,
                                    "loaded_context_byte_count": 30,
                                    "deferred_context_byte_count": 70,
                                    "available_context_byte_count": 100,
                                    "invocation_id": "invoke-1",
                                },
                            }
                        ),
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.completed",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "token_input": 130,
                                "token_output": 25,
                                "token_total": 155,
                                "token_cache_read_input": 12,
                                "token_cache_write_input": 1,
                                "usage_source": "provider",
                                "usage_precision": "exact",
                                "metadata": {"scenario_id": "demo", "branch": "with_skill"},
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = module.summarize_events(jsonl_path)

        self.assertEqual(2, summary["token_usage"]["event_count"])
        self.assertEqual(230, summary["token_usage"]["token_input"])
        self.assertEqual(275, summary["token_usage"]["token_total"])
        self.assertEqual(1, summary["skill_context"]["measured_count"])
        self.assertEqual("exact_char_and_byte", summary["skill_context"]["measurement_precision"])
        self.assertEqual("unavailable", summary["skill_context"]["token_count_status"])
        self.assertEqual(0.3, summary["skill_context"]["loaded_context_char_ratio"])
        self.assertEqual(0.7, summary["skill_context"]["deferred_context_char_ratio"])
        self.assertEqual(0.3, summary["skill_context"]["loaded_context_byte_ratio"])
        self.assertEqual(0.7, summary["skill_context"]["deferred_context_byte_ratio"])
        self.assertEqual(1, summary["skill_context"]["skill_invocation_event_count"])
        self.assertEqual(1, summary["skill_context"]["measured_invocation_count"])
        self.assertEqual(1.0, summary["skill_context"]["sampling_ratio"])
        self.assertEqual(0.7, summary["skill_context"]["by_skill"]["observability"]["deferred_context_byte_ratio"])
        self.assertEqual(1.0, summary["usage_quality"]["exact_usage_coverage_ratio"])
        self.assertIn("exact_token_branch_deltas", summary["context_efficiency"])
        self.assertEqual(
            "exact",
            summary["context_efficiency"]["exact_token_branch_deltas"]["source_precision"],
        )
        self.assertEqual(30, summary["context_efficiency"]["branch_deltas"]["demo"]["token_input_delta"])
        self.assertEqual(35, summary["context_efficiency"]["branch_deltas"]["demo"]["token_total_delta"])
        self.assertEqual(
            35,
            summary["context_efficiency"]["exact_token_branch_deltas"]["deltas"]["demo"]["token_total_delta"],
        )

    def test_summary_keeps_estimated_usage_out_of_exact_totals(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            jsonl_path = Path(tmpdir) / "execution-observability.jsonl"
            jsonl_path.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.completed",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "token_input": 100,
                                "token_output": 20,
                                "token_total": 120,
                                "token_cache_read_input": 0,
                                "token_cache_write_input": 0,
                                "usage_source": "runner",
                                "usage_precision": "estimated",
                                "metadata": {"scenario_id": "demo", "branch": "without_skill"},
                            }
                        ),
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.completed",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "token_input": 130,
                                "token_output": 25,
                                "token_total": 155,
                                "token_cache_read_input": 12,
                                "token_cache_write_input": 1,
                                "usage_source": "runner",
                                "usage_precision": "estimated",
                                "metadata": {"scenario_id": "demo", "branch": "with_skill"},
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = module.summarize_events(jsonl_path)

        self.assertEqual(0, summary["token_usage"]["event_count"])
        self.assertEqual(0, summary["token_usage"]["token_total"])
        self.assertEqual(2, summary["estimated_token_usage"]["event_count"])
        self.assertEqual(275, summary["estimated_token_usage"]["token_total"])
        self.assertTrue(summary["estimated_token_usage"]["advisory"])
        self.assertEqual(0.0, summary["usage_quality"]["exact_usage_coverage_ratio"])
        self.assertEqual({}, summary["context_efficiency"]["exact_token_branch_deltas"]["deltas"])
        self.assertTrue(summary["context_efficiency"]["estimated_token_branch_deltas_advisory"]["advisory"])
        self.assertEqual(
            35,
            summary["context_efficiency"]["estimated_token_branch_deltas_advisory"]["deltas"]["demo"]["token_total_delta"],
        )

    def test_provider_usage_without_precision_is_unknown_not_exact(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            jsonl_path = Path(tmpdir) / "execution-observability.jsonl"
            jsonl_path.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.completed",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "token_input": 100,
                                "token_output": 20,
                                "token_total": 120,
                                "usage_source": "provider",
                                "metadata": {"scenario_id": "demo", "branch": "without_skill"},
                            }
                        ),
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.completed",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "token_input": 130,
                                "token_output": 25,
                                "token_total": 155,
                                "usage_source": "provider",
                                "metadata": {"scenario_id": "demo", "branch": "with_skill"},
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = module.summarize_events(jsonl_path)
            breaches = module.evaluate_thresholds(summary, {"unknown_token_usage": {"max_count": 0}})

        self.assertEqual(0, summary["token_usage"]["event_count"])
        self.assertEqual(0, summary["token_usage"]["token_total"])
        self.assertEqual(2, summary["unknown_token_usage"]["event_count"])
        self.assertEqual(275, summary["unknown_token_usage"]["token_total"])
        self.assertEqual(0.0, summary["usage_quality"]["exact_usage_coverage_ratio"])
        self.assertEqual({}, summary["context_efficiency"]["exact_token_branch_deltas"]["deltas"])
        self.assertEqual({}, summary["context_efficiency"]["estimated_token_branch_deltas_advisory"]["deltas"])
        self.assertIn("unknown model usage count 2 exceeds max 0", breaches)

    def test_inconsistent_exact_total_is_invalid_not_exact(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            jsonl_path = Path(tmpdir) / "execution-observability.jsonl"
            jsonl_path.write_text(
                json.dumps(
                    {
                        "schema_version": "execution-event.v1",
                        "event_type": "model_usage.completed",
                        "status": "completed",
                        "runner": "copilot",
                        "skill_name": "observability",
                        "token_input": 100,
                        "token_output": 20,
                        "token_total": 999,
                        "usage_source": "provider",
                        "usage_precision": "exact",
                        "metadata": {"scenario_id": "demo", "branch": "with_skill"},
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            summary = module.summarize_events(jsonl_path)
            breaches = module.evaluate_thresholds(
                summary,
                {
                    "token_usage": {"min_exact_coverage_ratio": 1.0},
                    "invalid_token_usage": {"max_count": 0},
                },
            )

        self.assertEqual(0, summary["token_usage"]["event_count"])
        self.assertEqual(0, summary["token_usage"]["token_total"])
        self.assertEqual(1, summary["invalid_token_usage"]["event_count"])
        self.assertEqual(1, summary["invalid_token_usage"]["by_reason"]["exact_usage_total_mismatch"])
        self.assertEqual(0.0, summary["usage_quality"]["exact_usage_coverage_ratio"])
        self.assertEqual({}, summary["context_efficiency"]["exact_token_branch_deltas"]["deltas"])
        self.assertIn("exact model usage coverage 0.0000 below min 1.0000", breaches)
        self.assertIn("invalid model usage count 1 exceeds max 0", breaches)

    def test_untrusted_exact_usage_source_is_invalid_not_exact(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            jsonl_path = Path(tmpdir) / "execution-observability.jsonl"
            jsonl_path.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.completed",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "token_input": 100,
                                "token_output": 20,
                                "token_total": 120,
                                "usage_source": "unavailable",
                                "usage_precision": "exact",
                                "metadata": {"scenario_id": "demo", "branch": "without_skill"},
                            }
                        ),
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.completed",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "token_input": 130,
                                "token_output": 25,
                                "token_total": 155,
                                "usage_source": "custom-counter",
                                "usage_precision": "exact",
                                "metadata": {"scenario_id": "demo", "branch": "with_skill"},
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = module.summarize_events(jsonl_path)

        self.assertEqual(0, summary["token_usage"]["event_count"])
        self.assertEqual(0, summary["token_usage"]["token_total"])
        self.assertEqual(2, summary["invalid_token_usage"]["event_count"])
        self.assertEqual(2, summary["invalid_token_usage"]["by_reason"]["exact_usage_untrusted_source"])
        self.assertEqual(0.0, summary["usage_quality"]["exact_usage_coverage_ratio"])
        self.assertEqual({}, summary["context_efficiency"]["exact_token_branch_deltas"]["deltas"])

    def test_bool_exact_token_fields_are_invalid_not_exact(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            jsonl_path = Path(tmpdir) / "execution-observability.jsonl"
            jsonl_path.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.completed",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "token_input": True,
                                "token_output": 20,
                                "token_total": 21,
                                "usage_source": "provider",
                                "usage_precision": "exact",
                                "metadata": {"scenario_id": "demo", "branch": "without_skill"},
                            }
                        ),
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.completed",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "token_input": 130,
                                "token_output": 25,
                                "token_total": True,
                                "usage_source": "provider",
                                "usage_precision": "exact",
                                "metadata": {"scenario_id": "demo", "branch": "with_skill"},
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = module.summarize_events(jsonl_path)

        self.assertEqual(0, summary["token_usage"]["event_count"])
        self.assertEqual(0, summary["token_usage"]["token_total"])
        self.assertEqual(2, summary["invalid_token_usage"]["event_count"])
        self.assertEqual(2, summary["invalid_token_usage"]["by_reason"]["exact_usage_bool_token_fields"])
        self.assertEqual(0.0, summary["usage_quality"]["exact_usage_coverage_ratio"])
        self.assertEqual({}, summary["context_efficiency"]["exact_token_branch_deltas"]["deltas"])

    def test_negative_exact_token_fields_are_invalid_not_exact(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            jsonl_path = Path(tmpdir) / "execution-observability.jsonl"
            jsonl_path.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.completed",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "token_input": -1,
                                "token_output": 20,
                                "token_total": 19,
                                "usage_source": "provider",
                                "usage_precision": "exact",
                                "metadata": {"scenario_id": "demo", "branch": "without_skill"},
                            }
                        ),
                        json.dumps(
                            {
                                "schema_version": "execution-event.v1",
                                "event_type": "model_usage.completed",
                                "status": "completed",
                                "runner": "copilot",
                                "skill_name": "observability",
                                "token_input": 130,
                                "token_output": -25,
                                "token_total": 105,
                                "usage_source": "provider",
                                "usage_precision": "exact",
                                "metadata": {"scenario_id": "demo", "branch": "with_skill"},
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = module.summarize_events(jsonl_path)

        self.assertEqual(0, summary["token_usage"]["event_count"])
        self.assertEqual(0, summary["token_usage"]["token_total"])
        self.assertEqual(2, summary["invalid_token_usage"]["event_count"])
        self.assertEqual(2, summary["invalid_token_usage"]["by_reason"]["exact_usage_negative_token_fields"])
        self.assertEqual(0.0, summary["usage_quality"]["exact_usage_coverage_ratio"])
        self.assertEqual({}, summary["context_efficiency"]["exact_token_branch_deltas"]["deltas"])

    def test_thresholds_can_require_usage_and_skill_context_events(self):
        module = load_module()

        summary = {
            "recurring_failures": {},
            "missing_usage": {"count": 0},
            "high_risk_actions": [],
            "usage_quality": {"exact_usage_coverage_ratio": 0.25},
            "token_usage": {"event_count": 0},
            "estimated_token_usage": {"event_count": 2},
            "unknown_token_usage": {"event_count": 1},
            "invalid_token_usage": {"event_count": 1},
            "skill_context": {"measured_count": 0, "sampling_ratio": 0.25},
        }
        thresholds = {
            "token_usage": {"min_completed_count": 1, "min_exact_coverage_ratio": 1.0},
            "estimated_token_usage": {"max_count": 0},
            "unknown_token_usage": {"max_count": 0},
            "invalid_token_usage": {"max_count": 0},
            "skill_context": {"min_measured_count": 1, "min_sampling_ratio": 0.5},
        }

        breaches = module.evaluate_thresholds(summary, thresholds)

        self.assertIn("exact model usage completed count 0 below min 1", breaches)
        self.assertIn("exact model usage coverage 0.2500 below min 1.0000", breaches)
        self.assertIn("estimated model usage count 2 exceeds max 0", breaches)
        self.assertIn("unknown model usage count 1 exceeds max 0", breaches)
        self.assertIn("invalid model usage count 1 exceeds max 0", breaches)
        self.assertIn("skill context measured count 0 below min 1", breaches)
        self.assertIn("skill context sampling ratio 0.2500 below min 0.5000", breaches)


if __name__ == "__main__":
    unittest.main()
