#!/usr/bin/env python3
"""Execute todos os vetores JSON compartilhados do Origo."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "origo-alpha-ast" / "src"))
from origo_alpha_ast import alpha_ast_hash  # noqa: E402

vector_files = sorted((ROOT / "conformance" / "vectors").glob("*.json"))
total = passed = 0
failures: list[str] = []
for path in vector_files:
    vectors = json.loads(path.read_text(encoding="utf-8"))
    for vector in vectors:
        total += 1
        try:
            selector = vector.get("selector")
            left, _, _ = alpha_ast_hash(vector["left"], selector)
            right, _, _ = alpha_ast_hash(vector["right"], selector)
            actual = left.digest == right.digest
            if actual == vector["expect_equal"]:
                passed += 1
            else:
                failures.append(f"{path.name}:{vector['id']}: expected={vector['expect_equal']} actual={actual}")
        except Exception as exc:  # pragma: no cover - diagnóstico de fixture
            failures.append(f"{path.name}:{vector['id']}: {type(exc).__name__}: {exc}")

print(f"vectors={total} passed={passed} failed={len(failures)} files={len(vector_files)}")
for failure in failures:
    print(f"FAIL {failure}")
raise SystemExit(1 if failures or total != 635 else 0)
