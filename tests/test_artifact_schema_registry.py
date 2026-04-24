from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml

try:
    import jsonschema
except ImportError:  # pragma: no cover - exercised only when optional dependency is absent
    jsonschema = None


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "schemas" / "artifacts" / "registry.yml"


class ArtifactSchemaRegistryTests(unittest.TestCase):
    def load_artifact_schema(self, artifact_name: str) -> dict:
        registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
        entry = registry["artifacts"][artifact_name]
        return json.loads((REPO_ROOT / entry["schema_path"]).read_text(encoding="utf-8"))

    def test_registry_declares_core_artifacts(self):
        registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
        artifacts = registry["artifacts"]

        self.assertIn("intake-brief", artifacts)
        self.assertIn("course-correction-note", artifacts)
        self.assertIn("verification-record", artifacts)
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

    def test_verification_record_schema_and_template_stay_in_sync(self):
        registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
        entry = registry["artifacts"]["verification-record"]
        schema = json.loads((REPO_ROOT / entry["schema_path"]).read_text(encoding="utf-8"))
        template_text = (REPO_ROOT / entry["template_path"]).read_text(encoding="utf-8")

        self.assertEqual(
            {
                "artifact",
                "schema_version",
                "status",
                "claim",
                "claim_scope",
                "verified_at",
                "work_state_ref",
                "evidence_refs",
                "checks_run",
                "passed",
                "failed",
                "remaining_unverified",
                "claim_may_be_made",
            },
            set(schema["required"]),
        )
        self.assertEqual("verification-record", schema["properties"]["artifact"]["const"])
        self.assertEqual("verification-record.v1", schema["properties"]["schema_version"]["const"])
        self.assertEqual({"draft", "accepted", "rejected"}, set(schema["properties"]["status"]["enum"]))
        self.assertEqual("date-time", schema["properties"]["verified_at"]["format"])
        self.assertEqual(1, schema["properties"]["claim"]["minLength"])
        self.assertEqual(1, schema["properties"]["claim_scope"]["minLength"])
        self.assertEqual(1, schema["properties"]["work_state_ref"]["minLength"])
        self.assertEqual(1, schema["properties"]["evidence_refs"]["minItems"])
        self.assertEqual(1, schema["properties"]["evidence_refs"]["items"]["minLength"])
        self.assertEqual(1, schema["properties"]["checks_run"]["minItems"])
        self.assertFalse(schema["additionalProperties"])
        check_item = schema["properties"]["checks_run"]["items"]
        self.assertEqual({"name", "result", "evidence_ref"}, set(check_item["required"]))
        self.assertEqual(1, check_item["properties"]["name"]["minLength"])
        self.assertEqual({"passed", "failed", "skipped"}, set(check_item["properties"]["result"]["enum"]))
        self.assertEqual(1, check_item["properties"]["evidence_ref"]["minLength"])
        self.assertFalse(check_item["additionalProperties"])

        all_of = schema["allOf"]
        self.assertIn(
            {
                "if": {"properties": {"status": {"const": "accepted"}}, "required": ["status"]},
                "then": {"properties": {"claim_may_be_made": {"const": True}}},
            },
            all_of,
        )
        self.assertIn(
            {
                "if": {"properties": {"status": {"const": "rejected"}}, "required": ["status"]},
                "then": {"properties": {"claim_may_be_made": {"const": False}}},
            },
            all_of,
        )
        self.assertIn(
            {
                "if": {
                    "properties": {"claim_may_be_made": {"const": True}},
                    "required": ["claim_may_be_made"],
                },
                "then": {
                    "properties": {
                        "status": {"const": "accepted"},
                        "failed": {"maxItems": 0},
                        "remaining_unverified": {"maxItems": 0},
                        "checks_run": {
                            "items": {
                                "properties": {"result": {"const": "passed"}},
                                "required": ["result"],
                            }
                        },
                    }
                },
            },
            all_of,
        )

        for field_name in schema["required"]:
            self.assertIn(field_name, template_text)

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_verification_record_schema_rejects_invalid_claim_authorization(self):
        schema = self.load_artifact_schema("verification-record")
        valid_payload = {
            "artifact": "verification-record",
            "schema_version": "verification-record.v1",
            "status": "accepted",
            "claim": "The artifact registry check passed.",
            "claim_scope": "artifact-schema-registry",
            "verified_at": "2026-04-24T09:00:00Z",
            "work_state_ref": "git:abc123",
            "evidence_refs": ["command:validate-prodcraft-artifact-schema-registry"],
            "checks_run": [
                {
                    "name": "artifact-schema-registry",
                    "result": "passed",
                    "evidence_ref": "command:validate-prodcraft-artifact-schema-registry",
                }
            ],
            "passed": ["artifact-schema-registry"],
            "failed": [],
            "remaining_unverified": [],
            "claim_may_be_made": True,
        }

        jsonschema.validate(valid_payload, schema)

        invalid_payloads = [
            {
                **valid_payload,
                "status": "draft",
            },
            {
                **valid_payload,
                "status": "rejected",
            },
            {
                **valid_payload,
                "checks_run": [
                    {
                        "name": "artifact-schema-registry",
                        "result": "skipped",
                        "evidence_ref": "command:validate-prodcraft-artifact-schema-registry",
                    }
                ],
            },
            {
                **valid_payload,
                "failed": ["artifact-schema-registry"],
            },
            {
                **valid_payload,
                "remaining_unverified": ["curated-surface"],
            },
        ]

        for payload in invalid_payloads:
            with self.subTest(status=payload.get("status"), checks=payload.get("checks_run")):
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.validate(payload, schema)

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
