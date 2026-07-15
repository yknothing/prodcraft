from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import execution_state as execution_state_module
from tools.execution_state import (
    AUTHORITY_TERMINAL,
    canonical_json_digest,
    capture_git_worktree,
    claim_payload_projection,
    completion_basis_projection,
    terminal_authority_digest,
    validate_completion_attempts,
    validate_control_bundle,
    validate_execution_state_contract,
    validate_terminal_completion,
)


SHA = "sha256:" + "1" * 64


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def digest_record(record: dict) -> dict:
    payload = dict(record)
    payload.pop("record_digest", None)
    return {**record, "record_digest": canonical_json_digest(payload)}


def transition(sequence: int, source: str, target: str) -> dict:
    return digest_record(
        {
            "recorded_sequence": sequence,
            "record_digest": SHA,
            "from_state": source,
            "to_state": target,
            "occurred_at": "2026-07-10T00:00:00Z",
            "reason": f"{source} to {target}",
            "evidence_refs": [],
        }
    )


def phase_event(sequence: int, kind: str) -> dict:
    return digest_record(
        {
            "recorded_sequence": sequence,
            "record_digest": SHA,
            "kind": kind,
            "phase_index": 0,
            "phase": "04-implementation",
            "occurred_at": "2026-07-10T00:00:00Z",
            "evidence_refs": [],
        }
    )


