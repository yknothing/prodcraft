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
INTAKE_SKILL_PATH = REPO_ROOT / "skills" / "00-discovery" / "intake" / "SKILL.md"
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
            {"en", "zh", "mixed"},
            set(self.schema["properties"]["source_language"]["enum"]),
        )
        self.assertEqual(
            "en",
            self.schema["properties"]["artifact_record_language"]["const"],
        )
        self.assertEqual(
            {"en", "zh"},
            set(self.schema["properties"]["user_presentation_locale"]["enum"]),
        )

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
            "workflow_primary": "agile-sprint",
            "scope_assessment": "medium",
            "recommended_next_skill": "requirements-engineering",
            "routing_rationale": "Feature work in an existing product starts in specification.",
            "key_risks": ["Approval thresholds may be ambiguous."],
            "questions_asked": ["Does this affect an existing system?"],
            "routing_changed_by_answers": True,
            "approver": "user",
        }

        jsonschema.validate(valid_full_payload, self.schema)

        valid_fast_track_payload = {
            **valid_full_payload,
            "intake_mode": "fast-track",
            "work_type": "Bug Fix",
            "entry_phase": "04-implementation",
            "scope_assessment": "small",
        }
        valid_fast_track_payload.pop("workflow_primary")

        jsonschema.validate(valid_fast_track_payload, self.schema)

        invalid_cases = (
            ("work_type", "New Feture"),
            ("entry_phase", "whatever"),
            ("workflow_primary", "kanban"),
            ("source_language", "fr"),
            ("user_presentation_locale", "fr"),
        )
        for field_name, invalid_value in invalid_cases:
            payload = dict(valid_full_payload)
            payload[field_name] = invalid_value
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
