# Origo

Produto consolidado para overlays declarativos seguros e hashing AST alfa-estrutural.

## Componentes

- `origo-overlay/`: crate Rust 0.3.0 para extrair, validar, analisar e planejar overlays visíveis em código hospedeiro.
- `origo-alpha-ast/`: pacote Python 1.0.0 com o perfil versionado `origo-alpha-ast-v1`.
- `conformance/vectors/`: 635 vetores externos de conformidade.
- `scripts/`: validação integrada, execução de vetores e verificação de release.
- `docs/`: especificações, arquitetura, segurança e documento de desenvolvimento.

## Princípio de segurança

Nada invisível executa. Nenhum comando é ativado apenas pela presença de um overlay. A validação deve ser explícita e falhar de forma fechada em caso de erro de integridade, política, Unicode ou seletor.

## Requisitos

- Python 3.10 ou superior;
- Rust estável compatível com edition 2024;
- Cargo;
- Git.

## Instalação local

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ./origo-alpha-ast
cargo check --manifest-path origo-overlay/Cargo.toml
```

## Validação completa

```bash
./scripts/validate.sh
```

A validação executa testes Python, os 635 vetores, build/testes/Clippy Rust, verificações de documentação e checagem de artefatos.

Última execução registrada (2026-10-11, Windows 10, Rust 1.99.0, Python 3.12.10): **APROVADO** — veja [`docs/VALIDATION_REPORT.md`](docs/VALIDATION_REPORT.md), as evidências em [`docs/evidence/`](docs/evidence/) e o certificado em [`docs/CERTIFICADO_DE_VALIDACAO.md`](docs/CERTIFICADO_DE_VALIDACAO.md).

## Uso Python

```bash
origo-alpha-ast exemplo.py --list
origo-alpha-ast exemplo.py --selector modulo::funcao
```

API:

```python
from origo_alpha_ast import alpha_ast_hash
result, normalized, canonical = alpha_ast_hash("lambda value: value * 2")
print(result.compact)
```

## Uso Rust

```bash
cargo run --manifest-path origo-overlay/Cargo.toml -- scan origo-overlay/examples/prensa.rs
cargo run --manifest-path origo-overlay/Cargo.toml -- verify origo-overlay/examples/prensa.rs
cargo run --manifest-path origo-overlay/Cargo.toml -- plan origo-overlay/examples/prensa.rs
```

## Release

A publicação não é automática neste workspace. Primeiro execute `./scripts/validate.sh`, revise o changelog, crie uma tag e publique os artefatos somente mediante ação explícita.

## Documentação

Comece por [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md), depois consulte:

- [`docs/VALIDATION_REPORT.md`](docs/VALIDATION_REPORT.md): relatório da validação completa (2026-10-11);
- [`docs/CERTIFICADO_DE_VALIDACAO.md`](docs/CERTIFICADO_DE_VALIDACAO.md): certificado com hashes SHA-256;
- `origo-alpha-ast/docs/SPECIFICATION.md`;
- `origo-alpha-ast/README.md`;
- `origo-overlay/docs/SPEC.md`;
- `origo-overlay/docs/ARCHITECTURE.md`;
- `origo-overlay/SECURITY.md`.
