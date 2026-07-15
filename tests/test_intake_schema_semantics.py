from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

import yaml

try:
    import jsonschema
except ImportError:  # pragma: no cover - environment guard
    jsonschema = None


REPO_ROOT = Path(__file__).resolve().parents[1]
INTAKE_SKILL_PATH = REPO_ROOT / "skills" / "00-discovery" / "pc-intake" / "SKILL.md"
INTAKE_SCHEMA_PATH = REPO_ROOT / "schemas" / "artifacts" / "intake-brief.schema.json"
WORKFLOWS_DIR = REPO_ROOT / "workflows"
MANIFEST_PATH = REPO_ROOT / "manifest.yml"


def load_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError(f"{path} is missing valid YAML frontmatter")
    return yaml.safe_load(parts[1]) or {}, parts[2]


def extract_intake_work_types() -> list[str]:
    _frontmatter, body = load_frontmatter(INTAKE_SKILL_PATH)
    match = re.search(
        r"### Step 2: Classify Work Type\s*(?P<section>.*?)\n### Step 3: Ask Clarifying Questions",
        body,
        re.DOTALL,
    )
    if not match:
        raise AssertionError("could not find Step 2 work type section")

    work_types: list[str] = []
    for line in match.group("section").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        columns = [item.strip() for item in stripped.split("|")[1:-1]]
        if len(columns) != 5 or columns[0] in {"Type", "------"}:
            continue
        work_type = columns[0].replace("**", "").strip()
        if work_type and set(work_type) != {"-"}:
            work_types.append(work_type)
    return work_types


