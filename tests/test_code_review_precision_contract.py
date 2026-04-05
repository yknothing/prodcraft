from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class CodeReviewPrecisionContractTests(unittest.TestCase):
    def test_source_and_curated_skill_require_evidence_backed_blockers(self):
        source = (REPO_ROOT / "skills" / "05-quality" / "code-review" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        curated = (REPO_ROOT / "skills" / ".curated" / "code-review" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        for text in (source, curated):
            self.assertIn("Every blocking finding must be backed by evidence", text)
            self.assertIn("Do **not** report hypothetical regressions", text)
            self.assertIn("if a concern is only a plausible consequence of a blocker already reported", text)
            self.assertIn("Inventing blockers from suspicion alone", text)


if __name__ == "__main__":
    unittest.main()
