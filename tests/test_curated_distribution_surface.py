from __future__ import annotations

import importlib.util
import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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

    def test_frontmatter_reader_rejects_fifo_without_blocking(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            fifo = Path(tmpdir) / "SKILL.md"
            os.mkfifo(fifo)
            with self.assertRaisesRegex(ValueError, "regular file"):
                module.load_frontmatter(fifo)

    def test_curated_surface_contains_core_public_skills(self):
        index = json.loads((CURATED_DIR / "index.json").read_text(encoding="utf-8"))
        exported_names = {entry["name"] for entry in index["skills"]}

        self.assertIn("pc-prodcraft", exported_names)
        self.assertIn("pc-intake", exported_names)
        self.assertIn("pc-code-review", exported_names)
        self.assertIn("pc-incident-response", exported_names)
        self.assertIn("pc-verification-before-completion", exported_names)
        self.assertIn("pc-delivery-completion", exported_names)
        self.assertIn("pc-acceptance-criteria", exported_names)

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

            self.assertIn("pc-prodcraft", result["skills"])
            self.assertTrue((output_root / "pc-prodcraft" / "SKILL.md").exists())
            self.assertTrue((output_root / "pc-intake" / "SKILL.md").exists())
            self.assertEqual(self.snapshot_file_tree(output_root), self.snapshot_file_tree(CURATED_DIR))

    def test_invalid_registry_fails_before_mutating_output_tree(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            repo_root = temp_root / "repo"
            registry_root = repo_root / "schemas" / "distribution"
            registry_root.mkdir(parents=True)
            (registry_root / "public-skill-registry.json").write_text(
                json.dumps(
                    {
                        "schema_version": "public-skill-registry.v1",
                        "public_skills": [
                            {
                                "name": "intake",
                                "source": "skills/00-discovery/pc-intake",
                                "stability": "beta",
                                "readiness": "core",
                                "manual_allowlist": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (registry_root / "public-skill-portability.json").write_text(
                json.dumps(
                    {
                        "schema_version": "public-skill-portability.v1",
                        "skills": [
                            {
                                "name": "intake",
                                "portability": "portable_with_caveat",
                                "hidden_dependencies": [],
                                "required_context": "repository",
                                "public_caveat_text": "Requires repository context.",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            output_root = temp_root / "output"
            output_root.mkdir()
            sentinel = output_root / "sentinel.txt"
            sentinel.write_text("keep", encoding="utf-8")
            before = self.snapshot_file_tree(output_root)

            with self.assertRaisesRegex(ValueError, "must start with pc-"):
                module.export_curated_skills(repo_root=repo_root, output_root=output_root)

            self.assertEqual(before, self.snapshot_file_tree(output_root))

    def test_source_resource_swapped_to_symlink_after_preflight_does_not_leak(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            repo_root = temp_root / "repo"
            source_dir = repo_root / "skills" / "00-discovery" / "pc-example"
            assets_dir = source_dir / "assets"
            assets_dir.mkdir(parents=True)
            (source_dir / "SKILL.md").write_text(
                "---\nname: pc-example\ndescription: Use when testing safe curated export.\n---\n\n# Example\n",
                encoding="utf-8",
            )
            external_secret = temp_root / "outside-secret.txt"
            external_secret.write_text("TOP-SECRET", encoding="utf-8")
            leak_path = assets_dir / "leak.txt"
            leak_path.write_text("SAFE", encoding="utf-8")

            registry_root = repo_root / "schemas" / "distribution"
            registry_root.mkdir(parents=True)
            (registry_root / "public-skill-registry.json").write_text(
                json.dumps(
                    {
                        "schema_version": "public-skill-registry.v1",
                        "public_skills": [
                            {
                                "name": "pc-example",
                                "source": "skills/00-discovery/pc-example",
                                "stability": "beta",
                                "readiness": "experimental",
                                "manual_allowlist": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (registry_root / "public-skill-portability.json").write_text(
                json.dumps(
                    {
                        "schema_version": "public-skill-portability.v1",
                        "skills": [
                            {
                                "name": "pc-example",
                                "portability": "portable_with_caveat",
                                "hidden_dependencies": [],
                                "required_context": "repository",
                                "public_caveat_text": "Requires repository context.",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            output_root = temp_root / "output"
            output_root.mkdir()
            sentinel = output_root / "sentinel.txt"
            sentinel.write_text("keep", encoding="utf-8")
            before = self.snapshot_file_tree(output_root)

            original_validate = module.validate_public_source_tree
            swapped = False

            def swap_after_validation(**kwargs):
                nonlocal swapped
                source_dir = original_validate(**kwargs)
                if not swapped:
                    leak_path.unlink()
                    leak_path.symlink_to(external_secret)
                    swapped = True
                return source_dir

            with mock.patch.object(module, "validate_public_source_tree", swap_after_validation):
                with self.assertRaisesRegex(ValueError, "symlink"):
                    module.export_curated_skills(repo_root=repo_root, output_root=output_root)

            self.assertEqual(before, self.snapshot_file_tree(output_root))
            self.assertNotIn("TOP-SECRET", "".join(data.decode("utf-8") for data in before.values()))

    def test_source_skill_swapped_to_symlink_after_preflight_does_not_leak(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            repo_root = temp_root / "repo"
            source_dir = repo_root / "skills" / "00-discovery" / "pc-example"
            source_dir.mkdir(parents=True)
            skill_path = source_dir / "SKILL.md"
            skill_path.write_text(
                "---\nname: pc-example\ndescription: Use when testing safe curated export.\n---\n\n# Safe\n",
                encoding="utf-8",
            )
            external_skill = temp_root / "outside-skill.md"
            external_skill.write_text(
                "---\nname: pc-example\ndescription: Use when leaking external content.\n---\n\nTOP-SECRET\n",
                encoding="utf-8",
            )

            registry_root = repo_root / "schemas" / "distribution"
            registry_root.mkdir(parents=True)
            (registry_root / "public-skill-registry.json").write_text(
                json.dumps(
                    {
                        "schema_version": "public-skill-registry.v1",
                        "public_skills": [
                            {
                                "name": "pc-example",
                                "source": "skills/00-discovery/pc-example",
                                "stability": "beta",
                                "readiness": "experimental",
                                "manual_allowlist": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (registry_root / "public-skill-portability.json").write_text(
                json.dumps(
                    {
                        "schema_version": "public-skill-portability.v1",
                        "skills": [
                            {
                                "name": "pc-example",
                                "portability": "portable_with_caveat",
                                "hidden_dependencies": [],
                                "required_context": "repository",
                                "public_caveat_text": "Requires repository context.",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            output_root = temp_root / "output"
            output_root.mkdir()
            (output_root / "sentinel.txt").write_text("keep", encoding="utf-8")
            before = self.snapshot_file_tree(output_root)
            original_validate = module.validate_public_source_tree
            swapped = False

            def swap_after_validation(**kwargs):
                nonlocal swapped
                validated = original_validate(**kwargs)
                if not swapped:
                    skill_path.unlink()
                    skill_path.symlink_to(external_skill)
                    swapped = True
                return validated

            with mock.patch.object(module, "validate_public_source_tree", swap_after_validation):
                with self.assertRaisesRegex(ValueError, "non-symlink regular file"):
                    module.export_curated_skills(repo_root=repo_root, output_root=output_root)

            self.assertEqual(before, self.snapshot_file_tree(output_root))
            self.assertNotIn("TOP-SECRET", "".join(data.decode("utf-8") for data in before.values()))

    def test_export_restores_previous_surface_when_interrupted_after_backup(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir) / "output"
            output_root.mkdir()
            (output_root / "sentinel.txt").write_text("preserve me", encoding="utf-8")
            before = self.snapshot_file_tree(output_root)
            original_rename = Path.rename

            def interrupted_rename(path, destination):
                if path == output_root:
                    original_rename(path, destination)
                    raise KeyboardInterrupt("injected interruption")
                return original_rename(path, destination)

            with mock.patch.object(Path, "rename", interrupted_rename):
                with self.assertRaises(KeyboardInterrupt):
                    module.export_curated_skills(repo_root=REPO_ROOT, output_root=output_root)

            self.assertEqual(before, self.snapshot_file_tree(output_root))

    def test_exported_surface_rewrites_lifecycle_links_for_flattened_packages(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir)
            module.export_curated_skills(repo_root=REPO_ROOT, output_root=output_root)

            system_design = (output_root / "pc-system-design" / "SKILL.md").read_text(encoding="utf-8")
            problem_framing = (output_root / "pc-problem-framing" / "SKILL.md").read_text(encoding="utf-8")

            self.assertIn("[pc-spec-writing](../pc-spec-writing/SKILL.md)", system_design)
            self.assertNotIn("../../01-specification/pc-spec-writing/SKILL.md", system_design)
            self.assertIn("`pc-market-analysis`", problem_framing)
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
        content = (CURATED_DIR / "pc-prodcraft" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("default entry system for software-development tasks", content)
        self.assertIn("skipping Prodcraft preserves the same lifecycle guarantees", content)

    def test_curated_prodcraft_skill_defends_gateway_self_location_boundary(self):
        content = (CURATED_DIR / "pc-prodcraft" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn(
            "A `pc-prodcraft` directory that contains only this `SKILL.md` is a valid gateway install",
            content,
        )
        self.assertIn("Look for sibling skill packages beside `pc-prodcraft`", content)
        self.assertIn(
            "do not claim that downstream skills such as `pc-code-review`, `pc-testing-strategy`, or `pc-security-audit` ran",
            content,
        )
        self.assertIn("This is partial-entry guidance, not a completed Prodcraft workflow or evidence gate.", content)
        self.assertNotIn(str(REPO_ROOT), content)
        self.assertNotIn("/Users/", content)


if __name__ == "__main__":
    unittest.main()
