from __future__ import annotations

import unittest
from pathlib import Path

from scripts import validate_prodcraft
from tests import test_execution_state_completion as completion_support
from tools.execution_state import terminal_authority_digest
from tools.execution_validation import (
    ValidationDisposition,
    authorize_execution_state,
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


if __name__ == "__main__":
    unittest.main()
