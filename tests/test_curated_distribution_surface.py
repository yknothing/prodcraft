from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "export_curated_skills.py"
CURATED_DIR = REPO_ROOT / "skills" / ".curated"


def load_module():
    spec = importlib.util.spec_from_file_location("export_curated_skills", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CuratedDistributionSurfaceTests(unittest.TestCase):
    def test_curated_surface_contains_core_public_skills(self):
        index = json.loads((CURATED_DIR / "index.json").read_text(encoding="utf-8"))
        exported_names = {entry["name"] for entry in index["skills"]}

        self.assertIn("prodcraft", exported_names)
        self.assertIn("intake", exported_names)
        self.assertIn("code-review", exported_names)
        self.assertIn("incident-response", exported_names)

        for skill_name in exported_names:
            self.assertTrue((CURATED_DIR / skill_name / "SKILL.md").exists())

    def test_export_script_can_materialize_surface_into_temp_directory(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir)
            result = module.export_curated_skills(repo_root=REPO_ROOT, output_root=output_root)

            self.assertIn("prodcraft", result["skills"])
            self.assertTrue((output_root / "prodcraft" / "SKILL.md").exists())
            self.assertTrue((output_root / "intake" / "SKILL.md").exists())

    def test_exported_skills_do_not_have_dangling_packaged_references(self):
        for skill_path in CURATED_DIR.glob("*/SKILL.md"):
            text = skill_path.read_text(encoding="utf-8")
            for marker in ("references/", "scripts/", "assets/"):
                for fragment in [part.split(")", 1)[0] for part in text.split(f"({marker}")[1:]]:
                    self.assertTrue((skill_path.parent / marker / fragment).exists(), f"{skill_path} -> {marker}{fragment}")


if __name__ == "__main__":
    unittest.main()
