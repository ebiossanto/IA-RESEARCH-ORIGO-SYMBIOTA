.PHONY: install test vectors rust-check validate clean
install:
python3 -m pip install -e ./origo-alpha-ast

test:
python3 -m unittest discover -s origo-alpha-ast/tests -v
python3 -m unittest discover -s tests -v

vectors:
python3 scripts/run_all_vectors.py

rust-check:
cargo fmt --manifest-path origo-overlay/Cargo.toml --check
cargo check --manifest-path origo-overlay/Cargo.toml
cargo check --manifest-path origo-overlay/Cargo.toml --examples
cargo test --manifest-path origo-overlay/Cargo.toml
cargo clippy --manifest-path origo-overlay/Cargo.toml --all-targets -- -D warnings

validate:
./scripts/validate.sh

clean:
rm -rf .venv build dist origo-alpha-ast/build origo-alpha-ast/dist origo-alpha-ast/*.egg-info origo-alpha-ast/src/*.egg-info origo-overlay/target
