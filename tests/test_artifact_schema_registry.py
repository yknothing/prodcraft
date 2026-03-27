from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "schemas" / "artifacts" / "registry.yml"


class ArtifactSchemaRegistryTests(unittest.TestCase):
    def test_registry_declares_core_artifacts(self):
        registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
        artifacts = registry["artifacts"]

        self.assertIn("intake-brief", artifacts)
        self.assertIn("course-correction-note", artifacts)
        self.assertIn("problem-frame", artifacts)
        self.assertIn("requirements-doc", artifacts)
        self.assertIn("review-report", artifacts)

    def test_intake_brief_schema_and_template_stay_in_sync(self):
        registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
        entry = registry["artifacts"]["intake-brief"]
        schema = json.loads((REPO_ROOT / entry["schema_path"]).read_text(encoding="utf-8"))
        template_text = (REPO_ROOT / entry["template_path"]).read_text(encoding="utf-8")

        self.assertEqual(
            {
                "artifact",
                "schema_version",
                "status",
                "request_summary",
                "source_language",
                "artifact_record_language",
                "user_presentation_locale",
                "intake_mode",
                "work_type",
                "entry_phase",
                "scope_assessment",
                "recommended_next_skill",
                "routing_rationale",
                "key_risks",
                "questions_asked",
                "routing_changed_by_answers",
                "approver",
            },
            set(schema["required"]),
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertIn("enum", schema["properties"]["source_language"])
        self.assertEqual("en", schema["properties"]["artifact_record_language"]["const"])
        self.assertIn("enum", schema["properties"]["user_presentation_locale"])
        self.assertIn("enum", schema["properties"]["work_type"])
        self.assertIn("enum", schema["properties"]["entry_phase"])
        self.assertIn("enum", schema["properties"]["workflow_primary"])
        self.assertIn("enum", schema["properties"]["workflow_overlays"]["items"])
        self.assertEqual(1, schema["properties"]["workflow_overlays"]["minItems"])
        self.assertTrue(schema["properties"]["workflow_overlays"]["uniqueItems"])
        self.assertIn("allOf", schema)
        for field_name in schema["required"]:
            self.assertIn(field_name, template_text)
        self.assertIn("workflow_primary", template_text)
        self.assertIn("workflow_overlays", template_text)

    def test_course_correction_schema_and_template_stay_in_sync(self):
        registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
        entry = registry["artifacts"]["course-correction-note"]
        schema = json.loads((REPO_ROOT / entry["schema_path"]).read_text(encoding="utf-8"))
        template_text = (REPO_ROOT / entry["template_path"]).read_text(encoding="utf-8")

        self.assertEqual(
            {
                "artifact",
                "schema_version",
                "status",
                "source_phase",
                "target_phase",
                "trigger",
                "evidence_refs",
                "blocked_artifact",
                "preserved_constraints",
                "recommended_next_skill",
                "severity",
                "requires_user_reapproval",
            },
            set(schema["required"]),
        )
        for field_name in schema["required"]:
            self.assertIn(field_name, template_text)

    def test_problem_frame_and_requirements_doc_language_boundary_contracts(self):
        registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))

        for artifact_name in ("problem-frame", "requirements-doc"):
            with self.subTest(artifact=artifact_name):
                entry = registry["artifacts"][artifact_name]
                schema = json.loads((REPO_ROOT / entry["schema_path"]).read_text(encoding="utf-8"))
                template_text = (REPO_ROOT / entry["template_path"]).read_text(encoding="utf-8")

                self.assertIn("source_language", schema["required"])
                self.assertIn("artifact_record_language", schema["required"])
                self.assertIn("user_presentation_locale", schema["required"])
                self.assertEqual({"en", "zh", "mixed"}, set(schema["properties"]["source_language"]["enum"]))
                self.assertEqual("en", schema["properties"]["artifact_record_language"]["const"])
                self.assertEqual({"en", "zh"}, set(schema["properties"]["user_presentation_locale"]["enum"]))
                self.assertFalse(schema["additionalProperties"])

                for field_name in schema["required"]:
                    self.assertIn(field_name, template_text)


if __name__ == "__main__":
    unittest.main()
