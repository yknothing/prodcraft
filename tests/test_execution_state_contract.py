from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "schemas" / "artifacts" / "registry.yml"
MANIFEST_PATH = REPO_ROOT / "manifest.yml"
ROUTE_SCHEMA_PATH = REPO_ROOT / "schemas" / "artifacts" / "route-decision.schema.json"
STATE_SCHEMA_PATH = REPO_ROOT / "schemas" / "artifacts" / "execution-state.schema.json"
ROUTE_TEMPLATE_PATH = REPO_ROOT / "templates" / "route-decision.md"
STATE_TEMPLATE_PATH = REPO_ROOT / "templates" / "execution-state.md"
VALIDATION_WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "validate-skills.yml"


class ExecutionStateContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
        self.manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_registry_and_manifest_register_additive_execution_artifacts(self):
        artifacts = self.registry["artifacts"]
        self.assertEqual("route-decision.v1", artifacts["route-decision"]["schema_version"])
        self.assertEqual("execution-state.v1", artifacts["execution-state"]["schema_version"])
        self.assertEqual(
            "schemas/artifacts/route-decision.schema.json",
            artifacts["route-decision"]["schema_path"],
        )
        self.assertEqual(
            "schemas/artifacts/execution-state.schema.json",
            artifacts["execution-state"]["schema_path"],
        )

        artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}
        self.assertEqual("intake", artifact_flow["route-decision"]["produced_by"])
        self.assertEqual(
            {"intake", "task-execution", "verification-before-completion"},
            set(artifact_flow["execution-state"]["produced_by"]),
        )
        self.assertIn("verification-before-completion", artifact_flow["route-decision"]["consumed_by"])
        self.assertIn("verification-before-completion", artifact_flow["execution-state"]["consumed_by"])

    def test_route_decision_schema_is_closed_and_authoritative(self):
        schema = json.loads(ROUTE_SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual("route-decision", schema["properties"]["artifact"]["const"])
        self.assertEqual("route-decision.v1", schema["properties"]["schema_version"]["const"])
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(
            {
                "artifact",
                "schema_version",
                "status",
                "work_id",
                "route_id",
                "route_revision",
                "route_digest",
                "entry_phase",
                "workflow",
                "obligations",
                "approved_by",
                "approved_at",
                "approval_evidence",
            },
            set(schema["required"]),
        )
        self.assertEqual("approved", schema["properties"]["status"]["const"])
        workflow = schema["properties"]["workflow"]
        self.assertFalse(workflow["additionalProperties"])
        self.assertEqual(1, workflow["properties"]["focus_sequence"]["minItems"])
        obligation = schema["properties"]["obligations"]["items"]
        self.assertFalse(obligation["additionalProperties"])
        self.assertEqual(
            {"presence", "structural_valid", "approval_accepted"},
            set(obligation["properties"]["assurance"]["enum"]),
        )

    def test_execution_state_schema_closes_product_automaton_shape(self):
        schema = json.loads(STATE_SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual("execution-state", schema["properties"]["artifact"]["const"])
        self.assertEqual("execution-state.v1", schema["properties"]["schema_version"]["const"])
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(
            {
                "artifact",
                "schema_version",
                "work_id",
                "state_revision",
                "updated_at",
                "route_binding",
                "lifecycle_state",
                "lifecycle_transitions",
                "phase_events",
                "artifact_bindings",
                "block_contexts",
                "completion_attempts",
            },
            set(schema["required"]),
        )
        self.assertEqual(0, schema["properties"]["phase_events"]["minItems"])
        self.assertNotIn("workflow_cursor", schema["required"])
        self.assertEqual(
            {
                "routed",
                "gated",
                "executing",
                "blocked",
                "completion_claimed",
                "verified",
                "rejected",
                "completed",
                "rerouted",
            },
            set(schema["properties"]["lifecycle_state"]["enum"]),
        )

    def test_templates_expose_all_required_fields(self):
        for schema_path, template_path in (
            (ROUTE_SCHEMA_PATH, ROUTE_TEMPLATE_PATH),
            (STATE_SCHEMA_PATH, STATE_TEMPLATE_PATH),
        ):
            with self.subTest(template=template_path):
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
                template = template_path.read_text(encoding="utf-8")
                for field in schema["required"]:
                    self.assertIn(field, template)

    def test_authority_core_changes_trigger_push_and_pull_request_validation(self):
        workflow = VALIDATION_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertGreaterEqual(workflow.count("- 'tools/**'"), 2)


if __name__ == "__main__":
    unittest.main()
