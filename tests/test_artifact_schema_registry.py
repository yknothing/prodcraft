from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import yaml

try:
    import jsonschema
except ImportError:  # pragma: no cover - exercised only when optional dependency is absent
    jsonschema = None


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.validate_prodcraft import validate_verification_record_instance_contract  # noqa: E402

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
        work_state_ref = schema["properties"]["work_state_ref"]
        self.assertEqual("object", work_state_ref["type"])
        self.assertEqual({"id", "kind", "ref", "captured_at", "status"}, set(work_state_ref["required"]))
        self.assertEqual(1, work_state_ref["properties"]["id"]["minLength"])
        self.assertEqual({"git"}, set(work_state_ref["properties"]["kind"]["enum"]))
        self.assertEqual(1, work_state_ref["properties"]["ref"]["minLength"])
        self.assertEqual("date-time", work_state_ref["properties"]["captured_at"]["format"])
        self.assertEqual({"clean", "dirty"}, set(work_state_ref["properties"]["status"]["enum"]))
        self.assertEqual(1, work_state_ref["properties"]["diff_ref"]["minLength"])
        self.assertFalse(work_state_ref["additionalProperties"])
        self.assertIn(
            {
                "if": {
                    "properties": {"status": {"const": "dirty"}},
                    "required": ["status"],
                },
                "then": {"required": ["diff_ref"]},
            },
            work_state_ref["allOf"],
        )
        self.assertEqual(1, schema["properties"]["evidence_refs"]["minItems"])
        evidence_item = schema["properties"]["evidence_refs"]["items"]
        self.assertEqual("object", evidence_item["type"])
        self.assertEqual({"id", "kind", "ref", "captured_at", "work_state_ref"}, set(evidence_item["required"]))
        self.assertEqual(1, evidence_item["properties"]["id"]["minLength"])
        self.assertEqual({"command", "file", "diff", "test", "review", "other"}, set(evidence_item["properties"]["kind"]["enum"]))
        self.assertEqual(1, evidence_item["properties"]["ref"]["minLength"])
        self.assertEqual("date-time", evidence_item["properties"]["captured_at"]["format"])
        self.assertEqual(1, evidence_item["properties"]["work_state_ref"]["minLength"])
        self.assertFalse(evidence_item["additionalProperties"])
        self.assertEqual(1, schema["properties"]["checks_run"]["minItems"])
        self.assertFalse(schema["additionalProperties"])
        check_item = schema["properties"]["checks_run"]["items"]
        self.assertEqual({"name", "result", "evidence_ref", "work_state_ref"}, set(check_item["required"]))
        self.assertEqual(1, check_item["properties"]["name"]["minLength"])
        self.assertEqual({"passed", "failed", "skipped"}, set(check_item["properties"]["result"]["enum"]))
        self.assertEqual(1, check_item["properties"]["evidence_ref"]["minLength"])
        self.assertEqual(1, check_item["properties"]["work_state_ref"]["minLength"])
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
            "work_state_ref": {
                "id": "work-state:git:abc123",
                "kind": "git",
                "ref": "abc123",
                "captured_at": "2026-04-24T08:59:00Z",
                "status": "clean",
            },
            "evidence_refs": [
                {
                    "id": "evidence:validate-prodcraft-artifact-schema-registry",
                    "kind": "command",
                    "ref": "python3 scripts/validate_prodcraft.py --check artifact-schema-registry",
                    "captured_at": "2026-04-24T09:00:00Z",
                    "work_state_ref": "work-state:git:abc123",
                }
            ],
            "checks_run": [
                {
                    "name": "artifact-schema-registry",
                    "result": "passed",
                    "evidence_ref": "evidence:validate-prodcraft-artifact-schema-registry",
                    "work_state_ref": "work-state:git:abc123",
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
                        "evidence_ref": "evidence:validate-prodcraft-artifact-schema-registry",
                        "work_state_ref": "work-state:git:abc123",
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

    def test_verification_record_validator_rejects_stale_or_mismatched_completion_proof(self):
        valid_record = {
            "artifact": "verification-record",
            "schema_version": "verification-record.v1",
            "status": "accepted",
            "claim": "The artifact registry check passed.",
            "claim_scope": "artifact-schema-registry",
            "verified_at": "2026-04-24T09:01:00Z",
            "work_state_ref": {
                "id": "work-state:git:abc123",
                "kind": "git",
                "ref": "abc123",
                "captured_at": "2026-04-24T09:00:00Z",
                "status": "clean",
            },
            "evidence_refs": [
                {
                    "id": "evidence:validate-prodcraft-artifact-schema-registry",
                    "kind": "command",
                    "ref": "python3 scripts/validate_prodcraft.py --check artifact-schema-registry",
                    "captured_at": "2026-04-24T09:00:30Z",
                    "work_state_ref": "work-state:git:abc123",
                }
            ],
            "checks_run": [
                {
                    "name": "artifact-schema-registry",
                    "result": "passed",
                    "evidence_ref": "evidence:validate-prodcraft-artifact-schema-registry",
                    "work_state_ref": "work-state:git:abc123",
                }
            ],
            "passed": ["artifact-schema-registry"],
            "failed": [],
            "remaining_unverified": [],
            "claim_may_be_made": True,
        }

        errors: list[str] = []
        validate_verification_record_instance_contract(valid_record, "valid-record", errors)
        self.assertEqual([], errors)

        stale_record = {
            **valid_record,
            "evidence_refs": [
                {
                    **valid_record["evidence_refs"][0],
                    "captured_at": "2026-04-24T08:59:59Z",
                }
            ],
        }
        errors = []
        validate_verification_record_instance_contract(stale_record, "stale-record", errors)
        self.assertIn(
            "stale-record: accepted verification record evidence `evidence:validate-prodcraft-artifact-schema-registry` is older than work state `work-state:git:abc123`",
            errors,
        )

        mismatched_record = {
            **valid_record,
            "checks_run": [
                {
                    **valid_record["checks_run"][0],
                    "evidence_ref": "evidence:older-command",
                }
            ],
        }
        errors = []
        validate_verification_record_instance_contract(mismatched_record, "mismatched-record", errors)
        self.assertIn(
            "mismatched-record: check `artifact-schema-registry` references unknown evidence_ref `evidence:older-command`",
            errors,
        )

        mismatched_work_state_record = {
            **valid_record,
            "evidence_refs": [
                {
                    **valid_record["evidence_refs"][0],
                    "work_state_ref": "work-state:git:def456",
                }
            ],
        }
        errors = []
        validate_verification_record_instance_contract(
            mismatched_work_state_record, "mismatched-work-state-record", errors
        )
        self.assertIn(
            "mismatched-work-state-record: evidence `evidence:validate-prodcraft-artifact-schema-registry` binds to work_state_ref `work-state:git:def456` instead of current work state `work-state:git:abc123`",
            errors,
        )

        timezone_less_verified_record = {
            **valid_record,
            "verified_at": "2026-04-24T09:01:00",
        }
        errors = []
        validate_verification_record_instance_contract(
            timezone_less_verified_record, "timezone-less-verified-record", errors
        )
        self.assertIn(
            "timezone-less-verified-record: accepted verification record must include valid verified_at",
            errors,
        )

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
