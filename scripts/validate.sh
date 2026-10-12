#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
PYTHON=${PYTHON:-python3}

printf '%s\n' '== Python: instalação e testes =='
"$PYTHON" -m pip install --quiet --no-deps -e "$ROOT/origo-alpha-ast"
"$PYTHON" -m unittest discover -s "$ROOT/origo-alpha-ast/tests" -v
"$PYTHON" -m unittest discover -s "$ROOT/tests" -v
"$PYTHON" "$ROOT/scripts/run_all_vectors.py"
"$PYTHON" "$ROOT/origo-alpha-ast/scripts/release_check.py"

printf '%s\n' '== Python: CLI smoke =='
tmp=$(mktemp --suffix=.py)
trap 'rm -f "$tmp"' EXIT
printf 'def f(value):\n    return value + 1\n' > "$tmp"
"$ROOT/.venv/bin/origo-alpha-ast" "$tmp" --list 2>/dev/null || origo-alpha-ast "$tmp" --list

printf '%s\n' '== Rust: quality gates =='
cargo fmt --manifest-path "$ROOT/origo-overlay/Cargo.toml" --check
cargo check --manifest-path "$ROOT/origo-overlay/Cargo.toml"
cargo check --manifest-path "$ROOT/origo-overlay/Cargo.toml" --examples
cargo test --manifest-path "$ROOT/origo-overlay/Cargo.toml"
cargo clippy --manifest-path "$ROOT/origo-overlay/Cargo.toml" --all-targets -- -D warnings

printf '%s\n' 'VALIDATION PASSED: Python, 635 vectors and Rust gates'
