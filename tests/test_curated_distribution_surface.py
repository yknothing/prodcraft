from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "export_curated_skills.py"
CURATED_DIR = REPO_ROOT / "skills" / ".curated"
MARKDOWN_RELATIVE_REFERENCE_RE = re.compile(r"!?\[[^\]]*\]\((?P<target>[^)\s]+)\)")


def load_module():
    spec = importlib.util.spec_from_file_location("export_curated_skills", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CuratedDistributionSurfaceTests(unittest.TestCase):
    def snapshot_file_tree(self, root: Path) -> dict[str, bytes]:
        return {
            str(path.relative_to(root)): path.read_bytes()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def assert_packaged_skill_surface_is_loadable(self, root: Path) -> None:
        module = load_module()

        for skill_path in sorted(root.glob("*/SKILL.md")):
            frontmatter, body = module.load_frontmatter(skill_path)
            self.assertIsInstance(frontmatter, dict, skill_path)
            self.assertEqual(skill_path.parent.name, frontmatter.get("name"), skill_path)

            description = frontmatter.get("description")
            self.assertIsInstance(description, str, skill_path)
            self.assertGreater(len(description), 0, skill_path)
            self.assertLessEqual(len(description), 1024, skill_path)

            for match in MARKDOWN_RELATIVE_REFERENCE_RE.finditer(body):
                target = match.group("target")
                if target.startswith(("#", "/", "http://", "https://", "mailto:")):
                    continue
                target_path = skill_path.parent / target.split("#", 1)[0]
                self.assertTrue(target_path.exists(), f"{skill_path} -> {target}")

    def test_curated_surface_contains_core_public_skills(self):
        index = json.loads((CURATED_DIR / "index.json").read_text(encoding="utf-8"))
        exported_names = {entry["name"] for entry in index["skills"]}

        self.assertIn("prodcraft", exported_names)
        self.assertIn("intake", exported_names)
        self.assertIn("code-review", exported_names)
        self.assertIn("incident-response", exported_names)
        self.assertIn("verification-before-completion", exported_names)
        self.assertIn("delivery-completion", exported_names)
        self.assertIn("acceptance-criteria", exported_names)

        for skill_name in exported_names:
            self.assertTrue((CURATED_DIR / skill_name / "SKILL.md").exists())

        for entry in index["skills"]:
            self.assertIn("stability", entry, entry["name"])
            self.assertIn("readiness", entry, entry["name"])
            self.assertIn("portability", entry, entry["name"])
            self.assertIn(entry["portability"], {"portable_as_is", "portable_with_caveat"}, entry["name"])
            if entry["portability"] == "portable_with_caveat":
                self.assertIn("public_caveat_text", entry, entry["name"])
                self.assertGreater(len(entry["public_caveat_text"]), 0, entry["name"])

    def test_export_script_can_materialize_surface_into_temp_directory(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir)
            result = module.export_curated_skills(repo_root=REPO_ROOT, output_root=output_root)

            self.assertIn("prodcraft", result["skills"])
            self.assertTrue((output_root / "prodcraft" / "SKILL.md").exists())
            self.assertTrue((output_root / "intake" / "SKILL.md").exists())
            self.assertEqual(self.snapshot_file_tree(output_root), self.snapshot_file_tree(CURATED_DIR))

    def test_exported_surface_rewrites_lifecycle_links_for_flattened_packages(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir)
            module.export_curated_skills(repo_root=REPO_ROOT, output_root=output_root)

            system_design = (output_root / "system-design" / "SKILL.md").read_text(encoding="utf-8")
            problem_framing = (output_root / "problem-framing" / "SKILL.md").read_text(encoding="utf-8")

            self.assertIn("[spec-writing](../spec-writing/SKILL.md)", system_design)
            self.assertNotIn("../../01-specification/spec-writing/SKILL.md", system_design)
            self.assertIn("`market-analysis`", problem_framing)
            self.assertNotRegex(problem_framing, r"\[market-analysis\]\([^)]+SKILL\.md\)")

    def test_exported_surface_has_loadable_frontmatter_and_no_dangling_relative_references(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir)
            module.export_curated_skills(repo_root=REPO_ROOT, output_root=output_root)

            self.assert_packaged_skill_surface_is_loadable(output_root)

    def test_exported_skills_do_not_have_dangling_packaged_references(self):
        for skill_path in CURATED_DIR.glob("*/SKILL.md"):
            text = skill_path.read_text(encoding="utf-8")
            for marker in ("references/", "scripts/", "assets/"):
                for fragment in [part.split(")", 1)[0] for part in text.split(f"({marker}")[1:]]:
                    self.assertTrue((skill_path.parent / marker / fragment).exists(), f"{skill_path} -> {marker}{fragment}")

    def test_curated_prodcraft_skill_marks_default_software_entry_behavior(self):
        content = (CURATED_DIR / "prodcraft" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("default entry system for software-development tasks", content)
        self.assertIn("skipping Prodcraft preserves the same lifecycle guarantees", content)

    def test_curated_prodcraft_skill_defends_gateway_self_location_boundary(self):
        content = (CURATED_DIR / "prodcraft" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn(
            "A `prodcraft` directory that contains only this `SKILL.md` is a valid gateway install",
            content,
        )
        self.assertIn("Look for sibling skill packages beside `prodcraft`", content)
        self.assertIn(
            "do not claim that downstream skills such as `code-review`, `testing-strategy`, or `security-audit` ran",
            content,
        )
        self.assertIn("This is partial-entry guidance, not a completed Prodcraft workflow or evidence gate.", content)
        self.assertNotIn(str(REPO_ROOT), content)
        self.assertNotIn("/Users/", content)


if __name__ == "__main__":
    unittest.main()
