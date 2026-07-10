from __future__ import annotations

import unittest

from tools.execution_state import (
    AUTHORITY_GATE,
    AUTHORITY_STRUCTURAL,
    canonical_json_digest,
    validate_execution_state_contract,
    validate_route_decision_contract,
)


PHASES = {
    "00-discovery",
    "01-specification",
    "02-architecture",
    "03-planning",
    "04-implementation",
    "05-quality",
    "06-delivery",
    "07-operations",
    "08-evolution",
    "cross-cutting",
}
PRIMARY_WORKFLOWS = {"agile-sprint", "spec-driven", "iterative-waterfall"}
OVERLAYS = {"greenfield", "brownfield", "hotfix"}
ARTIFACTS = {"intake-brief", "requirements-doc", "architecture-doc", "verification-record"}
SHA = "sha256:" + "1" * 64


def digest_record(record: dict) -> dict:
    payload = dict(record)
    payload.pop("record_digest", None)
    return {**record, "record_digest": canonical_json_digest(payload)}


def make_route() -> dict:
    route = {
        "artifact": "route-decision",
        "schema_version": "route-decision.v1",
        "status": "approved",
        "work_id": "mel-review",
        "route_id": "route-mel",
        "route_revision": 1,
        "route_digest": SHA,
        "entry_phase": "01-specification",
        "workflow": {
            "primary": "agile-sprint",
            "overlays": ["brownfield"],
            "focus_sequence": ["01-specification"],
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
            },
            {
                "id": "requirements-present",
                "artifact": "requirements-doc",
                "gate": {
                    "kind": "phase_checkpoint",
                    "phase_index": 0,
                    "checkpoint": "entered",
                },
                "assurance": "presence",
            },
        ],
        "approved_by": "user",
        "approved_at": "2026-07-10T00:00:00Z",
        "approval_evidence": {"ref": "route-approval.json", "sha256": SHA},
    }
    route["route_digest"] = canonical_json_digest({k: v for k, v in route.items() if k != "route_digest"})
    return route


def approval_binding(sequence: int = 1) -> dict:
    return {
        "recorded_sequence": sequence,
        "obligation_id": "intake-approved",
        "artifact": "intake-brief",
        "ref": "intake-brief.json",
        "subject_sha256": SHA,
        "assurance": "approval_accepted",
        "approval": {
            "status": "accepted",
            "approver": "user",
            "approved_at": "2026-07-10T00:00:00Z",
            "subject_sha256": SHA,
            "evidence": {"ref": "intake-approval.json", "sha256": SHA},
        },
    }


def presence_binding(sequence: int) -> dict:
    return {
        "recorded_sequence": sequence,
        "obligation_id": "requirements-present",
        "artifact": "requirements-doc",
        "ref": "requirements.json",
        "subject_sha256": SHA,
        "assurance": "presence",
    }


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
            "phase": "01-specification",
            "occurred_at": "2026-07-10T00:00:00Z",
            "evidence_refs": [],
        }
    )


def make_routed_state(route: dict) -> dict:
    return {
        "artifact": "execution-state",
        "schema_version": "execution-state.v1",
        "work_id": route["work_id"],
        "state_revision": 2,
        "updated_at": "2026-07-10T00:00:00Z",
        "route_binding": {
            "ref": "route-decision.r1.json",
            "route_id": route["route_id"],
            "route_revision": route["route_revision"],
            "route_digest": route["route_digest"],
        },
        "lifecycle_state": "routed",
        "lifecycle_transitions": [transition(2, "received", "routed")],
        "phase_events": [],
        "artifact_bindings": [approval_binding(1)],
        "block_contexts": [],
        "completion_attempts": [],
    }


def make_executing_state(route: dict) -> dict:
    state = make_routed_state(route)
    state.update(
        {
            "state_revision": 7,
            "lifecycle_state": "executing",
            "workflow_cursor": {
                "phase_index": 0,
                "phase": "01-specification",
                "checkpoint": "exited",
            },
            "lifecycle_transitions": [
                transition(2, "received", "routed"),
                transition(3, "routed", "gated"),
                transition(4, "gated", "executing"),
            ],
            "artifact_bindings": [approval_binding(1), presence_binding(5)],
            "phase_events": [phase_event(6, "entered"), phase_event(7, "exited")],
        }
    )
    return state


