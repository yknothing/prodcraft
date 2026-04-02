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
MACHINE_SPECIFIC_TEXT_PATH_FRAGMENTS = (
    "/Users/whatsup/",
    "/tmp/topbrains-orch/",
    "/var/folders/",
)
TEXT_ARTIFACT_SUFFIXES = {".json", ".jsonl", ".log", ".md", ".txt"}
LOCAL_IGNORED_DIR_NAMES = {
    "explicit-benchmark-run-2026-03-16a",
    "explicit-benchmark-run-2026-03-16b",
}


def is_local_ignored_eval_artifact(path: Path) -> bool:
    for part in path.relative_to(EVAL_ROOT).parts:
        if part.startswith("run-"):
            return True
        if part.startswith("skill-creator-run-"):
            return True
        if part.startswith("isolated-benchmark-run-"):
            return True
        if part.startswith("explicit-benchmark-timeout-smoke-"):
            return True
        if part in LOCAL_IGNORED_DIR_NAMES:
            return True
        if part.startswith("post-redesign-benchmark-run-") and (
            part.endswith("-smoke") or part.endswith("-gemini") or part.endswith("-gemini-clean")
        ):
            return True
    return False


class EvalArtifactPathTests(unittest.TestCase):
    def test_eval_artifacts_do_not_reference_removed_workspace_directories(self):
        offenders: list[str] = []
        for path in EVAL_ROOT.rglob("*"):
            if path.suffix not in {".json", ".md"} or not path.is_file():
                continue
            if is_local_ignored_eval_artifact(path):
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
            if is_local_ignored_eval_artifact(path):
                continue
            text = path.read_text(encoding="utf-8")
            if ABSOLUTE_REPO_PREFIX in text:
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual([], offenders)

    def test_runtime_context_artifacts_do_not_store_ephemeral_absolute_paths(self):
        offenders: list[str] = []
        for path in EVAL_ROOT.rglob("runtime_context.json"):
            if is_local_ignored_eval_artifact(path):
                continue
            text = path.read_text(encoding="utf-8")
            if any(fragment in text for fragment in EPHEMERAL_PATH_FRAGMENTS):
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual([], offenders)

    def test_eval_text_artifacts_do_not_store_machine_specific_temp_paths(self):
        offenders: list[str] = []
        for path in EVAL_ROOT.rglob("*"):
            if not path.is_file() or path.suffix not in TEXT_ARTIFACT_SUFFIXES:
                continue
            if is_local_ignored_eval_artifact(path):
                continue
            text = path.read_text(encoding="utf-8")
            for fragment in MACHINE_SPECIFIC_TEXT_PATH_FRAGMENTS:
                if fragment in text:
                    offenders.append(f"{path.relative_to(REPO_ROOT)} -> {fragment}")
        self.assertEqual([], offenders)

    def test_run_metadata_records_runner(self):
        import json

        offenders: list[str] = []
        for path in EVAL_ROOT.rglob("run_metadata.json"):
            if is_local_ignored_eval_artifact(path):
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("runner") not in {"gemini", "claude", "copilot"}:
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