def extract_primary_workflows() -> set[str]:
    primary: set[str] = set()
    for path in sorted(WORKFLOWS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        frontmatter, _body = load_frontmatter(path)
        if frontmatter.get("workflow_kind") == "primary":
            primary.add(frontmatter["name"])
    return primary


def extract_overlay_workflows() -> set[str]:
    overlays: set[str] = set()
    for path in sorted(WORKFLOWS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        frontmatter, _body = load_frontmatter(path)
        if frontmatter.get("workflow_kind") == "overlay":
            overlays.add(frontmatter["name"])
    return overlays


class IntakeSchemaSemanticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = json.loads(INTAKE_SCHEMA_PATH.read_text(encoding="utf-8"))
        self.manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_work_type_enum_matches_intake_taxonomy(self):
        expected = set(extract_intake_work_types())
        actual = set(self.schema["properties"]["work_type"]["enum"])
        self.assertEqual(expected, actual)

    def test_entry_phase_enum_matches_manifest_phases_plus_cross_cutting(self):
        expected = {phase["id"] for phase in self.manifest["phases"]}
        expected.add("cross-cutting")
        actual = set(self.schema["properties"]["entry_phase"]["enum"])
        self.assertEqual(expected, actual)

    def test_language_boundary_fields_match_repo_policy(self):
        self.assertEqual(
            [
                {"type": "string", "pattern": "^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$"},
                {"const": "mixed"},
            ],
            self.schema["properties"]["source_language"]["oneOf"],
        )
        self.assertEqual(
            "en",
            self.schema["properties"]["artifact_record_language"]["const"],
        )
        self.assertEqual(
            "^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$",
            self.schema["properties"]["user_presentation_locale"]["pattern"],
        )

    def test_runtime_boundary_fields_define_quality_calibration_axis(self):
        quality_target = self.schema["properties"]["quality_target_context"]

        self.assertEqual(
            {
                "agent_internal_skill",
                "host_runtime_tool",
                "local_dev_harness",
                "internal_service",
                "public_service",
                "unknown",
            },
            set(quality_target["properties"]["runtime_context"]["enum"]),
        )
        self.assertEqual(
            {
                "no_network_listener",
                "localhost_only",
                "private_network",
                "public_internet",
                "unknown",
            },
            set(quality_target["properties"]["exposure_profile"]["enum"]),
        )
        self.assertEqual(
            {
                "runtime_context",
                "exposure_profile",
                "production_target",
                "non_targets",
                "evidence_refs",
            },
            set(quality_target["required"]),
        )
        self.assertFalse(quality_target["additionalProperties"])

    def test_workflow_primary_enum_matches_primary_workflows(self):
        expected = extract_primary_workflows()
        actual = set(self.schema["properties"]["workflow_primary"]["enum"])
        self.assertEqual(expected, actual)

    def test_workflow_overlay_enum_matches_overlay_workflows(self):
        expected = extract_overlay_workflows()
        actual = set(self.schema["properties"]["workflow_overlays"]["items"]["enum"])
        self.assertEqual(expected, actual)

    def test_schema_rejects_invalid_routing_values(self):
        if jsonschema is None:
            self.skipTest("jsonschema is not installed")

        valid_full_payload = {
            "artifact": "intake-brief",
            "schema_version": "intake-brief.v1",
            "status": "approved",
            "request_summary": "Add first-release approvals workflow",
            "source_language": "en",
            "artifact_record_language": "en",
            "user_presentation_locale": "zh",
            "intake_mode": "full",
            "work_type": "New Feature",
            "entry_phase": "01-specification",
            "quality_target_context": {
                "runtime_context": "internal_service",
                "exposure_profile": "private_network",
                "production_target": "Internal approval workflow",
                "non_targets": ["Public SaaS API"],
                "evidence_refs": ["architecture-doc"],
            },
            "workflow_primary": "agile-sprint",
            "scope_assessment": "medium",
            "recommended_next_skill": "pc-requirements-engineering",
            "routing_rationale": "Feature work in an existing product starts in specification.",
            "key_risks": ["Approval thresholds may be ambiguous."],
            "questions_asked": ["Does this affect an existing system?"],
            "routing_changed_by_answers": True,
            "approver": "user",
        }

        jsonschema.validate(valid_full_payload, self.schema)
        jsonschema.validate(
            {
                **valid_full_payload,
                "source_language": "fr-FR",
                "user_presentation_locale": "fr",
            },
            self.schema,
        )

        valid_fast_track_payload = {
            **valid_full_payload,
            "intake_mode": "fast-track",
            "work_type": "Bug Fix",
            "entry_phase": "04-implementation",
            "scope_assessment": "small",
        }
        valid_fast_track_payload.pop("workflow_primary")

        jsonschema.validate(valid_fast_track_payload, self.schema)

        # Micro mode omits workflow_primary like fast-track and may carry the
        # optional structured proposed_path.
        valid_micro_payload = {
            **valid_fast_track_payload,
            "intake_mode": "micro",
            "work_type": "Documentation",
            "entry_phase": "cross-cutting",
            "approver": "auto (micro policy)",
            "questions_asked": [],
            "routing_changed_by_answers": False,
            "quality_target_context": {
                **valid_fast_track_payload["quality_target_context"],
                "runtime_context": "agent_internal_skill",
                "exposure_profile": "no_network_listener",
            },
            "proposed_path": ["pc-documentation"],
            "micro_eligibility": {
                "single_revert": True,
                "zero_questions": True,
                "no_external_effect": True,
                "no_security_impact": True,
                "no_irreversible_action": True,
            },
        }
        jsonschema.validate(valid_micro_payload, self.schema)

        with self.assertRaises(jsonschema.ValidationError, msg="micro eligibility is required"):
            payload = dict(valid_micro_payload)
            payload.pop("micro_eligibility")
            jsonschema.validate(payload, self.schema)

        for invalid_patch in (
            {"scope_assessment": "medium"},
            {"status": "draft"},
            {"approver": "user"},
            {"workflow_primary": "agile-sprint"},
        ):
            with self.assertRaises(jsonschema.ValidationError, msg=str(invalid_patch)):
                jsonschema.validate({**valid_micro_payload, **invalid_patch}, self.schema)

        for eligibility_field in valid_micro_payload["micro_eligibility"]:
            payload = dict(valid_micro_payload)
            payload["micro_eligibility"] = dict(payload["micro_eligibility"])
            payload["micro_eligibility"][eligibility_field] = False
            with self.assertRaises(jsonschema.ValidationError, msg=eligibility_field):
                jsonschema.validate(payload, self.schema)

        contradictory_micro_patches = (
            {"questions_asked": ["Should this touch production?"]},
            {"routing_changed_by_answers": True},
            {"work_type": "Hotfix"},
            {
                "quality_target_context": {
                    **valid_micro_payload["quality_target_context"],
                    "runtime_context": "public_service",
                }
            },
            {
                "quality_target_context": {
                    **valid_micro_payload["quality_target_context"],
                    "exposure_profile": "public_internet",
                }
            },
        )
        for invalid_patch in contradictory_micro_patches:
            with self.assertRaises(jsonschema.ValidationError, msg=str(invalid_patch)):
                jsonschema.validate({**valid_micro_payload, **invalid_patch}, self.schema)

        with self.assertRaises(jsonschema.ValidationError, msg="non-micro must omit micro eligibility"):
            jsonschema.validate(
                {**valid_fast_track_payload, "micro_eligibility": valid_micro_payload["micro_eligibility"]},
                self.schema,
            )

        invalid_cases = (
            ("work_type", "New Feture"),
            ("entry_phase", "whatever"),
            ("workflow_primary", "kanban"),
            ("source_language", "not_a_locale"),
            ("source_language", "not a tag!"),
            ("user_presentation_locale", "not_a_locale"),
            ("user_presentation_locale", "mixed"),
        )
        for field_name, invalid_value in invalid_cases:
            payload = dict(valid_full_payload)
            payload[field_name] = invalid_value
            with self.assertRaises(jsonschema.ValidationError, msg=field_name):
                jsonschema.validate(payload, self.schema)

        for field_name, invalid_value in (
            ("runtime_context", "public_api_shape"),
            ("exposure_profile", "probably_public"),
        ):
            payload = dict(valid_full_payload)
            payload["quality_target_context"] = dict(payload["quality_target_context"])
            payload["quality_target_context"][field_name] = invalid_value
            with self.assertRaises(jsonschema.ValidationError, msg=field_name):
                jsonschema.validate(payload, self.schema)

        with self.assertRaises(jsonschema.ValidationError, msg="artifact_record_language"):
            jsonschema.validate({**valid_full_payload, "artifact_record_language": "zh"}, self.schema)

        with self.assertRaises(jsonschema.ValidationError, msg="unexpected property"):
            jsonschema.validate({**valid_full_payload, "unexpected": "value"}, self.schema)

        with self.assertRaises(jsonschema.ValidationError, msg="full route requires workflow_primary"):
            payload = dict(valid_full_payload)
            payload.pop("workflow_primary")
            jsonschema.validate(payload, self.schema)

        with self.assertRaises(jsonschema.ValidationError, msg="resume route requires workflow_primary"):
            payload = dict(valid_full_payload)
            payload["intake_mode"] = "resume"
            payload.pop("workflow_primary")
            jsonschema.validate(payload, self.schema)

        with self.assertRaises(jsonschema.ValidationError, msg="empty overlay list must be omitted"):
            jsonschema.validate({**valid_full_payload, "workflow_overlays": []}, self.schema)

        with self.assertRaises(jsonschema.ValidationError, msg="invalid overlay"):
            jsonschema.validate({**valid_full_payload, "workflow_overlays": ["legacy-mode"]}, self.schema)


if __name__ == "__main__":
    unittest.main()
