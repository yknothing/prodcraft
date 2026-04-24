from __future__ import annotations

import re
import unittest
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLAN_DIR = REPO_ROOT / "docs" / "plans" / "architecture-evolution"
MATRIX = PLAN_DIR / "2026-04-24-ar-01-enforcement-promotion-matrix.md"
CONNECTED_PLAN = PLAN_DIR / "2026-04-24-connected-architecture-evolution-plan.md"
PROTOCOL = (
    REPO_ROOT
    / "docs"
    / "architecture"
    / "ar-01-enforcement-promotion-measurement-protocol.md"
)

INDEX_ID_RE = re.compile(r"^\| (AR01-C\d{2}) \|", re.MULTILINE)
RECORD_HEADING_RE = re.compile(r"^### (AR01-C\d{2}): .+$", re.MULTILINE)
REVIEW_DATE_RE = re.compile(r"^- Review date: (\d{4}-\d{2}-\d{2})\.$", re.MULTILINE)

REQUIRED_FIELDS = (
    "Rule or discipline name",
    "Current home",
    "Failure mode",
    "Observed evidence source",
    "Failure frequency estimate",
    "Cost if missed",
    "Checkability",
    "Goodhart risk",
    "Recommended next move",
    "Recommended surface",
    "Owner",
    "Evidence source class",
    "Sample window",
    "False-positive risk",
    "False-negative risk",
    "Friction cost",
    "Decision owner",
    "Review date",
    "Semantic boundary",
)

MINIMUM_SECURITY_CONTROLS = {
    "Prompt injection authority boundaries are explicit",
    "Command safety requires explicit scope and approval basis",
    "External skill ideas must be re-expressed as local contracts",
    "Dynamic remote instruction imports are prohibited unless reviewed locally",
    "Secrets and PII must not leak into artifacts or logs",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def index_ids(content: str) -> list[str]:
    return INDEX_ID_RE.findall(content)


def measurement_records(content: str) -> dict[str, str]:
    matches = list(RECORD_HEADING_RE.finditer(content))
    records: dict[str, str] = {}
    promotion_groups_start = content.find("\n## Promotion Groups")

    for index, match in enumerate(matches):
        next_start = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else promotion_groups_start
        )
        records[match.group(1)] = content[match.start() : next_start]

    return records


class ArchitectureEvolutionAR01MatrixTests(unittest.TestCase):
    def test_matrix_declares_planning_boundary(self):
        content = read(MATRIX)

        self.assertIn("not canonical architecture policy", content)
        self.assertIn("not an ADR", content)
        self.assertIn("not an enforcement contract", content)
        self.assertIn("## Source Documents", content)
        self.assertIn("## Non-Goals", content)
        self.assertIn("## Authority Boundary", content)
        self.assertIn("## Validation Expectations", content)
        self.assertIn("## Graduation Path", content)
        self.assertIn("## Explicit Non-Claims", content)

    def test_connected_plan_and_protocol_point_to_matrix_contract(self):
        plan = read(CONNECTED_PLAN)
        protocol = read(PROTOCOL)

        self.assertIn(MATRIX.name, plan)
        self.assertIn("initial provisional matrix exists", plan)
        for field in REQUIRED_FIELDS[:-1]:
            self.assertIn(f"| {field} |", protocol)

    def test_decision_index_and_records_are_unique_and_aligned(self):
        content = read(MATRIX)
        ids = index_ids(content)
        records = measurement_records(content)

        self.assertGreaterEqual(len(ids), 17)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids, list(records))

    def test_each_record_has_required_measurement_fields(self):
        records = measurement_records(read(MATRIX))

        for control_id, record in records.items():
            with self.subTest(control_id=control_id):
                for field in REQUIRED_FIELDS:
                    self.assertIn(f"- {field}:", record)

    def test_security_candidate_set_is_present_but_not_overpromoted(self):
        content = read(MATRIX)

        for control in MINIMUM_SECURITY_CONTROLS:
            with self.subTest(control=control):
                self.assertIn(control, content)

        self.assertIn("Keep evidence-led or protocol-led for now", content)
        self.assertIn("AR01-C13", content)
        self.assertIn("AR01-C14", content)
        self.assertIn("AR01-C15", content)
        self.assertIn("AR01-C17", content)

    def test_non_claims_block_authority_drift(self):
        content = read(MATRIX)

        self.assertIn("This matrix does not prove semantic adequacy.", content)
        self.assertIn("does not assert that any control is enforced", content)
        self.assertIn("does not make a host adapter authoritative", content)
        self.assertIn("does not promote any public skill to `portable_as_is`", content)
        self.assertIn("should not be wired into `scripts/validate_prodcraft.py`", content)

    def test_review_dates_are_iso_dates_for_each_record(self):
        content = read(MATRIX)
        records = measurement_records(content)
        review_dates = REVIEW_DATE_RE.findall(content)

        self.assertEqual(len(review_dates), len(records))
        for value in review_dates:
            with self.subTest(review_date=value):
                self.assertEqual(date.fromisoformat(value).isoformat(), value)


if __name__ == "__main__":
    unittest.main()
