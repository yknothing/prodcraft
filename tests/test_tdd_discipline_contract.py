from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TDD_SKILL = REPO_ROOT / "skills" / "04-implementation" / "tdd" / "SKILL.md"


class TddDisciplineContractTests(unittest.TestCase):
    def test_tdd_skill_declares_iron_law_and_delete_means_delete(self):
        content = TDD_SKILL.read_text(encoding="utf-8")

        self.assertIn("## The Iron Law", content)
        self.assertIn("NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST", content)
        self.assertIn("delete it and start over from RED", content)
        self.assertIn("do not keep it as a \"reference\"", content)

    def test_tdd_skill_includes_rationalization_prevention_and_red_flags(self):
        content = TDD_SKILL.read_text(encoding="utf-8")

        self.assertIn("## Rationalization Prevention", content)
        self.assertIn("## Red Flags -- Stop and Start Over", content)
        self.assertIn("\"I'll write the tests after\"", content)
        self.assertIn("the next test will need it anyway", content)


if __name__ == "__main__":
    unittest.main()
