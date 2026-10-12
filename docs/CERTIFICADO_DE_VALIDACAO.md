# Certificado de validação — Origo

**Certificado nº** `ORIGO-VAL-2026-10-11-01`
**Emissão:** 2026-10-11, 22:36 (UTC-03:00)
**Emissor:** validação automatizada `scripts/validate.sh` no host `DESKTOP-SNCVTFN`
**Solicitante:** Euzébio Soares (GitHub `ebiossanto`)

## 1. Declaração

Certifica-se que o workspace **Origo** (`origo-overlay` 0.3.0 + `origo-alpha-ast` 1.0.0)
foi submetido à suíte oficial de validação neste ambiente e **obteve resultado
APROVADO, com código de saída 0**, sem nenhuma falha:

| Verificação | Resultado |
| --- | --- |
| Testes unitários Python (`origo-alpha-ast/tests`) | 20/20 — OK |
| Teste de conformidade externa (`tests/`) | 1/1 — OK |
| Vetores externos de conformidade | 635/635 em 8 arquivos — OK |
| Verificação de release (`release_check.py`) | 130 vetores — OK |
| Smoke test da CLI | OK |
| `cargo fmt --check` | OK |
| `cargo check` e `cargo check --examples` | OK |
| `cargo test` (unidade + integração + doc-tests) | 11/11 — OK |
| `cargo clippy --all-targets -- -D warnings` | OK |
| Integridade SHA-256 dos artefatos | 2/2 — OK |
| Varredura de segredos no repositório | 0 ocorrências |

## 2. Ambiente certificado

```text
Windows 10 Pro 10.0.19045 (64 bits) · Python 3.12.10 · rustc/cargo 1.99.0
toolchain stable-x86_64-pc-windows-gnu · rustfmt 1.10.0 · clippy 0.1.99
MinGW-W64 GCC 16.2.0 · Git 2.55.0 · GitHub CLI 2.101.0
```

## 3. Hashes SHA-256 dos itens certificados

```text
0cde959bd2d174ad68a26b7673158054efff4107178cf1993981f0a1398e1d4b  artifacts/origo-overlay-0.3.0-linux-x86_64
eb7d6f619656c7892b40f81d8ab4bc2486c529d6cf67464618af36149c54242c  artifacts/origo_alpha_ast-1.0.0-py3-none-any.whl
26c90bb8b093d3a19a45dadc324983cc8f8a7b9d53f1f71fde1f65552a324d1e  docs/VALIDATION_REPORT.md
19336e8f9d3197047157585ba5524acd61abe105496d9bd91347d358d934083c  docs/evidence/validate-2026-10-11.log
f341629160966bf9357578e3c604cb9a5f3c0ddec770402519fe69ef22c13c0a  docs/evidence/environment-2026-10-11.txt
43612b6907e3ffde4c94c09849c9066acaa8809dc67ae3265d74da7614cc2bf6  docs/evidence/ci-run-38192827682.txt
```

Os dois primeiros valores são idênticos aos registrados em
`artifacts/SHA256SUMS`, conferidos com `sha256sum -c`.

## 4. Verificação independente

```bash
sha256sum -c artifacts/SHA256SUMS
sha256sum docs/VALIDATION_REPORT.md docs/evidence/validate-2026-10-11.log \
          docs/evidence/environment-2026-10-11.txt
```

```powershell
Get-FileHash docs\VALIDATION_REPORT.md -Algorithm SHA256
```

## 5. Condições e limitações

- Este certificado atesta a execução da suíte no ambiente e data indicados;
  qualquer alteração de código, dependência ou toolchain invalida os hashes acima
  e exige nova validação (`./scripts/validate.sh`).
- Não substitui auditoria de segurança externa. As restrições conhecidas do
  produto permanecem descritas em `docs/LIMITATIONS.md` e `SECURITY.md`.
- Publicação de artefatos de release continua condicionada à ação explícita
  descrita na seção *Release* do `README.md`.

## 6. Reprodução

```bash
./scripts/validate.sh   # saída final esperada: VALIDATION PASSED
```

## 7. Validação independente em CI pública

O mesmo commit foi validado por máquina independente no GitHub Actions
([Origo CI — run 38192827682](https://github.com/ebiossanto/IA-RESEARCH-ORIGO-SYMBIOTA/actions/runs/38192827682)):

```text
conclusão: completed / success — 5 de 5 jobs aprovadas
python (3.10, 3.11, 3.12, 3.13) → install, 20+1 testes, 635 vetores, wheel: success
rust → fmt --check, check, check --examples, test, clippy -D warnings: success
evidência: docs/evidence/ci-run-38192827682.txt
```

*Documento gerado como parte da publicação do repositório. O relatório completo
com o diagnóstico do ambiente está em `docs/VALIDATION_REPORT.md`.*
