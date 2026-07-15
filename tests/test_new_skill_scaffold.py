from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCAFFOLDER_PATH = REPO_ROOT / "scripts" / "new_skill.py"


def load_scaffolder():
    spec = importlib.util.spec_from_file_location("new_skill_scaffold", SCAFFOLDER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def planned_block(name: str, phase: str) -> str:
    return (
        f"- name: {name}\n"
        f"  phase: {phase}\n"
        f"  target_file: skills/{phase}/{name}/SKILL.md\n"
        "  rationale: Reserved for a reviewed authoring task.\n"
    )


def write_fixture_repo(
    root: Path,
    *,
    planned: tuple[tuple[str, str], ...] = (),
    public_names: tuple[str, ...] = (),
    validator_exit: int = 0,
) -> bytes:
    manifest = (
        "schema_version: prodcraft-manifest.v1\n"
        "phases:\n"
        "- id: 04-implementation\n"
        "  name: Implementation\n"
        "skills:\n"
        "- name: pc-existing\n"
        "  phase: 04-implementation\n"
        "  file: skills/04-implementation/pc-existing/SKILL.md\n"
        "  status: draft\n"
        "  qa_tier: standard\n"
        "planned_skills:\n"
        + "".join(planned_block(name, phase) for name, phase in planned)
        + "workflows: []\n"
        "artifact_flow:\n"
        "# This comment and flow must remain byte-for-byte stable.\n"
        "- artifact: existing-output\n"
        "  produced_by: pc-existing\n"
        "  consumed_by: []\n"
    )
    manifest_path = root / "manifest.yml"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(manifest, encoding="utf-8")

    (root / "skills" / "04-implementation").mkdir(parents=True)
    (root / "eval" / "04-implementation").mkdir(parents=True)
    (root / "rules").mkdir(parents=True)
    (root / "rules" / "cross-cutting-matrix.yml").write_text(
        "schema_version: cross-cutting-matrix.v1\nrules: []\n",
        encoding="utf-8",
    )
    registry_path = root / "schemas" / "distribution" / "public-skill-registry.json"
    registry_path.parent.mkdir(parents=True)
    registry_path.write_text(
        json.dumps(
            {
                "schema_version": "public-skill-registry.v1",
                "public_skills": [{"name": name} for name in public_names],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    portability_path = root / "schemas" / "distribution" / "public-skill-portability.json"
    portability_path.write_text(
        '{"schema_version":"public-skill-portability.v1","skills":[]}\n',
        encoding="utf-8",
    )

    validator_path = root / "scripts" / "validate_prodcraft.py"
    validator_path.parent.mkdir(parents=True)
    validator_path.write_text(
        "from pathlib import Path\n"
        "import sys\n"
        "root = Path(__file__).resolve().parents[1]\n"
        "skill = root / 'skills/04-implementation/pc-demo/SKILL.md'\n"
        "strategy = root / 'eval/04-implementation/pc-demo/evals/eval-strategy.md'\n"
        f"sys.exit({validator_exit} if skill.is_file() and strategy.is_file() else 23)\n",
        encoding="utf-8",
    )
    return manifest.encode("utf-8")


def snapshot_tree(root: Path) -> dict[str, bytes | None]:
    snapshot: dict[str, bytes | None] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            snapshot[f"link:{rel}"] = os.fsencode(os.readlink(path))
        elif path.is_dir():
            snapshot[f"dir:{rel}"] = None
        elif path.is_file():
            snapshot[f"file:{rel}"] = path.read_bytes()
    return snapshot


def assert_candidate_has_draft(candidate_root: Path) -> None:
    manifest = yaml.safe_load((candidate_root / "manifest.yml").read_text(encoding="utf-8"))
    entry = next(item for item in manifest["skills"] if item["name"] == "pc-demo")
    assert entry["status"] == "draft"
    assert entry["phase"] == "04-implementation"
    assert (candidate_root / entry["file"]).is_file()
    assert (
        candidate_root / "eval" / "04-implementation" / "pc-demo" / "evals" / "eval-strategy.md"
    ).is_file()


class FailOnceReplace:
    def __init__(self, fail_on_call: int):
        self.fail_on_call = fail_on_call
        self.calls = 0

    def __call__(self, source: str | os.PathLike[str], target: str | os.PathLike[str]) -> None:
        self.calls += 1
        if self.calls == self.fail_on_call:
            raise OSError(f"injected replace failure at step {self.calls}")
        os.replace(source, target)


class NewSkillScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.scaffolder = load_scaffolder()

    def test_scaffold_creates_only_draft_authoring_surfaces_and_preserves_policy_surfaces(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            original_manifest = write_fixture_repo(root)
            protected = {
                path: (root / path).read_bytes()
                for path in (
                    "rules/cross-cutting-matrix.yml",
                    "schemas/distribution/public-skill-registry.json",
                    "schemas/distribution/public-skill-portability.json",
                )
            }
            before_tree = snapshot_tree(root)

            result = self.scaffolder.scaffold_skill(
                root,
                "04-implementation",
                "pc-demo",
                validator=assert_candidate_has_draft,
            )

            self.assertEqual(
                (root / "skills/04-implementation/pc-demo/SKILL.md").resolve(),
                result.skill_path,
            )
            self.assertEqual(
                (root / "eval/04-implementation/pc-demo/evals/eval-strategy.md").resolve(),
                result.eval_strategy_path,
            )
            manifest_text = (root / "manifest.yml").read_text(encoding="utf-8")
            manifest = yaml.safe_load(manifest_text)
            entry = next(item for item in manifest["skills"] if item["name"] == "pc-demo")
            self.assertEqual("draft", entry["status"])
            self.assertEqual("standard", entry["qa_tier"])
            self.assertEqual("routed", entry["evaluation_mode"])
            self.assertEqual([], manifest["artifact_flow"][0]["consumed_by"])
            self.assertNotIn("pc-demo", manifest_text.split("artifact_flow:", 1)[1])
            self.assertIn("# This comment and flow must remain byte-for-byte stable.", manifest_text)
            self.assertNotEqual(original_manifest, (root / "manifest.yml").read_bytes())

            skill_text = result.skill_path.read_text(encoding="utf-8")
            self.assertIn("name: pc-demo", skill_text)
            self.assertIn("description: Use when", skill_text)
            self.assertIn("inputs: []", skill_text)
            self.assertIn("outputs: []", skill_text)
            for heading in ("Context", "Inputs", "Process", "Outputs", "Quality Gate"):
                self.assertIn(f"## {heading}", skill_text)
            for path, expected in protected.items():
                self.assertEqual(expected, (root / path).read_bytes())
            added_paths = set(snapshot_tree(root)) - set(before_tree)
            self.assertEqual(
                {
                    "dir:skills/04-implementation/pc-demo",
                    "file:skills/04-implementation/pc-demo/SKILL.md",
                    "dir:eval/04-implementation/pc-demo",
                    "dir:eval/04-implementation/pc-demo/evals",
                    "file:eval/04-implementation/pc-demo/evals/eval-strategy.md",
                },
                added_paths,
            )

    def test_matching_planned_entry_is_converted_once_and_singleton_list_stays_valid_yaml(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_fixture_repo(root, planned=(("pc-demo", "04-implementation"),))

            self.scaffolder.scaffold_skill(
                root,
                "04-implementation",
                "pc-demo",
                validator=assert_candidate_has_draft,
            )

            manifest = yaml.safe_load((root / "manifest.yml").read_text(encoding="utf-8"))
            self.assertEqual([], manifest["planned_skills"])
            self.assertEqual(1, [item["name"] for item in manifest["skills"]].count("pc-demo"))

    def test_existing_public_filesystem_and_mismatched_planned_collisions_are_non_mutating(self):
        cases = (
            ("implemented", {}, "pc-existing", "04-implementation"),
            ("public", {"public_names": ("pc-demo",)}, "pc-demo", "04-implementation"),
            (
                "planned-wrong-phase",
                {"planned": (("pc-demo", "05-quality"),)},
                "pc-demo",
                "04-implementation",
            ),
        )
        for label, fixture_kwargs, name, phase in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmpdir:
                root = Path(tmpdir)
                write_fixture_repo(root, **fixture_kwargs)
                if label == "implemented":
                    name = "pc-existing"
                before = snapshot_tree(root)
                with self.assertRaises(self.scaffolder.ScaffoldError):
                    self.scaffolder.scaffold_skill(root, phase, name, validator=assert_candidate_has_draft)
                self.assertEqual(before, snapshot_tree(root))

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_fixture_repo(root)
            collision = root / "skills/04-implementation/pc-demo"
            collision.mkdir(parents=True)
            (collision / "unexpected.txt").write_text("owned\n", encoding="utf-8")
            before = snapshot_tree(root)
            with self.assertRaises(self.scaffolder.ScaffoldError):
                self.scaffolder.scaffold_skill(
                    root,
                    "04-implementation",
                    "pc-demo",
                    validator=assert_candidate_has_draft,
                )
            self.assertEqual(before, snapshot_tree(root))

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_fixture_repo(root)
            dangling = root / "skills/04-implementation/pc-demo"
            dangling.symlink_to(root / "missing-external-target", target_is_directory=True)
            before = snapshot_tree(root)
            with self.assertRaises(self.scaffolder.ScaffoldError):
                self.scaffolder.scaffold_skill(
                    root,
                    "04-implementation",
                    "pc-demo",
                    validator=assert_candidate_has_draft,
                )
            self.assertEqual(before, snapshot_tree(root))
            self.assertTrue(dangling.is_symlink())

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_fixture_repo(root, planned=(("pc-demo", "04-implementation"),))
            manifest_path = root / "manifest.yml"
            manifest_path.write_text(
                manifest_path.read_text(encoding="utf-8").replace(
                    "target_file: skills/04-implementation/pc-demo/SKILL.md",
                    "target_file: skills/05-quality/pc-demo/SKILL.md",
                ),
                encoding="utf-8",
            )
            before = snapshot_tree(root)
            with self.assertRaises(self.scaffolder.ScaffoldError):
                self.scaffolder.scaffold_skill(
                    root,
                    "04-implementation",
                    "pc-demo",
                    validator=assert_candidate_has_draft,
                )
            self.assertEqual(before, snapshot_tree(root))

    def test_invalid_phase_or_name_is_rejected_before_filesystem_mutation(self):
        cases = (
            ("unknown-phase", "pc-demo"),
            ("04-implementation", "demo"),
            ("04-implementation", "pc-demo/escape"),
            ("04-implementation", "pc-Demo"),
            ("../04-implementation", "pc-demo"),
        )
        for phase, name in cases:
            with self.subTest(phase=phase, name=name), tempfile.TemporaryDirectory() as tmpdir:
                root = Path(tmpdir)
                write_fixture_repo(root)
                before = snapshot_tree(root)
                with self.assertRaises(self.scaffolder.ScaffoldError):
                    self.scaffolder.scaffold_skill(root, phase, name, validator=assert_candidate_has_draft)
                self.assertEqual(before, snapshot_tree(root))

    def test_symlinked_authoring_phase_cannot_escape_candidate_repository(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_fixture_repo(root)
            phase_dir = root / "skills/04-implementation"
            phase_dir.rmdir()
            external_target = root / "external-skill-target"
            external_target.mkdir()
            phase_dir.symlink_to(external_target, target_is_directory=True)
            before = snapshot_tree(root)

            with self.assertRaises(self.scaffolder.ScaffoldError):
                self.scaffolder.scaffold_skill(
                    root,
                    "04-implementation",
                    "pc-demo",
                    validator=assert_candidate_has_draft,
                )

            self.assertEqual(before, snapshot_tree(root))
            self.assertFalse((external_target / "pc-demo").exists())

    def test_atomic_move_never_replaces_a_destination_that_appeared(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "source"
            source.mkdir()
            (source / "owned.txt").write_text("owned\n", encoding="utf-8")
            target = root / "target"
            target.symlink_to(root / "missing-target", target_is_directory=True)

            with self.assertRaises(OSError):
                self.scaffolder.atomic_move_no_replace(source, target)

            self.assertTrue(source.is_dir())
            self.assertTrue(target.is_symlink())

    def test_second_invocation_is_non_mutating_and_never_duplicates_manifest_entry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_fixture_repo(root)
            self.scaffolder.scaffold_skill(
                root,
                "04-implementation",
                "pc-demo",
                validator=assert_candidate_has_draft,
            )
            before_second = snapshot_tree(root)

            with self.assertRaises(self.scaffolder.ScaffoldError):
                self.scaffolder.scaffold_skill(
                    root,
                    "04-implementation",
                    "pc-demo",
                    validator=assert_candidate_has_draft,
                )

            self.assertEqual(before_second, snapshot_tree(root))
            manifest = yaml.safe_load((root / "manifest.yml").read_text(encoding="utf-8"))
            self.assertEqual(1, [item["name"] for item in manifest["skills"]].count("pc-demo"))

    def test_validator_failure_leaves_repository_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_fixture_repo(root)
            before = snapshot_tree(root)

            def reject_candidate(_candidate_root: Path) -> None:
                raise RuntimeError("candidate rejected")

            with self.assertRaises(self.scaffolder.ScaffoldError):
                self.scaffolder.scaffold_skill(
                    root,
                    "04-implementation",
                    "pc-demo",
                    validator=reject_candidate,
                )
            self.assertEqual(before, snapshot_tree(root))

    def test_default_external_validator_runs_against_candidate_and_fails_closed(self):
        for exit_code in (0, 7):
            with self.subTest(exit_code=exit_code), tempfile.TemporaryDirectory() as tmpdir:
                root = Path(tmpdir)
                write_fixture_repo(root, validator_exit=exit_code)
                before = snapshot_tree(root)
                if exit_code == 0:
                    self.scaffolder.scaffold_skill(root, "04-implementation", "pc-demo")
                    self.assertTrue((root / "skills/04-implementation/pc-demo/SKILL.md").is_file())
                else:
                    with self.assertRaises(self.scaffolder.ScaffoldError):
                        self.scaffolder.scaffold_skill(root, "04-implementation", "pc-demo")
                    self.assertEqual(before, snapshot_tree(root))

    def test_each_commit_replace_failure_rolls_back_byte_for_byte(self):
        for fail_on_call in (1, 2):
            with self.subTest(fail_on_call=fail_on_call), tempfile.TemporaryDirectory() as tmpdir:
                root = Path(tmpdir)
                write_fixture_repo(root)
                before = snapshot_tree(root)
                with self.assertRaises(self.scaffolder.ScaffoldError):
                    self.scaffolder.scaffold_skill(
                        root,
                        "04-implementation",
                        "pc-demo",
                        validator=assert_candidate_has_draft,
                        replace_fn=FailOnceReplace(fail_on_call),
                    )
                self.assertEqual(before, snapshot_tree(root))

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_fixture_repo(root)
            before = snapshot_tree(root)

            def fail_exchange(_source, _target):
                raise OSError("injected manifest exchange failure")

            with self.assertRaises(self.scaffolder.ScaffoldError):
                self.scaffolder.scaffold_skill(
                    root,
                    "04-implementation",
                    "pc-demo",
                    validator=assert_candidate_has_draft,
                    exchange_fn=fail_exchange,
                )
            self.assertEqual(before, snapshot_tree(root))

    def test_manifest_changed_during_candidate_validation_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            original = write_fixture_repo(root)

            def concurrent_writer(candidate_root: Path) -> None:
                assert_candidate_has_draft(candidate_root)
                (root / "manifest.yml").write_bytes(original + b"# concurrent owner change\n")

            with self.assertRaises(self.scaffolder.ScaffoldError):
                self.scaffolder.scaffold_skill(
                    root,
                    "04-implementation",
                    "pc-demo",
                    validator=concurrent_writer,
                )

            self.assertEqual(original + b"# concurrent owner change\n", (root / "manifest.yml").read_bytes())
            self.assertFalse((root / "skills/04-implementation/pc-demo").exists())
            self.assertFalse((root / "eval/04-implementation/pc-demo").exists())

    def test_manifest_changed_during_commit_is_preserved_and_created_directories_roll_back(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            original = write_fixture_repo(root)
            concurrent = original + b"# concurrent change during commit\n"

            class ConcurrentManifestWriter:
                def __init__(self):
                    self.calls = 0

                def __call__(self, source, target):
                    self.calls += 1
                    os.replace(source, target)
                    if self.calls == 1:
                        (root / "manifest.yml").write_bytes(concurrent)

            with self.assertRaises(self.scaffolder.ScaffoldError):
                self.scaffolder.scaffold_skill(
                    root,
                    "04-implementation",
                    "pc-demo",
                    validator=assert_candidate_has_draft,
                    replace_fn=ConcurrentManifestWriter(),
                )

            self.assertEqual(concurrent, (root / "manifest.yml").read_bytes())
            self.assertFalse((root / "skills/04-implementation/pc-demo").exists())
            self.assertFalse((root / "eval/04-implementation/pc-demo").exists())

    def test_manifest_changed_at_exchange_boundary_is_swapped_back_without_data_loss(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            original = write_fixture_repo(root)
            concurrent = original + b"# concurrent change at exchange boundary\n"

            def concurrent_exchange(source, target):
                (root / "manifest.yml").write_bytes(concurrent)
                self.scaffolder.atomic_exchange(source, target)

            with self.assertRaises(self.scaffolder.ScaffoldError):
                self.scaffolder.scaffold_skill(
                    root,
                    "04-implementation",
                    "pc-demo",
                    validator=assert_candidate_has_draft,
                    exchange_fn=concurrent_exchange,
                )

            self.assertEqual(concurrent, (root / "manifest.yml").read_bytes())
            self.assertFalse((root / "skills/04-implementation/pc-demo").exists())
            self.assertFalse((root / "eval/04-implementation/pc-demo").exists())

    def test_rollback_preserves_files_added_by_a_concurrent_owner(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            original = write_fixture_repo(root)
            concurrent_path = root / "skills/04-implementation/pc-demo/concurrent.txt"

            class ConcurrentWriterThenFailure:
                def __init__(self):
                    self.calls = 0

                def __call__(self, source, target):
                    self.calls += 1
                    if self.calls == 1:
                        os.replace(source, target)
                        concurrent_path.write_text("concurrent owner data\n", encoding="utf-8")
                        return
                    raise OSError("injected failure after concurrent write")

            with self.assertRaises(self.scaffolder.ScaffoldError):
                self.scaffolder.scaffold_skill(
                    root,
                    "04-implementation",
                    "pc-demo",
                    validator=assert_candidate_has_draft,
                    replace_fn=ConcurrentWriterThenFailure(),
                )

            self.assertEqual(original, (root / "manifest.yml").read_bytes())
            self.assertEqual("concurrent owner data\n", concurrent_path.read_text(encoding="utf-8"))
            self.assertFalse((concurrent_path.parent / "SKILL.md").exists())
            self.assertFalse((root / "eval/04-implementation/pc-demo").exists())

    def test_rollback_never_unlinks_a_replacement_installed_after_owned_bytes_are_read(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            original = write_fixture_repo(root)
            skill_path = root / "skills/04-implementation/pc-demo/SKILL.md"
            concurrent = b"concurrent owner replacement\n"
            failure_started = False
            replacement_installed = False
            real_read_bytes = Path.read_bytes

            class FailSecondMove:
                def __init__(self):
                    self.calls = 0

                def __call__(self, source, target):
                    nonlocal failure_started
                    self.calls += 1
                    if self.calls == 1:
                        os.replace(source, target)
                        return
                    failure_started = True
                    raise OSError("injected failure before rollback")

            def read_then_replace(path: Path) -> bytes:
                nonlocal replacement_installed
                data = real_read_bytes(path)
                if (
                    failure_started
                    and not replacement_installed
                    and b"name: pc-demo" in data
                ):
                    skill_path.write_bytes(concurrent)
                    replacement_installed = True
                return data

            with patch.object(Path, "read_bytes", read_then_replace):
                with self.assertRaises(self.scaffolder.ScaffoldError):
                    self.scaffolder.scaffold_skill(
                        root,
                        "04-implementation",
                        "pc-demo",
                        validator=assert_candidate_has_draft,
                        replace_fn=FailSecondMove(),
                    )

            self.assertTrue(replacement_installed)
            self.assertEqual(original, (root / "manifest.yml").read_bytes())
            self.assertEqual(concurrent, skill_path.read_bytes())
            self.assertFalse((root / "eval/04-implementation/pc-demo").exists())

    def test_rollback_restore_conflict_preserves_both_concurrent_versions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            original = write_fixture_repo(root)
            skill_path = root / "skills/04-implementation/pc-demo/SKILL.md"
            displaced_concurrent = b"concurrent owner version one\n"
            public_concurrent = b"concurrent owner version two\n"
            real_atomic_move = self.scaffolder.atomic_move_no_replace

            class ReplaceThenFail:
                def __init__(self):
                    self.calls = 0

                def __call__(self, source, target):
                    self.calls += 1
                    if self.calls == 1:
                        os.replace(source, target)
                        skill_path.write_bytes(displaced_concurrent)
                        return
                    raise OSError("injected failure before rollback")

            def install_newer_version_before_restore(source, target):
                target_path = Path(target)
                if target_path.resolve(strict=False) == skill_path.resolve(strict=False):
                    skill_path.write_bytes(public_concurrent)
                real_atomic_move(source, target)

            with patch.object(
                self.scaffolder,
                "atomic_move_no_replace",
                install_newer_version_before_restore,
            ):
                with self.assertRaises(self.scaffolder.ScaffoldError) as raised:
                    self.scaffolder.scaffold_skill(
                        root,
                        "04-implementation",
                        "pc-demo",
                        validator=assert_candidate_has_draft,
                        replace_fn=ReplaceThenFail(),
                    )

            quarantine_roots = list(root.glob(".new-skill-stage-*/rollback-quarantine"))
            self.assertEqual(original, (root / "manifest.yml").read_bytes())
            self.assertEqual(public_concurrent, skill_path.read_bytes())
            self.assertEqual(1, len(quarantine_roots))
            self.assertEqual(
                displaced_concurrent,
                (quarantine_roots[0] / "SKILL.md").read_bytes(),
            )
            self.assertIn("rollback conflict", str(raised.exception))

    def test_manifest_overwritten_after_exchange_is_preserved_and_owned_directories_roll_back(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            original = write_fixture_repo(root)
            concurrent = original + b"# concurrent overwrite after exchange\n"

            def overwrite_after_exchange(source, target):
                self.scaffolder.atomic_exchange(source, target)
                (root / "manifest.yml").write_bytes(concurrent)

            with self.assertRaises(self.scaffolder.ScaffoldError):
                self.scaffolder.scaffold_skill(
                    root,
                    "04-implementation",
                    "pc-demo",
                    validator=assert_candidate_has_draft,
                    exchange_fn=overwrite_after_exchange,
                )

            self.assertEqual(concurrent, (root / "manifest.yml").read_bytes())
            self.assertFalse((root / "skills/04-implementation/pc-demo").exists())
            self.assertFalse((root / "eval/04-implementation/pc-demo").exists())

    def test_authoring_schema_documents_draft_only_and_promotion_time_boundaries(self):
        authoring_schema = (REPO_ROOT / "skills" / "_schema.md").read_text(encoding="utf-8")

        self.assertIn("python scripts/new_skill.py <phase> <pc-skill-name>", authoring_schema)
        self.assertIn("draft-only", authoring_schema)
        self.assertIn("candidate repository", authoring_schema)
        self.assertIn("promotion-time", authoring_schema)
        for protected_surface in (
            "artifact_flow",
            "public-skill-registry.json",
            "public-skill-portability.json",
            "cross-cutting-matrix.yml",
        ):
            self.assertIn(protected_surface, authoring_schema)


if __name__ == "__main__":
    unittest.main()
