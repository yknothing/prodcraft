from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

try:
    import jsonschema
except ImportError:  # pragma: no cover - exercised only when optional dependency is absent
    jsonschema = None


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import validate_prodcraft  # noqa: E402
from scripts.validate_prodcraft import (  # noqa: E402
    validate_protocol_result_instance,
    validate_protocol_result_registry,
)


PROTOCOL_DIR = REPO_ROOT / "schemas" / "protocol"
REGISTRY_PATH = PROTOCOL_DIR / "registry.yml"
SHA256_A = "sha256:" + ("a" * 64)
SHA256_B = "sha256:" + ("b" * 64)


def authority_fixture(status: str) -> dict:
    fixtures = {
        "valid": {
            "schema_version": "execution-authority-result.v1",
            "status": "valid",
            "authority": "gate-authorized",
            "candidate_completion_digest": None,
            "errors": [],
        },
        "approval-required": {
            "schema_version": "execution-authority-result.v1",
            "status": "approval-required",
            "authority": None,
            "candidate_completion_digest": SHA256_A,
            "errors": ["terminal authority requires an operator completion pin"],
        },
        "invalid": {
            "schema_version": "execution-authority-result.v1",
            "status": "invalid",
            "authority": None,
            "candidate_completion_digest": None,
            "errors": ["execution state is invalid"],
        },
    }
    return copy.deepcopy(fixtures[status])


def authoring_fixture(status: str) -> dict:
    base = {
        "schema_version": "execution-authoring-result.v1",
        "status": status,
        "operation": "record-outcome",
        "mutations": [],
        "state_revision": None,
        "candidate_route_digest": None,
        "candidate_completion_digest": None,
        "capacities": [],
        "warnings": [],
        "errors": [],
    }
    if status == "written":
        base["mutations"] = [
            {
                "action": "replace",
                "path": ".prodcraft/artifacts/work-1/execution-state.json",
            }
        ]
        base["state_revision"] = 8
        base["capacities"] = [
            {
                "path": ".prodcraft/artifacts/work-1/execution-state.json",
                "used_bytes": 8192,
                "warning_bytes": 12582912,
                "limit_bytes": 16777216,
                "remaining_bytes": 16769024,
            }
        ]
    elif status == "candidate":
        base["mutations"] = [
            {
                "action": "replace",
                "path": ".prodcraft/artifacts/work-1/execution-state.json",
            }
        ]
        base["state_revision"] = 9
        base["candidate_completion_digest"] = SHA256_A
        base["capacities"] = [
            {
                "path": ".prodcraft/artifacts/work-1/execution-state.json",
                "used_bytes": 8192,
                "warning_bytes": 12582912,
                "limit_bytes": 16777216,
                "remaining_bytes": 16769024,
            }
        ]
    elif status == "recovery-required":
        base["errors"] = ["canonical materialization cannot be attributed safely"]
    elif status == "invalid":
        base["errors"] = ["expected revision is stale"]
    return base


class ProtocolResultContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        target = self.root / "schemas" / "protocol"
        target.parent.mkdir(parents=True)
        shutil.copytree(PROTOCOL_DIR, target)
        self.registry_path = target / "registry.yml"

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def validate_registry(self) -> list[str]:
        errors: list[str] = []
        validate_protocol_result_registry(
            errors,
            root=self.root,
            registry_path=self.registry_path,
        )
        return errors

    def mutate_registry(self, old: str, new: str) -> None:
        text = self.registry_path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        self.registry_path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def schema_path(self, result_name: str) -> Path:
        return self.root / "schemas" / "protocol" / f"{result_name}.v1.schema.json"

    def mutate_schema(self, result_name: str, mutate) -> None:
        path = self.schema_path(result_name)
        schema = json.loads(path.read_text(encoding="utf-8"))
        mutate(schema)
        path.write_text(json.dumps(schema), encoding="utf-8")

    def assert_registry_error(self, needle: str) -> None:
        errors = self.validate_registry()
        self.assertTrue(errors, "expected registry validation to fail")
        self.assertTrue(
            any(needle in error for error in errors),
            f"expected {needle!r} in {errors!r}",
        )

    def test_checked_in_registry_is_valid(self):
        self.assertEqual([], self.validate_registry())

    def test_protocol_registry_check_is_available_through_cli(self):
        result = subprocess.run(
            [
                sys.executable,
                "scripts/validate_prodcraft.py",
                "--check",
                "protocol-result-registry",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("Prodcraft validation passed\n", result.stdout)

    def test_missing_schema_is_rejected(self):
        self.schema_path("execution-authority-result").unlink()
        self.assert_registry_error("missing schema")

    def test_registry_and_schema_versions_must_match(self):
        self.mutate_registry(
            "schema_version: execution-authority-result.v1",
            "schema_version: execution-authority-result.v2",
        )
        self.assert_registry_error("does not match schema const")

        self.registry_path.write_text(
            self.registry_path.read_text(encoding="utf-8").replace(
                "protocol-result-registry.v1",
                "protocol-result-registry.v2",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_registry_error("must be `protocol-result-registry.v1`")

    def test_root_and_nested_objects_must_be_closed(self):
        self.mutate_schema(
            "execution-authority-result",
            lambda schema: schema.__setitem__("additionalProperties", True),
        )
        self.assert_registry_error("must be a closed object")

        shutil.rmtree(self.root / "schemas" / "protocol")
        shutil.copytree(PROTOCOL_DIR, self.root / "schemas" / "protocol")
        self.mutate_schema(
            "execution-authoring-result",
            lambda schema: schema["$defs"]["mutation"].__setitem__(
                "additionalProperties", True
            ),
        )
        self.assert_registry_error("must be a closed object")

    def test_declared_statuses_are_exact(self):
        self.mutate_schema(
            "execution-authority-result",
            lambda schema: schema["properties"]["status"]["enum"].append("unknown"),
        )
        self.assert_registry_error("status enum")

        shutil.rmtree(self.root / "schemas" / "protocol")
        shutil.copytree(PROTOCOL_DIR, self.root / "schemas" / "protocol")
        self.mutate_schema(
            "execution-authority-result",
            lambda schema: schema["properties"]["status"]["enum"].append("valid"),
        )
        self.assert_registry_error("status enum")

    def test_registry_rejects_removed_status_contracts_and_boolean_subschemas(self):
        self.mutate_schema(
            "execution-authoring-result",
            lambda schema: schema.pop("allOf"),
        )
        self.assert_registry_error("status contract")

        invalid_with_mutation = authoring_fixture("invalid")
        invalid_with_mutation["mutations"] = [
            {
                "action": "replace",
                "path": ".prodcraft/artifacts/work-1/execution-state.json",
            }
        ]
        errors: list[str] = []
        validate_protocol_result_instance(
            "execution-authoring-result",
            invalid_with_mutation,
            errors,
            root=self.root,
            registry_path=self.registry_path,
        )
        self.assertTrue(any("invalid" in error and "mutations" in error for error in errors), errors)

        shutil.rmtree(self.root / "schemas" / "protocol")
        shutil.copytree(PROTOCOL_DIR, self.root / "schemas" / "protocol")
        self.mutate_schema(
            "execution-authority-result",
            lambda schema: schema["properties"].__setitem__("status", True),
        )
        self.assert_registry_error("status enum")

    def test_registry_rejects_partial_status_contract_weakening(self):
        def remove_written_mutation_minimum(schema: dict) -> None:
            written = next(
                branch
                for branch in schema["allOf"]
                if branch["if"]["properties"]["status"].get("const") == "written"
            )
            written["then"]["properties"]["mutations"].pop("minItems")

        self.mutate_schema(
            "execution-authoring-result",
            remove_written_mutation_minimum,
        )
        self.assert_registry_error("status contract")

    def test_duplicate_yaml_keys_and_result_names_are_rejected(self):
        text = self.registry_path.read_text(encoding="utf-8")
        self.registry_path.write_text("schema_version: duplicate\n" + text, encoding="utf-8")
        self.assert_registry_error("duplicate YAML key `schema_version`")

        self.registry_path.write_text(
            text
            + "\n  execution-authority-result:\n"
            + "    schema_version: execution-authority-result.v1\n"
            + "    schema_path: schemas/protocol/execution-authority-result.v1.schema.json\n",
            encoding="utf-8",
        )
        self.assert_registry_error("duplicate YAML key `execution-authority-result`")

    def test_unsafe_schema_paths_are_rejected(self):
        unsafe_paths = (
            "../protocol/execution-authority-result.v1.schema.json",
            "/tmp/execution-authority-result.v1.schema.json",
            r"schemas\protocol\execution-authority-result.v1.schema.json",
            "file:schemas/protocol/execution-authority-result.v1.schema.json",
        )
        original = self.registry_path.read_text(encoding="utf-8")
        safe_path = "schemas/protocol/execution-authority-result.v1.schema.json"
        for unsafe_path in unsafe_paths:
            with self.subTest(schema_path=unsafe_path):
                self.registry_path.write_text(
                    original.replace(safe_path, unsafe_path, 1),
                    encoding="utf-8",
                )
                self.assert_registry_error("unsafe `schema_path`")

    def test_symlink_schema_target_is_rejected(self):
        schema_path = self.schema_path("execution-authority-result")
        content = schema_path.read_bytes()
        external = self.root / "external.schema.json"
        external.write_bytes(content)
        schema_path.unlink()
        schema_path.symlink_to(external)
        self.assert_registry_error("symlink")

    def test_schema_swap_to_symlink_after_resolution_is_rejected(self):
        schema_path = self.schema_path("execution-authority-result")
        external = self.root / "external.schema.json"
        external.write_bytes(schema_path.read_bytes())
        original_resolver = validate_prodcraft.resolve_protocol_schema_path
        swapped = False

        def resolve_then_swap(*args, **kwargs):
            nonlocal swapped
            resolved = original_resolver(*args, **kwargs)
            if resolved == schema_path and not swapped:
                schema_path.unlink()
                schema_path.symlink_to(external)
                swapped = True
            return resolved

        errors: list[str] = []
        with mock.patch.object(
            validate_prodcraft,
            "resolve_protocol_schema_path",
            side_effect=resolve_then_swap,
        ):
            validate_protocol_result_registry(
                errors,
                root=self.root,
                registry_path=self.registry_path,
            )
        self.assertTrue(any("symlink" in error for error in errors), errors)

    def test_schema_parent_swap_to_symlink_after_resolution_is_rejected(self):
        protocol_dir = self.root / "schemas" / "protocol"
        displaced_dir = self.root / "displaced-protocol"
        external_dir = self.root / "external-protocol"
        shutil.copytree(PROTOCOL_DIR, external_dir)
        original_resolver = validate_prodcraft.resolve_protocol_schema_path
        swapped = False

        def resolve_then_swap(*args, **kwargs):
            nonlocal swapped
            resolved = original_resolver(*args, **kwargs)
            if resolved is not None and not swapped:
                protocol_dir.rename(displaced_dir)
                protocol_dir.symlink_to(external_dir, target_is_directory=True)
                swapped = True
            return resolved

        errors: list[str] = []
        with mock.patch.object(
            validate_prodcraft,
            "resolve_protocol_schema_path",
            side_effect=resolve_then_swap,
        ):
            validate_protocol_result_registry(
                errors,
                root=self.root,
                registry_path=self.registry_path,
            )
        self.assertTrue(any("symlink" in error for error in errors), errors)

    def test_non_regular_schema_target_is_rejected(self):
        schema_path = self.schema_path("execution-authority-result")
        schema_path.unlink()
        schema_path.mkdir()
        self.assert_registry_error("regular file")

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_every_authority_and_authoring_status_has_a_valid_fixture(self):
        for status in ("valid", "approval-required", "invalid"):
            with self.subTest(contract="authority", status=status):
                errors: list[str] = []
                validate_protocol_result_instance(
                    "execution-authority-result",
                    authority_fixture(status),
                    errors,
                )
                self.assertEqual([], errors)

        for status in ("written", "candidate", "recovery-required", "invalid"):
            with self.subTest(contract="authoring", status=status):
                errors = []
                validate_protocol_result_instance(
                    "execution-authoring-result",
                    authoring_fixture(status),
                    errors,
                )
                self.assertEqual([], errors)

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_unknown_status_and_malformed_digest_are_rejected(self):
        unknown = authority_fixture("valid")
        unknown["status"] = "unknown"
        malformed = authority_fixture("approval-required")
        malformed["candidate_completion_digest"] = "sha256:ABC"
        for payload in (unknown, malformed):
            with self.subTest(payload=payload):
                errors: list[str] = []
                validate_protocol_result_instance(
                    "execution-authority-result",
                    payload,
                    errors,
                )
                self.assertTrue(errors)

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_result_paths_reject_nul(self):
        for field_name in ("mutations", "capacities"):
            payload = authoring_fixture("written")
            payload[field_name][0]["path"] = "bad\x00path"
            errors: list[str] = []
            validate_protocol_result_instance(
                "execution-authoring-result",
                payload,
                errors,
            )
            self.assertTrue(errors, field_name)

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_unknown_operation_and_zero_state_revision_are_rejected(self):
        unknown_operation = authoring_fixture("written")
        unknown_operation["operation"] = "unknown"
        zero_revision = authoring_fixture("written")
        zero_revision["state_revision"] = 0
        for payload in (unknown_operation, zero_revision):
            with self.subTest(payload=payload):
                errors: list[str] = []
                validate_protocol_result_instance(
                    "execution-authoring-result",
                    payload,
                    errors,
                )
                self.assertTrue(errors)

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_duplicate_mutation_and_capacity_paths_are_rejected(self):
        duplicate_mutation = authoring_fixture("candidate")
        duplicate_mutation["mutations"].append(
            {
                "action": "remove",
                "path": duplicate_mutation["mutations"][0]["path"],
            }
        )
        duplicate_capacity = authoring_fixture("candidate")
        duplicate_capacity["capacities"].append(
            {
                **duplicate_capacity["capacities"][0],
                "used_bytes": 1,
                "remaining_bytes": 16777215,
            }
        )
        for field_name, payload in (
            ("mutations", duplicate_mutation),
            ("capacities", duplicate_capacity),
        ):
            with self.subTest(field_name=field_name):
                errors: list[str] = []
                validate_protocol_result_instance(
                    "execution-authoring-result",
                    payload,
                    errors,
                )
                self.assertTrue(any(f"duplicate {field_name} path" in error for error in errors), errors)

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_capacity_constants_and_arithmetic_are_exact(self):
        invalid_capacities = []
        for field_name, value in (
            ("warning_bytes", 12582911),
            ("limit_bytes", 16777215),
            ("remaining_bytes", 1),
            ("used_bytes", 16777217),
        ):
            payload = authoring_fixture("written")
            payload["capacities"][0][field_name] = value
            invalid_capacities.append(payload)

        for payload in invalid_capacities:
            with self.subTest(capacity=payload["capacities"][0]):
                errors: list[str] = []
                validate_protocol_result_instance(
                    "execution-authoring-result",
                    payload,
                    errors,
                )
                self.assertTrue(errors)

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_closed_contract_rejects_unknown_fields(self):
        payload = authority_fixture("valid")
        payload["unexpected"] = True
        errors: list[str] = []
        validate_protocol_result_instance(
            "execution-authority-result",
            payload,
            errors,
        )
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
