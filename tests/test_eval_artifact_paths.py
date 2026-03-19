import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EVAL_ROOT = REPO_ROOT / "eval"
LEGACY_PATH_FRAGMENTS = (
    "requirements-engineering-workspace/",
    "problem-framing-workspace/",
    "user-research-workspace/",
    "intake-workspace/",
)
ABSOLUTE_REPO_PREFIX = '"/Users/whatsup/workspace/2026/prodcraft/'
EPHEMERAL_PATH_FRAGMENTS = ('"/var/folders/', '"/tmp/')


class EvalArtifactPathTests(unittest.TestCase):
    def test_eval_artifacts_do_not_reference_removed_workspace_directories(self):
        offenders: list[str] = []
        for path in EVAL_ROOT.rglob("*"):
            if path.suffix not in {".json", ".md"} or not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for fragment in LEGACY_PATH_FRAGMENTS:
                if fragment in text:
                    offenders.append(f"{path.relative_to(REPO_ROOT)} -> {fragment}")
        self.assertEqual([], offenders)

    def test_benchmark_and_eval_metadata_do_not_store_absolute_repo_paths(self):
        offenders: list[str] = []
        for path in EVAL_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if path.name not in {"run_metadata.json", "eval_metadata.json"} and not path.name.endswith("benchmark.json"):
                continue
            text = path.read_text(encoding="utf-8")
            if ABSOLUTE_REPO_PREFIX in text:
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual([], offenders)

    def test_runtime_context_artifacts_do_not_store_ephemeral_absolute_paths(self):
        offenders: list[str] = []
        for path in EVAL_ROOT.rglob("runtime_context.json"):
            text = path.read_text(encoding="utf-8")
            if any(fragment in text for fragment in EPHEMERAL_PATH_FRAGMENTS):
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual([], offenders)

    def test_run_metadata_records_runner(self):
        import json

        offenders: list[str] = []
        for path in EVAL_ROOT.rglob("run_metadata.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("runner") not in {"gemini", "claude"}:
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
