import json
import unittest
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SYSTEMATIC_EVAL_ROOT = REPO_ROOT / "eval" / "04-implementation" / "pc-systematic-debugging"
E2E_EVAL_ROOT = REPO_ROOT / "eval" / "05-quality" / "pc-e2e-scenario-design" / "evals"


class SystematicDebuggingRevalidationAssetTests(unittest.TestCase):
    def test_benchmark_defines_all_four_post_rewrite_scenarios(self):
        benchmark_path = SYSTEMATIC_EVAL_ROOT / "isolated-benchmark.json"
        scenarios = json.loads(benchmark_path.read_text(encoding="utf-8"))

        self.assertEqual(
            [scenario["id"] for scenario in scenarios],
            [
                "multi-hypothesis-regression",
                "flaky-failure-stabilization",
                "stale-artifact-trap",
                "structural-mismatch-escalation",
            ],
        )
        for scenario in scenarios:
            with self.subTest(scenario=scenario["id"]):
                self.assertTrue(scenario["machine_assertions"])
                self.assertTrue(scenario["judge_assertions"])
                self.assertIn("Return exactly one JSON object", scenario["prompt"])
                for context_file in scenario["context_files"]:
                    self.assertTrue((benchmark_path.parent / context_file).is_file())

    def test_bug_fix_scenarios_require_causality_and_structural_scenario_requires_escalation(self):
        scenarios = {
            item["id"]: item
            for item in json.loads(
                (SYSTEMATIC_EVAL_ROOT / "isolated-benchmark.json").read_text(encoding="utf-8")
            )
        }
        for scenario_id in (
            "multi-hypothesis-regression",
            "flaky-failure-stabilization",
            "stale-artifact-trap",
        ):
            assertions = scenarios[scenario_id]["machine_assertions"]
            expected = {(item["path"], item["operator"], item.get("expected")) for item in assertions}
            self.assertIn(("output_kind", "equals", "bug-fix-report"), expected)
            self.assertIn(
                ("bug_fix_report.two_way_causality.with_fix_passed", "equals", True),
                expected,
            )
            self.assertIn(
                ("bug_fix_report.two_way_causality.fix_removed_failure_returned", "equals", True),
                expected,
            )

        structural = scenarios["structural-mismatch-escalation"]["machine_assertions"]
        expected = {(item["path"], item["operator"], item.get("expected")) for item in structural}
        self.assertIn(("output_kind", "equals", "course-correction-note"), expected)
        self.assertIn(("bug_fix_report", "not_present", None), expected)
        self.assertIn(("local_patch_attempted", "equals", False), expected)
        self.assertIn(("failed_fix_count", "equals", 3), expected)

    def test_trigger_eval_set_is_vendored_harness_compatible_and_bucketed(self):
        eval_set = json.loads((E2E_EVAL_ROOT / "trigger-eval.json").read_text(encoding="utf-8"))

        self.assertIsInstance(eval_set, list)
        self.assertEqual(len(eval_set), 20)
        self.assertEqual(
            Counter(item["category"] for item in eval_set),
            {"core-positive": 5, "overlap": 5, "negative": 10},
        )
        for item in eval_set:
            with self.subTest(query=item.get("query")):
                self.assertIsInstance(item.get("query"), str)
                self.assertTrue(item["query"].strip())
                self.assertIsInstance(item.get("should_trigger"), bool)
        self.assertTrue(all(item["should_trigger"] for item in eval_set if item["category"] == "core-positive"))
        self.assertTrue(all(not item["should_trigger"] for item in eval_set if item["category"] == "negative"))


if __name__ == "__main__":
    unittest.main()
