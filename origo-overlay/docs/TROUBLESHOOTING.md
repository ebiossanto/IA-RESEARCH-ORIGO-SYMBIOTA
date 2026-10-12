# Solução de erros comuns

Este guia cobre erros frequentes de instalação, compilação, testes, integridade, análise Rust e publicação da Origo Overlay.

## Diagnóstico rápido

Antes de investigar um erro específico, execute:

```bash
rustc --version
cargo --version
cargo metadata --no-deps
cargo check
cargo test
```

Para obter mais detalhes de uma falha do Cargo:

```bash
cargo check -vv
```

## `cargo: command not found`

### Causa

Rust e Cargo não estão instalados ou o diretório de ferramentas não está no `PATH`.

### Solução

Depois de instalar Rust por uma fonte confiável, abra um novo terminal e verifique:

```bash
rustc --version
cargo --version
```

Em instalações via `rustup`, o diretório normalmente precisa estar disponível no `PATH`:

```bash
source "$HOME/.cargo/env"
```

## Edição Rust 2024 não suportada

### Sintoma

```text
failed to parse manifest
feature `edition2024` is required
```

### Causa

A toolchain é antiga para o manifesto:

```toml
edition = "2024"
```

### Solução

Atualize a toolchain e confirme a versão:

```bash
rustup update stable
rustup default stable
rustc --version
cargo --version
```

## Falha ao baixar `sha2`

### Sintomas

```text
failed to get `sha2` as a dependency
```

ou:

```text
Could not resolve host
```

### Causas possíveis

- rede indisponível;
- proxy corporativo;
- certificado TLS interceptado;
- registro bloqueado;
- cache local ainda vazio.

### Soluções

Tente baixar explicitamente:

```bash
cargo fetch -vv
```

Depois, se o cache já estiver preparado:

```bash
cargo check --offline
cargo test --offline
```

Em rede corporativa, configure o proxy segundo a política local. Não desative validação TLS para contornar certificados.

## `cargo fmt --check` falhou

### Causa

Os arquivos não seguem o formato produzido por `rustfmt`.

### Solução

```bash
cargo fmt
cargo fmt --check
```

Confira o diff antes do commit:

```bash
git diff -- src tests examples
```

## Clippy encontrou avisos

### Sintoma

```text
error: could not compile ... due to previous warning
```

Isso pode ocorrer porque a validação usa:

```bash
cargo clippy --all-targets -- -D warnings
```

### Solução

Execute sem promover avisos para entender o diagnóstico:

```bash
cargo clippy --all-targets
```

Corrija os avisos e repita:

```bash
cargo clippy --all-targets -- -D warnings
```

Evite adicionar `#[allow(...)]` apenas para ocultar um problema sem justificativa técnica.

## `nenhum bloco Origo Overlay encontrado`

### Causa

O arquivo não possui o envelope completo ou os marcadores foram alterados.

### Forma correta

```rust
// @origo-begin
// overlay "quality" {
// capability observe;
// observe variable "temperatura" -> trace "T3";
// }
// @origo-end
```

### Verificações

```bash
grep -n "@origo-" arquivo.rs
cargo run -- inspect arquivo.rs
```

## Bloco aninhado ou não encerrado

### Sintomas

```text
bloco aninhado
```

ou:

```text
bloco iniciado ... nao foi encerrado
```

### Solução

Cada `@origo-begin` precisa de um único `@origo-end`. Blocos não podem ser aninhados.

## `acao requer capability ...`

### Causa

A regra usa uma ação sem declarar a capacidade correspondente.

### Matriz

```text
trace   -> capability observe
record  -> capability observe
emit    -> capability emit
warn    -> capability warn
reject  -> capability reject
```

### Exemplo corrigido

```origo
overlay "quality" {
    capability emit;
    observe return "calcular" -> emit "quality.calculated";
}
```

## `seletores Rust nao resolvidos`

### Causas possíveis

- nome digitado incorretamente;
- variável inexistente;
- parâmetro com função errada;
- símbolo gerado por macro;
- desestruturação ainda não suportada;
- método ou construção fora do subconjunto lexical atual.

### Diagnóstico

```bash
cargo run -- rust-check arquivo.rs
cargo run -- rust-plan arquivo.rs
```

Confira o formato do parâmetro:

```origo
observe parameter "calcular::forca" -> trace "P1";
```

O adaptador 0.3 ainda não oferece resolução semântica completa do compilador Rust.

## Assinatura multilinha não reconhecida

### Verifique

- se a função possui a palavra-chave `fn` explícita;
- se os parênteses estão balanceados;
- se existe corpo delimitado por `{` e `}`;
- se a função não foi criada por macro;
- se os nomes dos parâmetros são padrões simples.

### Forma suportada

