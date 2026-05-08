from __future__ import annotations

import json
import unittest
from pathlib import Path

try:
    import jsonschema
except ImportError:  # pragma: no cover - environment guard
    jsonschema = None


REPO_ROOT = Path(__file__).resolve().parents[1]


class QualityTargetContextContractTests(unittest.TestCase):
    def test_gateway_and_phase_require_quality_target_context(self):
        gateway = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")
        phase = (REPO_ROOT / "skills" / "05-quality" / "_phase.md").read_text(
            encoding="utf-8"
        )

        for text in (gateway, phase):
            self.assertIn("quality_target_context", text)
            self.assertIn("runtime_context", text)
            self.assertIn("exposure_profile", text)
            self.assertIn("production_target", text)
            self.assertIn("non_targets", text)
            self.assertIn("evidence_refs", text)
            self.assertIn("Do not assume public HTTP service", text)

    def test_source_and_curated_quality_skills_calibrate_agent_internal_targets(self):
        skill_names = ("code-review", "security-audit", "testing-strategy")

        for skill_name in skill_names:
            with self.subTest(skill=skill_name, surface="source"):
                source = (
                    REPO_ROOT / "skills" / "05-quality" / skill_name / "SKILL.md"
                ).read_text(encoding="utf-8")
                self.assertIn("quality_target_context", source)
                self.assertIn("agent-internal skill", source)
                self.assertIn("public HTTP service", source)

            with self.subTest(skill=skill_name, surface="curated"):
                curated = (
                    REPO_ROOT / "skills" / ".curated" / skill_name / "SKILL.md"
                ).read_text(encoding="utf-8")
                self.assertIn("quality_target_context", curated)
                self.assertIn("agent-internal skill", curated)
                self.assertIn("public HTTP service", curated)

    def test_intake_schema_accepts_agent_internal_quality_target(self):
        if jsonschema is None:
            self.skipTest("jsonschema is not installed")

        schema = json.loads(
            (REPO_ROOT / "schemas" / "artifacts" / "intake-brief.schema.json").read_text(
                encoding="utf-8"
            )
        )
        payload = {
            "artifact": "intake-brief",
            "schema_version": "intake-brief.v1",
            "status": "approved",
            "request_summary": "Review an agent-internal chatbot skill implementation",
            "source_language": "en",
            "artifact_record_language": "en",
            "user_presentation_locale": "zh",
            "intake_mode": "fast-track",
            "work_type": "Enhancement",
            "entry_phase": "05-quality",
            "quality_target_context": {
                "runtime_context": "agent_internal_skill",
                "exposure_profile": "no_network_listener",
                "production_target": "Agent runtime skill invoked by an agent",
                "non_targets": ["Public SaaS API", "browser-facing service"],
                "evidence_refs": ["user screenshot", "repository files"],
            },
            "scope_assessment": "medium",
            "recommended_next_skill": "code-review",
            "routing_rationale": "The implementation is complete and needs calibrated quality review.",
            "key_risks": ["Overbuilding service controls or under-checking agent boundaries."],
            "questions_asked": [],
            "routing_changed_by_answers": False,
            "approver": "user",
        }

        jsonschema.validate(payload, schema)

        missing_context = dict(payload)
        missing_context.pop("quality_target_context")
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(missing_context, schema)

    def test_bug_record_preserves_safety_boundary(self):
        record = (
            REPO_ROOT / "docs" / "quality" / "2026-05-08-quality-target-context-bug.md"
        ).read_text(encoding="utf-8")

        self.assertIn("agent-internal skill", record)
        self.assertIn("quality_target_context", record)
        self.assertIn("This fix does not create an internal-skill bypass", record)
        self.assertIn("Public services", record)
        self.assertIn("secrets and PII", record)


if __name__ == "__main__":
    unittest.main()
