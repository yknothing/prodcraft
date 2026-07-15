from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_prodcraft.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_prodcraft_gateway_tokens", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class GatewayReferenceTokenTests(unittest.TestCase):
    def test_planned_pc_name_does_not_match_ordinary_english_word(self):
        validator = load_validator()

        self.assertEqual([], validator._skill_name_occurrences("pc-deprecation", "deprecation policy"))
        self.assertEqual([], validator._skill_name_occurrences("pc-deprecation", "pre-pc-deprecation"))

    def test_complete_pc_name_is_still_detected_with_or_without_backticks(self):
        validator = load_validator()

        for line in ("Use pc-deprecation (planned).", "Use `pc-deprecation` (planned)."):
            matches = validator._skill_name_occurrences("pc-deprecation", line)
            self.assertEqual(1, len(matches))
            self.assertTrue(validator._occurrence_has_marker(line, matches[0]))


if __name__ == "__main__":
    unittest.main()

