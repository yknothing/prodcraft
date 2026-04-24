from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"
CHINESE_README = REPO_ROOT / "README.zh-CN.md"
LOCALIZED_COMPANION_DOCS = {CHINESE_README}
TEXT_FILE_SUFFIXES = {".json", ".md", ".py", ".yaml", ".yml"}
SKIPPED_DIRS = {".git", ".pytest_cache", "__pycache__", "build"}
CANONICAL_SCAN_ROOTS = (
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "CLAUDE.md",
    REPO_ROOT / "README.md",
    REPO_ROOT / ".github",
    REPO_ROOT / "docs",
    REPO_ROOT / "schemas",
    REPO_ROOT / "scripts",
    REPO_ROOT / "tests",
    REPO_ROOT / "workflows",
    REPO_ROOT / "personas",
    REPO_ROOT / "rules",
    REPO_ROOT / "templates",
    REPO_ROOT / "skills",
)

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
ZH_TITLE = "\u975e\u89c4\u8303\u6027\u4e2d\u6587\u5bfc\u8bfb"
ZH_NON_RULES = "\u4e0d\u5b9a\u4e49\u6216\u4fee\u6539\u4efb\u4f55\u9879\u76ee\u89c4\u5219"
ZH_ENGLISH_README = "\u82f1\u6587 `README.md`"


def markdown_slug(heading: str) -> str:
    slug = heading.strip().lower()
    slug = re.sub(r"`([^`]*)`", r"\1", slug)
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug.strip("-")


def heading_slugs(path: Path) -> set[str]:
    slugs: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            slugs.add(markdown_slug(match.group(1)))
    return slugs


def iter_canonical_text_files() -> list[Path]:
    paths: list[Path] = []
    for root in CANONICAL_SCAN_ROOTS:
        candidates = [root] if root.is_file() else root.rglob("*")
        for path in candidates:
            if not path.is_file():
                continue
            if any(part in SKIPPED_DIRS for part in path.relative_to(REPO_ROOT).parts):
                continue
            if path.suffix in TEXT_FILE_SUFFIXES:
                paths.append(path)
    return sorted(paths)


class ReadmeContractTests(unittest.TestCase):
    def test_readmes_exist_and_cross_link(self):
        self.assertTrue(README.exists())
        self.assertTrue(CHINESE_README.exists())

        english = README.read_text(encoding="utf-8")
        chinese = CHINESE_README.read_text(encoding="utf-8")

        self.assertRegex(english, r"\]\(\.?/?README\.zh-CN\.md\)")
        self.assertRegex(chinese, r"\]\(\.?/?README\.md\)")

    def test_chinese_readme_is_non_authoritative(self):
        content = CHINESE_README.read_text(encoding="utf-8")

        self.assertRegex(content, ZH_TITLE)
        self.assertRegex(content, ZH_NON_RULES)
        self.assertIn(ZH_ENGLISH_README, content)
        self.assertIn("schemas", content)
        self.assertIn("validators", content)
        self.assertIn("distribution registries", content)

    def test_language_policy_allows_only_explicit_localized_companion_docs(self):
        claude = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        english = README.read_text(encoding="utf-8")
        chinese = CHINESE_README.read_text(encoding="utf-8")

        self.assertIn("Canonical repository content is in English", claude)
        self.assertIn("Localized companion reader guides", claude)
        self.assertIn("non-authoritative", claude)
        self.assertIsNone(CJK_RE.search(english))
        self.assertIsNotNone(CJK_RE.search(chinese))

        for path in iter_canonical_text_files():
            if path in LOCALIZED_COMPANION_DOCS:
                continue
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                self.assertIsNone(CJK_RE.search(path.read_text(encoding="utf-8")))

    def test_readme_relative_links_resolve(self):
        for source in (README, CHINESE_README):
            text = source.read_text(encoding="utf-8")
            for raw_target in MARKDOWN_LINK_RE.findall(text):
                if re.match(r"^[a-z][a-z0-9+.-]*:", raw_target, re.IGNORECASE):
                    continue

                target, _separator, anchor = raw_target.partition("#")
                target = unquote(target)
                target_path = (source.parent / target).resolve() if target else source

                with self.subTest(source=source.name, target=raw_target):
                    self.assertTrue(str(target_path).startswith(str(REPO_ROOT)))
                    self.assertTrue(target_path.exists(), raw_target)
                    if anchor:
                        self.assertIn(unquote(anchor), heading_slugs(target_path), raw_target)


if __name__ == "__main__":
    unittest.main()
