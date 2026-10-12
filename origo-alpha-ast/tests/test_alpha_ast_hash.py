import json
import unittest
from pathlib import Path

from origo_alpha_ast import alpha_ast_hash, list_functions, SelectorError


ROOT = Path(__file__).parent
VECTORS = json.loads((ROOT / "vectors" / "alpha_vectors.json").read_text(encoding="utf-8"))


class AlphaAstVectorTests(unittest.TestCase):
    def test_all_vectors(self):
        for vector in VECTORS:
            with self.subTest(vector=vector["id"]):
                selector = vector.get("selector")
                left, _, _ = alpha_ast_hash(vector["left"], selector)
                right, _, _ = alpha_ast_hash(vector["right"], selector)
                self.assertEqual(
                    left.digest == right.digest,
                    vector["expect_equal"],
                    vector["description"],
                )

    def test_deterministic(self):
        source = "lambda value: value * 2"
        first, first_tree, first_bytes = alpha_ast_hash(source)
        second, second_tree, second_bytes = alpha_ast_hash(source)
        self.assertEqual(first.digest, second.digest)
        self.assertEqual(first_tree, second_tree)
        self.assertEqual(first_bytes, second_bytes)

    def test_selector_listing(self):
        source = "def outer(x):\n    def inner(y):\n        return x + y\n    return lambda z: inner(z)\n"
        names = list_functions(source)
        self.assertEqual(names, ["outer", "outer::inner", "outer::lambda#1"])

    def test_ambiguous_selector_fails(self):
        source = "def a():\n    def run():\n        pass\n\ndef b():\n    def run():\n        pass\n"
        with self.assertRaises(SelectorError):
            alpha_ast_hash(source, "run")

    def test_full_selector_resolves(self):
        source = "def a():\n    def run():\n        return 1\n    return run\n"
        result, _, _ = alpha_ast_hash(source, "a::run")
        self.assertEqual(result.digest_algorithm, "sha256")
        self.assertTrue(result.compact.startswith("origo-alpha-ast-v1:python:"))


    def test_comprehension_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "comprehension"]
        self.assertGreaterEqual(len(selected), 8)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])

    def test_decorator_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "decorator"]
        self.assertGreaterEqual(len(selected), 5)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])


    def test_nested_comprehension_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "nested_comprehension"]
        self.assertGreaterEqual(len(selected), 7)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])

    def test_decorator_lambda_call_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "decorator_lambda_call"]
        self.assertGreaterEqual(len(selected), 8)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])


    def test_async_comprehension_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "async_comprehension"]
        self.assertGreaterEqual(len(selected), 8)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])

    def test_decorator_closure_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "decorator_closure"]
        self.assertGreaterEqual(len(selected), 8)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])


    def test_nested_async_generator_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "nested_async_generator"]
        self.assertGreaterEqual(len(selected), 8)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])

    def test_chained_decorator_closure_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "chained_decorator_closure"]
        self.assertGreaterEqual(len(selected), 8)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])


    def test_async_generator_yield_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "async_generator_yield"]
        self.assertGreaterEqual(len(selected), 8)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])

    def test_parameterized_decorator_chain_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "parameterized_decorator_chain"]
        self.assertGreaterEqual(len(selected), 8)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])


    def test_generator_yield_from_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "generator_yield_from"]
        self.assertGreaterEqual(len(selected), 8)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])

    def test_decorator_star_args_kwargs_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "decorator_star_args_kwargs"]
        self.assertGreaterEqual(len(selected), 8)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])


    def test_mixed_decorator_argument_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "mixed_decorator_arguments"]
        self.assertGreaterEqual(len(selected), 8)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])

    def test_recursive_generator_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "recursive_generator"]
        self.assertGreaterEqual(len(selected), 8)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])


    def test_decorator_dict_literal_vectors(self):
        selected = [v for v in VECTORS if v.get("category") == "decorator_dict_literal"]
        self.assertGreaterEqual(len(selected), 10)
        for vector in selected:
            with self.subTest(vector=vector["id"]):
                left, _, _ = alpha_ast_hash(vector["left"], vector.get("selector"))
                right, _, _ = alpha_ast_hash(vector["right"], vector.get("selector"))
                self.assertEqual(left.digest == right.digest, vector["expect_equal"])


if __name__ == "__main__":
    unittest.main()