class CompletionFixture(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmpdir.name)
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Prodcraft Test")
        (self.repo / "app.txt").write_text("governed work\n", encoding="utf-8")
        self.git("add", "app.txt")
        self.git("commit", "-qm", "initial")

        self.control = self.repo / ".prodcraft" / "artifacts" / "work-1"
        self.control.mkdir(parents=True)
        self.write("route-approval.json", {"approved": True})
        self.write("intake-brief.json", {"artifact": "intake-brief"})
        self.write("intake-approval.json", {"accepted": True})
        self.write("test-output.txt", "9 tests passed\n", raw=True)

        self.work_snapshot = capture_git_worktree(
            self.repo,
            excluded_control_root=self.control,
            captured_at="2026-07-10T00:00:00Z",
        )
        self.route = self.make_route()
        self.write("route-decision.r1.json", self.route)
        self.verification = self.make_verification()
        self.write("verification-record.json", self.verification)
        self.state = self.make_completed_state()

    def tearDown(self):
        self.tmpdir.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=self.repo,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def write(self, relative: str, payload, *, raw: bool = False) -> Path:
        path = self.control / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if raw:
            path.write_text(payload, encoding="utf-8")
        else:
            path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        return path

    def make_route(self) -> dict:
        route = {
            "artifact": "route-decision",
            "schema_version": "route-decision.v1",
            "status": "approved",
            "work_id": "work-1",
            "route_id": "route-1",
            "route_revision": 1,
            "route_digest": SHA,
            "entry_phase": "04-implementation",
            "workflow": {
                "primary": "agile-sprint",
                "overlays": ["brownfield"],
                "focus_sequence": ["04-implementation"],
            },
            "obligations": [
                {
                    "id": "intake-approved",
                    "artifact": "intake-brief",
                    "gate": {
                        "kind": "lifecycle_transition",
                        "from_state": "received",
                        "to_state": "routed",
                    },
                    "assurance": "approval_accepted",
                }
            ],
            "approved_by": "user",
            "approved_at": "2026-07-10T00:00:00Z",
            "approval_evidence": {
                "ref": "route-approval.json",
                "sha256": file_digest(self.control / "route-approval.json"),
            },
        }
        route["route_digest"] = canonical_json_digest(
            {key: value for key, value in route.items() if key != "route_digest"}
        )
        return route

    def make_verification(self) -> dict:
        work_id = self.work_snapshot["content_digest"]
        return {
            "artifact": "verification-record",
            "schema_version": "verification-record.v1",
            "status": "accepted",
            "claim": "Direction 2 implementation is complete",
            "claim_scope": "minimal execution loop",
            "verified_at": "2026-07-10T00:02:00Z",
            "work_state_ref": {
                "id": work_id,
                "kind": "git",
                "ref": self.work_snapshot["head"],
                "captured_at": self.work_snapshot["captured_at"],
                "status": self.work_snapshot["status"],
            },
            "evidence_refs": [
                {
                    "id": "focused-tests",
                    "kind": "test",
                    "ref": "../../this-is-opaque-not-a-local-path",
                    "captured_at": "2026-07-10T00:01:00Z",
                    "work_state_ref": work_id,
                }
            ],
            "checks_run": [
                {
                    "name": "focused tests",
                    "result": "passed",
                    "evidence_ref": "focused-tests",
                    "work_state_ref": work_id,
                }
            ],
            "passed": ["focused tests"],
            "failed": [],
            "remaining_unverified": [],
            "claim_may_be_made": True,
        }

    def make_completed_state(self) -> dict:
        intake_path = self.control / "intake-brief.json"
        approval_path = self.control / "intake-approval.json"
        events = [
            transition(2, "received", "routed"),
            transition(3, "routed", "gated"),
            transition(4, "gated", "executing"),
            transition(7, "executing", "completion_claimed"),
            transition(8, "completion_claimed", "verified"),
            transition(9, "verified", "completed"),
        ]
        verification_commitment = {
            "verification_record_ref": "verification-record.json",
            "verification_record_sha256": file_digest(
                self.control / "verification-record.json"
            ),
            "evidence_bindings": [
                {
                    "evidence_id": "focused-tests",
                    "local_ref": "test-output.txt",
                    "sha256": file_digest(self.control / "test-output.txt"),
                }
            ],
            "work_snapshot": self.work_snapshot,
        }
        attempt = {
            "attempt_id": "attempt-1",
            "attempt_revision": 1,
            "claim": self.verification["claim"],
            "claim_scope": self.verification["claim_scope"],
            "claim_digest": SHA,
            "completion_basis_digest": SHA,
            "claim_cut_sequence": 7,
            "route_id": self.route["route_id"],
            "route_revision": self.route["route_revision"],
            "route_digest": self.route["route_digest"],
            "work_snapshot": self.work_snapshot,
            "verification_commitment": verification_commitment,
            "claimed_at": "2026-07-10T00:00:00Z",
            "terminal_transitions": [
                {"recorded_sequence": 8, "record_digest": events[-2]["record_digest"]},
                {"recorded_sequence": 9, "record_digest": events[-1]["record_digest"]},
            ],
        }
        attempt["claim_digest"] = canonical_json_digest(claim_payload_projection(attempt))
        state = {
            "artifact": "execution-state",
            "schema_version": "execution-state.v1",
            "work_id": self.route["work_id"],
            "state_revision": 9,
            "updated_at": "2026-07-10T00:02:00Z",
            "route_binding": {
                "ref": "route-decision.r1.json",
                "route_id": self.route["route_id"],
                "route_revision": self.route["route_revision"],
                "route_digest": self.route["route_digest"],
            },
            "lifecycle_state": "completed",
            "workflow_cursor": {
                "phase_index": 0,
                "phase": "04-implementation",
                "checkpoint": "exited",
            },
            "lifecycle_transitions": events,
            "phase_events": [phase_event(5, "entered"), phase_event(6, "exited")],
            "artifact_bindings": [
                {
                    "recorded_sequence": 1,
                    "obligation_id": "intake-approved",
                    "artifact": "intake-brief",
                    "ref": "intake-brief.json",
                    "subject_sha256": file_digest(intake_path),
                    "assurance": "approval_accepted",
                    "approval": {
                        "status": "accepted",
                        "approver": "user",
                        "approved_at": "2026-07-10T00:00:00Z",
                        "subject_sha256": file_digest(intake_path),
                        "evidence": {
                            "ref": "intake-approval.json",
                            "sha256": file_digest(approval_path),
                        },
                    },
                }
            ],
            "block_contexts": [],
            "completion_attempts": [attempt],
            "current_completion_attempt_id": attempt["attempt_id"],
        }
        attempt["completion_basis_digest"] = canonical_json_digest(
            completion_basis_projection(state, attempt)
        )
        attempt["completion_binding"] = {
            "attempt_id": attempt["attempt_id"],
            "attempt_revision": attempt["attempt_revision"],
            "claim_digest": attempt["claim_digest"],
            "completion_basis_digest": attempt["completion_basis_digest"],
            "route_id": attempt["route_id"],
            "route_revision": attempt["route_revision"],
            "route_digest": attempt["route_digest"],
            "verification_record_ref": verification_commitment["verification_record_ref"],
            "verification_record_sha256": verification_commitment[
                "verification_record_sha256"
            ],
            "evidence_bindings": copy.deepcopy(verification_commitment["evidence_bindings"]),
            "terminal_transition_digests": [
                events[-2]["record_digest"],
                events[-1]["record_digest"],
            ],
            "work_snapshot": verification_commitment["work_snapshot"],
        }
        return state

    def state_result(self, state: dict, *, terminal_passed: bool = False):
        return validate_execution_state_contract(
            state,
            self.route,
            approved_route_digest=self.route["route_digest"],
            is_canonical_current=True,
            authority_mode=True,
            terminal_validation_passed=terminal_passed,
            approved_completion_digest=(
                terminal_authority_digest(state) if terminal_passed else None
            ),
        )

    def test_valid_completion_is_terminal_authorized_and_legacy_refs_stay_opaque(self):
        self.assertEqual([], validate_completion_attempts(self.state, self.route))
        self.assertEqual(
            [],
            validate_terminal_completion(
                self.state,
                self.route,
                control_root=self.control,
                repo_root=self.repo,
            ),
        )
        result = self.state_result(self.state, terminal_passed=True)
        self.assertEqual([], result.errors)
        self.assertEqual(AUTHORITY_TERMINAL, result.authority)

    def test_verification_digest_and_semantics_use_one_file_snapshot(self):
        invalid_verification = b"not valid JSON\n"
        invalid_digest = "sha256:" + hashlib.sha256(invalid_verification).hexdigest()
        state = copy.deepcopy(self.state)
        attempt = state["completion_attempts"][0]
        attempt["verification_commitment"]["verification_record_sha256"] = invalid_digest
        attempt["completion_binding"]["verification_record_sha256"] = invalid_digest

        verification_path = self.control / "verification-record.json"
        original_reader = execution_state_module._read_regular_file_bytes
        verification_reads = 0

        def alternating_reader(path: Path) -> bytes:
            nonlocal verification_reads
            if path == verification_path:
                verification_reads += 1
                if verification_reads == 1:
                    return invalid_verification
            return original_reader(path)

        with mock.patch(
            "tools.execution_state._read_regular_file_bytes",
            side_effect=alternating_reader,
        ):
            errors = validate_terminal_completion(
                state,
                self.route,
                control_root=self.control,
                repo_root=self.repo,
            )

        self.assertEqual(1, verification_reads)
        self.assertTrue(any("verification record is invalid" in error for error in errors), errors)

    def test_terminal_pin_binds_updated_at_and_verified_to_completed_requires_reapproval(self):
        completed_pin = terminal_authority_digest(self.state)
        timestamp_changed = copy.deepcopy(self.state)
        timestamp_changed["updated_at"] = "2030-01-01T00:00:00Z"
        self.assertNotEqual(completed_pin, terminal_authority_digest(timestamp_changed))
        timestamp_result = validate_execution_state_contract(
            timestamp_changed,
            self.route,
            approved_route_digest=self.route["route_digest"],
            approved_completion_digest=completed_pin,
            is_canonical_current=True,
            authority_mode=True,
            terminal_validation_passed=True,
        )
        self.assertTrue(
            any("completion pin" in error for error in timestamp_result.errors),
            timestamp_result.errors,
        )

        verified = copy.deepcopy(self.state)
        verified["state_revision"] = 8
        verified["updated_at"] = "2026-07-10T00:01:00Z"
        verified["lifecycle_state"] = "verified"
        verified["lifecycle_transitions"] = verified["lifecycle_transitions"][:-1]
        attempt = verified["completion_attempts"][0]
        attempt["terminal_transitions"] = attempt["terminal_transitions"][:-1]
        attempt["completion_binding"]["terminal_transition_digests"] = attempt[
            "completion_binding"
        ]["terminal_transition_digests"][:-1]
        verified_pin = terminal_authority_digest(verified)
        verified_result = validate_execution_state_contract(
            verified,
            self.route,
            approved_route_digest=self.route["route_digest"],
            approved_completion_digest=verified_pin,
            is_canonical_current=True,
            authority_mode=True,
            terminal_validation_passed=True,
        )
        self.assertEqual([], verified_result.errors)
        self.assertEqual(AUTHORITY_TERMINAL, verified_result.authority)
        self.assertNotEqual(verified_pin, completed_pin)

        completed_with_verified_pin = validate_execution_state_contract(
            self.state,
            self.route,
            approved_route_digest=self.route["route_digest"],
            approved_completion_digest=verified_pin,
            is_canonical_current=True,
            authority_mode=True,
            terminal_validation_passed=True,
        )
        self.assertTrue(
            any("completion pin" in error for error in completed_with_verified_pin.errors),
            completed_with_verified_pin.errors,
        )

    def test_claim_basis_transition_verification_evidence_and_work_mutations_fail(self):
        mutations = []

        claim = copy.deepcopy(self.state)
        claim["completion_attempts"][0]["claim"] = "a different claim"
        mutations.append(("claim_digest", claim, None))

        transition_changed = copy.deepcopy(self.state)
        transition_changed["lifecycle_transitions"][-1]["reason"] = "edited terminal reason"
        transition_changed["lifecycle_transitions"][-1] = digest_record(
            transition_changed["lifecycle_transitions"][-1]
        )
        mutations.append(("terminal transition", transition_changed, None))

        for expected, state, _ in mutations:
            with self.subTest(expected=expected):
                errors = [
                    *validate_completion_attempts(state, self.route),
                    *validate_terminal_completion(
                        state,
                        self.route,
                        control_root=self.control,
                        repo_root=self.repo,
                    ),
                ]
                self.assertTrue(any(expected in error for error in errors), errors)

        verification_path = self.control / "verification-record.json"
        verification_path.write_text("{}\n", encoding="utf-8")
        errors = validate_terminal_completion(
            self.state, self.route, control_root=self.control, repo_root=self.repo
        )
        self.assertTrue(any("verification record digest" in error for error in errors), errors)
        self.write("verification-record.json", self.verification)

        coordinated_verification = copy.deepcopy(self.state)
        changed_verification = copy.deepcopy(self.verification)
        changed_verification["evidence_refs"][0]["notes"] = "edited after approval"
        changed_path = self.write("verification-record.json", changed_verification)
        coordinated_verification["completion_attempts"][0]["completion_binding"][
            "verification_record_sha256"
        ] = file_digest(changed_path)
        errors = validate_terminal_completion(
            coordinated_verification,
            self.route,
            control_root=self.control,
            repo_root=self.repo,
        )
        self.assertTrue(any("verification commitment" in error for error in errors), errors)
        self.write("verification-record.json", self.verification)

        (self.control / "test-output.txt").write_text("changed\n", encoding="utf-8")
        errors = validate_terminal_completion(
            self.state, self.route, control_root=self.control, repo_root=self.repo
        )
        self.assertTrue(any("evidence binding" in error for error in errors), errors)
        self.write("test-output.txt", "9 tests passed\n", raw=True)

        coordinated_evidence = copy.deepcopy(self.state)
        evidence_path = self.write("test-output.txt", "coordinated change\n", raw=True)
        coordinated_evidence["completion_attempts"][0]["completion_binding"][
            "evidence_bindings"
        ][0]["sha256"] = file_digest(evidence_path)
        errors = validate_terminal_completion(
            coordinated_evidence,
            self.route,
            control_root=self.control,
            repo_root=self.repo,
        )
        self.assertTrue(any("verification commitment" in error for error in errors), errors)
        self.write("test-output.txt", "9 tests passed\n", raw=True)

        (self.repo / "app.txt").write_text("changed governed work\n", encoding="utf-8")
        errors = validate_terminal_completion(
            self.state, self.route, control_root=self.control, repo_root=self.repo
        )
        self.assertTrue(any("live work snapshot" in error for error in errors), errors)

    def test_completion_claim_requires_final_phase_exit(self):
        state = copy.deepcopy(self.state)
        state["state_revision"] = 7
        state["lifecycle_state"] = "completion_claimed"
        state["lifecycle_transitions"] = [
            transition(2, "received", "routed"),
            transition(3, "routed", "gated"),
            transition(4, "gated", "executing"),
            transition(7, "executing", "completion_claimed"),
        ]
        state["phase_events"] = []
        state.pop("workflow_cursor")
        state["artifact_bindings"][0]["recorded_sequence"] = 1
        attempt = state["completion_attempts"][0]
        attempt["terminal_transitions"] = []
        attempt.pop("completion_binding")
        attempt["claim_digest"] = canonical_json_digest(claim_payload_projection(attempt))
        attempt["completion_basis_digest"] = canonical_json_digest(
            completion_basis_projection(state, attempt)
        )

        result = self.state_result(state)
        self.assertTrue(any("final phase" in error for error in result.errors), result.errors)

    def test_coordinated_bundle_rewrite_still_fails_old_operator_completion_pin(self):
        old_pin = terminal_authority_digest(self.state)
        rewritten = copy.deepcopy(self.state)
        evidence_path = self.write("test-output.txt", "rewritten evidence\n", raw=True)
        attempt = rewritten["completion_attempts"][0]
        new_evidence_digest = file_digest(evidence_path)
        attempt["verification_commitment"]["evidence_bindings"][0][
            "sha256"
        ] = new_evidence_digest
        attempt["completion_binding"]["evidence_bindings"][0][
            "sha256"
        ] = new_evidence_digest
        attempt["claim_digest"] = canonical_json_digest(claim_payload_projection(attempt))
        attempt["completion_binding"]["claim_digest"] = attempt["claim_digest"]
        attempt["completion_basis_digest"] = canonical_json_digest(
            completion_basis_projection(rewritten, attempt)
        )
        attempt["completion_binding"]["completion_basis_digest"] = attempt[
            "completion_basis_digest"
        ]

        self.assertNotEqual(old_pin, terminal_authority_digest(rewritten))
        self.assertEqual(
            [],
            validate_terminal_completion(
                rewritten,
                self.route,
                control_root=self.control,
                repo_root=self.repo,
            ),
        )
        result = validate_execution_state_contract(
            rewritten,
            self.route,
            approved_route_digest=self.route["route_digest"],
            is_canonical_current=True,
            authority_mode=True,
            terminal_validation_passed=True,
            approved_completion_digest=old_pin,
        )
        self.assertTrue(any("completion pin" in error for error in result.errors), result.errors)

    def test_control_bundle_is_closed_and_every_authority_file_is_content_bound(self):
        state_path = self.write("execution-state.json", self.state)
        self.assertEqual(
            [],
            validate_control_bundle(
                self.control,
                state_path=state_path,
                state=self.state,
                route=self.route,
            ),
        )

        extra = self.control / "unbound-notes.txt"
        extra.write_text("not content bound\n", encoding="utf-8")
        errors = validate_control_bundle(
            self.control,
            state_path=state_path,
            state=self.state,
            route=self.route,
        )
        self.assertTrue(any("unbound control file" in error for error in errors), errors)
        extra.unlink()

        (self.control / "intake-brief.json").write_text("{}\n", encoding="utf-8")
        errors = validate_control_bundle(
            self.control,
            state_path=state_path,
            state=self.state,
            route=self.route,
        )
        self.assertTrue(any("intake-brief.json" in error and "digest" in error for error in errors), errors)

    def test_unreadable_control_directory_cannot_hide_unbound_files(self):
        state_path = self.write("execution-state.json", self.state)
        hidden = self.control / "hidden"
        hidden.mkdir()
        (hidden / "unbound.txt").write_text("hidden\n", encoding="utf-8")
        hidden.chmod(0)
        try:
            if hidden.exists() and os.access(hidden, os.R_OK):
                self.skipTest("current platform/user can still read chmod 000 directories")
            errors = validate_control_bundle(
                self.control,
                state_path=state_path,
                state=self.state,
                route=self.route,
            )
            self.assertTrue(any("fully enumerated" in error for error in errors), errors)
        finally:
            hidden.chmod(0o700)

    def test_rejected_attempt_is_immutable_history_before_retry(self):
        state = copy.deepcopy(self.state)
        rejected = state["completion_attempts"][0]
        rejected.pop("completion_binding")
        rejected_transition = transition(8, "completion_claimed", "rejected")
        rejected["terminal_transitions"] = [
            {
                "recorded_sequence": 8,
                "record_digest": rejected_transition["record_digest"],
            }
        ]
        state["lifecycle_transitions"] = [
            *state["lifecycle_transitions"][:4],
            rejected_transition,
            transition(9, "rejected", "gated"),
            transition(10, "gated", "executing"),
            transition(11, "executing", "completion_claimed"),
        ]
        state["state_revision"] = 11
        state["lifecycle_state"] = "completion_claimed"
        state["updated_at"] = "2026-07-10T00:03:00Z"

        retry = {
            "attempt_id": "attempt-2",
            "attempt_revision": 2,
            "claim": "Direction 2 retry is complete",
            "claim_scope": "minimal execution loop retry",
            "claim_digest": SHA,
            "completion_basis_digest": SHA,
            "claim_cut_sequence": 11,
            "route_id": self.route["route_id"],
            "route_revision": self.route["route_revision"],
            "route_digest": self.route["route_digest"],
            "work_snapshot": self.work_snapshot,
            "verification_commitment": {
                "verification_record_ref": "retry-verification-record.json",
                "verification_record_sha256": "sha256:" + "2" * 64,
                "evidence_bindings": [
                    {
                        "evidence_id": "retry-tests",
                        "local_ref": "retry-test-output.txt",
                        "sha256": "sha256:" + "2" * 64,
                    }
                ],
                "work_snapshot": self.work_snapshot,
            },
            "claimed_at": "2026-07-10T00:03:00Z",
            "terminal_transitions": [],
        }
        state["completion_attempts"].append(retry)
        state["current_completion_attempt_id"] = retry["attempt_id"]
        retry["claim_digest"] = canonical_json_digest(claim_payload_projection(retry))
        retry["completion_basis_digest"] = canonical_json_digest(
            completion_basis_projection(state, retry)
        )

        self.assertEqual([], validate_completion_attempts(state, self.route))
        result = self.state_result(state)
        self.assertEqual([], result.errors)

        overwritten = copy.deepcopy(state)
        overwritten["completion_attempts"][1]["attempt_revision"] = 1
        errors = validate_completion_attempts(overwritten, self.route)
        self.assertTrue(any("attempt_revision" in error for error in errors), errors)

        bound_rejection = copy.deepcopy(state)
        bound_rejection["completion_attempts"][0]["completion_binding"] = {
            "unexpected": "binding"
        }
        errors = validate_completion_attempts(bound_rejection, self.route)
        self.assertTrue(any("rejected attempt" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
