from __future__ import annotations

import json
import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

import yaml

try:
    import jsonschema
except ImportError:  # pragma: no cover - exercised in dependency-light local runs
    jsonschema = None


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_PREFIX = "pc-"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_prodcraft.py"
MARKDOWN_SKILL_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]*SKILL\.md(?:#[^)\s]+)?)\)")
LOCAL_EVAL_FILE_RE = re.compile(
    r"`(?P<path>eval/[^`\s]+)`"
)


def load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise AssertionError(f"{path} is missing valid YAML frontmatter")
    return yaml.safe_load(parts[1]) or {}


def authored_skill_paths() -> list[Path]:
    return sorted(
        path
        for path in (REPO_ROOT / "skills").glob("*/*/SKILL.md")
        if ".curated" not in path.parts
    )


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_prodcraft", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SkillIdentityPrefixTests(unittest.TestCase):
    def test_validator_accepts_pc_name_and_rejects_unprefixed_name(self):
        validator = load_validator_module()

        valid_errors: list[str] = []
        validator.validate_skill_name("pc-intake", Path("pc-intake/SKILL.md"), valid_errors)
        self.assertEqual([], valid_errors)

        invalid_errors: list[str] = []
        validator.validate_skill_name("intake", Path("intake/SKILL.md"), invalid_errors)
        self.assertEqual(1, len(invalid_errors))
        self.assertIn("must start with `pc-`", invalid_errors[0])

    def test_validator_rejects_scalar_prerequisites(self):
        validator = load_validator_module()
        source = """---
name: pc-example
description: Use when testing validation behavior.
metadata:
  phase: 00-discovery
  inputs: []
  outputs: []
  prerequisites: pc-intake
  roles: []
  methodologies: []
---

# Example

## Context
Test context.

## Inputs
None.

## Process
Validate.

## Outputs
Errors.

## Quality Gate
- [ ] Scalar prerequisites are rejected.
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            skill_path = Path(tmpdir) / "00-discovery" / "pc-example" / "SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_path.write_text(source, encoding="utf-8")
            errors: list[str] = []
            validator.validate_skill_file(skill_path, errors)

        self.assertTrue(
            any("`metadata.prerequisites` must be a list" in error for error in errors),
            errors,
        )

    def test_authored_skill_names_are_pc_prefixed_and_match_directories(self):
        paths = authored_skill_paths()
        authored_names = {path.parent.name for path in paths}

        self.assertEqual(46, len(paths))
        for skill_path in paths:
            with self.subTest(skill=skill_path.parent.name):
                frontmatter = load_frontmatter(skill_path)
                name = frontmatter.get("name")
                self.assertIsInstance(name, str, skill_path)
                self.assertRegex(name, SKILL_NAME_RE, skill_path)
                self.assertTrue(name.startswith(SKILL_PREFIX), skill_path)
                self.assertEqual(skill_path.parent.name, name, skill_path)

                prerequisites = frontmatter.get("metadata", {}).get("prerequisites", [])
                self.assertIsInstance(prerequisites, list, skill_path)
                for prerequisite in prerequisites:
                    self.assertIn(prerequisite, authored_names, skill_path)
                    self.assertNotEqual(name, prerequisite, skill_path)

                body = skill_path.read_text(encoding="utf-8").split("---\n", 2)[2]
                for match in MARKDOWN_SKILL_LINK_RE.finditer(body):
                    target = match.group("target").split("#", 1)[0]
                    if target.startswith(("http://", "https://")):
                        continue
                    self.assertTrue((skill_path.parent / target).resolve().is_file(), f"{skill_path} -> {target}")

    def test_manifest_implemented_and_planned_skills_are_pc_prefixed(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        authored_names = {path.parent.name for path in authored_skill_paths()}

        for section in ("skills", "planned_skills"):
            for entry in manifest.get(section, []):
                with self.subTest(section=section, skill=entry.get("name")):
                    self.assertTrue(entry["name"].startswith(SKILL_PREFIX), entry)
                    if section == "planned_skills":
                        self.assertEqual(
                            f"skills/{entry['phase']}/{entry['name']}/SKILL.md",
                            entry["target_file"],
                            entry,
                        )

        implemented_names = {entry["name"] for entry in manifest["skills"]}
        self.assertEqual(authored_names, implemented_names)
        for edge in manifest.get("iterative_feedback_edges", []):
            for field in ("from", "to"):
                with self.subTest(edge=edge, field=field):
                    self.assertIn(edge[field], implemented_names)

    def test_public_distribution_registries_only_use_pc_prefixed_names(self):
        public_registry = json.loads(
            (REPO_ROOT / "schemas" / "distribution" / "public-skill-registry.json").read_text(
                encoding="utf-8"
            )
        )
        portability_registry = json.loads(
            (REPO_ROOT / "schemas" / "distribution" / "public-skill-portability.json").read_text(
                encoding="utf-8"
            )
        )
        curated_index = json.loads(
            (REPO_ROOT / "skills" / ".curated" / "index.json").read_text(encoding="utf-8")
        )

        surfaces = {
            "public registry": public_registry["public_skills"],
            "portability registry": portability_registry["skills"],
            "curated index": curated_index["skills"],
        }
        surface_names = {
            surface: {entry["name"] for entry in entries}
            for surface, entries in surfaces.items()
        }
        self.assertEqual(1, len({frozenset(names) for names in surface_names.values()}), surface_names)
        for surface, entries in surfaces.items():
            for entry in entries:
                with self.subTest(surface=surface, skill=entry.get("name")):
                    self.assertTrue(entry["name"].startswith(SKILL_PREFIX), entry)

    def test_curated_packages_are_pc_prefixed_and_loadable(self):
        curated_root = REPO_ROOT / "skills" / ".curated"
        package_dirs = sorted(path for path in curated_root.iterdir() if path.is_dir())
        index = json.loads((curated_root / "index.json").read_text(encoding="utf-8"))
        index_names = {entry["name"] for entry in index["skills"]}

        self.assertGreater(len(package_dirs), 0)
        self.assertEqual(index_names, {path.name for path in package_dirs})
        for package_dir in package_dirs:
            with self.subTest(skill=package_dir.name):
                self.assertTrue(package_dir.name.startswith(SKILL_PREFIX), package_dir)
                skill_path = package_dir / "SKILL.md"
                self.assertTrue(skill_path.is_file(), skill_path)
                frontmatter = load_frontmatter(skill_path)
                self.assertEqual(package_dir.name, frontmatter.get("name"), skill_path)
                description = frontmatter.get("description")
                self.assertIsInstance(description, str, skill_path)
                self.assertLessEqual(len(description), 1024, skill_path)

    def test_eval_directories_mirroring_authored_skills_use_pc_prefix(self):
        authored_by_phase = {
            (skill_path.parents[1].name, skill_path.parent.name)
            for skill_path in authored_skill_paths()
        }
        eval_mirrors = {
            (path.parent.name, path.name)
            for path in (REPO_ROOT / "eval").glob("*/*")
            if path.is_dir() and path.parent.name != "meta"
        }
        allowed_eval_only = {("05-quality", "xcuitest-webview-e2e")}
        self.assertEqual(authored_by_phase, eval_mirrors - allowed_eval_only)

        for phase, skill_name in authored_by_phase:
            eval_dir = REPO_ROOT / "eval" / phase / skill_name
            with self.subTest(phase=phase, skill=skill_name):
                self.assertTrue(eval_dir.is_dir(), eval_dir)

        legacy_mirror_dirs = {
            REPO_ROOT / "eval" / phase / skill_name.removeprefix(SKILL_PREFIX)
            for phase, skill_name in authored_by_phase
        }
        self.assertEqual(set(), {path for path in legacy_mirror_dirs if path.exists()})

    def test_active_eval_configs_use_enclosing_pc_skill_identity(self):
        root_configs = set((REPO_ROOT / "eval").glob("*/*/evals.json"))
        configs = root_configs | set((REPO_ROOT / "eval").glob("*/*/evals/*.json"))

        for config_path in sorted(configs):
            payload = json.loads(config_path.read_text(encoding="utf-8"))
            if config_path in root_configs:
                self.assertIsInstance(payload, dict, config_path)
                self.assertIsInstance(payload.get("skill_name"), str, config_path)
            if not isinstance(payload, dict) or "skill_name" not in payload:
                continue
            expected = config_path.relative_to(REPO_ROOT / "eval").parts[1]
            with self.subTest(config=config_path):
                self.assertEqual(expected, payload["skill_name"])

    def test_manifest_qa_docs_do_not_link_to_missing_eval_files(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

        for entry in manifest["skills"]:
            for key, relative_path in entry.get("qa", {}).items():
                if not key.endswith("_path") or not isinstance(relative_path, str):
                    continue
                qa_path = REPO_ROOT / relative_path
                if qa_path.suffix != ".md":
                    continue
                text = qa_path.read_text(encoding="utf-8")
                for match in LOCAL_EVAL_FILE_RE.finditer(text):
                    local_path = match.group("path")
                    if any(marker in local_path for marker in ("*", "<", ">", "{", "}")):
                        continue
                    with self.subTest(qa=relative_path, linked=local_path):
                        self.assertTrue((REPO_ROOT / local_path).exists())

    def test_active_benchmark_context_files_exist(self):
        benchmarks = set((REPO_ROOT / "eval").glob("*/*/*benchmark*.json"))
        benchmarks.update((REPO_ROOT / "eval").glob("*/*/evals/*benchmark*.json"))
        self.assertEqual(38, len(benchmarks))
        for benchmark_path in sorted(benchmarks):
            benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
            self.assertIsInstance(benchmark, list, benchmark_path)
            for case in benchmark:
                for context_file in case.get("context_files", []):
                    candidate = (benchmark_path.parent / context_file).resolve()
                    with self.subTest(benchmark=benchmark_path, context=context_file):
                        candidate.relative_to((REPO_ROOT / "eval").resolve())
                        self.assertTrue(candidate.is_file())

    def test_artifact_skill_reference_fields_require_pc_prefixed_names(self):
        contracts = {
            "intake-brief.schema.json": "recommended_next_skill",
            "problem-frame.schema.json": "next_skill_to_invoke",
            "course-correction-note.schema.json": "recommended_next_skill",
        }

        for filename, field in contracts.items():
            schema = json.loads(
                (REPO_ROOT / "schemas" / "artifacts" / filename).read_text(encoding="utf-8")
            )
            property_schema = schema["properties"][field]
            with self.subTest(schema=filename, field=field):
                pattern = property_schema.get("pattern")
                self.assertIsInstance(pattern, str)
                self.assertIsNotNone(re.fullmatch(pattern, "pc-system-design"))
                self.assertIsNone(re.fullmatch(pattern, "system-design"))
                if jsonschema is not None:
                    jsonschema.validate("pc-system-design", property_schema)
                    with self.assertRaises(jsonschema.ValidationError):
                        jsonschema.validate("system-design", property_schema)

    def test_active_skill_navigation_does_not_publish_unprefixed_ids(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        canonical_names = {
            entry["name"]
            for section in ("skills", "planned_skills")
            for entry in manifest.get(section, [])
        }
        legacy_names = {name.removeprefix(SKILL_PREFIX) for name in canonical_names}

        gateway = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")
        repo_local_gateway = gateway.split("## Integration with Existing Skills", 1)[0]
        active_docs = [
            REPO_ROOT / "skills" / "_schema.md",
            REPO_ROOT / "skills" / "_quality-assurance.md",
            REPO_ROOT / "examples" / "README.md",
        ]
        active_docs.extend(
            path
            for path in (REPO_ROOT / "skills").rglob("*.md")
            if ".curated" not in path.parts and path.name != "_gateway.md"
        )

        for path, text in [
            (REPO_ROOT / "skills" / "_gateway.md", repo_local_gateway),
            *((path, path.read_text(encoding="utf-8")) for path in active_docs),
        ]:
            for legacy_name in legacy_names:
                with self.subTest(path=path, legacy_name=legacy_name):
                    self.assertIsNone(
                        re.search(rf"(?<!pc-)`{re.escape(legacy_name)}`", text),
                        f"{path} publishes legacy skill id `{legacy_name}`",
                    )

        for phase_doc in (REPO_ROOT / "skills").glob("*/_phase.md"):
            text = phase_doc.read_text(encoding="utf-8")
            key_skills = text.split("## Key Skills", 1)[1].split("## ", 1)[0]
            rows = [line for line in key_skills.splitlines() if line.startswith("|")][2:]
            for row in rows:
                label = row.split("|", 2)[1].strip()
                link_match = re.fullmatch(r"\[([^]]+)\]\([^)]+\)", label)
                skill_name = link_match.group(1) if link_match else label
                with self.subTest(phase_doc=phase_doc, skill_name=skill_name):
                    self.assertTrue(skill_name.startswith(SKILL_PREFIX), row)
                    self.assertIn(skill_name, canonical_names, row)


if __name__ == "__main__":
    unittest.main()
