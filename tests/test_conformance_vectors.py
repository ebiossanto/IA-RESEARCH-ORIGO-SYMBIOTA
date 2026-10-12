import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "origo-alpha-ast" / "src"))
from origo_alpha_ast import alpha_ast_hash  # noqa: E402


class ExternalConformanceTests(unittest.TestCase):
    def test_all_external_vectors(self):
        total = 0
        for path in sorted((ROOT / "conformance" / "vectors").glob("*.json")):
            for vector in json.loads(path.read_text(encoding="utf-8")):
                with self.subTest(vector=vector["id"]):
                    total += 1
                    selector = vector.get("selector")
                    left, _, _ = alpha_ast_hash(vector["left"], selector)
                    right, _, _ = alpha_ast_hash(vector["right"], selector)
                    self.assertEqual(
                        left.digest == right.digest,
                        vector["expect_equal"],
                        vector["description"],
                    )
        self.assertEqual(total, 635)


if __name__ == "__main__":
    unittest.main()
