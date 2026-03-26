from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class CourseCorrectionContractTests(unittest.TestCase):
    def test_manifest_tracks_course_correction_artifact(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        artifact_names = {entry["artifact"] for entry in manifest["artifact_flow"]}
        self.assertIn("course-correction-note", artifact_names)

    def test_gateway_and_phase_docs_call_out_course_corrections(self):
        gateway = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")
        implementation_phase = (REPO_ROOT / "skills" / "04-implementation" / "_phase.md").read_text(encoding="utf-8")
        operations_phase = (REPO_ROOT / "skills" / "07-operations" / "_phase.md").read_text(encoding="utf-8")

        self.assertIn("course-correction-note", gateway)
        self.assertIn("04-implementation -> 01-specification", gateway)
        self.assertIn("course-correction-note", implementation_phase)
        self.assertIn("course-correction-note", operations_phase)

    def test_course_correction_schema_declares_phase_and_reapproval_fields(self):
        schema = json.loads(
            (REPO_ROOT / "schemas" / "artifacts" / "course-correction-note.schema.json").read_text(encoding="utf-8")
        )
        properties = schema["properties"]
        self.assertIn("source_phase", properties)
        self.assertIn("target_phase", properties)
        self.assertIn("requires_user_reapproval", properties)


if __name__ == "__main__":
    unittest.main()
