# Contributing

## Local setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

The core has no runtime dependencies.

## Required checks

```bash
python -m unittest discover -s tests -v
python run_vectors.py
python scripts/release_check.py
```

Optional development checks:

```bash
python -m pip install -e '.[dev]'
ruff check src tests scripts
mypy src/origo_alpha_ast
pytest
```

## Adding a normalization rule

1. document the intended equivalence boundary;
2. add at least one equal and one unequal vector;
3. preserve deterministic serialization;
4. do not change `origo-alpha-ast-v1` behavior silently;
5. create a new profile when compatibility changes.