```rust
fn calcular<T>(
    forca: f64,
    entrada: Option<Result<T, String>>,
) -> f64
where
    T: Clone,
{
    let indice = forca;
    indice
}
```

## Diagnóstico `OO-UNICODE-001`, `002` ou `003`

### Significado

```text
OO-UNICODE-001  controle bidirecional
OO-UNICODE-002  caractere invisível
OO-UNICODE-003  seletor de variação
```

### Solução

Não copie novamente o caractere suspeito. Reescreva manualmente a linha em um editor que exiba caracteres invisíveis e execute:

```bash
cargo run -- scan arquivo.rs
```

A Origo Overlay não permite esses caracteres como mecanismo de execução ou sintaxe oculta.

## `hash deve usar o prefixo sha256:`

### Forma inválida

```origo
integrity hash "7c61...";
```

### Forma válida

```origo
integrity hash "sha256:7c61...";
```

Gere o valor pelo próprio projeto:

```bash
cargo run -- hash arquivo.rs
```

## `SHA-256 deve conter exatamente 64 digitos hexadecimais`

### Causa

O digest está incompleto, contém caractere não hexadecimal ou possui tamanho incorreto.

### Solução

Não edite o digest manualmente. Gere novamente:

```bash
cargo run -- hash arquivo.rs
```

## `hash divergente`

### Causa

O código hospedeiro mudou depois da criação da declaração de integridade.

### Procedimento seguro

1. confira o diff;
2. confirme que a alteração é legítima;
3. execute testes;
4. gere o novo hash;
5. atualize `integrity hash`;
6. verifique novamente.

```bash
git diff -- arquivo.rs
cargo test
cargo run -- hash arquivo.rs
cargo run -- integrity-check arquivo.rs
```

Nunca atualize automaticamente o hash sem revisar as mudanças que o invalidaram.

## Arquivo indisponível, código 66

### Causas

- caminho incorreto;
- arquivo inexistente;
- falta de permissão;
- diretório usado no lugar de arquivo.

### Diagnóstico

```bash
ls -l arquivo.rs
cargo run -- scan arquivo.rs
echo $?
```

## Instrumentação não foi criada

### Verifique

- se todos os seletores foram resolvidos;
- se o diretório de saída existe;
- se há permissão de escrita;
- se o destino não é um diretório.

```bash
cargo run -- rust-check arquivo.rs
mkdir -p target/origo
cargo run -- rust-instrument arquivo.rs target/origo/arquivo.origo.rs
```

## `cargo package` inclui arquivos indesejados

### Diagnóstico

```bash
cargo package --list
```

### Solução

Configure `include` ou `exclude` no `Cargo.toml`, remova artefatos gerados e repita:

```bash
cargo clean
cargo package --list
cargo package
```

## `cargo publish --dry-run` falhou por metadados

### Causa

O manifesto de publicação pode estar sem campos como repositório, documentação, homepage ou README, ou conter valores provisórios.

### Solução

Revise `Cargo.toml` antes de publicar:

```toml
[package]
name = "origo-overlay"
version = "0.3.0"
description = "Safe declarative provenance overlay language"
license = "MIT OR Apache-2.0"
readme = "README.md"
repository = "https://github.com/SEU_USUARIO/origo-overlay"
documentation = "https://docs.rs/origo-overlay"
homepage = "https://github.com/SEU_USUARIO/origo-overlay"
```

Substitua `SEU_USUARIO` pelo endereço real. Não publique com placeholders.

## Nome da crate indisponível

### Diagnóstico

```bash
cargo search origo-overlay
```

### Solução

Escolha um nome disponível no manifesto, mantendo o nome público do projeto no README se necessário. Nomes no registro são atribuídos por ordem de publicação.

## Versão já publicada

Versões publicadas não podem ser sobrescritas. Incremente a versão:

```bash
cargo set-version 0.3.1
```

Se `cargo-edit` não estiver instalado, altere manualmente o campo `version` em `Cargo.toml` e execute:

```bash
cargo check
cargo package
```

## Token de publicação ausente ou inválido

### Solução

Autentique-se sem colocar o token no repositório:

```bash
cargo login
```

Ou use variável de ambiente no ambiente de CI:

```bash
export CARGO_REGISTRY_TOKEN="TOKEN_RESTRITO"
cargo publish --dry-run
```

Revogue imediatamente qualquer token exposto em logs, commits ou mensagens.

## Tag ou release já existe

### Diagnóstico

```bash
git tag --list

gh release view v0.3.0
```

### Solução

Não force uma tag pública sem avaliar consumidores. Corrija a versão e crie uma nova tag, ou edite a release existente quando apropriado.

## Checklist final de diagnóstico

```bash
cargo fmt --check
cargo check
cargo check --examples
cargo test
cargo clippy --all-targets -- -D warnings
cargo package --list
cargo publish --dry-run
```
