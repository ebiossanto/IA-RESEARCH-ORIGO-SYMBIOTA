"""Compatibility wrapper for the original prototype import path."""

from origo_alpha_ast.core import *  # noqa: F401,F403
from origo_alpha_ast.core import main

if __name__ == "__main__":
    raise SystemExit(main())
