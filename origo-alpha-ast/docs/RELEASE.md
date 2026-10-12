# Release procedure

```bash
python scripts/release_check.py
python -m pip wheel . --no-deps --no-build-isolation -w dist
```

When development tools are installed:

```bash
python -m build
python -m twine check dist/*
```

Before publishing:

1. update `version` in `pyproject.toml` and `src/origo_alpha_ast/__init__.py`;
2. update `CHANGELOG.md`;
3. run all checks on supported Python versions;
4. inspect wheel and source distribution contents;
5. create an annotated Git tag;
6. create a release draft;
7. publish only after reviewing artifacts and checksums.
