from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class TaskExecutionSkillTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

    def test_task_execution_skill_files_exist(self):
        targets = [
            REPO_ROOT / "skills" / "04-implementation" / "task-execution" / "SKILL.md",
            REPO_ROOT / "skills" / "04-implementation" / "task-execution" / "references" / "gotchas.md",
        ]
        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_manifest_registers_task_execution_as_critical_tested_skill(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}
        entry = entries["task-execution"]

        self.assertEqual("04-implementation", entry["phase"])
        self.assertEqual("tested", entry["status"])
        self.assertEqual("critical", entry["qa_tier"])
        self.assertEqual("routed", entry["evaluation_mode"])
        self.assertIn("benchmark_results_path", entry["qa"])

    def test_artifact_flow_and_gateway_keep_task_execution_tactical(self):
        artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}
        skill_text = (REPO_ROOT / "skills" / "04-implementation" / "task-execution" / "SKILL.md").read_text(encoding="utf-8")
        gateway = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")
        implementation_phase = (REPO_ROOT / "skills" / "04-implementation" / "_phase.md").read_text(encoding="utf-8")

        self.assertIn("task-execution", artifact_flow["task-list"]["consumed_by"])
        self.assertIn("task-execution", artifact_flow["dependency-graph"]["consumed_by"])
        self.assertEqual("task-execution", artifact_flow["execution-batch-plan"]["produced_by"])
        self.assertEqual("task-execution", artifact_flow["execution-checkpoint"]["produced_by"])
        self.assertIn("feature-development", artifact_flow["execution-batch-plan"]["consumed_by"])
        self.assertIn("systematic-debugging", artifact_flow["execution-batch-plan"]["consumed_by"])
        self.assertIn("verification-before-completion", artifact_flow["execution-checkpoint"]["consumed_by"])

        self.assertIn("It does **not** replace `feature-development`, `systematic-debugging`, or `tdd`", skill_text)
        self.assertIn("2-5 minute", skill_text)
        self.assertIn("### Implementation Routing Quick Map", gateway)
        self.assertIn("optional tactical wrapper", gateway)
        self.assertIn("### Implementation Routing Quick Map", implementation_phase)
        self.assertIn("use `task-execution` only when the batch itself needs explicit checkpoints", implementation_phase)

    def test_tested_artifacts_exist(self):
        targets = [
            REPO_ROOT / "eval" / "04-implementation" / "task-execution" / "isolated-benchmark.json",
            REPO_ROOT / "eval" / "04-implementation" / "task-execution" / "isolated-benchmark-review.md",
            REPO_ROOT / "eval" / "04-implementation" / "task-execution" / "tactical-batch-review.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)


if __name__ == "__main__":
    unittest.main()
