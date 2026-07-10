from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import execution_state as execution_state_module
from tools.execution_state import (
    StrictJSONError,
    WorktreeSnapshotError,
    capture_git_worktree,
    canonical_json_digest,
    file_sha256,
    load_strict_json,
    resolve_control_ref,
)


class StrictJSONTests(unittest.TestCase):
    def write(self, root: Path, text: str) -> Path:
        path = root / "instance.json"
        path.write_text(text, encoding="utf-8")
        return path

    def test_duplicate_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.write(Path(tmpdir), '{"route_id":"a","route_id":"b"}')
            with self.assertRaisesRegex(StrictJSONError, "duplicate JSON key"):
                load_strict_json(path)

    def test_nonportable_numbers_and_non_ascii_member_names_are_rejected(self):
        invalid_payloads = (
            '{"value":1.25}',
            '{"value":-0}',
            '{"value":9007199254740992}',
            '{"\u8def\u7531":"r1"}',
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            for payload in invalid_payloads:
                with self.subTest(payload=payload):
                    path = self.write(root, payload)
                    with self.assertRaises(StrictJSONError):
                        load_strict_json(path)

        for payload in ({"value": 1.25}, {"\u8def\u7531": "r1"}, {"value": 9007199254740992}):
            with self.subTest(canonical_payload=payload), self.assertRaises(ValueError):
                canonical_json_digest(payload)

    def test_valid_unicode_string_and_integer_boundary_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.write(
                Path(tmpdir),
                json.dumps({"label": "\u8def\u7531", "value": 9007199254740991}, ensure_ascii=False),
            )
            self.assertEqual(
                {"label": "\u8def\u7531", "value": 9007199254740991},
                load_strict_json(path),
            )

    def test_strict_loader_rejects_surrogates_symlinks_and_non_regular_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            surrogate = self.write(root, '{"value":"\\ud800"}')
            with self.assertRaisesRegex(StrictJSONError, "surrogate"):
                load_strict_json(surrogate)

            target = root / "target.json"
            target.write_text("{}\n", encoding="utf-8")
            linked = root / "linked.json"
            linked.symlink_to(target)
            with self.assertRaisesRegex(StrictJSONError, "symlink"):
                load_strict_json(linked)

            fifo = root / "state.json"
            os.mkfifo(fifo)
            with self.assertRaisesRegex(StrictJSONError, "regular file"):
                load_strict_json(fifo)

    def test_strict_loader_wraps_deep_nesting_and_huge_integer_failures(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            deep = self.write(root, '{"value":' + "[" * 1500 + "0" + "]" * 1500 + "}")
            with self.assertRaises(StrictJSONError):
                load_strict_json(deep)

            huge = self.write(root, '{"value":' + "9" * 5000 + "}")
            with self.assertRaises(StrictJSONError):
                load_strict_json(huge)

    def test_strict_loader_rejects_documents_above_the_size_limit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.write(Path(tmpdir), '{"value":"' + "x" * 64 + '"}')
            with mock.patch.object(execution_state_module, "STRICT_JSON_MAX_BYTES", 32):
                with self.assertRaisesRegex(StrictJSONError, "exceeds 32 bytes"):
                    load_strict_json(path)

    def test_content_digest_streams_without_whole_file_helper(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "evidence.bin"
            for size in (
                0,
                execution_state_module.FILE_HASH_CHUNK_BYTES,
                execution_state_module.FILE_HASH_CHUNK_BYTES + 1,
            ):
                with self.subTest(size=size):
                    content = b"x" * size
                    path.write_bytes(content)
                    with mock.patch(
                        "tools.execution_state._read_regular_file_bytes",
                        side_effect=AssertionError("whole-file helper used"),
                    ):
                        self.assertEqual(
                            "sha256:" + hashlib.sha256(content).hexdigest(),
                            file_sha256(path),
                        )


class ControlReferenceTests(unittest.TestCase):
    def test_ref_must_remain_inside_control_root_and_avoid_symlinks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "control"
            root.mkdir()
            (root / "evidence.json").write_text("{}", encoding="utf-8")
            outside = Path(tmpdir) / "outside.json"
            outside.write_text("{}", encoding="utf-8")

            self.assertEqual(
                root / "evidence.json",
                resolve_control_ref(root, "evidence.json"),
            )
            for ref in (
                "../outside.json",
                "/tmp/outside.json",
                "C:/outside.json",
                "a\\b",
                "file:x",
                "./evidence.json",
                "evidence.json/",
                "nested//evidence.json",
            ):
                with self.subTest(ref=ref), self.assertRaises(ValueError):
                    resolve_control_ref(root, ref)

            (root / "linked.json").symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "symlink"):
                resolve_control_ref(root, "linked.json")

            (root / "linked-dir").symlink_to(Path(tmpdir))
            with self.assertRaisesRegex(ValueError, "symlink"):
                resolve_control_ref(root, "linked-dir/outside.json")


class GitWorktreeSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Prodcraft Test")
        (self.root / "tracked.txt").write_text("v1\n", encoding="utf-8")
        (self.root / ".gitignore").write_text(".prodcraft/\n", encoding="utf-8")
        self.git("add", "tracked.txt", ".gitignore")
        self.git("commit", "-qm", "initial")
        self.control_root = self.root / ".prodcraft" / "artifacts" / "work-1"
        self.control_root.mkdir(parents=True)
        (self.control_root / "execution-state.json").write_text("{}", encoding="utf-8")

    def tearDown(self):
        self.tmpdir.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def capture(self) -> dict:
        return capture_git_worktree(
            self.root,
            excluded_control_root=self.control_root,
            captured_at="2026-07-10T00:00:00Z",
        )

    def test_current_control_root_is_excluded_but_other_work_roots_are_governed(self):
        baseline = self.capture()
        self.assertEqual("clean", baseline["status"])
        self.assertEqual(
            "sha256:39974239f285417fab813671b4c2a421348e3c0510753cb8fd697c895d0b132d",
            baseline["content_digest"],
        )

        (self.control_root / "execution-state.json").write_text('{"changed":true}', encoding="utf-8")
        control_changed = self.capture()
        self.assertEqual(baseline["content_digest"], control_changed["content_digest"])
        self.assertEqual("clean", control_changed["status"])

        other = self.root / ".prodcraft" / "artifacts" / "work-2"
        other.mkdir(parents=True)
        (other / "execution-state.json").write_text("{}", encoding="utf-8")
        other_changed = self.capture()
        self.assertNotEqual(baseline["content_digest"], other_changed["content_digest"])
        self.assertEqual("dirty", other_changed["status"])

    def test_tracked_untracked_symlink_target_and_mode_affect_digest(self):
        baseline = self.capture()["content_digest"]

        (self.root / "tracked.txt").write_text("v2\n", encoding="utf-8")
        tracked = self.capture()["content_digest"]
        self.assertNotEqual(baseline, tracked)

        (self.root / "untracked.txt").write_text("new\n", encoding="utf-8")
        untracked = self.capture()["content_digest"]
        self.assertNotEqual(tracked, untracked)

        link = self.root / "link"
        link.symlink_to("tracked.txt")
        linked = self.capture()["content_digest"]
        link.unlink()
        link.symlink_to("untracked.txt")
        self.assertNotEqual(linked, self.capture()["content_digest"])

        mode_before = self.capture()["content_digest"]
        os.chmod(self.root / "tracked.txt", os.stat(self.root / "tracked.txt").st_mode | stat.S_IXUSR)
        self.assertNotEqual(mode_before, self.capture()["content_digest"])

    def test_untracked_gitignore_info_exclude_and_special_files_fail_closed(self):
        (self.root / "nested").mkdir()
        (self.root / "nested" / ".gitignore").write_text("*.tmp\n", encoding="utf-8")
        with self.assertRaisesRegex(WorktreeSnapshotError, "untracked .gitignore"):
            self.capture()

        (self.root / "nested" / ".gitignore").unlink()
        (self.root / ".git" / "info" / "exclude").write_text("*.private\n", encoding="utf-8")
        with self.assertRaisesRegex(WorktreeSnapshotError, "info/exclude"):
            self.capture()

        (self.root / ".git" / "info" / "exclude").write_text("# comments only\n", encoding="utf-8")
        fifo = self.root / "unsupported.fifo"
        os.mkfifo(fifo)
        with self.assertRaisesRegex(WorktreeSnapshotError, "unsupported special file"):
            self.capture()

        fifo.unlink()
        info_exclude = self.root / ".git" / "info" / "exclude"
        info_exclude.unlink()
        os.mkfifo(info_exclude)
        with self.assertRaisesRegex(WorktreeSnapshotError, "regular non-symlink"):
            self.capture()

        info_exclude.unlink()
        info_exclude.write_text("# comments only\n", encoding="utf-8")
        index_path = self.root / ".git" / "index"
        index_path.unlink()
        os.mkfifo(index_path)
        with self.assertRaisesRegex(WorktreeSnapshotError, "Git index must be a regular"):
            self.capture()

    def test_info_exclude_uses_the_safe_descriptor_reader(self):
        info_exclude = self.root / ".git" / "info" / "exclude"
        info_exclude.write_text("# comments only\n", encoding="utf-8")
        with mock.patch.object(
            Path,
            "read_text",
            side_effect=AssertionError("Path.read_text used for Git metadata"),
        ):
            snapshot = self.capture()
        self.assertEqual("clean", snapshot["status"])

    def test_git_environment_and_snapshot_relevant_config_do_not_change_identity(self):
        baseline = self.capture()
        alternate_index = self.root / ".git" / "alternate-index"
        environment = os.environ.copy()
        environment["GIT_INDEX_FILE"] = str(alternate_index)
        subprocess.run(
            ["git", "read-tree", "--empty"],
            cwd=self.root,
            env=environment,
            check=True,
            capture_output=True,
        )
        with mock.patch.dict(os.environ, {"GIT_INDEX_FILE": str(alternate_index)}):
            self.assertEqual(baseline, self.capture())

        os.chmod(self.root / "tracked.txt", os.stat(self.root / "tracked.txt").st_mode | stat.S_IXUSR)
        self.git("config", "core.filemode", "false")
        filemode_false = self.capture()
        self.git("config", "core.filemode", "true")
        filemode_true = self.capture()
        self.assertEqual(filemode_false, filemode_true)
        self.assertEqual("dirty", filemode_true["status"])

    def test_unicode_and_case_config_do_not_change_snapshot_identity(self):
        self.git("config", "core.precomposeUnicode", "false")
        decomposed_name = "cafe\u0301.txt"
        (self.root / decomposed_name).write_text("unicode\n", encoding="utf-8")
        self.git("add", "--", decomposed_name)
        self.git("commit", "-qm", "add unicode path")
        unicode_false = self.capture()
        self.git("config", "core.precomposeUnicode", "true")
        unicode_true = self.capture()
        self.assertEqual(unicode_false, unicode_true)

        upper = self.root / "CaseOnly.txt"
        lower = self.root / "caseonly.txt"
        upper.write_text("case\n", encoding="utf-8")
        self.git("add", "CaseOnly.txt")
        self.git("commit", "-qm", "add case path")
        upper.rename(lower)
        self.git("config", "core.ignoreCase", "true")
        case_true = self.capture()
        self.git("config", "core.ignoreCase", "false")
        case_false = self.capture()
        self.assertEqual(case_true, case_false)
        self.assertEqual("dirty", case_false["status"])

    def test_replace_refs_do_not_change_snapshot_identity(self):
        (self.root / "tracked.txt").write_text("replacement tree\n", encoding="utf-8")
        self.git("add", "tracked.txt")
        replacement_tree = self.git("write-tree")
        replacement_commit = self.git("commit-tree", replacement_tree, "-m", "replacement")
        head = self.git("rev-parse", "HEAD")

        self.git("replace", head, replacement_commit)
        with_replace = self.capture()
        self.git("replace", "-d", head)
        without_replace = self.capture()

        self.assertEqual(with_replace, without_replace)
        self.assertEqual("dirty", without_replace["status"])

    def test_index_cannot_hide_content_that_differs_from_head_and_verified_worktree(self):
        (self.root / "tracked.txt").write_text("staged but not verified\n", encoding="utf-8")
        self.git("add", "tracked.txt")
        (self.root / "tracked.txt").write_text("v1\n", encoding="utf-8")

        with self.assertRaisesRegex(
            WorktreeSnapshotError,
            "index entry differs from both HEAD and governed worktree",
        ):
            self.capture()

    def test_fsmonitor_hook_is_never_executed(self):
        hook = self.root / "fsmonitor-hook.sh"
        marker = self.root / "fsmonitor-executed"
        hook.write_text(
            f"#!/bin/sh\ntouch {marker}\nprintf '0\\n'\n",
            encoding="utf-8",
        )
        hook.chmod(0o755)
        self.git("config", "core.fsmonitor", str(hook))

        self.capture()
        self.assertFalse(marker.exists())

    def test_git_command_timeout_fails_closed(self):
        self.assertEqual(300, execution_state_module.GIT_COMMAND_TIMEOUT_SECONDS)
        timeout = subprocess.TimeoutExpired(["git", "rev-parse"], timeout=5)
        with mock.patch("tools.execution_state.subprocess.run", side_effect=timeout):
            with self.assertRaisesRegex(WorktreeSnapshotError, "timed out"):
                self.capture()

    def test_worktree_capture_streams_without_path_read_bytes(self):
        with mock.patch.object(
            Path,
            "read_bytes",
            side_effect=AssertionError("Path.read_bytes used"),
        ):
            snapshot = self.capture()
        self.assertEqual("clean", snapshot["status"])

    def test_blocking_local_git_config_include_times_out(self):
        include_fifo = self.root / "blocking.gitconfig"
        os.mkfifo(include_fifo)
        with (self.root / ".git" / "config").open("a", encoding="utf-8") as config:
            config.write(f"\n[include]\n\tpath = {include_fifo}\n")

        with mock.patch("tools.execution_state.GIT_COMMAND_TIMEOUT_SECONDS", 0.2):
            with self.assertRaisesRegex(WorktreeSnapshotError, "timed out"):
                self.capture()

    def test_intermediate_symlink_and_uninitialized_submodule_fail_closed(self):
        tracked_dir = self.root / "tracked-dir"
        tracked_dir.mkdir()
        (tracked_dir / "payload.txt").write_text("inside\n", encoding="utf-8")
        self.git("add", "tracked-dir/payload.txt")
        self.git("commit", "-qm", "add nested file")

        with tempfile.TemporaryDirectory() as outside_tmpdir:
            outside = Path(outside_tmpdir)
            (outside / "payload.txt").write_text("outside\n", encoding="utf-8")
            (tracked_dir / "payload.txt").unlink()
            tracked_dir.rmdir()
            tracked_dir.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(WorktreeSnapshotError, "intermediate symlink"):
                self.capture()

        tracked_dir.unlink()
        head = self.git("rev-parse", "HEAD")
        self.git("update-index", "--add", "--cacheinfo", f"160000,{head},missing-submodule")
        with self.assertRaisesRegex(WorktreeSnapshotError, "submodule worktree is not initialized"):
            self.capture()

    def test_nested_submodule_config_and_index_flags_cannot_hide_dirty_content(self):
        with tempfile.TemporaryDirectory() as nested_tmpdir, tempfile.TemporaryDirectory() as mid_tmpdir:
            nested_source = Path(nested_tmpdir)
            mid_source = Path(mid_tmpdir)

            def run(repo: Path, *args: str) -> str:
                return subprocess.run(
                    ["git", *args],
                    cwd=repo,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()

            for repo in (nested_source, mid_source):
                run(repo, "init", "-q")
                run(repo, "config", "user.email", "test@example.com")
                run(repo, "config", "user.name", "Prodcraft Test")

            (nested_source / "payload.txt").write_text("nested\n", encoding="utf-8")
            run(nested_source, "add", "payload.txt")
            run(nested_source, "commit", "-qm", "nested initial")

            (mid_source / "mid.txt").write_text("mid\n", encoding="utf-8")
            run(mid_source, "add", "mid.txt")
            run(mid_source, "commit", "-qm", "mid initial")
            run(
                mid_source,
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "add",
                str(nested_source),
                "nested",
            )
            run(mid_source, "commit", "-qam", "add nested submodule")

            self.git(
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "add",
                str(mid_source),
                "mid",
            )
            self.git(
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "update",
                "--init",
                "--recursive",
            )
            self.git("commit", "-qam", "add mid submodule")

            mid_worktree = self.root / "mid"
            nested_worktree = mid_worktree / "nested"
            run(mid_worktree, "config", "submodule.nested.ignore", "all")
            run(nested_worktree, "update-index", "--assume-unchanged", "payload.txt")
            (nested_worktree / "payload.txt").write_text("hidden change\n", encoding="utf-8")

            with self.assertRaisesRegex(WorktreeSnapshotError, "submodule worktree is dirty"):
                self.capture()

    def test_unreadable_governed_directory_fails_closed_when_permissions_are_enforced(self):
        hidden = self.root / "hidden"
        hidden.mkdir()
        (hidden / "payload.txt").write_text("hidden\n", encoding="utf-8")
        hidden.chmod(0)
        try:
            if os.access(hidden, os.R_OK):
                self.skipTest("current platform/user can still read chmod 000 directories")
            with self.assertRaisesRegex(WorktreeSnapshotError, "enumerate governed worktree"):
                self.capture()
        finally:
            hidden.chmod(0o700)


if __name__ == "__main__":
    unittest.main()
