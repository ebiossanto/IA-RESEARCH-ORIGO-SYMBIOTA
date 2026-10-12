# Publicação da Origo Overlay

Esta referência descreve um fluxo conservador para publicar o código no Git, criar uma release e publicar a crate em `crates.io`.

> Publicações de uma versão de crate não devem ser tratadas como reversíveis. Revise o pacote produzido antes do envio.

## 1. Preparar metadados

Antes de publicar, complete o `Cargo.toml` com endereços reais:

```toml
[package]
name = "origo-overlay"
version = "0.3.0"
edition = "2024"
description = "Safe declarative provenance overlay language for host source code"
license = "MIT OR Apache-2.0"
readme = "README.md"
repository = "https://github.com/SEU_USUARIO/origo-overlay"
documentation = "https://docs.rs/origo-overlay"
homepage = "https://github.com/SEU_USUARIO/origo-overlay"
keywords = ["provenance", "overlay", "audit", "rust"]
categories = ["development-tools", "parser-implementations"]
```

Não use `SEU_USUARIO` literalmente. Confirme também que o nome da crate está disponível:

```bash
cargo search origo-overlay
```

## 2. Incluir licenças

O manifesto declara:

```text
MIT OR Apache-2.0
```

Antes da publicação, inclua os textos completos:

```text
LICENSE-MIT
LICENSE-APACHE
```

Confirme o conteúdo do pacote:

```bash
cargo package --list
```

## 3. Validar a árvore de trabalho

```bash
git status --short
cargo fmt --check
cargo check
cargo check --examples
cargo test
cargo clippy --all-targets -- -D warnings
cargo doc --no-deps
```

Revise mudanças:

```bash
git diff --check
git diff
```

## 4. Validar o pacote local

Liste os arquivos:

```bash
cargo package --list
```

Crie e valide o pacote:

```bash
cargo package
```

Simule a publicação sem upload:

```bash
cargo publish --dry-run
```

Os artefatos são criados em:

```text
target/package/
```

Inspecione:

```bash
find target/package -maxdepth 2 -type f -print
```

## 5. Preparar commit e tag

```bash
git add \
    Cargo.toml \
    Cargo.lock \
    README.md \
    CHANGELOG.md \
    SECURITY.md \
    ROADMAP.md \
    docs \
    examples \
    src \
    tests \
    LICENSE-MIT \
    LICENSE-APACHE

git commit -m "release: prepara Origo Overlay 0.3.0"
```

Crie uma tag anotada:

```bash
git tag -a v0.3.0 \
    -m "Origo Overlay 0.3.0"
```

Confira:

```bash
git show v0.3.0 --stat
```

Envie branch e tag:

```bash
git push origin main
git push origin v0.3.0
```

## 6. Criar release no GitHub

Autentique a CLI:

```bash
gh auth login
```

Crie primeiro como rascunho, usando uma tag já enviada:

```bash
gh release create v0.3.0 \
    --verify-tag \
    --draft \
    --title "Origo Overlay 0.3.0" \
    --notes-file RELEASE_NOTES.md
```

Anexe o pacote-fonte, se desejado:

```bash
gh release upload v0.3.0 \
    origo-overlay-0.3.0.zip
```

Revise o rascunho:

```bash
gh release view v0.3.0
```

Depois publique pela interface do GitHub ou edite a release conforme o fluxo adotado pelo projeto.

Também é possível gerar notas automaticamente:

```bash
gh release create v0.3.0 \
    --verify-tag \
    --draft \
    --generate-notes
```

## 7. Autenticar no crates.io

Crie um token de API restrito e autentique a máquina:

```bash
cargo login
```

Em CI, prefira variável secreta do ambiente:

```bash
export CARGO_REGISTRY_TOKEN="TOKEN_RESTRITO"
```

Nunca registre o token no Git, README, histórico de shell compartilhado ou saída pública de CI.

## 8. Publicar a crate

Repita a simulação final:

```bash
cargo publish --dry-run
```

Publique:

```bash
cargo publish
```

Confirme no registro:

```bash
cargo search origo-overlay
cargo info origo-overlay
```

## 9. Validar instalação pública

Depois que o registro indexar a versão:

```bash
cargo install origo-overlay --version 0.3.0
```

Teste o binário instalado:

```bash
origo-overlay scan examples/prensa.rs
origo-overlay rust-check examples/prensa.rs
```

Em um projeto consumidor:

```bash
cargo add origo-overlay@0.3.0
```

## 10. Publicar uma nova versão

Atualize:

```text
Cargo.toml
CHANGELOG.md
README.md
RELEASE_NOTES.md
```

Valide novamente:

```bash
cargo fmt --check
cargo check
cargo check --examples
cargo test
cargo clippy --all-targets -- -D warnings
cargo publish --dry-run
```

Crie nova tag e publique. Nunca tente sobrescrever uma versão já existente.

## 11. Retirar uma versão da resolução automática

Se uma versão publicada apresentar problema sério, ela não é apagada. Consulte a documentação do Cargo e, quando apropriado, use:

```bash
cargo yank --version 0.3.0
```

Para desfazer o yank:

```bash
cargo yank --version 0.3.0 --undo
```

Use yank apenas com justificativa documentada no changelog e na release.

## Checklist de publicação

```text
[ ] Nome da crate disponível
[ ] Metadados reais no Cargo.toml
[ ] LICENSE-MIT e LICENSE-APACHE presentes
[ ] README e documentação atualizados
[ ] Changelog e notas de release atualizados
[ ] cargo fmt --check aprovado
[ ] cargo check aprovado
[ ] cargo check --examples aprovado
[ ] cargo test aprovado
[ ] cargo clippy aprovado
[ ] cargo package --list revisado
[ ] cargo publish --dry-run aprovado
[ ] Árvore Git limpa
[ ] Tag anotada criada e enviada
[ ] Release criada como rascunho e revisada
[ ] Token restrito configurado
[ ] cargo publish executado
[ ] Instalação pública testada
```
