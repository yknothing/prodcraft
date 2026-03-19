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


if __name__ == "__main__":
    unittest.main()
