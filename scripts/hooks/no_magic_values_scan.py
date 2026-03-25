#!/usr/bin/env python3
"""Scan text-ish source files for likely magic values and hardcoded configuration.

This script intentionally uses lightweight heuristics suitable for many languages.
It is not a semantic analyzer: it encodes Prodcraft's baseline expectations and pairs
with human review via `skills/05-quality/code-review/SKILL.md`.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

# File extensions that are reasonable to scan as UTF-8 text for cross-language repos.
TEXT_CODE_EXTENSIONS = {
    ".py",
    ".pyi",
    ".pyx",
    ".pyw",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".mts",
    ".cts",
    ".java",
    ".kt",
    ".kts",
    ".scala",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".cs",
    ".swift",
    ".c",
    ".h",
    ".cc",
    ".cpp",
    ".hpp",
    ".hxx",
    ".hh",
    ".sql",
    ".sh",
    ".bash",
    ".zsh",
    ".fish",
    ".ps1",
    ".yaml",
    ".yml",
    ".toml",
    ".json",
    ".jsonc",
    ".xml",
    ".html",
    ".htm",
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".md",
    ".mdx",
    ".vue",
    ".svelte",
}

class MagicValueScanConfig:
    """Centralized thresholds for heuristic scans.

    This intentionally keeps numeric thresholds out of logic branches to avoid
    scattering "magic values" across the scanner.
    """

    # Exception annotations are required within a small lookback window.
    ANNOTATION_LOOKBACK_LINES = 2

    # Heuristic: small integers are commonly used for indexes or sizes.
    ALLOWED_SMALL_INTEGER_VALUES = frozenset({0, 1, 2})

    # Heuristic: large integer literals are often IDs/ports/timeouts.
    LARGE_INTEGER_MIN_VALUE = 1000

    # Heuristic: long digit runs (e.g. IDs) are usually not domain literals.
    MIN_LONG_DIGIT_RUN_LENGTH = 6

    # Heuristic: long string literals are often hardcoded identifiers.
    MIN_LONG_STRING_CHARS = 12

    # Heuristic: ports <= 1 are usually privileged-service placeholders.
    MAX_EXEMPT_PORT_VALUE = 1

    # Heuristic: allow common local/test domains.
    DEFAULT_EXAMPLE_DOMAINS = frozenset({"example.com", "example.org", "example.net"})


# Regex exception annotation: `ALLOW_MAGIC_NUMBER: reason, ticket`.
ALLOW_ANNOTATION_RE = re.compile(r"ALLOW_MAGIC_NUMBER:\s*.+?\s*,\s*\S+")

# Likely network hosts / URLs / IPs embedded in source.
URL_LIKE_RE = re.compile(r"\bhttps?://[^\s\"'<>]+")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
DNS_HOST_RE = re.compile(r"\b(?:[a-z0-9-]+\.)+[a-z]{2,}\b", re.IGNORECASE)

# Email-ish literals that are rarely acceptable as hardcoded production identifiers.
EMAIL_RE = re.compile(r"\b[^\s@]+@[^\s@]+\.[^\s@]+\b")

# Long unbroken string literals are often configuration or identifiers.
STRING_LITERAL_RE = re.compile(r"([\"'])(?:(?=(\\?))\2.)*?\1")

# Repeated digit runs (common for IDs/ports) and suspicious port literals.
LONG_DIGIT_RUN_RE = re.compile(
    rf"\b\d{{{MagicValueScanConfig.MIN_LONG_DIGIT_RUN_LENGTH},}}\b"
)
PORT_RE = re.compile(
    rf"\b(?::|\bport\b\s*=\s*)(\d{{2,{5}}})\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Finding:
    """Represents a single finding line for reporting."""

    path: Path
    line_number: int
    line: str
    reason: str


def _split_git_z_entries(blob: bytes) -> list[str]:
    """Split a NUL-delimited `git` output payload into paths."""

    if not blob:
        return []
    return [entry.decode("utf-8", errors="replace") for entry in blob.split(b"\0") if entry]


def _git_diff_name_only(range_spec: str) -> list[str]:
    """Return changed file paths for a given git diff range."""

    completed = subprocess.run(
        ["git", "-c", "core.quotepath=false", "diff", "--name-only", "--diff-filter=ACMRT", range_spec],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.decode("utf-8", errors="replace").strip())

    text = completed.stdout.decode("utf-8", errors="replace")
    return [line.strip() for line in text.splitlines() if line.strip()]


def _git_ls_files(pathspecs: list[str]) -> list[str]:
    """Return tracked files matching pathspecs."""

    completed = subprocess.run(
        ["git", "-c", "core.quotepath=false", "ls-files", "-z", *pathspecs],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.decode("utf-8", errors="replace").strip())

    return _split_git_z_entries(completed.stdout)


def _should_scan_path(path: Path) -> bool:
    """Return True when the path looks like a scannable text source file."""

    if path.suffix.lower() not in TEXT_CODE_EXTENSIONS:
        return False

    # Avoid scanning vendored or generated trees by convention.
    parts_lower = {part.lower() for part in path.parts}
    if "node_modules" in parts_lower or "vendor" in parts_lower or "dist" in parts_lower or "build" in parts_lower:
        return False

    return True


def _line_has_annotation(line: str) -> bool:
    """Return True when the line contains an approved exception annotation."""

    return bool(ALLOW_ANNOTATION_RE.search(line))


def _previous_lines_context(lines: list[str], index: int, lookback: int) -> str:
    """Return a small concatenated context window for annotation scanning."""

    start = max(0, index - lookback)
    return "\n".join(lines[start : index + 1])


def _scan_line_for_findings(
    *,
    path: Path,
    line_number: int,
    line: str,
    lines: list[str],
    line_index: int,
) -> list[Finding]:
    """Scan a single line for heuristic findings."""

    findings: list[Finding] = []

    stripped = line.strip()
    if not stripped:
        return findings

    # Allow comments to carry the annotation for the line below.
    if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*"):
        return findings

    context = _previous_lines_context(
        lines,
        line_index,
        lookback=MagicValueScanConfig.ANNOTATION_LOOKBACK_LINES,
    )
    if ALLOW_ANNOTATION_RE.search(context):
        return findings

    if URL_LIKE_RE.search(line) or IPV4_RE.search(line):
        findings.append(
            Finding(
                path=path,
                line_number=line_number,
                line=line.rstrip("\n"),
                reason="Likely hardcoded URL/IP/network host literal",
            )
        )

    dns_matches = DNS_HOST_RE.findall(line)
    for host in dns_matches:
        if host.lower().startswith("localhost."):
            continue
        if host.lower() in MagicValueScanConfig.DEFAULT_EXAMPLE_DOMAINS:
            continue
        findings.append(
            Finding(
                path=path,
                line_number=line_number,
                line=line.rstrip("\n"),
                reason=f"Likely hardcoded DNS hostname: `{host}`",
            )
        )

    if EMAIL_RE.search(line):
        findings.append(
            Finding(
                path=path,
                line_number=line_number,
                line=line.rstrip("\n"),
                reason="Likely hardcoded email address literal",
            )
        )

    for match in re.finditer(r"\b\d+\b", line):
        value = int(match.group(0))
        if value in MagicValueScanConfig.ALLOWED_SMALL_INTEGER_VALUES:
            continue
        if value >= MagicValueScanConfig.LARGE_INTEGER_MIN_VALUE:
            findings.append(
                Finding(
                    path=path,
                    line_number=line_number,
                    line=line.rstrip("\n"),
                    reason=f"Suspicious numeric literal `{value}` (large integer)",
                )
            )

    for match in LONG_DIGIT_RUN_RE.finditer(line):
        findings.append(
            Finding(
                path=path,
                line_number=line_number,
                line=line.rstrip("\n"),
                reason=f"Suspicious long digit run `{match.group(0)}`",
            )
        )

    for match in PORT_RE.finditer(line):
        port = int(match.group(1))
        if port <= MagicValueScanConfig.MAX_EXEMPT_PORT_VALUE:
            continue
        findings.append(
            Finding(
                path=path,
                line_number=line_number,
                line=line.rstrip("\n"),
                reason=f"Suspicious port literal `{port}`",
            )
        )

    for match in STRING_LITERAL_RE.finditer(line):
        literal = match.group(0)
        inner = literal[1:-1]
        if len(inner) < MagicValueScanConfig.MIN_LONG_STRING_CHARS:
            continue
        if inner.isdigit():
            continue
        findings.append(
            Finding(
                path=path,
                line_number=line_number,
                line=line.rstrip("\n"),
                reason=f"Likely hardcoded long string literal ({len(inner)} chars)",
            )
        )

    return findings


def _scan_file(path: Path) -> list[Finding]:
    """Scan a single file and return findings."""

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [
            Finding(
                path=path,
                line_number=0,
                line="",
                reason="File is not valid UTF-8; skipping content scan",
            )
        ]

    lines = text.splitlines(keepends=True)
    findings: list[Finding] = []
    normalized_lines = [ln.rstrip("\n") for ln in lines]

    for index, raw_line in enumerate(lines):
        line_number = index + 1
        line_text = raw_line
        if _line_has_annotation(line_text):
            continue

        findings.extend(
            _scan_line_for_findings(
                path=path,
                line_number=line_number,
                line=line_text,
                lines=normalized_lines,
                line_index=index,
            )
        )

    return findings


def _select_paths_from_git(diff_mode: str) -> list[Path]:
    """Select candidate paths based on git mode."""

    if diff_mode == "staged":
        files = _git_diff_name_only("--cached")
    elif diff_mode == "working-tree":
        files = _git_diff_name_only("HEAD")
    elif diff_mode == "tracked":
        files = _git_ls_files([])
    else:
        raise ValueError(f"Unsupported diff mode: {diff_mode}")

    paths: list[Path] = []
    for rel in files:
        path = (REPO_ROOT / rel).resolve()
        if path.is_file() and _should_scan_path(path):
            paths.append(path)

    return sorted(set(paths))


def _format_findings(findings: list[Finding]) -> str:
    """Format findings for terminal output."""

    lines: list[str] = []
    for item in findings:
        if item.line_number == 0:
            lines.append(f"{item.path.relative_to(REPO_ROOT)}: {item.reason}")
            continue
        lines.append(f"{item.path.relative_to(REPO_ROOT)}:{item.line_number}: {item.reason}")
        lines.append(f"    {item.line}")
    return "\n".join(lines)


def main() -> int:
    """CLI entrypoint."""

    parser = argparse.ArgumentParser(description="Heuristic scan for magic values and hardcoded configuration.")
    parser.add_argument(
        "--git",
        choices=("staged", "working-tree", "tracked"),
        default="staged",
        help="Which files to scan. `staged` is intended for pre-commit hooks.",
    )
    parser.add_argument(
        "--fail-on-findings",
        action="store_true",
        help="Exit with non-zero status when findings are present.",
    )
    args = parser.parse_args()

    try:
        paths = _select_paths_from_git(args.git)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    all_findings: list[Finding] = []
    for path in paths:
        all_findings.extend(_scan_file(path))

    if all_findings:
        print(_format_findings(all_findings))
        if args.fail_on_findings:
            return 1
        return 0

    print("No heuristic magic-value findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
