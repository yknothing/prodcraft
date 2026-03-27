from __future__ import annotations

import json
import unittest
from pathlib import Path

try:
    import jsonschema
except ImportError:  # pragma: no cover - dependency may be absent in some environments
    jsonschema = None

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
APPROVED_JUMPS = {
    ("04-implementation", "01-specification"),
    ("04-implementation", "02-architecture"),
    ("05-quality", "02-architecture"),
    ("07-operations", "02-architecture"),
    ("07-operations", "03-planning"),
    ("08-evolution", "01-specification"),
    ("08-evolution", "02-architecture"),
    ("08-evolution", "03-planning"),
}


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

    def test_course_correction_schema_declares_machine_enforced_jump_contract(self):
        schema = json.loads(
            (REPO_ROOT / "schemas" / "artifacts" / "course-correction-note.schema.json").read_text(encoding="utf-8")
        )
        properties = schema["properties"]
        self.assertIn("source_phase", properties)
        self.assertIn("target_phase", properties)
        self.assertIn("requires_user_reapproval", properties)
        self.assertFalse(schema["additionalProperties"])

        schema_pairs = {
            (
                option["properties"]["source_phase"]["const"],
                option["properties"]["target_phase"]["const"],
            )
            for option in schema["anyOf"]
        }
        self.assertEqual(APPROVED_JUMPS, schema_pairs)
        self.assertEqual(
            {source for source, _target in APPROVED_JUMPS},
            set(properties["source_phase"]["enum"]),
        )
        self.assertEqual(
            {target for _source, target in APPROVED_JUMPS},
            set(properties["target_phase"]["enum"]),
        )

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_schema_accepts_approved_pairs_and_rejects_unapproved_pairs(self):
        schema = json.loads(
            (REPO_ROOT / "schemas" / "artifacts" / "course-correction-note.schema.json").read_text(encoding="utf-8")
        )

        for source_phase, target_phase in sorted(APPROVED_JUMPS):
            payload = {
                "artifact": "course-correction-note",
                "schema_version": "course-correction-note.v1",
                "status": "approved",
                "source_phase": source_phase,
                "target_phase": target_phase,
                "trigger": "Contract mismatch discovered during downstream work.",
                "evidence_refs": ["docs/adr/example.md"],
                "blocked_artifact": "implementation-plan",
                "preserved_constraints": ["Existing API surface remains frozen."],
                "recommended_next_skill": "system-design",
                "severity": "high",
                "requires_user_reapproval": True,
            }
            with self.subTest(source_phase=source_phase, target_phase=target_phase):
                jsonschema.validate(payload, schema)

        invalid_pair = {
            "artifact": "course-correction-note",
            "schema_version": "course-correction-note.v1",
            "status": "approved",
            "source_phase": "03-planning",
            "target_phase": "00-discovery",
            "trigger": "Invalid jump",
            "evidence_refs": ["docs/adr/example.md"],
            "blocked_artifact": "implementation-plan",
            "preserved_constraints": ["Existing API surface remains frozen."],
            "recommended_next_skill": "intake",
            "severity": "high",
            "requires_user_reapproval": True,
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(invalid_pair, schema)


if __name__ == "__main__":
    unittest.main()
