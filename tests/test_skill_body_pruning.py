from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
BASELINE_BODY_CHARS = 235_790
TARGET_REMAINING_RATIO = 0.69
CRITICAL_ANTI_PATTERN_FRAGMENTS = {
    "pc-documentation": (
        "Outdated docs are worse than no docs.",
        '"The code is self-documenting" is only true for WHAT, never for WHY.',
    ),
    "pc-tech-debt-management": (
        "Debt accumulates continuously; reduction should be continuous too.",
        "Use evidence and recurrence, not frustration alone.",
    ),
    "pc-retrospective": (
        "Facilitator must redirect to systems thinking.",
        "If follow-ups never become planned work, the retro is theater.",
    ),
    "pc-ci-cd": (
        "Every deployment must have a tested rollback path.",
        "Pipeline that ignores release boundaries",
    ),
    "pc-e2e-scenario-design": (
        "never leaving and re-entering the flow",
        "adding fixed waits instead of deterministic state or network-based synchronization",
    ),
}


def source_skill_paths() -> list[Path]:
    return sorted(
        path
        for path in SKILLS_ROOT.rglob("SKILL.md")
        if ".curated" not in path.parts
    )


def skill_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise AssertionError(f"{path} has malformed frontmatter")
    return parts[2]


def section(body: str, heading: str) -> str | None:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$(?P<content>.*?)(?=^##\s+|\Z)",
        body,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(0) if match else None


class SkillBodyPruningTests(unittest.TestCase):
    def test_source_skill_body_budget_has_31_percent_buffer(self):
        body_chars = sum(len(skill_body(path)) for path in source_skill_paths())
        target = int(BASELINE_BODY_CHARS * TARGET_REMAINING_RATIO)
        self.assertLessEqual(body_chars, target, f"body chars {body_chars} exceed target {target}")

    def test_pure_related_skill_indexes_are_removed(self):
        offenders: list[str] = []
        for path in source_skill_paths():
            related = section(skill_body(path), "Related Skills")
            if related is None:
                continue
            lines = [line.strip() for line in related.splitlines()[1:] if line.strip()]
            if lines and all(line.startswith("- [") for line in lines):
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual([], offenders)

    def test_noncritical_anti_patterns_are_lazy_or_removed(self):
        offenders: list[str] = []
        for path in source_skill_paths():
            if path.parent.name in CRITICAL_ANTI_PATTERN_FRAGMENTS:
                continue
            anti_patterns = section(skill_body(path), "Anti-Patterns")
            body = skill_body(path)
            has_lazy_notes = (path.parent / "references" / "anti-patterns.md").is_file()
            if anti_patterns is not None or (has_lazy_notes and "references/anti-patterns.md" not in body):
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual([], offenders)

    def test_critical_anti_pattern_semantics_remain_in_runtime_body(self):
        by_name = {path.parent.name: skill_body(path) for path in source_skill_paths()}
        for name, fragments in CRITICAL_ANTI_PATTERN_FRAGMENTS.items():
            for fragment in fragments:
                with self.subTest(skill=name, fragment=fragment):
                    self.assertIn(fragment, by_name[name])

    def test_context_keeps_a_boundary_summary(self):
        for path in source_skill_paths():
            context = section(skill_body(path), "Context")
            self.assertIsNotNone(context, path)
            content = context.split("\n", 1)[1].strip()
            content_without_links = re.sub(r"\[[^]]+\]\([^)]+\)", "", content)
            self.assertGreaterEqual(len(content_without_links), 40, path)

    def test_context_explanation_is_lazy_loaded(self):
        offenders: list[str] = []
        for path in source_skill_paths():
            context = section(skill_body(path), "Context")
            if (
                context is None
                or len(context) > 360
                or "references/context.md" not in context
                or not (path.parent / "references" / "context.md").is_file()
            ):
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual([], offenders)

    def test_lazy_references_do_not_contain_lifecycle_skill_links(self):
        offenders: list[str] = []
        for path in SKILLS_ROOT.rglob("references/*.md"):
            if ".curated" in path.parts:
                continue
            if "SKILL.md" in path.read_text(encoding="utf-8"):
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual([], offenders)

    def test_reference_markdown_links_are_runtime_loadable(self):
        offenders: list[str] = []
        link_re = re.compile(r"!?\[[^]]*\]\((?P<target>[^)\s]+)\)")
        for path in SKILLS_ROOT.rglob("references/*.md"):
            text = path.read_text(encoding="utf-8")
            for match in link_re.finditer(text):
                target = match.group("target")
                if target.startswith(("#", "/", "http://", "https://", "mailto:")):
                    continue
                resolved = path.parent / target.split("#", 1)[0]
                if not resolved.exists():
                    offenders.append(f"{path.relative_to(REPO_ROOT)} -> {target}")
        self.assertEqual([], offenders)

    def test_io_names_are_lazy_but_authority_and_quality_stay_visible(self):
        offenders: list[str] = []
        for path in source_skill_paths():
            body = skill_body(path)
            inputs = section(body, "Inputs")
            outputs = section(body, "Outputs")
            notes = path.parent / "references" / "io-contract.md"
            if (
                inputs is None
                or outputs is None
                or len(inputs) + len(outputs) > 220
                or "references/io-contract.md" not in inputs
                or "authority" not in inputs.lower()
                or "quality" not in outputs.lower()
                or not notes.is_file()
            ):
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual([], offenders)

    def test_reference_material_indexes_are_lazy(self):
        offenders = [
            str(path.relative_to(REPO_ROOT))
            for path in source_skill_paths()
            if section(skill_body(path), "Reference Material") is not None
        ]
        self.assertEqual([], offenders)

    def test_related_skills_sections_do_not_carry_cross_skill_links(self):
        offenders: list[str] = []
        for path in source_skill_paths():
            related = section(skill_body(path), "Related Skills")
            if related is not None and "SKILL.md" in related:
                offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
