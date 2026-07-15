from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import validate_prodcraft
from tests import test_execution_state_completion as completion_support
from tools import execution_state as execution_state_module
from tools.execution_state import (
    canonical_json_digest,
    file_sha256,
    terminal_authority_digest,
    validate_control_bundle,
)
from tools.execution_validation import (
    CandidateBundleView,
    ValidationDisposition,
    authorize_execution_state,
    validate_execution_candidate,
    validate_registered_artifact_payload,
    validate_verification_record_instance_contract,
)


class ExecutionValidationServiceTests(unittest.TestCase):
    def setUp(self):
        self.fixture = completion_support.CompletionFixture(
            "test_valid_completion_is_terminal_authorized_and_legacy_refs_stay_opaque"
        )
        self.fixture.setUp()

    def tearDown(self):
        self.fixture.tearDown()

    def test_registered_artifact_validation_is_repository_owned(self):
        errors: list[str] = []

        valid = validate_registered_artifact_payload(
            self.fixture.route,
            self.fixture.control / "route-decision.r1.json",
            errors,
        )

        self.assertTrue(valid)
        self.assertEqual([], errors)

    def test_validation_service_owns_moved_contracts_without_importing_cli(self):
        self.assertEqual(
            "tools.execution_validation",
            validate_registered_artifact_payload.__module__,
        )
        self.assertEqual(
            "tools.execution_validation",
            validate_verification_record_instance_contract.__module__,
        )
        service_source = Path(__file__).parents[1] / "tools" / "execution_validation.py"
        self.assertNotIn("scripts.validate_prodcraft", service_source.read_text())

    def test_cli_directly_reexports_legacy_validation_imports(self):
        self.assertIs(
            validate_registered_artifact_payload,
            validate_prodcraft.validate_registered_artifact_payload,
        )
        self.assertIs(
            validate_verification_record_instance_contract,
            validate_prodcraft.validate_verification_record_instance_contract,
        )

    def test_missing_completion_pin_has_typed_approval_required_disposition(self):
        state_path = self.fixture.write("execution-state.json", self.fixture.state)
        errors: list[str] = []

        outcome = authorize_execution_state(
            state_path,
            self.fixture.route["route_digest"],
            None,
            errors,
        )

        self.assertEqual(ValidationDisposition.APPROVAL_REQUIRED, outcome.disposition)
        self.assertIsNone(outcome.authority)
        self.assertEqual(
            terminal_authority_digest(self.fixture.state),
            outcome.candidate_completion_digest,
        )
        self.assertEqual(1, len(errors))
        self.assertIn("operator completion pin", errors[0])

    def test_outer_error_suppresses_candidate_without_parsing_error_text(self):
        state_path = self.fixture.write("execution-state.json", self.fixture.state)
        errors = ["outer validation failed"]

        outcome = authorize_execution_state(
            state_path,
            self.fixture.route["route_digest"],
            None,
            errors,
        )

        self.assertEqual(ValidationDisposition.INVALID, outcome.disposition)
        self.assertIsNone(outcome.authority)
        self.assertIsNone(outcome.candidate_completion_digest)
        self.assertEqual(["outer validation failed"], errors)

    def test_candidate_bundle_view_overrides_adds_removes_and_enumerates(self):
        replacement = b'{"approved": false}\n'
        view = CandidateBundleView(
            self.fixture.control,
            overrides={
                "route-approval.json": replacement,
                "new-evidence.json": b'{"new": true}\n',
            },
            removals={"test-output.txt"},
        )

        self.assertEqual(replacement, view.read_bytes("route-approval.json"))
        self.assertEqual(
            "sha256:" + hashlib.sha256(replacement).hexdigest(),
            view.sha256("route-approval.json"),
        )
        self.assertEqual(b'{"new": true}\n', view.read_bytes("new-evidence.json"))
        self.assertIn("new-evidence.json", view.iter_relative_files())
        self.assertNotIn("test-output.txt", view.iter_relative_files())
        with self.assertRaisesRegex(ValueError, "removed"):
            view.read_bytes("test-output.txt")

    def test_candidate_bundle_view_rejects_unsafe_or_conflicting_paths(self):
        unsafe_paths = (
            "../escape.json",
            "/absolute.json",
            "file:///tmp/evidence.json",
            "C:/evidence.json",
            "nested\\evidence.json",
            "nested//evidence.json",
        )
        for path in unsafe_paths:
            with self.subTest(path=path), self.assertRaises(ValueError):
                CandidateBundleView(
                    self.fixture.control,
                    overrides={path: b"{}\n"},
                )

        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaisesRegex(ValueError, "control root cannot be inspected"):
                CandidateBundleView(Path(tmpdir) / "missing")

        with self.assertRaisesRegex(ValueError, "both overridden and removed"):
            CandidateBundleView(
                self.fixture.control,
                overrides={"route-approval.json": b"{}\n"},
                removals={"route-approval.json"},
            )

        for overrides in (
            {"future": b"parent\n", "future/child.json": b"{}\n"},
            {"future/child.json": b"{}\n", "future": b"parent\n"},
        ):
            with self.subTest(overrides=tuple(overrides)), self.assertRaisesRegex(
                ValueError, "ancestor and descendant"
            ):
                CandidateBundleView(self.fixture.control, overrides=overrides)

        nested = CandidateBundleView(
            self.fixture.control,
            overrides={"missing-parent/evidence.json": b"{}\n"},
        )
        self.assertEqual(b"{}\n", nested.read_bytes("missing-parent/evidence.json"))
        self.assertIn("missing-parent/evidence.json", nested.iter_relative_files())
        with self.assertRaisesRegex(ValueError, "does not resolve"):
            CandidateBundleView(
                self.fixture.control,
                removals={"missing.json"},
            )

        linked = self.fixture.control / "unsafe-live.json"
        linked.symlink_to(self.fixture.control / "route-approval.json")
        try:
            with self.assertRaisesRegex(ValueError, "symlink"):
                CandidateBundleView(
                    self.fixture.control,
                    overrides={linked.name: b"{}\n"},
                )
        finally:
            linked.unlink()

    def test_candidate_live_hash_stays_streamed_and_live_strict_reads_are_bounded(self):
        live_ref = "route-approval.json"
        view = CandidateBundleView(self.fixture.control)
        expected_digest = file_sha256(self.fixture.control / live_ref)
        with mock.patch.object(
            CandidateBundleView,
            "read_bytes",
            side_effect=AssertionError("live hash must not buffer through read_bytes"),
        ):
            self.assertEqual(expected_digest, view.sha256(live_ref))

        oversized = self.fixture.control / "oversized.json"
        oversized.write_bytes(b" " * (execution_state_module.STRICT_JSON_MAX_BYTES + 1))
        try:
            with self.assertRaisesRegex(ValueError, "exceeds 16777216 bytes"):
                view.read_bytes(oversized.name)
        finally:
            oversized.unlink()

    def test_candidate_overlay_matches_materialized_legacy_filesystem_validation(self):
        for stale_file in ("verification-record.json", "test-output.txt"):
            (self.fixture.control / stale_file).unlink()
        state = ExecutionStateCLIFixture.routed_state(self.fixture.state)
        state_path = self.fixture.write("execution-state.json", state)
        scenarios = (
            (
                "override",
                {"intake-approval.json": b'{"accepted": false}\n'},
                set(),
                "digest mismatch",
            ),
            ("add", {"unbound.json": b"{}\n"}, set(), "unbound control file"),
            (
                "nested-add",
                {"history/unbound.json": b"{}\n"},
                set(),
                "unbound control file",
            ),
            ("remove", {}, {"intake-brief.json"}, "does not resolve"),
        )
        for name, overrides, removals, expected_fragment in scenarios:
            with self.subTest(name=name):
                candidate = validate_execution_candidate(
                    repo_root=self.fixture.repo,
                    control_root=self.fixture.control,
                    state_path=state_path,
                    state=state,
                    route=self.fixture.route,
                    view=CandidateBundleView(
                        self.fixture.control,
                        overrides=overrides,
                        removals=removals,
                    ),
                    approved_route_digest=self.fixture.route["route_digest"],
                )

                with tempfile.TemporaryDirectory() as tmpdir:
                    isolated_root = Path(tmpdir) / "work-1"
                    shutil.copytree(self.fixture.control, isolated_root)
                    for relative, content in overrides.items():
                        isolated_path = isolated_root / relative
                        isolated_path.parent.mkdir(parents=True, exist_ok=True)
                        isolated_path.write_bytes(content)
                    for relative in removals:
                        (isolated_root / relative).unlink()
                    isolated = validate_execution_candidate(
                        repo_root=self.fixture.repo,
                        control_root=isolated_root,
                        state_path=isolated_root / "execution-state.json",
                        state=state,
                        route=self.fixture.route,
                        view=CandidateBundleView(isolated_root),
                        approved_route_digest=self.fixture.route["route_digest"],
                    )

                changed_paths = set(overrides) | removals
                originals = {
                    relative: (self.fixture.control / relative).read_bytes()
                    if (self.fixture.control / relative).exists()
                    else None
                    for relative in changed_paths
                }
                try:
                    for relative, content in overrides.items():
                        materialized_path = self.fixture.control / relative
                        materialized_path.parent.mkdir(parents=True, exist_ok=True)
                        materialized_path.write_bytes(content)
                    for relative in removals:
                        (self.fixture.control / relative).unlink()
                    legacy_errors: list[str] = []
                    materialized = authorize_execution_state(
                        state_path,
                        self.fixture.route["route_digest"],
                        None,
                        legacy_errors,
                    )
                finally:
                    for relative, original in originals.items():
                        materialized_path = self.fixture.control / relative
                        if original is None:
                            materialized_path.unlink(missing_ok=True)
                            parent = materialized_path.parent
                            if parent != self.fixture.control and not any(parent.iterdir()):
                                parent.rmdir()
                        else:
                            materialized_path.parent.mkdir(parents=True, exist_ok=True)
                            materialized_path.write_bytes(original)

                self.assertTrue(candidate.errors)
                self.assertEqual(candidate.errors, isolated.errors)
                self.assertEqual(ValidationDisposition.INVALID, candidate.disposition)
                self.assertEqual(ValidationDisposition.INVALID, materialized.disposition)
                self.assertTrue(
                    any(expected_fragment in error for error in candidate.errors),
                    candidate.errors,
                )
                self.assertTrue(
                    any(expected_fragment in error for error in legacy_errors),
                    legacy_errors,
                )

    def test_empty_candidate_view_matches_materialized_completed_bundle(self):
        state_path = self.fixture.write("execution-state.json", self.fixture.state)
        pin = terminal_authority_digest(self.fixture.state)

        candidate = validate_execution_candidate(
            repo_root=self.fixture.repo,
            control_root=self.fixture.control,
            state_path=state_path,
            state=self.fixture.state,
            route=self.fixture.route,
            view=CandidateBundleView(self.fixture.control),
            approved_route_digest=self.fixture.route["route_digest"],
            approved_completion_digest=pin,
        )

        self.assertEqual(ValidationDisposition.VALID, candidate.disposition)
        self.assertEqual("terminal-authorized", candidate.authority)
        self.assertEqual((), candidate.errors)

    def test_candidate_rejects_structural_only_authority_like_legacy_filesystem(self):
        for stale_file in ("verification-record.json", "test-output.txt"):
            (self.fixture.control / stale_file).unlink()
        rerouted = copy.deepcopy(self.fixture.state)
        rerouted["state_revision"] = 7
        rerouted["lifecycle_state"] = "rerouted"
        rerouted["updated_at"] = "2026-07-10T00:03:00Z"
        rerouted["lifecycle_transitions"] = [
            *rerouted["lifecycle_transitions"][:3],
            completion_support.transition(7, "executing", "rerouted"),
        ]
        rerouted["completion_attempts"] = []
        rerouted.pop("current_completion_attempt_id")
        state_path = self.fixture.write("execution-state.json", rerouted)

        candidate = validate_execution_candidate(
            repo_root=self.fixture.repo,
            control_root=self.fixture.control,
            state_path=state_path,
            state=rerouted,
            route=self.fixture.route,
            view=CandidateBundleView(self.fixture.control),
            approved_route_digest=self.fixture.route["route_digest"],
        )
        legacy_errors: list[str] = []
        legacy = authorize_execution_state(
            state_path,
            self.fixture.route["route_digest"],
            None,
            legacy_errors,
        )

        self.assertEqual(ValidationDisposition.INVALID, candidate.disposition)
        self.assertEqual(ValidationDisposition.INVALID, legacy.disposition)
        self.assertTrue(any("structural-only" in error for error in candidate.errors))
        self.assertTrue(any("structural-only" in error for error in legacy_errors))

    def test_candidate_addition_is_unbound_and_bound_removal_is_unreadable(self):
        for stale_file in ("verification-record.json", "test-output.txt"):
            (self.fixture.control / stale_file).unlink()
        state = ExecutionStateCLIFixture.routed_state(self.fixture.state)
        state_path = self.fixture.write("execution-state.json", state)

        added = validate_execution_candidate(
            repo_root=self.fixture.repo,
            control_root=self.fixture.control,
            state_path=state_path,
            state=state,
            route=self.fixture.route,
            view=CandidateBundleView(
                self.fixture.control,
                overrides={"unbound.json": b"{}\n"},
            ),
            approved_route_digest=self.fixture.route["route_digest"],
        )
        self.assertTrue(any("unbound control file" in error for error in added.errors))

        removed = validate_execution_candidate(
            repo_root=self.fixture.repo,
            control_root=self.fixture.control,
            state_path=state_path,
            state=state,
            route=self.fixture.route,
            view=CandidateBundleView(
                self.fixture.control,
                removals={"intake-brief.json"},
            ),
            approved_route_digest=self.fixture.route["route_digest"],
        )
        self.assertTrue(
            any("does not resolve" in error for error in removed.errors),
            removed.errors,
        )

    def test_candidate_strict_document_limit_applies_to_overlay_bytes(self):
        oversized = b'{"artifact":"execution-state","padding":"' + b"x" * 128 + b'"}\n'
        with mock.patch.object(execution_state_module, "STRICT_JSON_MAX_BYTES", 64):
            result = validate_execution_candidate(
                repo_root=self.fixture.repo,
                control_root=self.fixture.control,
                state_path=self.fixture.control / "execution-state.json",
                state=self.fixture.state,
                route=self.fixture.route,
                view=CandidateBundleView(
                    self.fixture.control,
                    overrides={"execution-state.json": oversized},
                ),
                approved_route_digest=self.fixture.route["route_digest"],
            )

        self.assertTrue(any("exceeds 64 bytes" in error for error in result.errors), result.errors)

    def test_candidate_route_and_state_overrides_are_the_validation_source(self):
        for stale_file in ("verification-record.json", "test-output.txt"):
            (self.fixture.control / stale_file).unlink()
        route = copy.deepcopy(self.fixture.route)
        route["approved_by"] = "review-board"
        route["route_digest"] = canonical_json_digest(
            {key: value for key, value in route.items() if key != "route_digest"}
        )
        state = ExecutionStateCLIFixture.routed_state(self.fixture.state)
        state["route_binding"]["route_digest"] = route["route_digest"]
        overrides = {
            "route-decision.r1.json": self.json_bytes(route),
            "execution-state.json": self.json_bytes(state),
        }

        result = validate_execution_candidate(
            repo_root=self.fixture.repo,
            control_root=self.fixture.control,
            state_path=self.fixture.control / "execution-state.json",
            state=state,
            route=route,
            view=CandidateBundleView(self.fixture.control, overrides=overrides),
            approved_route_digest=route["route_digest"],
        )

        self.assertEqual((), result.errors)
        self.assertEqual("gate-authorized", result.authority)

        mismatched_state = copy.deepcopy(state)
        mismatched_state["updated_at"] = "2026-07-10T00:01:00Z"
        mismatch = validate_execution_candidate(
            repo_root=self.fixture.repo,
            control_root=self.fixture.control,
            state_path=self.fixture.control / "not-the-selector.json",
            state=mismatched_state,
            route=self.fixture.route,
            view=CandidateBundleView(self.fixture.control, overrides=overrides),
            approved_route_digest=route["route_digest"],
        )
        self.assertTrue(
            any("canonical" in error for error in mismatch.errors),
            mismatch.errors,
        )
        self.assertTrue(
            any("supplied state payload" in error for error in mismatch.errors),
            mismatch.errors,
        )
        self.assertTrue(
            any("supplied route payload" in error for error in mismatch.errors),
            mismatch.errors,
        )

    def test_candidate_terminal_verification_and_evidence_overrides_are_used(self):
        state_path = self.fixture.write("execution-state.json", self.fixture.state)
        cases = {
            "verification-record.json": b"{}\n",
            "test-output.txt": b"changed evidence\n",
        }
        for relative, replacement in cases.items():
            with self.subTest(relative=relative):
                result = validate_execution_candidate(
                    repo_root=self.fixture.repo,
                    control_root=self.fixture.control,
                    state_path=state_path,
                    state=self.fixture.state,
                    route=self.fixture.route,
                    view=CandidateBundleView(
                        self.fixture.control,
                        overrides={relative: replacement},
                    ),
                    approved_route_digest=self.fixture.route["route_digest"],
                    approved_completion_digest=terminal_authority_digest(self.fixture.state),
                )
                self.assertTrue(
                    any("digest" in error for error in result.errors),
                    result.errors,
                )

    def test_candidate_predecessor_route_and_history_overrides_are_used(self):
        for stale_file in ("verification-record.json", "test-output.txt"):
            (self.fixture.control / stale_file).unlink()
        archived = copy.deepcopy(self.fixture.state)
        archived["state_revision"] = 7
        archived["lifecycle_state"] = "rerouted"
        archived["updated_at"] = "2026-07-10T00:03:00Z"
        archived["lifecycle_transitions"] = [
            *archived["lifecycle_transitions"][:3],
            completion_support.transition(7, "executing", "rerouted"),
        ]
        archived["completion_attempts"] = []
        archived.pop("current_completion_attempt_id")
        archived_bytes = self.json_bytes(archived)
        archive_digest = "sha256:" + hashlib.sha256(archived_bytes).hexdigest()
        archive_ref = (
            "history/execution-state.r1.s7."
            f"{archive_digest.removeprefix('sha256:')}.json"
        )
        (self.fixture.control / "history").mkdir()

        route2 = copy.deepcopy(self.fixture.route)
        route2["route_revision"] = 2
        route2["previous_route"] = {
            "revision": 1,
            "digest": self.fixture.route["route_digest"],
            "ref": "route-decision.r1.json",
        }
        route2["route_digest"] = canonical_json_digest(
            {key: value for key, value in route2.items() if key != "route_digest"}
        )
        state2 = ExecutionStateCLIFixture.routed_state(self.fixture.state)
        state2["route_binding"] = {
            "ref": "route-decision.r2.json",
            "route_id": route2["route_id"],
            "route_revision": 2,
            "route_digest": route2["route_digest"],
        }
        state2["previous_execution"] = {
            "ref": archive_ref,
            "sha256": archive_digest,
            "lifecycle_state": "rerouted",
        }
        overrides = {
            "route-decision.r2.json": self.json_bytes(route2),
            "execution-state.json": self.json_bytes(state2),
            archive_ref: archived_bytes,
        }

        result = validate_execution_candidate(
            repo_root=self.fixture.repo,
            control_root=self.fixture.control,
            state_path=self.fixture.control / "execution-state.json",
            state=state2,
            route=route2,
            view=CandidateBundleView(self.fixture.control, overrides=overrides),
            approved_route_digest=route2["route_digest"],
        )

        self.assertEqual((), result.errors)
        self.assertEqual("gate-authorized", result.authority)

        broken_predecessor = validate_execution_candidate(
            repo_root=self.fixture.repo,
            control_root=self.fixture.control,
            state_path=self.fixture.control / "execution-state.json",
            state=state2,
            route=route2,
            view=CandidateBundleView(
                self.fixture.control,
                overrides={
                    **overrides,
                    "route-decision.r1.json": b"{}\n",
                },
            ),
            approved_route_digest=route2["route_digest"],
        )
        self.assertTrue(
            any("predecessor" in error for error in broken_predecessor.errors),
            broken_predecessor.errors,
        )

        archive_path = self.fixture.control / archive_ref
        archive_path.write_bytes(archived_bytes)
        without_archive = dict(overrides)
        without_archive.pop(archive_ref)
        removed_archive = validate_execution_candidate(
            repo_root=self.fixture.repo,
            control_root=self.fixture.control,
            state_path=self.fixture.control / "execution-state.json",
            state=state2,
            route=route2,
            view=CandidateBundleView(
                self.fixture.control,
                overrides=without_archive,
                removals={archive_ref},
            ),
            approved_route_digest=route2["route_digest"],
        )
        self.assertTrue(
            any("does not resolve" in error for error in removed_archive.errors),
            removed_archive.errors,
        )

    def test_candidate_structural_subject_override_is_replayed(self):
        for stale_file in ("verification-record.json", "test-output.txt"):
            (self.fixture.control / stale_file).unlink()
        route = copy.deepcopy(self.fixture.route)
        route["obligations"].append(
            {
                "id": "route-subject-valid",
                "artifact": "route-decision",
                "gate": {
                    "kind": "lifecycle_transition",
                    "from_state": "routed",
                    "to_state": "gated",
                },
                "assurance": "structural_valid",
            }
        )
        route["route_digest"] = canonical_json_digest(
            {key: value for key, value in route.items() if key != "route_digest"}
        )
        subject = copy.deepcopy(route)
        subject_bytes = self.json_bytes(subject)
        subject_digest = "sha256:" + hashlib.sha256(subject_bytes).hexdigest()
        state = ExecutionStateCLIFixture.routed_state(self.fixture.state)
        state["route_binding"]["route_digest"] = route["route_digest"]
        state["state_revision"] = 4
        state["lifecycle_state"] = "gated"
        state["artifact_bindings"].append(
            {
                "recorded_sequence": 3,
                "obligation_id": "route-subject-valid",
                "artifact": "route-decision",
                "ref": "route-subject.json",
                "subject_sha256": subject_digest,
                "assurance": "structural_valid",
                "structural_evidence": {
                    "validator_id": "prodcraft",
                    "validator_version": "1",
                    "check_set": ["artifact-contract"],
                    "result": "passed",
                    "evidence": {
                        "ref": "route-approval.json",
                        "sha256": self.fixture.route["approval_evidence"]["sha256"],
                    },
                },
            }
        )
        state["lifecycle_transitions"].append(
            completion_support.transition(4, "routed", "gated")
        )
        overrides = {
            "route-decision.r1.json": self.json_bytes(route),
            "route-subject.json": subject_bytes,
            "execution-state.json": self.json_bytes(state),
        }

        result = validate_execution_candidate(
            repo_root=self.fixture.repo,
            control_root=self.fixture.control,
            state_path=self.fixture.control / "execution-state.json",
            state=state,
            route=route,
            view=CandidateBundleView(self.fixture.control, overrides=overrides),
            approved_route_digest=route["route_digest"],
        )

        self.assertEqual((), result.errors)
        self.assertEqual("gate-authorized", result.authority)

    def test_empty_view_rejects_symlink_fifo_and_socket_entries(self):
        for kind in ("symlink", "fifo", "socket"):
            with self.subTest(kind=kind):
                path = self.fixture.control / f"unsafe-{kind}"
                cleanup = None
                if kind == "symlink":
                    path.symlink_to(self.fixture.control / "route-approval.json")
                elif kind == "fifo":
                    os.mkfifo(path)
                else:
                    import socket

                    cleanup = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    cleanup.bind(str(path))
                try:
                    with self.assertRaisesRegex(ValueError, "symlink|unsupported file type"):
                        CandidateBundleView(self.fixture.control).iter_relative_files()
                finally:
                    if cleanup is not None:
                        cleanup.close()
                    path.unlink()

    def test_empty_view_reports_enumeration_races_as_validation_errors(self):
        with mock.patch(
            "tools.execution_state.os.walk",
            return_value=[(str(self.fixture.control), [], ["vanished.json"])],
        ):
            with self.assertRaisesRegex(ValueError, "cannot be inspected"):
                CandidateBundleView(self.fixture.control).iter_relative_files()

    def test_default_bundle_validation_preserves_legacy_multi_error_aggregation(self):
        state_path = self.fixture.write("execution-state.json", self.fixture.state)
        symlink = self.fixture.control / "unsafe-symlink"
        fifo = self.fixture.control / "unsafe-fifo"
        symlink.symlink_to(self.fixture.control / "route-approval.json")
        os.mkfifo(fifo)
        try:
            errors = validate_control_bundle(
                self.fixture.control,
                state_path=state_path,
                state=self.fixture.state,
                route=self.fixture.route,
            )
        finally:
            symlink.unlink()
            fifo.unlink()

        self.assertTrue(any("symlink file: unsafe-symlink" in error for error in errors), errors)
        self.assertTrue(
            any("unsupported file type: unsafe-fifo" in error for error in errors),
            errors,
        )

    def test_validation_module_does_not_reverse_import_the_cli(self):
        source = (Path(__file__).parents[1] / "tools" / "execution_validation.py").read_text()
        self.assertNotIn("scripts.validate_prodcraft", source)

    @staticmethod
    def json_bytes(payload: dict) -> bytes:
        return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode()


class ExecutionStateCLIFixture:
    @staticmethod
    def routed_state(completed: dict) -> dict:
        return {
            "artifact": completed["artifact"],
            "schema_version": completed["schema_version"],
            "work_id": completed["work_id"],
            "state_revision": 2,
            "updated_at": completed["updated_at"],
            "route_binding": completed["route_binding"],
            "lifecycle_state": "routed",
            "lifecycle_transitions": [completed["lifecycle_transitions"][0]],
            "phase_events": [],
            "artifact_bindings": completed["artifact_bindings"],
            "block_contexts": [],
            "completion_attempts": [],
        }


if __name__ == "__main__":
    unittest.main()
