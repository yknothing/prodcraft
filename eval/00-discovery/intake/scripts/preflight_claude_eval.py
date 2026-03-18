#!/usr/bin/env python3
"""Small preflight check for Claude CLI before long eval runs.

Usage:
  python3 intake-workspace/scripts/preflight_claude_eval.py
  python3 intake-workspace/scripts/preflight_claude_eval.py --model claude-opus-4-6
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether Claude CLI is usable before running evals."
    )
    parser.add_argument("--model", help="Optional Claude model name")
    args = parser.parse_args()

    cmd = ["claude", "-p", "say only OK", "--output-format", "text"]
    if args.model:
        cmd.extend(["--model", args.model])

    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env,
        cwd="/Users/whatsup/workspace/2026/prodcraft",
    )

    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()
    combined = "\n".join(part for part in [stdout, stderr] if part)
    lower = combined.lower()

    quota_blocked = "out of extra usage" in lower
    ok = result.returncode == 0 and stdout == "OK"

    payload = {
        "ok": ok,
        "model": args.model or "<default>",
        "returncode": result.returncode,
        "quota_blocked": quota_blocked,
        "stdout": stdout,
        "stderr": stderr,
    }

    print(json.dumps(payload, ensure_ascii=True, indent=2))

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
