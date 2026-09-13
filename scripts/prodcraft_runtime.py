#!/usr/bin/env python3
"""Standard-library bootstrap for an explicitly configured Prodcraft Python.

Setup is explicit. Hook execution never installs packages, searches for another
interpreter, or depends on the bootstrap Python's site-packages.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "build" / "prodcraft-runtime.json"
SCHEMA_VERSION = "prodcraft-python-runtime.v1"
SUPPORTED_MINORS = {(3, 11), (3, 12)}
PROBE_TIMEOUT = 5
TARGETS = {
    "pretooluse": ".claude/hooks/prodcraft_pretooluse.py",
    "validate": "scripts/validate_prodcraft.py",
    "manage": "scripts/manage_execution_state.py",
    "codex": "scripts/run_codex_strict.py",
}
PROBE = (
    "import json,sys; from importlib.metadata import version; "
    "import yaml,jsonschema; "
    "print(json.dumps({'version':list(sys.version_info[:3]),"
    "'dependencies':{'PyYAML':version('PyYAML'),'jsonschema':version('jsonschema')}}))"
)


def inspect_python(executable):
    result = subprocess.run(
        [executable, "-I", "-c", PROBE], capture_output=True, text=True,
        timeout=PROBE_TIMEOUT,
    )
    if result.returncode:
        raise ValueError("configured Python needs PyYAML and jsonschema: " + result.stderr.strip())
    info = json.loads(result.stdout)
    if tuple(info["version"][:2]) not in SUPPORTED_MINORS:
        raise ValueError("Prodcraft requires Python 3.11 or 3.12")
    return info


def safe_config_path(create=False):
    directory = CONFIG.parent
    if create:
        directory.mkdir(exist_ok=True)
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError("runtime configuration requires a real build directory")
    if CONFIG.is_symlink() or (CONFIG.exists() and not CONFIG.is_file()):
        raise ValueError("runtime configuration must be a regular non-symlink file")


def setup(executable):
    located = shutil.which(executable) if not Path(executable).is_absolute() else executable
    if not located:
        raise ValueError("explicit Python executable was not found")
    # Preserve a virtualenv's executable path: resolving its symlink selects the
    # base Python and would silently discard the configured dependencies.
    executable = os.path.abspath(located)
    info = inspect_python(executable)
    safe_config_path(create=True)
    payload = {"schema_version": SCHEMA_VERSION, "python_executable": executable, **info}
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=CONFIG.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(payload, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, CONFIG)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return payload


def configured_runtime():
    safe_config_path()
    descriptor = os.open(CONFIG, os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(descriptor, "rb") as handle:
        metadata = os.fstat(handle.fileno())
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > 8192:
            raise ValueError("invalid runtime configuration file")
        config = json.loads(handle.read(8193))
    executable = config.get("python_executable")
    if config.get("schema_version") != SCHEMA_VERSION or not isinstance(executable, str) or not Path(executable).is_absolute():
        raise ValueError("invalid configured Python runtime")
    info = inspect_python(executable)
    return executable, info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    configure = commands.add_parser("setup", help="bind a supported dependency-equipped Python explicitly")
    configure.add_argument("--python", required=True)
    commands.add_parser("check", help="verify the configured runtime without downloading or installing")
    run = commands.add_parser("run", help="run a repository-owned target using the configured Python")
    run.add_argument("target", choices=sorted(TARGETS))
    run.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        if args.operation == "setup":
            print(json.dumps({"status": "ready", **setup(args.python)}))
            return 0
        executable, info = configured_runtime()
        if args.operation == "check":
            print(json.dumps({"status": "ready", "python_executable": executable, **info}))
            return 0
        target = ROOT / TARGETS[args.target]
        if target.is_symlink() or not target.is_file():
            raise ValueError("repository-owned runtime target is unavailable: " + str(target))
        arguments = args.arguments[1:] if args.arguments[:1] == ["--"] else args.arguments
        os.execv(executable, [executable, "-I", str(target), *arguments])
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(
            "Prodcraft runtime unavailable: " + str(exc)
            + "\nConfigure Python 3.11/3.12 with PyYAML and jsonschema, then run:"
            + "\npython3 scripts/prodcraft_runtime.py setup --python /absolute/path/to/python",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
