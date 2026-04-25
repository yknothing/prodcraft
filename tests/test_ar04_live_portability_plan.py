from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLAN = (
    REPO_ROOT
    / "docs"
    / "plans"
    / "architecture-evolution"
    / "2026-04-25-ar-04-live-portability-benchmark-plan.md"
)

REQUIRED_MATRIX_FIELDS = (
    "Model/runtime",
    "Prompt",
    "Full-repo output path",
    "Curated-only output path",
    "Overclaim finding",
    "Handoff preservation score",
    "Route correctness score",
    "Caveat decision",
)

REQUIRED_PROBES = (
    "AR04-P01",
    "AR04-P02",
    "AR04-P03",
    "AR04-P04",
    "AR04-P05",
)


def read_plan() -> str:
    return PLAN.read_text(encoding="utf-8")


def normalized(content: str) -> str:
    return " ".join(content.split())


class AR04LivePortabilityPlanTests(unittest.TestCase):
    def test_plan_declares_non_canonical_boundary(self):
        content = read_plan()

        self.assertIn("non-canonical planning artifact", content)
        self.assertIn("not architecture policy", content)
        self.assertIn("not an ADR", content)
        self.assertIn("not a distribution registry", content)
        self.assertIn("not a portability classification update", content)

    def test_probe_matrix_contains_required_fields_and_first_batch(self):
        content = read_plan()

        for field in REQUIRED_MATRIX_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, content)

        for probe_id in REQUIRED_PROBES:
            with self.subTest(probe_id=probe_id):
                self.assertIn(probe_id, content)

        self.assertIn("intake/start", content)
        self.assertIn("completion claim", content)
        self.assertIn("code-review", content)
        self.assertIn("course-correction/ops", content)
        self.assertIn("public install self-description", content)

    def test_no_promotion_rule_requires_live_curated_only_evidence(self):
        content = read_plan()

        self.assertIn("No-Promotion Rule", content)
        self.assertIn("No exported skill may be upgraded to `portable_as_is`", content)
        self.assertIn("live curated-only evidence", content)
        self.assertIn("Until that evidence exists, `portable_with_caveat` remains", content)

    def test_observability_keeps_exact_usage_separate_from_estimates(self):
        content = read_plan()
        flat_content = normalized(content)

        self.assertIn("usage_precision: exact", content)
        self.assertIn("estimated/advisory bucket", content)
        self.assertIn("estimated_token_branch_deltas_advisory", content)
        self.assertIn("skill_context.measured", content)
        self.assertIn("char and byte counts are context-size evidence", content)
        self.assertIn(
            "They may show how much skill material was loaded or deferred, but they are not "
            "token savings unless a model-specific tokenizer or provider token-count API "
            "produced exact token counts.",
            flat_content,
        )
        self.assertIn("This plan does not make estimated usage exact.", content)
        self.assertIn("This plan does not turn context-size char/byte savings into token savings.", content)

    def test_plan_does_not_instruct_registry_or_curated_surface_changes(self):
        content = read_plan()

        self.assertIn("Do not modify `schemas/distribution/public-skill-portability.json`", content)
        self.assertIn("Do not modify `skills/.curated/index.json`", content)
        self.assertIn("The result does not modify distribution registry classification", content)


if __name__ == "__main__":
    unittest.main()
