from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.execution_observability import ExecutionTrace, measure_skill_context, new_span_id


class ExecutionObservabilityHelperTests(unittest.TestCase):
    def test_measure_skill_context_records_exact_size_without_token_estimates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "skills" / "cross-cutting" / "observability"
            references_dir = skill_dir / "references"
            references_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "\n".join(
                    [
                        "---",
                        "name: observability",
                        "description: Use when execution telemetry is needed.",
                        "metadata:",
                        "  phase: cross-cutting",
                        "---",
                        "",
                        "# Observability",
                        "",
                        "Emit structured events.",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (references_dir / "gotchas.md").write_text("Do not invent token usage.\n", encoding="utf-8")

            measurement = measure_skill_context(skill_dir)

        self.assertEqual("observability", measurement["skill_name"])
        self.assertEqual("cross-cutting", measurement["phase"])
        self.assertEqual("unavailable", measurement["token_count_status"])
        self.assertGreater(measurement["skill_file_char_count"], 0)
        self.assertGreater(measurement["skill_metadata_char_count"], 0)
        self.assertGreater(measurement["skill_file_byte_count"], 0)
        self.assertEqual(1, measurement["supporting_context_file_count"])
        self.assertEqual(
            measurement["skill_file_char_count"] + measurement["supporting_context_char_count"],
            measurement["total_available_context_char_count"],
        )
        self.assertEqual(
            measurement["skill_file_byte_count"] + measurement["supporting_context_byte_count"],
            measurement["total_available_context_byte_count"],
        )

    def test_execution_trace_emit_preserves_cache_token_fields(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "execution-observability.jsonl"
            trace = ExecutionTrace(
                output_path=output_path,
                runner="copilot",
                model_name="claude-sonnet",
                skill_name="observability",
                phase="cross-cutting",
                workflow="benchmark",
            )

            trace.emit(
                event_type="model_usage.completed",
                status="completed",
                span_id=new_span_id(),
                token_input=100,
                token_output=20,
                token_total=120,
                token_cache_read_input=10,
                token_cache_write_input=2,
                usage_source="runner",
                usage_precision="exact",
            )

            event = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(100, event["token_input"])
        self.assertEqual(20, event["token_output"])
        self.assertEqual(120, event["token_total"])
        self.assertEqual(10, event["token_cache_read_input"])
        self.assertEqual(2, event["token_cache_write_input"])
        self.assertEqual("exact", event["usage_precision"])


if __name__ == "__main__":
    unittest.main()
