import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "score_explicit_skill_benchmark.py"


def load_module():
    spec = importlib.util.spec_from_file_location("score_explicit_skill_benchmark", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ScoreExplicitSkillBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.manifest_skills = {"pc-systematic-debugging", "pc-tdd", "pc-system-design"}

    def test_machine_assertions_accept_structured_bug_fix_report(self):
        scenario = {
            "id": "multi-hypothesis-regression",
            "machine_assertions": [
                {"name": "kind", "path": "output_kind", "operator": "equals", "expected": "bug-fix-report"},
                {"name": "report", "path": "bug_fix_report", "operator": "non_empty"},
                {"name": "journal", "path": "debug_journal", "operator": "min_items", "expected": 2},
                {"name": "no-bypass", "path": "gate_bypass", "operator": "equals", "expected": False},
                {"name": "skills", "path": "downstream_skills", "operator": "manifest_skill_list"},
            ],
        }
        payload = {
            "scenario_id": "multi-hypothesis-regression",
            "output_kind": "bug-fix-report",
            "gate_bypass": False,
            "bug_fix_report": {
                "reproduction": "failing test",
                "root_cause": "cache key omitted tenant",
                "confirming_evidence": ["experiment 2"],
                "fix_boundary": "cache key only",
                "regression_protection": "tenant-specific regression",
                "two_way_causality": {
                    "with_fix_passed": True,
                    "fix_removed_failure_returned": True,
                },
            },
            "debug_journal": [{"hypothesis": "one"}, {"hypothesis": "two"}],
            "downstream_skills": ["pc-tdd"],
        }

        result = self.module.score_case_response(
            json.dumps(payload), scenario, self.manifest_skills
        )

        self.assertTrue(result["passed"])
        self.assertTrue(all(assertion["passed"] for assertion in result["assertions"]))

    def test_manifest_skill_resolution_is_exact_and_rejects_invented_skill(self):
        scenario = {
            "id": "manifest-resolution",
            "machine_assertions": [
                {"name": "skills", "path": "downstream_skills", "operator": "manifest_skill_list"}
            ],
        }
        payload = {
            "scenario_id": "manifest-resolution",
            "downstream_skills": ["pc-tdd", "pc-debugging-finish"],
        }

        result = self.module.score_case_response(
            f"```json\n{json.dumps(payload)}\n```", scenario, self.manifest_skills
        )

        self.assertFalse(result["passed"])
        skill_assertion = next(
            item for item in result["assertions"] if item["name"] == "skills"
        )
        self.assertIn("pc-debugging-finish", skill_assertion["detail"])

    def test_structural_mismatch_requires_course_correction_and_zero_fourth_patch(self):
        scenario = {
            "id": "structural-mismatch-escalation",
            "machine_assertions": [
                {"name": "kind", "path": "output_kind", "operator": "equals", "expected": "course-correction-note"},
                {"name": "note", "path": "course_correction_note", "operator": "non_empty"},
                {"name": "no-report", "path": "bug_fix_report", "operator": "not_present"},
                {"name": "no-fourth-patch", "path": "local_patch_attempted", "operator": "equals", "expected": False},
                {"name": "three-failures", "path": "failed_fix_count", "operator": "equals", "expected": 3},
                {"name": "skills", "path": "downstream_skills", "operator": "manifest_skill_list"},
            ],
        }
        payload = {
            "scenario_id": "structural-mismatch-escalation",
            "output_kind": "course-correction-note",
            "local_patch_attempted": False,
            "failed_fix_count": 3,
            "course_correction_note": {
                "artifact": "course-correction-note",
                "schema_version": "course-correction-note.v1",
                "recommended_next_skill": "pc-system-design",
            },
            "downstream_skills": ["pc-system-design"],
        }

        passing = self.module.score_case_response(
            json.dumps(payload), scenario, self.manifest_skills
        )
        self.assertTrue(passing["passed"])

        payload["local_patch_attempted"] = True
        payload["bug_fix_report"] = {"root_cause": "invented"}
        failing = self.module.score_case_response(
            json.dumps(payload), scenario, self.manifest_skills
        )
        self.assertFalse(failing["passed"])
        self.assertEqual(
            {item["name"] for item in failing["assertions"] if not item["passed"]},
            {"no-report", "no-fourth-patch"},
        )

    def test_judge_contradiction_blocks_acceptance_and_is_recorded(self):
        machine_cases = [
            {
                "scenario_id": "multi-hypothesis-regression",
                "run_number": 1,
                "arm": "with_skill",
                "response_sha256": "a" * 64,
                "passed": True,
            }
        ]
        judge_payload = {
            "schema_version": "explicit-benchmark-judge-results.v1",
            "cases": [
                {
                    "scenario_id": "multi-hypothesis-regression",
                    "run_number": 1,
                    "arm": "with_skill",
                    "response_sha256": "a" * 64,
                    "verdict": "fail",
                    "assertions": [{"name": "causality-is-substantive", "passed": False}],
                }
            ],
        }

        result = self.module.cross_validate_judge(machine_cases, judge_payload)

        self.assertFalse(result["acceptance_ready"])
        self.assertEqual(result["judge_status"], "contradiction")
        self.assertEqual(result["contradictions"][0]["type"], "machine-pass-judge-fail")

    def test_judge_must_cover_exact_declared_assertion_set(self):
        machine_cases = [
            {
                "scenario_id": "multi-hypothesis-regression",
                "run_number": 1,
                "arm": "with_skill",
                "response_sha256": "b" * 64,
                "passed": True,
                "judge_assertion_names": ["evidence-grounded", "smallest-safe-fix"],
            }
        ]
        judge_payload = {
            "schema_version": "explicit-benchmark-judge-results.v1",
            "cases": [
                {
                    "scenario_id": "multi-hypothesis-regression",
                    "run_number": 1,
                    "arm": "with_skill",
                    "response_sha256": "b" * 64,
                    "verdict": "pass",
                    "assertions": [{"name": "evidence-grounded", "passed": True}],
                }
            ],
        }

        result = self.module.cross_validate_judge(machine_cases, judge_payload)

        self.assertFalse(result["acceptance_ready"])
        self.assertIn(
            "judge-assertion-set-mismatch",
            {item["type"] for item in result["contradictions"]},
        )

    def test_cli_machine_only_writes_non_authoritative_summary(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            benchmark_path = root / "benchmark.json"
            manifest_path = root / "manifest.yml"
            run_dir = root / "run"
            response_path = run_dir / "eval-1-demo" / "with_skill" / "response.md"
            response_path.parent.mkdir(parents=True)
            response = json.dumps(
                {
                    "scenario_id": "demo",
                    "output_kind": "bug-fix-report",
                    "downstream_skills": ["pc-tdd"],
                }
            )
            response_path.write_text(response + "\n", encoding="utf-8")
            benchmark_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "demo",
                            "machine_assertions": [
                                {"name": "kind", "path": "output_kind", "operator": "equals", "expected": "bug-fix-report"},
                                {"name": "skills", "path": "downstream_skills", "operator": "manifest_skill_list"},
                            ],
                        }
                    ]
                ),
                encoding="utf-8",
            )
            manifest_path.write_text("skills:\n- name: pc-tdd\n", encoding="utf-8")
            execution_summary = {
                "schema_version": "explicit-benchmark-execution-summary.v1",
                "benchmark_sha256": self.module.sha256_file(benchmark_path),
                "skill_file_sha256": "c" * 64,
                "cases": [
                    {
                        "scenario_id": "demo",
                        "run_number": 1,
                        "arm": "with_skill",
                        "status": "completed",
                        "artifact_path": str(response_path.relative_to(run_dir)),
                        "artifact_sha256": self.module.sha256_file(response_path),
                    }
                ],
            }
            (run_dir / "execution_summary.json").write_text(
                json.dumps(execution_summary), encoding="utf-8"
            )
            output_path = root / "score.json"
            argv = [
                "score_explicit_skill_benchmark.py",
                "--run-dir",
                str(run_dir),
                "--benchmark",
                str(benchmark_path),
                "--manifest",
                str(manifest_path),
                "--output",
                str(output_path),
                "--machine-only",
            ]

            with mock.patch.object(sys, "argv", argv):
                self.assertEqual(self.module.main(), 0)

            summary = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertTrue(summary["machine_passed"])
            self.assertFalse(summary["acceptance_ready"])
            self.assertEqual(summary["judge_status"], "not-run")

    def test_cli_judge_covers_both_arms_while_acceptance_uses_with_skill(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            benchmark_path = root / "benchmark.json"
            manifest_path = root / "manifest.yml"
            run_dir = root / "run"
            benchmark_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "demo",
                            "machine_assertions": [
                                {
                                    "name": "kind",
                                    "path": "output_kind",
                                    "operator": "equals",
                                    "expected": "bug-fix-report",
                                }
                            ],
                            "judge_assertions": [
                                {"name": "substantive", "description": "The report is substantive."}
                            ],
                        }
                    ]
                ),
                encoding="utf-8",
            )
            manifest_path.write_text("skills:\n- name: pc-tdd\n", encoding="utf-8")
            execution_cases = []
            judge_cases = []
            for arm in ("without_skill", "with_skill"):
                response_path = run_dir / "eval-1-demo" / arm / "response.md"
                response_path.parent.mkdir(parents=True, exist_ok=True)
                response_path.write_text(
                    json.dumps({"scenario_id": "demo", "output_kind": "bug-fix-report"}) + "\n",
                    encoding="utf-8",
                )
                response_sha256 = self.module.sha256_file(response_path)
                execution_cases.append(
                    {
                        "scenario_id": "demo",
                        "run_number": 1,
                        "arm": arm,
                        "status": "completed",
                        "artifact_path": str(response_path.relative_to(run_dir)),
                        "artifact_sha256": response_sha256,
                    }
                )
                judge_cases.append(
                    {
                        "scenario_id": "demo",
                        "run_number": 1,
                        "arm": arm,
                        "response_sha256": response_sha256,
                        "verdict": "pass",
                        "assertions": [
                            {"name": "substantive", "passed": True, "detail": "Substantive."}
                        ],
                    }
                )

            (run_dir / "execution_summary.json").write_text(
                json.dumps(
                    {
                        "schema_version": "explicit-benchmark-execution-summary.v1",
                        "benchmark_sha256": self.module.sha256_file(benchmark_path),
                        "skill_file_sha256": "e" * 64,
                        "scenario_count": 1,
                        "runs_per_scenario": 1,
                        "cases": execution_cases,
                    }
                ),
                encoding="utf-8",
            )
            judge_path = root / "judge.json"
            judge_path.write_text(
                json.dumps(
                    {
                        "schema_version": "explicit-benchmark-judge-results.v1",
                        "cases": judge_cases,
                    }
                ),
                encoding="utf-8",
            )
            output_path = root / "score.json"
            argv = [
                "score_explicit_skill_benchmark.py",
                "--run-dir",
                str(run_dir),
                "--benchmark",
                str(benchmark_path),
                "--manifest",
                str(manifest_path),
                "--output",
                str(output_path),
                "--judge-results",
                str(judge_path),
            ]

            with mock.patch.object(sys, "argv", argv):
                self.assertEqual(self.module.main(), 0)

            summary = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertTrue(summary["acceptance_ready"])
            self.assertEqual(summary["judge_status"], "pass")
            self.assertEqual(summary["contradictions"], [])

    def test_cli_rejects_execution_summary_bound_to_different_benchmark(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            benchmark_path = root / "benchmark.json"
            manifest_path = root / "manifest.yml"
            run_dir = root / "run"
            run_dir.mkdir()
            benchmark_path.write_text(
                json.dumps([{"id": "demo", "machine_assertions": []}]),
                encoding="utf-8",
            )
            manifest_path.write_text("skills:\n- name: pc-tdd\n", encoding="utf-8")
            (run_dir / "execution_summary.json").write_text(
                json.dumps(
                    {
                        "schema_version": "explicit-benchmark-execution-summary.v1",
                        "benchmark_sha256": "0" * 64,
                        "skill_file_sha256": "d" * 64,
                        "cases": [],
                    }
                ),
                encoding="utf-8",
            )
            output_path = root / "score.json"
            argv = [
                "score_explicit_skill_benchmark.py",
                "--run-dir",
                str(run_dir),
                "--benchmark",
                str(benchmark_path),
                "--manifest",
                str(manifest_path),
                "--output",
                str(output_path),
                "--machine-only",
            ]

            with mock.patch.object(sys, "argv", argv):
                self.assertEqual(self.module.main(), 2)

            summary = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertIn("benchmark hash mismatch", summary["error"])


if __name__ == "__main__":
    unittest.main()
