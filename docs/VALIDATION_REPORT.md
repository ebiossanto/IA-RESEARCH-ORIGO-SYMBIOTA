# Relatório de validação — Origo

**Data:** 2026-10-11 (UTC-03:00)
**Comando oficial:** `./scripts/validate.sh`
**Resultado:** **APROVADO — exit code 0** (`VALIDATION PASSED: Python, 635 vectors and Rust gates`)
**Ambiente:** Windows 10 Pro 10.0.19045 (64 bits), host `DESKTOP-SNCVTFN`
**Evidências brutas:** [`evidence/validate-2026-10-11.log`](evidence/validate-2026-10-11.log) e [`evidence/environment-2026-10-11.txt`](evidence/environment-2026-10-11.txt)

## 1. Ferramentas do ambiente

| Ferramenta | Versão |
| --- | --- |
| Python | 3.12.10 (venv do projeto em `.venv/`) |
| rustc / cargo | 1.99.0 (2026-09-28), toolchain `stable-x86_64-pc-windows-gnu` |
| rustfmt / clippy | rustfmt 1.10.0-stable / clippy 0.1.99 |
| Linkador C | MinGW-W64 GCC 16.2.0 (`x86_64-w64-mingw32-gcc`) |
| Git / GitHub CLI | 2.55.0.windows.3 / 2.101.0 (conta `ebiossanto`) |
| Shell de validação | Git Bash (`/usr/bin/bash` do Git for Windows) |

Variáveis fixadas para o ambiente: `RUSTUP_HOME=C:\rustup`, `CARGO_HOME=C:\cargo`,
`PATH` com `C:\cargo\bin`. Todas as variáveis foram gravadas no nível de usuário
(persistem entre sessões).

## 2. Preparação executada nesta máquina

1. **Rust instalado via rustup** (perfil `default`: `rustc`, `cargo`, `rustfmt`,
   `clippy`), toolchain estável 1.99.0.
2. **Toolchain GNU selecionada** como padrão: a máquina não possui Visual Studio
   nem Windows SDK, portanto o alvo `x86_64-pc-windows-msvc` não tinha linkador.
   O alvo `x86_64-pc-windows-gnu` usa o MinGW-W64 já presente em `C:\mingw64\bin`.
3. **Caminhos 100% ASCII** — correção do defeito de build descrito na seção 5:
   `.rustup` → `C:\rustup`, `.cargo` → `C:\cargo` e o workspace →
   `C:\dev\origo-product-final` (junction de conveniência no Desktop aponta para
   o novo local).
4. **venv recriado** no caminho novo e pacote instalado em modo editável:
   `python -m pip install --no-deps -e ./origo-alpha-ast`.
5. **Identidade Git global** configurada (`user.name`, `user.email`,
   `init.defaultBranch=main`).
6. **Auditoria de segredos:** varredura por padrões de chaves/tokens (AWS, GitHub,
   OpenAI, Google, JWT, chaves privadas, Slack) em todos os arquivos do repositório
   → **0 ocorrências**.

## 3. Resultados por gate

### Python

```text
origo-alpha-ast/tests ............. Ran 20 tests ....... OK
tests/ (conformance externa) ...... Ran 1 test ......... OK
vetores externos .................. vectors=635 passed=635 failed=0 files=8
release_check.py .................. release checks passed: 130 vectors
CLI smoke (origo-alpha-ast --list)  executável gerado e respondeu corretamente
```

### Rust (`origo-overlay` 0.3.0)

```text
cargo fmt --check ................................ PASS
cargo check ...................................... PASS
cargo check --examples ........................... PASS
cargo test ....................................... PASS
    unittests src/lib.rs ......... 7 passed, 0 failed
    unittests src/main.rs ........ 0 passed, 0 failed
    tests/overlay.rs ............. 4 passed, 0 failed
    doc-tests .................... 0 passed, 0 failed
cargo clippy --all-targets -- -D warnings ........ PASS
```

**Total: 21 verificações de teste automatizado (20 + 1 Python, 11 Rust) +
635 vetores de conformidade + 130 vetores de release, 0 falhas.**

### Integridade dos artefatos

```text
$ sha256sum -c artifacts/SHA256SUMS
artifacts/origo-overlay-0.3.0-linux-x86_64: OK
artifacts/origo_alpha_ast-1.0.0-py3-none-any.whl: OK
```

Checksums conferem com `artifacts/SHA256SUMS` (recálculo manual via SHA-256
independente também reproduziu os mesmos valores).

## 4. Escopo do que foi validado

- Perfil `origo-alpha-ast-v1` (hash estrutural alfa) contra 635 vetores externos
  em 8 arquivos de `conformance/vectors/`;
- Seletores, ambiguidade, determinismo e detecção de mudança sintática
  (130 casos do `release_check`);
- Extração/validação de overlays, bloqueio de Unicode invisível e exigência de
  capacidade (testes de integração Rust);
- SHA-256 de blocos com e sem overlay (testes unitários Rust);
- Gates de qualidade: formatação, `check`, `clippy -D warnings`, doc-tests.

## 5. Defeito encontrado e corrigido na preparação

**Sintoma:** `cargo build`/`cargo test` falhavam com dezenas de
`ld.exe: cannot find ... No such file or directory` apontando arquivos que
existiam (`.rlib` do sysroot e `.rcgu.o` do próprio projeto).

**Diagnóstico reproducível:**

1. O caminho do perfil do usuário contém caractere não-ASCII
   (`C:\Users\Euzébio Soares\...`).
2. Para comandos longos, o GCC Windows grava a lista de objetos/`.rlib` em um
   **arquivo de resposta** (`@...ccXXXXXX`) codificado em UTF-8.
3. O `ld` do MinGW-W64 interpreta esse arquivo como ANSI/CP1252: `é` vira `Ã©`,
   o caminho deixa de existir e o link falha.
4. **Prova reproduzida em laboratório:** `ld @resp-utf8.txt` →
   `cannot find ...obj ã.o`; `ld @resp-ansi.txt` → arquivo encontrado (o link
   segue e falha apenas por `__main`, esperado no teste isolado).

**Correção aplicada (sem alterar código):** todos os caminhos envolvidos no link
(sysroot do `rustc`, diretório do projeto, `CARGO_HOME`) passaram a ser ASCII.
Validação reexecutada do zero após a mudança: **PASS**.

## 6. Reprodução

```powershell
# PowerShell (Windows)
$env:RUSTUP_HOME="C:\rustup"; $env:CARGO_HOME="C:\cargo"
$env:Path="C:\cargo\bin;$PWD\.venv\Scripts;$env:Path"
$env:PYTHON="/c/dev/origo-product-final/origo-product/.venv/Scripts/python.exe"
& "C:\Program Files\Git\bin\bash.exe" ./scripts/validate.sh
```

```bash
# Linux/macOS
python3 -m venv .venv && . .venv/bin/activate
python -m pip install --no-deps -e ./origo-alpha-ast
./scripts/validate.sh
```

## 7. Conclusão

O workspace está **aprovado para execução local, CI e publicação**. As ressalvas
permanecem as documentadas em [`LIMITATIONS.md`](LIMITATIONS.md): o adaptador Rust
é lexical e não substitui uma AST completa de compilador, e nenhum artefato é
publicado sem ação explícita (política de release do repositório).

O certificado emitido sobre esta validação está em
[`CERTIFICADO_DE_VALIDACAO.md`](CERTIFICADO_DE_VALIDACAO.md).
