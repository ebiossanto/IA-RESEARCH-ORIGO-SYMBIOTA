#!/usr/bin/env python3
"""Dependency-free release readiness checks."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "pyproject.toml",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "docs/SPECIFICATION.md",
    "src/origo_alpha_ast/core.py",
    "tests/vectors/alpha_vectors.json",
]


def run(*args: str) -> None:
    env = dict(__import__("os").environ)
    source_path = str(ROOT / "src")
    env["PYTHONPATH"] = source_path + (
        __import__("os").pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    subprocess.run(args, cwd=ROOT, check=True, env=env)


def main() -> int:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        print("missing required files:", ", ".join(missing), file=sys.stderr)
        return 1

    vectors = json.loads((ROOT / "tests/vectors/alpha_vectors.json").read_text(encoding="utf-8"))
    ids = [item["id"] for item in vectors]
    if len(ids) != len(set(ids)):
        print("duplicate vector identifiers", file=sys.stderr)
        return 1
    if len(vectors) < 130:
        print(f"expected at least 130 vectors, found {len(vectors)}", file=sys.stderr)
        return 1

    run(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v")
    run(sys.executable, "run_vectors.py")
    print(f"release checks passed: {len(vectors)} vectors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