class ExecutionStateValidatorTests(unittest.TestCase):
    def route_errors(self, route: dict) -> list[str]:
        return validate_route_decision_contract(
            route,
            phases=PHASES,
            primary_workflows=PRIMARY_WORKFLOWS,
            overlays=OVERLAYS,
            artifact_names=ARTIFACTS,
        )

    def state_result(
        self,
        state: dict,
        route: dict,
        *,
        pin: str | None = None,
        canonical: bool = True,
        authority_mode: bool = True,
    ):
        return validate_execution_state_contract(
            state,
            route,
            approved_route_digest=pin,
            is_canonical_current=canonical,
            authority_mode=authority_mode,
        )

    def test_valid_route_and_routed_state_are_gate_authorized_with_pin(self):
        route = make_route()
        self.assertEqual([], self.route_errors(route))

        result = self.state_result(make_routed_state(route), route, pin=route["route_digest"])
        self.assertEqual([], result.errors)
        self.assertEqual(AUTHORITY_GATE, result.authority)

    def test_route_focus_must_start_at_entry_phase(self):
        route = make_route()
        route["workflow"]["focus_sequence"] = ["02-architecture"]
        route["route_digest"] = canonical_json_digest({k: v for k, v in route.items() if k != "route_digest"})
        self.assertIn("focus_sequence[0] must equal entry_phase", self.route_errors(route))

    def test_route_obligation_rewrite_cannot_preserve_operator_authority(self):
        route = make_route()
        old_pin = route["route_digest"]
        route["obligations"] = [route["obligations"][0]]
        route["route_digest"] = canonical_json_digest({k: v for k, v in route.items() if k != "route_digest"})
        state = make_routed_state(route)

        result = self.state_result(state, route, pin=old_pin)
        self.assertTrue(any("operator pin" in error for error in result.errors))

    def test_no_pin_or_noncanonical_state_is_structural_only(self):
        route = make_route()
        state = make_routed_state(route)

        without_pin = self.state_result(state, route, pin=None, authority_mode=False)
        self.assertEqual([], without_pin.errors)
        self.assertEqual(AUTHORITY_STRUCTURAL, without_pin.authority)

        historical = self.state_result(
            state,
            route,
            pin=route["route_digest"],
            canonical=False,
            authority_mode=False,
        )
        self.assertEqual([], historical.errors)
        self.assertEqual(AUTHORITY_STRUCTURAL, historical.authority)

    def test_global_recorded_sequence_must_be_contiguous(self):
        route = make_route()
        state = make_executing_state(route)
        state["phase_events"][0]["recorded_sequence"] = 8

        result = self.state_result(state, route, pin=route["route_digest"])
        self.assertTrue(any("recorded_sequence" in error for error in result.errors))

    def test_phase_events_are_only_legal_while_executing(self):
        route = make_route()
        state = make_executing_state(route)
        state["phase_events"][0]["recorded_sequence"] = 3
        state["lifecycle_transitions"][1]["recorded_sequence"] = 6
        state["lifecycle_transitions"][1] = digest_record(state["lifecycle_transitions"][1])

        result = self.state_result(state, route, pin=route["route_digest"])
        self.assertTrue(any("phase event" in error and "executing" in error for error in result.errors))

    def test_reached_phase_obligation_must_be_bound_before_event(self):
        route = make_route()
        state = make_executing_state(route)
        state["artifact_bindings"] = [approval_binding(1)]
        state["state_revision"] = 6
        state["phase_events"] = [phase_event(5, "entered"), phase_event(6, "exited")]

        result = self.state_result(state, route, pin=route["route_digest"])
        self.assertTrue(any("requirements-present" in error for error in result.errors))

    def test_final_phase_exit_is_valid_without_out_of_range_cursor(self):
        route = make_route()
        state = make_executing_state(route)

        result = self.state_result(state, route, pin=route["route_digest"])
        self.assertEqual([], result.errors)
        self.assertEqual(AUTHORITY_GATE, result.authority)

    def test_phase_event_while_blocked_is_rejected(self):
        route = make_route()
        state = make_executing_state(route)
        state["state_revision"] = 9
        state["lifecycle_state"] = "blocked"
        state["lifecycle_transitions"].append(transition(8, "executing", "blocked"))
        state["phase_events"].append(phase_event(9, "entered"))
        state["block_contexts"] = [
            {"transition_sequence": 8, "reason": "blocked", "evidence_refs": []}
        ]

        result = self.state_result(state, route, pin=route["route_digest"])
        self.assertTrue(any("phase event" in error and "blocked" in error for error in result.errors))

    def test_block_resume_must_close_the_active_block_context(self):
        route = make_route()
        state = make_executing_state(route)
        state["state_revision"] = 9
        state["lifecycle_transitions"].extend(
            [
                transition(8, "executing", "blocked"),
                transition(9, "blocked", "executing"),
            ]
        )
        state["block_contexts"] = [
            {
                "transition_sequence": 8,
                "resume_transition_sequence": 9,
                "reason": "dependency unavailable",
                "evidence_refs": [],
            }
        ]

        valid = self.state_result(state, route, pin=route["route_digest"])
        self.assertEqual([], valid.errors)
        self.assertEqual(AUTHORITY_GATE, valid.authority)

        state["block_contexts"][0].pop("resume_transition_sequence")
        invalid = self.state_result(state, route, pin=route["route_digest"])
        self.assertTrue(any("resume" in error and "block_context" in error for error in invalid.errors))

    def test_artifact_binding_after_terminal_state_is_rejected(self):
        route = make_route()
        state = make_executing_state(route)
        state["state_revision"] = 9
        state["lifecycle_state"] = "rerouted"
        state["lifecycle_transitions"].append(transition(8, "executing", "rerouted"))
        state["artifact_bindings"].append(presence_binding(9))

        result = self.state_result(state, route, pin=route["route_digest"])
        self.assertTrue(
            any("artifact binding 9" in error and "rerouted" in error for error in result.errors),
            result.errors,
        )

    def test_rerouted_state_is_structural_only_until_successor_replaces_selector(self):
        route = make_route()
        state = make_executing_state(route)
        state["state_revision"] = 8
        state["lifecycle_state"] = "rerouted"
        state["lifecycle_transitions"].append(transition(8, "executing", "rerouted"))

        result = self.state_result(state, route, pin=route["route_digest"])
        self.assertEqual([], result.errors)
        self.assertEqual(AUTHORITY_STRUCTURAL, result.authority)


if __name__ == "__main__":
    unittest.main()
