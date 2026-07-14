from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "prodcraft_gateway_skill.py"


def load_module():
    spec = importlib.util.spec_from_file_location("prodcraft_gateway_skill", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ProdcraftGatewayLocatorContractTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_global_gateway_skill_points_to_repo_locator_and_warns_about_singleton_directory(self):
        content = self.module.render_prodcraft_skill(REPO_ROOT, install_surface="global")

        self.assertNotIn(str(REPO_ROOT), content)
        self.assertIn("read `prodcraft-runtime.json` beside this file", content)
        self.assertIn("the `gateway_path` recorded in `prodcraft-runtime.json`", content)
        self.assertIn("locator's `canonical_repo_root`", content)
        self.assertIn(
            "A `pc-prodcraft` directory that contains only this `SKILL.md` is a valid gateway install",
            content,
        )
        self.assertIn("Do not search for downstream skills inside the `pc-prodcraft` directory", content)
        self.assertIn("Do not recursively search arbitrary parent directories or run shell commands", content)

    def test_curated_gateway_skill_uses_sibling_or_source_repo_resolution_without_local_paths(self):
        content = self.module.render_prodcraft_skill(REPO_ROOT, install_surface="curated")

        self.assertIn("source repository", content)
        self.assertIn("Look for sibling skill packages beside `pc-prodcraft`", content)
        self.assertIn("partial entry install", content)
        self.assertIn("This is partial-entry guidance, not a completed Prodcraft workflow or evidence gate.", content)
        self.assertIn(
            "do not claim that downstream skills such as `pc-code-review`, `pc-testing-strategy`, or `pc-security-audit` ran",
            content,
        )
        self.assertIn("if the quality target context is missing", content)
        self.assertIn("runtime_context", content)
        self.assertIn("exposure_profile", content)
        self.assertIn("do not assume public HTTP service", content)
        self.assertNotIn(str(REPO_ROOT), content)


if __name__ == "__main__":
    unittest.main()
