from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = REPO_ROOT / "tools" / "execution_observability_validator.py"
SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_execution_observability.py"


def load_module():
    spec = importlib.util.spec_from_file_location("execution_observability_validator", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_jsonl(path: Path, events: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")


class ExecutionObservabilityValidatorTests(unittest.TestCase):
    def test_collects_jsonl_files_recursively(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            direct = root / "execution-observability.jsonl"
            nested = root / "nested" / "other.jsonl"
            ignored = root / "nested" / "notes.txt"
            write_jsonl(direct, [])
            write_jsonl(nested, [])
            ignored.write_text("not jsonl\n", encoding="utf-8")

            paths, issues = module.collect_jsonl_paths([root])

        self.assertEqual([], issues)
        self.assertEqual(["execution-observability.jsonl", "other.jsonl"], sorted(path.name for path in paths))

    def test_accepts_exact_model_usage_and_default_skill_context_measurement(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "execution-observability.jsonl"
            write_jsonl(
                path,
                [
                    {
                        "schema_version": "execution-event.v1",
                        "event_type": "model_usage.completed",
                        "status": "completed",
                        "runner": "copilot",
                        "token_input": 100,
                        "token_output": 25,
                        "token_total": 125,
                        "usage_source": "provider",
                        "usage_precision": "exact",
                        "metadata": {},
                    },
                    {
                        "schema_version": "execution-event.v1",
                        "event_type": "skill_context.measured",
                        "status": "completed",
                        "runner": "copilot",
                        "token_input": None,
                        "token_output": None,
                        "token_total": None,
                        "usage_precision": "unavailable",
                        "metadata": {
                            "skill_file_sha256": "abc123",
                            "skill_file_char_count": 10,
                            "skill_file_byte_count": 10,
                        },
                    },
                ],
            )

            issues = module.validate_jsonl_file(path)

        self.assertEqual([], issues)

    def test_rejects_missing_or_invalid_exact_model_usage(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "execution-observability.jsonl"
            write_jsonl(
                path,
                [
                    {
                        "event_type": "model_usage.completed",
                        "token_input": 1,
                        "token_output": 2,
                        "token_total": 3,
                    },
                    {
                        "event_type": "model_usage.completed",
                        "token_input": 1,
                        "token_output": 2,
                        "token_total": 4,
                        "usage_precision": "exact",
                    },
                    {
                        "event_type": "model_usage.completed",
                        "token_input": True,
                        "token_output": 2,
                        "token_total": 3,
                        "usage_precision": "exact",
                    },
                    {
                        "event_type": "model_usage.completed",
                        "token_input": None,
                        "token_output": None,
                        "token_total": None,
                        "usage_precision": "approximate",
                    },
                ],
            )

            rendered = [issue.render() for issue in module.validate_jsonl_file(path)]

        self.assertGreaterEqual(sum("requires usage_precision" in issue for issue in rendered), 2)
        self.assertTrue(any("token_total must equal" in issue for issue in rendered))
        self.assertTrue(any("token_input must be a non-negative integer" in issue for issue in rendered))

    def test_non_exact_model_usage_is_not_treated_as_exact(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "execution-observability.jsonl"
            write_jsonl(
                path,
                [
                    {
                        "event_type": "model_usage.completed",
                        "usage_source": "runner",
                        "token_input": 130,
                        "token_output": 25,
                        "token_total": 155,
                        "token_cache_read_input": 12,
                        "token_cache_write_input": 1,
                        "usage_precision": "estimated",
                    },
                    {
                        "event_type": "model_usage.completed",
                        "token_input": None,
                        "token_output": None,
                        "token_total": None,
                        "usage_precision": "estimated",
                    },
                    {
                        "event_type": "model_usage.completed",
                        "usage_precision": "unknown",
                    },
                    {
                        "event_type": "model_usage.completed",
                        "usage_precision": "unavailable",
                    },
                ],
            )

            issues = module.validate_jsonl_file(path)

        self.assertEqual([], issues)

    def test_rejects_unavailable_usage_with_token_fields(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "execution-observability.jsonl"
            write_jsonl(
                path,
                [
                    {
                        "event_type": "model_usage.unavailable",
                        "token_input": 1,
                        "token_output": None,
                        "token_total": None,
                        "usage_source": "unavailable",
                        "usage_precision": "unavailable",
                    },
                    {
                        "event_type": "model_usage.unavailable",
                        "token_input": None,
                        "token_output": None,
                        "token_total": None,
                        "usage_source": "runner",
                        "usage_precision": "unknown",
                    },
                ],
            )

            rendered = [issue.render() for issue in module.validate_jsonl_file(path)]

        self.assertTrue(any("requires all token fields to be null" in issue for issue in rendered))
        self.assertTrue(any("requires usage_source" in issue for issue in rendered))
        self.assertTrue(any("requires usage_precision unavailable or null" in issue for issue in rendered))

    def test_rejects_completed_unknown_or_unavailable_usage_with_tokens(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "execution-observability.jsonl"
            write_jsonl(
                path,
                [
                    {
                        "event_type": "model_usage.completed",
                        "token_input": 1,
                        "token_output": 1,
                        "token_total": 2,
                        "usage_precision": "unknown",
                    },
                    {
                        "event_type": "model_usage.completed",
                        "token_input": None,
                        "token_output": None,
                        "token_total": None,
                        "token_cache_read_input": 1,
                        "usage_precision": "unavailable",
                    },
                    {
                        "event_type": "model_usage.completed",
                        "token_input": 1,
                        "token_output": 1,
                        "token_total": 2,
                        "usage_source": "provider",
                        "usage_precision": "estimated",
                    },
                ],
            )

            rendered = [issue.render() for issue in module.validate_jsonl_file(path)]

        self.assertTrue(any("unknown or unavailable precision must keep token fields null" in issue for issue in rendered))
        self.assertTrue(any("requires usage_source runner" in issue for issue in rendered))

    def test_rejects_exact_model_usage_without_trusted_source(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "execution-observability.jsonl"
            write_jsonl(
                path,
                [
                    {
                        "event_type": "model_usage.completed",
                        "token_input": 1,
                        "token_output": 1,
                        "token_total": 2,
                        "usage_source": "unavailable",
                        "usage_precision": "exact",
                    },
                    {
                        "event_type": "model_usage.completed",
                        "token_input": 1,
                        "token_output": 1,
                        "token_total": 2,
                        "usage_source": "custom-counter",
                        "usage_precision": "exact",
                    },
                ],
            )

            rendered = [issue.render() for issue in module.validate_jsonl_file(path)]

        self.assertEqual(2, sum("requires usage_source provider or runner" in issue for issue in rendered))

    def test_rejects_skill_context_tokens_without_trusted_exact_evidence(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "execution-observability.jsonl"
            write_jsonl(
                path,
                [
                    {
                        "event_type": "skill_context.measured",
                        "token_input": 10,
                        "token_output": 0,
                        "token_total": 10,
                        "usage_precision": "estimated",
                        "metadata": {"chars_per_token": 4},
                    },
                    {
                        "event_type": "skill_context.measured",
                        "token_input": 10,
                        "token_output": 0,
                        "token_total": 10,
                        "usage_precision": "exact",
                        "metadata": {},
                    },
                ],
            )

            rendered = [issue.render() for issue in module.validate_jsonl_file(path)]

        self.assertTrue(any("token fields must be null" in issue for issue in rendered))
        self.assertTrue(any("exact token fields require metadata" in issue for issue in rendered))

    def test_accepts_skill_context_exact_tokens_with_trusted_provider_evidence(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "execution-observability.jsonl"
            write_jsonl(
                path,
                [
                    {
                        "event_type": "skill_context.measured",
                        "token_input": 10,
                        "token_output": 0,
                        "token_total": 10,
                        "usage_precision": "exact",
                        "metadata": {
                            "token_count_method": "provider_api",
                            "token_provider": "provider-name",
                        },
                    },
                    {
                        "event_type": "skill_context.measured",
                        "token_input": 7,
                        "token_output": 0,
                        "token_total": 7,
                        "usage_precision": "exact",
                        "metadata": {
                            "token_count_method": "official_tokenizer",
                            "tokenizer": "model-tokenizer",
                            "model": "model-name",
                        },
                    },
                ],
            )

            issues = module.validate_jsonl_file(path)

        self.assertEqual([], issues)

    def test_cli_returns_nonzero_and_prints_readable_errors(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "execution-observability.jsonl"
            write_jsonl(
                path,
                [
                    {
                        "event_type": "model_usage.completed",
                        "token_input": 1,
                        "token_output": 1,
                        "token_total": 3,
                        "usage_precision": "exact",
                    }
                ],
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(path)],
                cwd=REPO_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

        self.assertEqual(1, result.returncode)
        self.assertIn("Execution observability validation failed", result.stderr)
        self.assertIn("token_total must equal", result.stderr)


if __name__ == "__main__":
    unittest.main()
