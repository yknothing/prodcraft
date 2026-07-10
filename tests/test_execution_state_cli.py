from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

try:
    from . import test_execution_state_completion as completion_support
except ImportError:
    import test_execution_state_completion as completion_support
from tools.execution_state import (
    STRICT_JSON_MAX_BYTES,
    canonical_json_digest,
    terminal_authority_digest,
)


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_prodcraft.py"


class ExecutionStateCLITests(unittest.TestCase):
    def setUp(self):
        self.fixture = completion_support.CompletionFixture(
            "test_valid_completion_is_terminal_authorized_and_legacy_refs_stay_opaque"
        )
        self.fixture.setUp()

    def tearDown(self):
        self.fixture.tearDown()

    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), *args],
            cwd=self.fixture.repo,
            capture_output=True,
            text=True,
            timeout=10,
        )

    def run_validator_json(self, *args: str) -> tuple[subprocess.CompletedProcess[str], dict]:
        result = self.run_validator(*args, "--output-format", "json")
        return result, json.loads(result.stdout)

    def write_state(self, state: dict) -> Path:
        return self.fixture.write("execution-state.json", state)

    def make_routed_state(self) -> dict:
        completed = self.fixture.state
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

    def test_authority_mode_emits_machine_distinct_gate_and_terminal_results(self):
        for stale_file in ("verification-record.json", "test-output.txt"):
            (self.fixture.control / stale_file).unlink()
        state_path = self.write_state(self.make_routed_state())
        gate = self.run_validator(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            self.fixture.route["route_digest"],
        )
        self.assertEqual(0, gate.returncode, gate.stdout + gate.stderr)
        self.assertIn("gate-authorized", gate.stdout)

        self.fixture.write("test-output.txt", "9 tests passed\n", raw=True)
        self.fixture.write("verification-record.json", self.fixture.verification)
        state_path = self.write_state(self.fixture.state)
        terminal = self.run_validator(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            self.fixture.route["route_digest"],
            "--approved-completion-digest",
            terminal_authority_digest(self.fixture.state),
        )
        self.assertEqual(0, terminal.returncode, terminal.stdout + terminal.stderr)
        self.assertIn("terminal-authorized", terminal.stdout)

        missing_completion_pin = self.run_validator(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            self.fixture.route["route_digest"],
        )
        self.assertNotEqual(0, missing_completion_pin.returncode)
        self.assertIn("operator completion pin", missing_completion_pin.stdout + missing_completion_pin.stderr)

    def test_json_output_distinguishes_structural_candidate_and_terminal_results(self):
        route_path = self.fixture.control / "route-decision.r1.json"
        structural, structural_payload = self.run_validator_json(
            "--artifact-instance",
            str(route_path),
        )
        self.assertEqual(0, structural.returncode)
        self.assertEqual(
            {
                "status": "valid",
                "authority": None,
                "candidate_completion_digest": None,
                "errors": [],
            },
            structural_payload,
        )

        state_path = self.write_state(self.fixture.state)
        completion_digest = terminal_authority_digest(self.fixture.state)
        candidate, candidate_payload = self.run_validator_json(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            self.fixture.route["route_digest"],
        )
        self.assertEqual(1, candidate.returncode)
        self.assertEqual("invalid", candidate_payload["status"])
        self.assertIsNone(candidate_payload["authority"])
        self.assertEqual(
            completion_digest,
            candidate_payload["candidate_completion_digest"],
        )
        self.assertEqual(1, len(candidate_payload["errors"]))
        self.assertIn("operator completion pin", candidate_payload["errors"][0])

        self.fixture.write("test-output.txt", "mutated after verification\n", raw=True)
        invalid, invalid_payload = self.run_validator_json(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            self.fixture.route["route_digest"],
        )
        self.assertEqual(1, invalid.returncode)
        self.assertEqual("invalid", invalid_payload["status"])
        self.assertIsNone(invalid_payload["candidate_completion_digest"])
        self.assertTrue(
            any("evidence binding" in error for error in invalid_payload["errors"]),
            invalid_payload["errors"],
        )
        self.fixture.write("test-output.txt", "9 tests passed\n", raw=True)

        unbound_path = self.fixture.control / "unbound.txt"
        unbound_path.write_text("not part of the closed bundle\n", encoding="utf-8")
        unbound, unbound_payload = self.run_validator_json(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            self.fixture.route["route_digest"],
        )
        self.assertEqual(1, unbound.returncode)
        self.assertIsNone(unbound_payload["candidate_completion_digest"])
        self.assertTrue(
            any("unbound control file" in error for error in unbound_payload["errors"]),
            unbound_payload["errors"],
        )
        self.assertFalse(
            any("candidate completion digest" in error for error in unbound_payload["errors"]),
            unbound_payload["errors"],
        )
        unbound_text = self.run_validator(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            self.fixture.route["route_digest"],
        )
        self.assertEqual(1, unbound_text.returncode)
        self.assertNotIn(
            "candidate completion digest",
            unbound_text.stdout + unbound_text.stderr,
        )
        unbound_path.unlink()

        terminal, terminal_payload = self.run_validator_json(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            self.fixture.route["route_digest"],
            "--approved-completion-digest",
            completion_digest,
        )
        self.assertEqual(0, terminal.returncode)
        self.assertEqual(
            {
                "status": "valid",
                "authority": "terminal-authorized",
                "candidate_completion_digest": None,
                "errors": [],
            },
            terminal_payload,
        )

    def test_missing_pin_mismatch_historical_duplicate_json_and_unbound_file_fail_closed(self):
        state_path = self.write_state(self.fixture.state)

        missing = self.run_validator("--authorize-execution-state", str(state_path))
        self.assertNotEqual(0, missing.returncode)
        self.assertIn("approved-route-digest", missing.stdout + missing.stderr)

        mismatch = self.run_validator(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            "sha256:" + "0" * 64,
        )
        self.assertNotEqual(0, mismatch.returncode)
        self.assertIn("operator pin", mismatch.stdout + mismatch.stderr)

        historical_path = self.fixture.control / "history" / "execution-state.json"
        historical_path.parent.mkdir()
        historical_path.write_bytes(state_path.read_bytes())
        historical = self.run_validator(
            "--authorize-execution-state",
            str(historical_path),
            "--approved-route-digest",
            self.fixture.route["route_digest"],
        )
        self.assertNotEqual(0, historical.returncode)
        self.assertIn("canonical current", historical.stdout + historical.stderr)
        historical_path.unlink()
        historical_path.parent.rmdir()

        (self.fixture.control / "unbound.txt").write_text("unbound\n", encoding="utf-8")
        unbound = self.run_validator(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            self.fixture.route["route_digest"],
        )
        self.assertNotEqual(0, unbound.returncode)
        self.assertIn("unbound control file", unbound.stdout + unbound.stderr)
        (self.fixture.control / "unbound.txt").unlink()

        route_path = self.fixture.control / "route-decision.r1.json"
        renamed_route = self.fixture.control / "arbitrary-route.json"
        route_path.rename(renamed_route)
        state = copy.deepcopy(self.fixture.state)
        state["route_binding"]["ref"] = renamed_route.name
        self.write_state(state)
        noncanonical_route = self.run_validator(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            self.fixture.route["route_digest"],
            "--approved-completion-digest",
            "sha256:" + "0" * 64,
        )
        self.assertNotEqual(0, noncanonical_route.returncode)
        self.assertIn("canonical route filename", noncanonical_route.stdout + noncanonical_route.stderr)
        renamed_route.rename(route_path)
        self.write_state(self.fixture.state)

        state_path.write_text(
            '{"artifact":"execution-state","artifact":"route-decision"}\n',
            encoding="utf-8",
        )
        duplicate = self.run_validator(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            self.fixture.route["route_digest"],
        )
        self.assertNotEqual(0, duplicate.returncode)
        self.assertIn("duplicate JSON key", duplicate.stdout + duplicate.stderr)

    def test_generic_artifact_inspection_checks_route_semantics_without_emitting_authority(self):
        route = copy.deepcopy(self.fixture.route)
        route["workflow"]["focus_sequence"] = ["05-quality"]
        route["route_digest"] = canonical_json_digest(
            {key: value for key, value in route.items() if key != "route_digest"}
        )
        path = self.fixture.repo / "invalid-route.json"
        path.write_text(json.dumps(route) + "\n", encoding="utf-8")
        result = self.run_validator("--artifact-instance", str(path))
        self.assertNotEqual(0, result.returncode)
        self.assertIn("focus_sequence[0] must equal entry_phase", result.stdout + result.stderr)
        self.assertNotIn("authorized", result.stdout + result.stderr)

        path.write_text('{"artifact":"route-decision","artifact":"execution-state"}\n')
        duplicate = self.run_validator("--artifact-instance", str(path))
        self.assertNotEqual(0, duplicate.returncode)
        self.assertIn("duplicate JSON key", duplicate.stdout + duplicate.stderr)

        path.write_text(
            '{"artifact":"route-decision","approved_by":"\\ud800"}\n',
            encoding="utf-8",
        )
        surrogate = self.run_validator("--artifact-instance", str(path))
        self.assertNotEqual(0, surrogate.returncode)
        self.assertIn("surrogate", surrogate.stdout + surrogate.stderr)
        self.assertNotIn("Traceback", surrogate.stdout + surrogate.stderr)

        invalid_time = copy.deepcopy(self.fixture.route)
        invalid_time["approved_at"] = "not-a-date"
        invalid_time["route_digest"] = canonical_json_digest(
            {key: value for key, value in invalid_time.items() if key != "route_digest"}
        )
        path.write_text(json.dumps(invalid_time) + "\n")
        timestamp = self.run_validator("--artifact-instance", str(path))
        self.assertNotEqual(0, timestamp.returncode)
        self.assertIn("not a 'date-time'", timestamp.stdout + timestamp.stderr)

        yaml_path = self.fixture.repo / "route.yaml"
        yaml_path.write_text(
            "artifact: route-decision\nschema_version: route-decision.v1\n",
            encoding="utf-8",
        )
        yaml_result = self.run_validator("--artifact-instance", str(yaml_path))
        self.assertNotEqual(0, yaml_result.returncode)
        self.assertIn("must use JSON", yaml_result.stdout + yaml_result.stderr)

    def test_generic_artifact_inspection_rejects_fifo_without_blocking(self):
        path = self.fixture.repo / "state.json"
        os.mkfifo(path)
        result = self.run_validator("--artifact-instance", str(path))
        self.assertNotEqual(0, result.returncode)
        self.assertIn("regular file", result.stdout + result.stderr)

    def test_authority_entry_rejects_oversized_json_before_parsing(self):
        path = self.fixture.repo / "oversized-route.json"
        with path.open("wb") as handle:
            handle.seek(STRICT_JSON_MAX_BYTES)
            handle.write(b" ")
        result = self.run_validator(
            "--authorize-execution-state",
            str(path),
            "--approved-route-digest",
            "sha256:" + "0" * 64,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn(
            f"exceeds {STRICT_JSON_MAX_BYTES} bytes",
            result.stdout + result.stderr,
        )

    def test_generic_artifact_inspection_preserves_large_legacy_documents(self):
        path = self.fixture.repo / "large-intake-brief.json"
        payload = {
            "artifact": "intake-brief",
            "schema_version": "intake-brief.v1",
            "status": "approved",
            "request_summary": "x" * (STRICT_JSON_MAX_BYTES + 1),
            "source_language": "en",
            "artifact_record_language": "en",
            "user_presentation_locale": "zh",
            "intake_mode": "full",
            "work_type": "New Feature",
            "entry_phase": "01-specification",
            "quality_target_context": {
                "runtime_context": "internal_service",
                "exposure_profile": "private_network",
                "production_target": "Internal workflow",
                "non_targets": [],
                "evidence_refs": [],
            },
            "workflow_primary": "agile-sprint",
            "scope_assessment": "medium",
            "recommended_next_skill": "requirements-engineering",
            "routing_rationale": "Existing feature work starts in specification.",
            "key_risks": [],
            "questions_asked": [],
            "routing_changed_by_answers": False,
            "approver": "user",
        }
        path.write_text(json.dumps(payload), encoding="utf-8")
        result = self.run_validator("--artifact-instance", str(path))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_reroute_requires_valid_predecessor_chain_and_archived_state_binding(self):
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
        temporary_archive = self.fixture.write("history/archive.tmp.json", archived)
        archive_digest = "sha256:" + hashlib.sha256(temporary_archive.read_bytes()).hexdigest()
        archive_path = temporary_archive.with_name(
            f"execution-state.r1.s7.{archive_digest.removeprefix('sha256:')}.json"
        )
        temporary_archive.rename(archive_path)

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
        self.fixture.write("route-decision.r2.json", route2)

        state2 = self.make_routed_state()
        state2["route_binding"] = {
            "ref": "route-decision.r2.json",
            "route_id": route2["route_id"],
            "route_revision": route2["route_revision"],
            "route_digest": route2["route_digest"],
        }
        state2["previous_execution"] = {
            "ref": f"history/{archive_path.name}",
            "sha256": archive_digest,
            "lifecycle_state": "rerouted",
        }
        state_path = self.write_state(state2)

        valid = self.run_validator(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            route2["route_digest"],
        )
        self.assertEqual(0, valid.returncode, valid.stdout + valid.stderr)
        self.assertIn("gate-authorized", valid.stdout)

        archived_authority = self.run_validator(
            "--authorize-execution-state",
            str(archive_path),
            "--approved-route-digest",
            self.fixture.route["route_digest"],
        )
        self.assertNotEqual(0, archived_authority.returncode)
        self.assertIn("canonical current", archived_authority.stdout + archived_authority.stderr)

        noncanonical_archive = self.fixture.control / "not-content-addressed.json"
        archive_path.rename(noncanonical_archive)
        state2["previous_execution"]["ref"] = noncanonical_archive.name
        self.write_state(state2)
        bad_archive_name = self.run_validator(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            route2["route_digest"],
        )
        self.assertNotEqual(0, bad_archive_name.returncode)
        self.assertIn("canonical content-addressed history filename", bad_archive_name.stdout + bad_archive_name.stderr)
        noncanonical_archive.rename(archive_path)
        state2["previous_execution"]["ref"] = f"history/{archive_path.name}"
        self.write_state(state2)

        route2["previous_route"]["digest"] = "sha256:" + "0" * 64
        route2["route_digest"] = canonical_json_digest(
            {key: value for key, value in route2.items() if key != "route_digest"}
        )
        self.fixture.write("route-decision.r2.json", route2)
        state2["route_binding"]["route_digest"] = route2["route_digest"]
        self.write_state(state2)
        broken_chain = self.run_validator(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            route2["route_digest"],
        )
        self.assertNotEqual(0, broken_chain.returncode)
        self.assertIn("previous_route.digest", broken_chain.stdout + broken_chain.stderr)

    def test_generic_execution_state_inspection_replays_product_automaton_without_authority(self):
        for stale_file in ("verification-record.json", "test-output.txt"):
            (self.fixture.control / stale_file).unlink()
        state = self.make_routed_state()
        state["lifecycle_transitions"][0]["from_state"] = "gated"
        state["lifecycle_transitions"][0] = completion_support.digest_record(
            state["lifecycle_transitions"][0]
        )
        state_path = self.write_state(state)

        result = self.run_validator("--artifact-instance", str(state_path))
        self.assertNotEqual(0, result.returncode)
        self.assertIn("replay state", result.stdout + result.stderr)
        self.assertNotIn("authorized", result.stdout + result.stderr)

    def test_route_obligations_accept_manifest_artifacts_without_registered_schemas(self):
        route = copy.deepcopy(self.fixture.route)
        route["obligations"].append(
            {
                "id": "architecture-present",
                "artifact": "architecture-doc",
                "gate": {
                    "kind": "phase_checkpoint",
                    "phase_index": 0,
                    "checkpoint": "exited",
                },
                "assurance": "presence",
            }
        )
        route["route_digest"] = canonical_json_digest(
            {key: value for key, value in route.items() if key != "route_digest"}
        )
        path = self.fixture.repo / "route-with-manifest-artifact.json"
        path.write_text(json.dumps(route) + "\n", encoding="utf-8")

        result = self.run_validator("--artifact-instance", str(path))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("authorized", result.stdout + result.stderr)

    def test_structural_assurance_replays_subject_semantics_not_only_schema(self):
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
        self.fixture.write("route-decision.r1.json", route)

        invalid_subject = copy.deepcopy(route)
        invalid_subject["workflow"]["focus_sequence"] = ["05-quality"]
        invalid_subject["route_digest"] = canonical_json_digest(
            {key: value for key, value in invalid_subject.items() if key != "route_digest"}
        )
        subject_path = self.fixture.write("invalid-route-subject.json", invalid_subject)
        evidence_path = self.fixture.write("structural-validation.json", {"result": "passed"})

        state = self.make_routed_state()
        state["state_revision"] = 4
        state["lifecycle_state"] = "gated"
        state["route_binding"]["route_digest"] = route["route_digest"]
        state["artifact_bindings"].append(
            {
                "recorded_sequence": 3,
                "obligation_id": "route-subject-valid",
                "artifact": "route-decision",
                "ref": subject_path.name,
                "subject_sha256": completion_support.file_digest(subject_path),
                "assurance": "structural_valid",
                "structural_evidence": {
                    "validator_id": "prodcraft",
                    "validator_version": "1",
                    "check_set": ["artifact-contract"],
                    "result": "passed",
                    "evidence": {
                        "ref": evidence_path.name,
                        "sha256": completion_support.file_digest(evidence_path),
                    },
                },
            }
        )
        state["lifecycle_transitions"].append(
            completion_support.transition(4, "routed", "gated")
        )
        state_path = self.write_state(state)

        result = self.run_validator(
            "--authorize-execution-state",
            str(state_path),
            "--approved-route-digest",
            route["route_digest"],
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("focus_sequence[0] must equal entry_phase", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
