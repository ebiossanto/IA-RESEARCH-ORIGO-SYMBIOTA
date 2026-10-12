#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from origo_alpha_ast import alpha_ast_hash

ROOT = Path(__file__).parent
vectors = json.loads((ROOT / "tests" / "vectors" / "alpha_vectors.json").read_text(encoding="utf-8"))
failed = 0
for vector in vectors:
    selector = vector.get("selector")
    left, _, _ = alpha_ast_hash(vector["left"], selector)
    right, _, _ = alpha_ast_hash(vector["right"], selector)
    actual = left.digest == right.digest
    status = "PASS" if actual == vector["expect_equal"] else "FAIL"
    print(f"{status:4} {vector['id']}: equal={actual}, expected={vector['expect_equal']}")
    if status == "FAIL":
        failed += 1
raise SystemExit(1 if failed else 0)
