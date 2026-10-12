# Relatório final de build — Origo

**Data:** 2026-10-11  
**Commit:** consulte `git rev-parse HEAD` (o hash é informado na entrega; o próprio relatório não pode conter seu hash sem alterar o commit).
**Ambiente:** Ubuntu 24.04, Python 3.12.3, Rust 1.99.0, Cargo 1.99.0

## Resultado

**Aprovado para execução local e CI**, com a ressalva de que o adaptador Rust continua lexical e não substitui uma AST completa do compilador.

## Testes executados

### Python

```text
20 testes internos: PASS
1 teste consolidado com 635 vetores: PASS
635/635 vetores: PASS
release_check.py: PASS (130 vetores internos)
CLI instalada: PASS
```

### Rust

```text
cargo fmt --check: PASS
cargo check: PASS
cargo check --examples: PASS
cargo test: PASS (7 testes unitários + 4 integração)
cargo clippy --all-targets -- -D warnings: PASS
doc-tests: PASS (0 testes, sem falhas)
```

### CLI Overlay

```text
scan: PASS
inspect: PASS
verify: PASS
plan JSON: PASS (2 eventos)
rust-check: PASS (2 seletores, 7 símbolos)
rust-plan: PASS
rust-instrument: PASS
```

## Artefatos

- `artifacts/origo_alpha_ast-1.0.0-py3-none-any.whl`
- `artifacts/origo-overlay-0.3.0-linux-x86_64`
- `artifacts/SHA256SUMS`

Os checksums devem ser verificados antes de distribuir os artefatos.

## Comando oficial

```bash
./scripts/validate.sh
```
