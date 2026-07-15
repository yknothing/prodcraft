from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
METER_PATH = REPO_ROOT / "scripts" / "measure_context_cost.py"
BUDGET_PATH = REPO_ROOT / "schemas" / "context-budget.json"


def load_meter():
    spec = importlib.util.spec_from_file_location("measure_context_cost_budget", METER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ContextBudgetTests(unittest.TestCase):
    def test_current_runtime_surface_stays_within_checked_in_budget(self):
        meter = load_meter()
        budget = json.loads(BUDGET_PATH.read_text(encoding="utf-8"))

        self.assertEqual([], meter.evaluate_budget(meter.measure(), budget))

    def test_budget_preserves_fable_reduction_targets_and_fails_on_overage(self):
        meter = load_meter()
        budget = json.loads(BUDGET_PATH.read_text(encoding="utf-8"))
        baselines = budget["baseline_chars"]
        limits = budget["max_chars"]

        self.assertEqual("main@b41e032", budget["baseline_ref"])
        self.assertEqual(
            {
                "skill_descriptions": 10330,
                "entry_stack": 38279,
                "workflows": 68556,
                "skill_bodies": 235790,
            },
            baselines,
        )
        self.assertLessEqual(limits["skill_bodies"], int(baselines["skill_bodies"] * 0.70))
        self.assertLessEqual(limits["workflows"], int(baselines["workflows"] * 0.60))

        report = meter.measure()
        report["entry_stack"]["total_chars"] = limits["entry_stack"] + 1
        errors = meter.evaluate_budget(report, budget)

        self.assertTrue(any("entry_stack" in error and "exceeds" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
