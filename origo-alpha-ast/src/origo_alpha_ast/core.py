#!/usr/bin/env python3
"""Reference implementation of Origo Overlay alpha_ast_hash for Python.

Profile: origo-alpha-ast-v1
Language: python
AST schema: cpython-ast-<major>.<minor>

The implementation normalizes bound parameters and local variables by lexical
binding identity. Free/global names, attributes, literals, operators, control
flow and statement order remain significant.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

PROFILE = "origo-alpha-ast-v1"
DOMAIN = b"ORIGO\0ALPHA_AST\0V1\0"


class AlphaAstError(Exception):
    """Base error for alpha AST processing."""


class SelectorError(AlphaAstError):
    """Raised when a selector is unresolved or ambiguous."""


@dataclass(frozen=True)
class HashResult:
    profile: str
    language: str
    language_version: str
    ast_schema: str
    digest_algorithm: str
    digest: str
    canonical_size: int

    @property
    def compact(self) -> str:
        return (
            f"{self.profile}:{self.language}:{self.ast_schema}:"
            f"{self.digest_algorithm}:{self.digest}"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "alpha_ast_hash",
            "profile": self.profile,
            "language": self.language,
            "language_version": self.language_version,
            "ast_schema": self.ast_schema,
            "digest_algorithm": self.digest_algorithm,
            "digest": self.digest,
            "compact": self.compact,
            "canonical_size": self.canonical_size,
            "binding_policy": {
                "parameters": "lexical_slot",
                "locals": "lexical_slot",
                "captures": "preserve_name",
                "globals": "preserve_name",
                "attributes": "preserve_name",
            },
        }


@dataclass
class Scope:
    parent: "Scope | None"
    kind: str
    bindings: dict[str, tuple[str, int]]

    def bind(self, name: str, kind: str) -> tuple[str, int]:
        existing = self.bindings.get(name)
        if existing is not None:
            return existing
        binding = (kind, len(self.bindings))
        self.bindings[name] = binding
        return binding

    def resolve_local(self, name: str) -> tuple[int, str, int] | None:
        depth = 0
        scope: Scope | None = self
        while scope is not None:
            if name in scope.bindings:
                kind, slot = scope.bindings[name]
                return depth, kind, slot
            depth += 1
            scope = scope.parent
        return None


FUNCTION_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)


def python_schema() -> str:
    return f"cpython-ast-{sys.version_info.major}.{sys.version_info.minor}"


def parse_expression_or_module(source: str, mode: str = "auto") -> ast.AST:
    if mode == "eval":
        return ast.parse(source, mode="eval")
    if mode == "exec":
        return ast.parse(source, mode="exec")
    try:
        return ast.parse(source, mode="eval")
    except SyntaxError:
        return ast.parse(source, mode="exec")


def qualified_functions(tree: ast.AST) -> list[tuple[str, ast.AST]]:
    found: list[tuple[str, ast.AST]] = []

    def visit(node: ast.AST, path: list[str], lambda_counts: dict[tuple[str, ...], int]) -> None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            current = path + [node.name]
            found.append(("::".join(current), node))
            for child in node.body:
                visit(child, current, lambda_counts)
            return
        if isinstance(node, ast.Lambda):
            parent_key = tuple(path)
            index = lambda_counts.get(parent_key, 0) + 1
            lambda_counts[parent_key] = index
            name = f"lambda#{index}"
            found.append(("::".join(path + [name]), node))
            visit(node.body, path + [name], lambda_counts)
            return
        for child in ast.iter_child_nodes(node):
            visit(child, path, lambda_counts)

    visit(tree, [], {})
    return found


def select_function(tree: ast.AST, selector: str | None) -> ast.AST:
    if isinstance(tree, ast.Expression) and isinstance(tree.body, ast.Lambda):
        if selector in (None, "lambda#1"):
            return tree.body
    functions = qualified_functions(tree)
    if selector is None:
        if len(functions) == 1:
            return functions[0][1]
        if not functions:
            raise SelectorError("no function or lambda found")
        raise SelectorError(
            "selector required; candidates: " + ", ".join(name for name, _ in functions)
        )
    matches = [(name, node) for name, node in functions if name == selector or name.endswith("::" + selector)]
    if not matches:
        raise SelectorError(
            f"selector {selector!r} unresolved; candidates: "
            + ", ".join(name for name, _ in functions)
        )
    if len(matches) > 1:
        raise SelectorError(
            f"selector {selector!r} ambiguous; matches: "
            + ", ".join(name for name, _ in matches)
        )
    return matches[0][1]


def bound_names_from_target(target: ast.AST) -> Iterable[str]:
    if isinstance(target, ast.Name):
        yield target.id
    elif isinstance(target, (ast.Tuple, ast.List)):
        for item in target.elts:
            yield from bound_names_from_target(item)
    elif isinstance(target, ast.Starred):
        yield from bound_names_from_target(target.value)


def collect_local_bindings(node: ast.AST, scope: Scope) -> None:
    """Collect bindings in this function without descending into nested functions."""
    for child in ast.walk(node):
        if child is not node and isinstance(child, FUNCTION_NODES):
            continue
        if isinstance(child, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            targets = child.targets if isinstance(child, ast.Assign) else [child.target]
            for target in targets:
                for name in bound_names_from_target(target):
                    scope.bind(name, "local")
        elif isinstance(child, ast.AugAssign):
            for name in bound_names_from_target(child.target):
                scope.bind(name, "local")
        elif isinstance(child, (ast.For, ast.AsyncFor)):
            for name in bound_names_from_target(child.target):
                scope.bind(name, "local")
        elif isinstance(child, (ast.With, ast.AsyncWith)):
            for item in child.items:
                if item.optional_vars:
                    for name in bound_names_from_target(item.optional_vars):
                        scope.bind(name, "local")
        elif isinstance(child, ast.ExceptHandler) and isinstance(child.name, str):
            scope.bind(child.name, "exception")
        elif isinstance(child, (ast.Import, ast.ImportFrom)):
            for alias in child.names:
                scope.bind(alias.asname or alias.name.split(".")[0], "import_local")
        elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and child is not node:
            scope.bind(child.name, "local")


def parameter_nodes(args: ast.arguments) -> list[tuple[str, str, ast.AST | None]]:
    output: list[tuple[str, str, ast.AST | None]] = []
    positional = list(args.posonlyargs) + list(args.args)
    default_start = len(positional) - len(args.defaults)
    for index, arg in enumerate(args.posonlyargs):
        default = args.defaults[index - default_start] if index >= default_start else None
        output.append((arg.arg, "positional_only", default))
    for local_index, arg in enumerate(args.args, start=len(args.posonlyargs)):
        default = args.defaults[local_index - default_start] if local_index >= default_start else None
        output.append((arg.arg, "positional", default))
    if args.vararg:
        output.append((args.vararg.arg, "vararg", None))
    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        output.append((arg.arg, "keyword_only", default))
    if args.kwarg:
        output.append((args.kwarg.arg, "kwarg", None))
    return output


class AlphaNormalizer:
    def __init__(self) -> None:
        self.scope: Scope | None = None
        self.global_names: set[str] = set()
        self.nonlocal_names: set[str] = set()

    def normalize_function(self, node: ast.AST) -> Any:
        if not isinstance(node, FUNCTION_NODES):
            raise AlphaAstError(f"unsupported function node: {type(node).__name__}")
        return self._function(node, parent=None)

    def _function(self, node: ast.AST, parent: Scope | None) -> Any:
        assert isinstance(node, FUNCTION_NODES)
        kind = (
            "lambda" if isinstance(node, ast.Lambda)
            else "async_function" if isinstance(node, ast.AsyncFunctionDef)
            else "function"
        )
        scope = Scope(parent=parent, kind=kind, bindings={})
        previous_scope = self.scope
        previous_globals = self.global_names
        previous_nonlocals = self.nonlocal_names
        self.scope = scope
        self.global_names = set()
        self.nonlocal_names = set()

        params = []
        for name, parameter_kind, default in parameter_nodes(node.args):
            _, slot = scope.bind(name, "parameter")
            params.append({
                "slot": slot,
                "kind": parameter_kind,
                "default": self.visit(default) if default is not None else None,
            })

        body_source = node.body if isinstance(node, ast.Lambda) else node
        collect_local_bindings(body_source, scope)

        if isinstance(node, ast.Lambda):
            body = self.visit(node.body)
            decorators = []
            returns = None
        else:
            # global/nonlocal declarations affect resolution for this function.
            for statement in node.body:
                if isinstance(statement, ast.Global):
                    self.global_names.update(statement.names)
                elif isinstance(statement, ast.Nonlocal):
                    self.nonlocal_names.update(statement.names)
            body = [self.visit(statement) for statement in node.body]

            # Decorator expressions are evaluated in the enclosing lexical
            # scope, before the decorated function is bound. They must not
            # resolve against parameters or locals of the decorated function.
            self.scope = parent
            decorators = [self.visit(item) for item in node.decorator_list]
            self.scope = scope

            returns = self.visit(node.returns) if node.returns else None

        result = {
            "node": "Function",
            "kind": kind,
            "parameters": params,
            "decorators": decorators,
            "returns": returns,
            "body": body,
        }
        self.scope = previous_scope
        self.global_names = previous_globals
        self.nonlocal_names = previous_nonlocals
        return result

    def visit(self, node: ast.AST | None) -> Any:
        if node is None:
            return None
        if isinstance(node, FUNCTION_NODES):
            return self._function(node, self.scope)
        method = getattr(self, f"visit_{type(node).__name__}", None)
        if method:
            return method(node)
        return self.generic_visit(node)

    def generic_visit(self, node: ast.AST) -> Any:
        fields = []
        for field, value in ast.iter_fields(node):
            if field in {"type_comment", "kind"} and value is None:
                continue
            if isinstance(value, ast.AST):
                normalized = self.visit(value)
            elif isinstance(value, list):
                normalized = [self.visit(item) if isinstance(item, ast.AST) else item for item in value]
            else:
                normalized = value
            fields.append((field, normalized))
        return {"node": type(node).__name__, "fields": fields}

    def visit_Name(self, node: ast.Name) -> Any:
        # Names in decorators and annotations of a top-level function are
        # evaluated in module scope, represented here as free references.
        if self.scope is None:
            return {"node": "FreeRef", "origin": "module", "name": node.id}
        if node.id in self.global_names:
            return {"node": "FreeRef", "origin": "global", "name": node.id}
        resolved = self.scope.resolve_local(node.id)
        if resolved and node.id not in self.nonlocal_names:
            depth, kind, slot = resolved
            return {"node": "BoundRef", "depth": depth, "kind": kind, "slot": slot}
        if resolved and node.id in self.nonlocal_names:
            depth, kind, slot = resolved
            return {"node": "CaptureRef", "depth": depth, "kind": kind, "slot": slot, "name": node.id}
        return {"node": "FreeRef", "origin": "external", "name": node.id}

    def visit_arg(self, node: ast.arg) -> Any:
        assert self.scope is not None
        resolved = self.scope.resolve_local(node.arg)
        if resolved is None:
            raise AlphaAstError(f"unresolved parameter binding: {node.arg}")
        depth, kind, slot = resolved
        return {
            "node": "ParameterRef",
            "depth": depth,
            "kind": kind,
            "slot": slot,
            "annotation": self.visit(node.annotation) if node.annotation else None,
        }

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        return {
            "node": "Attribute",
            "value": self.visit(node.value),
            "attribute": node.attr,
            "context": type(node.ctx).__name__,
        }

    def visit_Constant(self, node: ast.Constant) -> Any:
        value = node.value
        if isinstance(value, float):
            encoded = {"type": "float", "value": value.hex()}
        elif isinstance(value, complex):
            encoded = {"type": "complex", "real": value.real.hex(), "imag": value.imag.hex()}
        elif isinstance(value, bytes):
            encoded = {"type": "bytes", "value": value.hex()}
        else:
            encoded = {"type": type(value).__name__, "value": value}
        return {"node": "Constant", "value": encoded}

    def _bind_comprehension_target(self, target: ast.AST, scope: Scope) -> Any:
        for name in bound_names_from_target(target):
            scope.bind(name, "comprehension")
        return self.visit(target)

    def _normalize_comprehension(
        self,
        node_kind: str,
        element: ast.AST,
        generators: list[ast.comprehension],
        *,
        key: ast.AST | None = None,
    ) -> Any:
        """Normalize a comprehension using its own lexical scope.

        The first iterable is evaluated in the enclosing scope. Each target is
        then bound for its filters, subsequent iterables, and result expression.
        """
        previous_scope = self.scope
        assert previous_scope is not None
        comprehension_scope = Scope(
            parent=previous_scope,
            kind="comprehension",
            bindings={},
        )
        normalized_generators = []
        try:
            for index, generator in enumerate(generators):
                # Python evaluates the first iterable outside the implicit
                # comprehension scope. Later iterables can reference prior targets.
                if index == 0:
                    self.scope = previous_scope
                    normalized_iter = self.visit(generator.iter)
                    self.scope = comprehension_scope
                else:
                    self.scope = comprehension_scope
                    normalized_iter = self.visit(generator.iter)

                normalized_target = self._bind_comprehension_target(
                    generator.target,
                    comprehension_scope,
                )
                normalized_ifs = [self.visit(condition) for condition in generator.ifs]
                normalized_generators.append({
                    "target": normalized_target,
                    "iter": normalized_iter,
                    "ifs": normalized_ifs,
                    "is_async": bool(generator.is_async),
                })

            self.scope = comprehension_scope
            result = {
                "node": node_kind,
                "generators": normalized_generators,
                "element": self.visit(element),
            }
            if key is not None:
                result["key"] = self.visit(key)
            return result
        finally:
            self.scope = previous_scope

    def visit_ListComp(self, node: ast.ListComp) -> Any:
        return self._normalize_comprehension(
            "ListComp",
            node.elt,
            node.generators,
        )

    def visit_SetComp(self, node: ast.SetComp) -> Any:
        return self._normalize_comprehension(
            "SetComp",
            node.elt,
            node.generators,
        )

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> Any:
        return self._normalize_comprehension(
            "GeneratorExp",
            node.elt,
            node.generators,
        )

    def visit_DictComp(self, node: ast.DictComp) -> Any:
        return self._normalize_comprehension(
            "DictComp",
            node.value,
            node.generators,
            key=node.key,
        )

    def visit_Global(self, node: ast.Global) -> Any:
        return {"node": "Global", "names": sorted(node.names)}

    def visit_Nonlocal(self, node: ast.Nonlocal) -> Any:
        return {"node": "Nonlocal", "names": sorted(node.names)}



def canonical_bytes(normalized: Any) -> bytes:
    return json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def alpha_ast_hash(
    source: str,
    selector: str | None = None,
    *,
    mode: str = "auto",
) -> tuple[HashResult, Any, bytes]:
    tree = parse_expression_or_module(source, mode=mode)
    function = select_function(tree, selector)
    normalized = AlphaNormalizer().normalize_function(function)
    canonical = canonical_bytes(normalized)
    language_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    schema = python_schema()
    metadata = {
        "profile": PROFILE,
        "language": "python",
        "language_version": language_version,
        "ast_schema": schema,
    }
    payload = DOMAIN + canonical_bytes(metadata) + b"\0" + canonical
    digest = hashlib.sha256(payload).hexdigest()
    result = HashResult(
        profile=PROFILE,
        language="python",
        language_version=language_version,
        ast_schema=schema,
        digest_algorithm="sha256",
        digest=digest,
        canonical_size=len(canonical),
    )
    return result, normalized, canonical


def list_functions(source: str) -> list[str]:
    tree = parse_expression_or_module(source)
    return [name for name, _ in qualified_functions(tree)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Origo alpha_ast_hash reference implementation")
    parser.add_argument("file", type=Path, help="Python source file")
    parser.add_argument("--selector", help="qualified function selector, e.g. outer::lambda#1")
    parser.add_argument("--list", action="store_true", help="list selectable functions")
    parser.add_argument("--show-normalized", action="store_true", help="include normalized tree")
    arguments = parser.parse_args(argv)

    source = arguments.file.read_text(encoding="utf-8")
    if arguments.list:
        for name in list_functions(source):
            print(name)
        return 0

    try:
        result, normalized, _ = alpha_ast_hash(source, arguments.selector)
    except (AlphaAstError, SyntaxError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    document = result.to_dict()
    if arguments.show_normalized:
        document["normalized_tree"] = normalized
    print(json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
