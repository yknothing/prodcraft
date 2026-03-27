from __future__ import annotations

import json
import unittest
from pathlib import Path

try:
    import jsonschema
except ImportError:  # pragma: no cover - dependency may be absent in some environments
    jsonschema = None


REPO_ROOT = Path(__file__).resolve().parents[1]


class LanguageBoundaryContractTests(unittest.TestCase):
    def load_schema(self, artifact_name: str) -> dict:
        schema_path = REPO_ROOT / "schemas" / "artifacts" / f"{artifact_name}.schema.json"
        return json.loads(schema_path.read_text(encoding="utf-8"))

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_problem_frame_and_requirements_doc_reject_invalid_language_boundary_values(self):
        problem_frame = {
            "artifact": "problem-frame",
            "schema_version": "problem-frame.v1",
            "status": "approved",
            "source_language": "mixed",
            "artifact_record_language": "en",
            "user_presentation_locale": "zh",
            "problem_statement": "Clarify the problem before spec work starts.",
            "recommended_option": "Option 1",
            "next_skill_to_invoke": "requirements-engineering",
        }
        requirements_doc = {
            "artifact": "requirements-doc",
            "schema_version": "requirements-doc.v1",
            "status": "approved",
            "source_language": "mixed",
            "artifact_record_language": "en",
            "user_presentation_locale": "zh",
            "requirements": ["The system shall preserve bilingual acceptance context."],
            "acceptance_summary": "Acceptance criteria normalized into canonical English requirements.",
        }

        jsonschema.validate(problem_frame, self.load_schema("problem-frame"))
        jsonschema.validate(requirements_doc, self.load_schema("requirements-doc"))

        invalid_payloads = (
            ("problem-frame", {**problem_frame, "source_language": "fr"}),
            ("problem-frame", {**problem_frame, "artifact_record_language": "zh"}),
            ("requirements-doc", {**requirements_doc, "user_presentation_locale": "fr"}),
            ("requirements-doc", {**requirements_doc, "artifact_record_language": "zh"}),
        )
        for artifact_name, payload in invalid_payloads:
            with self.subTest(artifact=artifact_name, payload=payload):
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.validate(payload, self.load_schema(artifact_name))


if __name__ == "__main__":
    unittest.main()
