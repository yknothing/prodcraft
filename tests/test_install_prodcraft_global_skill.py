from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "install_prodcraft_global_skill.py"


def load_module():
    spec = importlib.util.spec_from_file_location("install_prodcraft_global_skill", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class InstallProdcraftGlobalSkillTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.skills_root = self.root / "skills"
        self.skills_root.mkdir(parents=True, exist_ok=True)
        self.state_path = self.root / "state.json"
        self.log_path = self.root / "events.jsonl"

    def read_events(self) -> list[dict]:
        if not self.log_path.exists():
            return []
        return [json.loads(line) for line in self.log_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def write_legacy_gateway(self, *, extra_file: bool = False, repo_root: Path = REPO_ROOT) -> Path:
        legacy_dir = self.skills_root / "prodcraft"
        legacy_dir.mkdir()
        (legacy_dir / "SKILL.md").write_text(
            "---\nname: prodcraft\ndescription: legacy gateway\n---\n",
            encoding="utf-8",
        )
        (legacy_dir / "prodcraft-runtime.json").write_text(
            json.dumps(
                {
                    "schema_version": "prodcraft-runtime-locator.v1",
                    "skill_name": "prodcraft",
                    "install_surface": "global",
                    "global_skill_path": str(legacy_dir),
                    "canonical_repo_root": str(repo_root),
                }
            ),
            encoding="utf-8",
        )
        if extra_file:
            (legacy_dir / "user-notes.md").write_text("preserve me", encoding="utf-8")
        return legacy_dir

    def test_install_creates_pc_prodcraft_skill_and_logs_event(self):
        result = self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="enable prodcraft globally",
        )

        skill_dir = self.skills_root / "pc-prodcraft"
        self.assertEqual("installed", result["status"])
        self.assertTrue(skill_dir.exists())
        self.assertTrue((skill_dir / "SKILL.md").exists())
        self.assertEqual("enable prodcraft globally", result["reason"])
        self.assertEqual("install", result["last_action"])

        content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: pc-prodcraft", content)
        self.assertIn("prodcraft-runtime.json", content)
        self.assertIn("Canonical repo source: recorded in `prodcraft-runtime.json`", content)
        self.assertNotIn(str(REPO_ROOT), content)
        self.assertIn(
            "A `pc-prodcraft` directory that contains only this `SKILL.md` is a valid gateway install",
            content,
        )
        self.assertIn("trust the current workspace as the source repository only when", content)
        self.assertIn(
            "do not claim that downstream skills such as `pc-code-review`, `pc-testing-strategy`, or `pc-security-audit` ran",
            content,
        )
        self.assertIn("default entry system for software-development tasks", content)
        self.assertIn("user explicitly chooses it", content)
        self.assertIn("skipping Prodcraft preserves the same lifecycle guarantees", content)

        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertEqual("installed", state["status"])
        self.assertEqual(str(skill_dir / "prodcraft-runtime.json"), state["runtime_locator_path"])

        locator = json.loads((skill_dir / "prodcraft-runtime.json").read_text(encoding="utf-8"))
        self.assertEqual("prodcraft-runtime-locator.v1", locator["schema_version"])
        self.assertEqual("pc-prodcraft", locator["skill_name"])
        self.assertEqual(str(REPO_ROOT), locator["canonical_repo_root"])
        self.assertEqual(str(REPO_ROOT / "skills" / "_gateway.md"), locator["gateway_path"])
        self.assertEqual(str(REPO_ROOT / "skills"), locator["source_skills_root"])
        self.assertEqual(str(REPO_ROOT / "workflows"), locator["workflow_root"])
        self.assertTrue(locator["singleton_gateway_directory_is_expected"])

        events = self.read_events()
        self.assertEqual(1, len(events))
        self.assertEqual("install", events[0]["action"])
        self.assertEqual("installed", events[0]["status_after"])

    def test_status_reports_installed_skill(self):
        self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="enable prodcraft globally",
        )

        result = self.module.get_status(
            target_root=self.skills_root,
            state_path=self.state_path,
        )

        self.assertEqual("installed", result["status"])
        self.assertTrue(result["skill_exists"])
        self.assertEqual(str(self.skills_root / "pc-prodcraft" / "prodcraft-runtime.json"), result["runtime_locator_path"])

    def test_status_reports_unmanaged_gateway_as_conflict(self):
        target = self.skills_root / "pc-prodcraft"
        target.mkdir()
        (target / "user.txt").write_text("not managed by Prodcraft", encoding="utf-8")

        result = self.module.get_status(
            target_root=self.skills_root,
            state_path=self.state_path,
        )

        self.assertEqual("conflict", result["status"])
        self.assertFalse(result["managed"])
        self.assertIn("unmanaged entries", result["conflict_reason"])

    def test_remove_deletes_skill_and_logs_event(self):
        self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="enable prodcraft globally",
        )

        result = self.module.remove_skill(
            target_root=self.skills_root,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="cleanup after experiment",
        )

        self.assertEqual("removed", result["status"])
        self.assertEqual("cleanup after experiment", result["reason"])
        self.assertEqual("remove", result["last_action"])
        self.assertFalse((self.skills_root / "pc-prodcraft").exists())

        events = self.read_events()
        self.assertEqual(["install", "remove"], [event["action"] for event in events])
        self.assertEqual("removed", events[-1]["status_after"])

    def test_install_migrates_only_locator_owned_legacy_gateway(self):
        legacy_dir = self.write_legacy_gateway()

        result = self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="migrate canonical prefix",
        )

        self.assertFalse(legacy_dir.exists())
        self.assertTrue((self.skills_root / "pc-prodcraft" / "SKILL.md").is_file())
        self.assertTrue(result["legacy_skill_removed"])

    def test_install_rejects_legacy_gateway_with_unmanaged_files_without_mutation(self):
        legacy_dir = self.write_legacy_gateway(extra_file=True)
        before = {
            path.relative_to(legacy_dir): path.read_bytes()
            for path in legacy_dir.rglob("*")
            if path.is_file()
        }

        with self.assertRaisesRegex(self.module.SkillInstallConflict, "unmanaged entries"):
            self.module.install_skill(
                target_root=self.skills_root,
                repo_root=REPO_ROOT,
                state_path=self.state_path,
                log_path=self.log_path,
                reason="migrate canonical prefix",
            )

        after = {
            path.relative_to(legacy_dir): path.read_bytes()
            for path in legacy_dir.rglob("*")
            if path.is_file()
        }
        self.assertEqual(before, after)
        self.assertFalse((self.skills_root / "pc-prodcraft").exists())
        self.assertFalse(self.state_path.exists())
        self.assertFalse(self.log_path.exists())

    def test_install_rejects_unowned_pc_prodcraft_without_overwrite(self):
        target = self.skills_root / "pc-prodcraft"
        target.mkdir()
        skill_path = target / "SKILL.md"
        skill_path.write_text("user managed", encoding="utf-8")

        with self.assertRaisesRegex(self.module.SkillInstallConflict, "not a managed"):
            self.module.install_skill(
                target_root=self.skills_root,
                repo_root=REPO_ROOT,
                state_path=self.state_path,
                log_path=self.log_path,
                reason="install canonical prefix",
            )

        self.assertEqual("user managed", skill_path.read_text(encoding="utf-8"))
        self.assertFalse(self.state_path.exists())
        self.assertFalse(self.log_path.exists())

    def test_install_rejects_symlinked_observability_files_without_mutation(self):
        for field in ("state", "log"):
            with self.subTest(field=field):
                victim = self.root / f"{field}-victim.txt"
                victim.write_text("preserve me", encoding="utf-8")
                state_path = self.root / f"{field}-state.json"
                log_path = self.root / f"{field}-events.jsonl"
                (state_path if field == "state" else log_path).symlink_to(victim)

                with self.assertRaisesRegex(self.module.SkillInstallConflict, "must not be a symlink"):
                    self.module.install_skill(
                        target_root=self.skills_root,
                        repo_root=REPO_ROOT,
                        state_path=state_path,
                        log_path=log_path,
                        reason="reject unsafe observability path",
                    )

                self.assertEqual("preserve me", victim.read_text(encoding="utf-8"))
                self.assertFalse((self.skills_root / "pc-prodcraft").exists())

    def test_install_rejects_symlinked_lock_file_without_mutation(self):
        victim = self.root / "lock-victim.txt"
        victim.write_text("preserve me", encoding="utf-8")
        (self.skills_root / self.module.LOCK_FILENAME).symlink_to(victim)

        with self.assertRaisesRegex(self.module.SkillInstallConflict, "installer lock is not a safe"):
            self.module.install_skill(
                target_root=self.skills_root,
                repo_root=REPO_ROOT,
                state_path=self.state_path,
                log_path=self.log_path,
                reason="reject unsafe lock",
            )

        self.assertEqual("preserve me", victim.read_text(encoding="utf-8"))
        self.assertFalse((self.skills_root / "pc-prodcraft").exists())

    def test_install_rejects_symlinked_observability_parent_without_mutation(self):
        for field in ("state", "log"):
            with self.subTest(field=field):
                outside = self.root / f"{field}-outside"
                outside.mkdir()
                victim = outside / f"{field}.json"
                victim.write_text("preserve me", encoding="utf-8")
                routed = self.root / f"{field}-routed"
                routed.symlink_to(outside, target_is_directory=True)
                state_path = routed / "state.json" if field == "state" else self.state_path
                log_path = routed / "log.json" if field == "log" else self.log_path

                with self.assertRaisesRegex(self.module.SkillInstallConflict, "contains a symlink"):
                    self.module.install_skill(
                        target_root=self.skills_root,
                        repo_root=REPO_ROOT,
                        state_path=state_path,
                        log_path=log_path,
                        reason="reject symlinked observability parent",
                    )

                self.assertEqual("preserve me", victim.read_text(encoding="utf-8"))
                self.assertFalse((self.skills_root / "pc-prodcraft").exists())

    def test_install_rejects_non_directory_observability_parent_before_migration(self):
        legacy_dir = self.write_legacy_gateway()
        blocked_parent = self.root / "blocked"
        blocked_parent.write_text("not a directory", encoding="utf-8")

        with self.assertRaisesRegex(self.module.SkillInstallConflict, "parent is not a directory"):
            self.module.install_skill(
                target_root=self.skills_root,
                repo_root=REPO_ROOT,
                state_path=blocked_parent / "state.json",
                log_path=self.log_path,
                reason="reject blocked state parent",
            )

        self.assertTrue(legacy_dir.exists())
        self.assertFalse((self.skills_root / "pc-prodcraft").exists())

    def test_install_restores_previous_gateway_when_interrupted_after_backup(self):
        self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="initial install",
        )
        target = self.skills_root / "pc-prodcraft"
        before = {
            path.relative_to(target): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }
        original_rename = Path.rename

        def interrupted_rename(path, destination):
            if path.name == "staged":
                raise KeyboardInterrupt("injected interruption")
            return original_rename(path, destination)

        with mock.patch.object(Path, "rename", interrupted_rename):
            with self.assertRaises(KeyboardInterrupt):
                self.module.install_skill(
                    target_root=self.skills_root,
                    repo_root=REPO_ROOT,
                    state_path=self.state_path,
                    log_path=self.log_path,
                    reason="interrupted reinstall",
                )

        after = {
            path.relative_to(target): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }
        self.assertEqual(before, after)

    def test_install_revalidates_gateway_after_atomic_move(self):
        self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="initial install",
        )
        target = self.skills_root / "pc-prodcraft"
        parked = self.root / "parked-managed-gateway"
        original_assert = self.module.assert_managed_gateway
        swapped = False

        def swap_after_validation(path, **kwargs):
            nonlocal swapped
            result = original_assert(path, **kwargs)
            if path == target and not swapped:
                target.rename(parked)
                target.mkdir()
                (target / "user.txt").write_text("preserve user data", encoding="utf-8")
                swapped = True
            return result

        with mock.patch.object(self.module, "assert_managed_gateway", swap_after_validation):
            with self.assertRaisesRegex(self.module.SkillInstallConflict, "unmanaged entries"):
                self.module.install_skill(
                    target_root=self.skills_root,
                    repo_root=REPO_ROOT,
                    state_path=self.state_path,
                    log_path=self.log_path,
                    reason="exercise swap defense",
                )

        self.assertEqual("preserve user data", (target / "user.txt").read_text(encoding="utf-8"))
        self.assertTrue(parked.exists())

    def test_fresh_install_preserves_directory_created_before_staged_rename(self):
        target = self.skills_root / "pc-prodcraft"
        original_rename = Path.rename

        def create_conflict_before_staged_rename(path, destination):
            if path.name == "staged":
                target.mkdir()
                (target / "user.txt").write_text("preserve user data", encoding="utf-8")
            return original_rename(path, destination)

        with mock.patch.object(Path, "rename", create_conflict_before_staged_rename):
            with self.assertRaises(OSError):
                self.module.install_skill(
                    target_root=self.skills_root,
                    repo_root=REPO_ROOT,
                    state_path=self.state_path,
                    log_path=self.log_path,
                    reason="exercise fresh install race defense",
                )

        self.assertEqual("preserve user data", (target / "user.txt").read_text(encoding="utf-8"))
        self.assertFalse(self.state_path.exists())
        self.assertFalse(self.log_path.exists())

    def test_install_rolls_back_gateway_and_observability_when_event_write_fails(self):
        with mock.patch.object(self.module, "log_event", side_effect=OSError("injected log failure")):
            with self.assertRaisesRegex(OSError, "injected log failure"):
                self.module.install_skill(
                    target_root=self.skills_root,
                    repo_root=REPO_ROOT,
                    state_path=self.state_path,
                    log_path=self.log_path,
                    reason="exercise observability rollback",
                )

        self.assertFalse((self.skills_root / "pc-prodcraft").exists())
        self.assertFalse(self.state_path.exists())
        self.assertFalse(self.log_path.exists())

    def test_reinstall_restores_previous_gateway_when_event_write_fails(self):
        self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="initial install",
        )
        target = self.skills_root / "pc-prodcraft"
        gateway_before = {
            path.relative_to(target): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }
        state_before = self.state_path.read_bytes()
        log_before = self.log_path.read_bytes()

        with mock.patch.object(self.module, "log_event", side_effect=OSError("injected log failure")):
            with self.assertRaisesRegex(OSError, "injected log failure"):
                self.module.install_skill(
                    target_root=self.skills_root,
                    repo_root=REPO_ROOT,
                    state_path=self.state_path,
                    log_path=self.log_path,
                    reason="failed reinstall",
                )

        gateway_after = {
            path.relative_to(target): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }
        self.assertEqual(gateway_before, gateway_after)
        self.assertEqual(state_before, self.state_path.read_bytes())
        self.assertEqual(log_before, self.log_path.read_bytes())

    def test_install_rejects_symlinked_legacy_gateway_without_mutation(self):
        external = self.root / "external-gateway"
        external.mkdir()
        marker = external / "marker.txt"
        marker.write_text("preserve me", encoding="utf-8")
        (self.skills_root / "prodcraft").symlink_to(external, target_is_directory=True)

        with self.assertRaisesRegex(self.module.SkillInstallConflict, "not a managed gateway directory"):
            self.module.install_skill(
                target_root=self.skills_root,
                repo_root=REPO_ROOT,
                state_path=self.state_path,
                log_path=self.log_path,
                reason="migrate canonical prefix",
            )

        self.assertEqual("preserve me", marker.read_text(encoding="utf-8"))
        self.assertFalse((self.skills_root / "pc-prodcraft").exists())
        self.assertFalse(self.state_path.exists())
        self.assertFalse(self.log_path.exists())

    def test_install_rejects_current_gateway_owned_by_another_repository(self):
        target = self.skills_root / "pc-prodcraft"
        target.mkdir()
        (target / "SKILL.md").write_text(
            "---\nname: pc-prodcraft\ndescription: managed-looking gateway\n---\n",
            encoding="utf-8",
        )
        locator_path = target / "prodcraft-runtime.json"
        locator_path.write_text(
            json.dumps(
                {
                    "schema_version": "prodcraft-runtime-locator.v1",
                    "skill_name": "pc-prodcraft",
                    "install_surface": "global",
                    "global_skill_path": str(target),
                    "canonical_repo_root": str(self.root / "another-repository"),
                }
            ),
            encoding="utf-8",
        )
        before = locator_path.read_text(encoding="utf-8")

        with self.assertRaisesRegex(self.module.SkillInstallConflict, "belongs to another repository"):
            self.module.install_skill(
                target_root=self.skills_root,
                repo_root=REPO_ROOT,
                state_path=self.state_path,
                log_path=self.log_path,
                reason="install canonical prefix",
            )

        self.assertEqual(before, locator_path.read_text(encoding="utf-8"))
        self.assertFalse(self.state_path.exists())
        self.assertFalse(self.log_path.exists())

    def test_remove_rejects_broken_symlink_instead_of_reporting_success(self):
        target = self.skills_root / "pc-prodcraft"
        target.symlink_to(self.root / "missing-target", target_is_directory=True)

        with self.assertRaisesRegex(self.module.SkillInstallConflict, "not a managed gateway directory"):
            self.module.remove_skill(
                target_root=self.skills_root,
                state_path=self.state_path,
                log_path=self.log_path,
                reason="remove canonical gateway",
            )

        self.assertTrue(target.is_symlink())
        self.assertFalse(self.state_path.exists())
        self.assertFalse(self.log_path.exists())

    def test_remove_rejects_blocked_observability_path_before_mutation(self):
        self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="initial install",
        )
        blocked_parent = self.root / "blocked-remove"
        blocked_parent.write_text("not a directory", encoding="utf-8")

        with self.assertRaisesRegex(self.module.SkillInstallConflict, "parent is not a directory"):
            self.module.remove_skill(
                target_root=self.skills_root,
                state_path=self.state_path,
                log_path=blocked_parent / "events.jsonl",
                reason="reject blocked event log",
            )

        self.assertTrue((self.skills_root / "pc-prodcraft").exists())

    def test_remove_restores_gateway_when_interrupted_after_quarantine(self):
        self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="initial install",
        )
        target = self.skills_root / "pc-prodcraft"
        original_rename = Path.rename
        interrupted = False

        def interrupted_rename(path, destination):
            nonlocal interrupted
            if path == target and not interrupted:
                interrupted = True
                original_rename(path, destination)
                raise KeyboardInterrupt("injected interruption")
            return original_rename(path, destination)

        with mock.patch.object(Path, "rename", interrupted_rename):
            with self.assertRaises(KeyboardInterrupt):
                self.module.remove_skill(
                    target_root=self.skills_root,
                    state_path=self.state_path,
                    log_path=self.log_path,
                    reason="interrupted remove",
                )

        self.assertTrue((target / "SKILL.md").is_file())
        self.assertTrue((target / "prodcraft-runtime.json").is_file())

    def test_remove_revalidates_gateway_after_atomic_move(self):
        self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="initial install",
        )
        target = self.skills_root / "pc-prodcraft"
        parked = self.root / "parked-remove-gateway"
        original_assert = self.module.assert_managed_gateway
        target_validations = 0

        def swap_after_second_validation(path, **kwargs):
            nonlocal target_validations
            result = original_assert(path, **kwargs)
            if path == target:
                target_validations += 1
                if target_validations == 2:
                    target.rename(parked)
                    target.mkdir()
                    (target / "user.txt").write_text("preserve user data", encoding="utf-8")
            return result

        with mock.patch.object(self.module, "assert_managed_gateway", swap_after_second_validation):
            with self.assertRaisesRegex(self.module.SkillInstallConflict, "unmanaged entries"):
                self.module.remove_skill(
                    target_root=self.skills_root,
                    state_path=self.state_path,
                    log_path=self.log_path,
                    reason="exercise remove swap defense",
                )

        self.assertEqual("preserve user data", (target / "user.txt").read_text(encoding="utf-8"))
        self.assertTrue(parked.exists())

    def test_remove_restores_gateway_and_observability_when_state_write_fails(self):
        self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="initial install",
        )
        target = self.skills_root / "pc-prodcraft"
        state_before = self.state_path.read_bytes()
        log_before = self.log_path.read_bytes()

        with mock.patch.object(self.module, "persist_state", side_effect=OSError("injected state failure")):
            with self.assertRaisesRegex(OSError, "injected state failure"):
                self.module.remove_skill(
                    target_root=self.skills_root,
                    state_path=self.state_path,
                    log_path=self.log_path,
                    reason="failed remove",
                )

        self.assertTrue((target / "SKILL.md").is_file())
        self.assertEqual(state_before, self.state_path.read_bytes())
        self.assertEqual(log_before, self.log_path.read_bytes())


if __name__ == "__main__":
    unittest.main()
