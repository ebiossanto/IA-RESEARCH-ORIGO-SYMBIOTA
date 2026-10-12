# Tabela de comandos Rust

Esta referência reúne os comandos de desenvolvimento, validação e uso do adaptador Rust da Origo Overlay.

## Comandos de desenvolvimento Rust

| Comando | Finalidade | Resultado esperado |
|---|---|---|
| Verificar versão do compilador | Confirma a instalação do compilador Rust | Exibe a versão instalada |
| Verificar versão do Cargo | Confirma a instalação do gerenciador de projetos | Exibe a versão instalada |
| Baixar dependências | Obtém as crates declaradas no manifesto | Dependências disponíveis no cache local |
| Formatar o projeto | Aplica o padrão oficial de formatação Rust | Arquivos formatados |
| Verificar formatação | Valida a formatação sem alterar arquivos | Código de saída zero quando estiver correto |
| Verificar compilação | Analisa tipos e compilação sem gerar executável final | Projeto validado rapidamente |
| Compilar em modo de desenvolvimento | Gera binários com informações de depuração | Artefatos em target/debug |
| Compilar em modo de produção | Gera binários otimizados | Artefatos em target/release |
| Executar todos os testes | Roda testes unitários, integração e exemplos de teste | Relatório da suíte |
| Executar Clippy | Detecta problemas de estilo e padrões suspeitos | Nenhum aviso quando usado em modo estrito |
| Verificar exemplos | Compila todos os programas da pasta examples | Exemplos validados |
| Gerar documentação Rust | Cria a documentação da API pública | Documentação em target/doc |

### Invocações

```bash
rustc --version
cargo --version
cargo fetch
cargo fmt
cargo fmt --check
cargo check
cargo build
cargo build --release
cargo test
cargo clippy --all-targets -- -D warnings
cargo check --examples
cargo doc --no-deps --open
```

## Comandos da Origo Overlay para arquivos Rust

| Comando | Finalidade | Entrada | Saída principal | Código de falha específico |
|---|---|---|---|---:|
| Scanner de Unicode | Detecta controles bidirecionais, caracteres invisíveis e seletores de variação | Arquivo-fonte | Diagnósticos de segurança | 2 |
| Inspeção de overlays | Lista overlays, linhas e quantidade de regras | Arquivo-fonte | Resumo textual | 1 |
| Validação declarativa | Verifica sintaxe, capacidades e ações | Arquivo-fonte | Confirmação de validade | 3 |
| Planejamento genérico | Converte regras em eventos neutros | Arquivo-fonte | JSON de eventos | 1 ou 3 |
| Cálculo de hash | Calcula SHA-256 do host canônico | Arquivo-fonte | Digest com prefixo sha256 | 1 |
| Verificação de integridade | Compara o hash declarado com o calculado | Arquivo-fonte | Confirmação ou divergência | 5 |
| Verificação Rust | Indexa símbolos e resolve todos os seletores | Arquivo Rust | Quantidade de símbolos e seletores | 4 |
| Plano Rust | Produz eventos com linha, coluna e símbolo | Arquivo Rust | JSON do plano Rust | 4 |
| Instrumentação Rust | Gera uma cópia com marcadores declarativos | Arquivo Rust e destino opcional | Novo arquivo Rust | 1 ou 4 |

### Invocações

```bash
cargo run -- scan examples/prensa.rs
cargo run -- inspect examples/prensa.rs
cargo run -- verify examples/prensa.rs
cargo run -- plan examples/prensa.rs
cargo run -- hash examples/prensa.rs
cargo run -- integrity-check examples/prensa.rs
cargo run -- rust-check examples/prensa.rs
cargo run -- rust-plan examples/prensa.rs
cargo run -- rust-instrument examples/prensa.rs examples/prensa.origo.rs
```

## Exemplos Rust executáveis

| Exemplo | Objetivo | Conceitos demonstrados |
|---|---|---|
| Prensa | Executa o programa industrial hospedeiro | Função multilinha, cálculo industrial e overlay incorporado |
| API básica | Usa a biblioteca diretamente | Carrier, política, engine e JSON de eventos |
| Análise Rust | Resolve símbolos em código Rust | Parâmetros, genéricos, variáveis, retorno e instrumentação |
| Integridade SHA-256 | Demonstra detecção de alteração | Canonicalização, digest e verificação criptográfica |

### Invocações

```bash
cargo run --example prensa
cargo run --example api_basica
cargo run --example analisar_rust
cargo run --example integridade_sha256
```

## Códigos de saída

| Código | Significado |
|---:|---|
| 0 | Operação concluída com sucesso |
| 1 | Erro de parsing, validação geral, serialização ou escrita |
| 2 | Caractere Unicode considerado perigoso |
| 3 | Política ou capacidade negada |
| 4 | Seletor Rust não resolvido |
| 5 | Integridade SHA-256 divergente |
| 64 | Uso incorreto da linha de comando |
| 66 | Arquivo de entrada indisponível |

## Sequência recomendada antes de um commit

```bash
cargo fmt --check
cargo check
cargo check --examples
cargo test
cargo clippy --all-targets -- -D warnings
```

## Sequência recomendada para validar a prensa

```bash
cargo run -- scan examples/prensa.rs
cargo run -- integrity-check examples/prensa.rs
cargo run -- rust-check examples/prensa.rs
cargo run -- rust-plan examples/prensa.rs
```

## Sequência recomendada para gerar uma cópia instrumentada

```bash
cargo run -- rust-instrument \
    examples/prensa.rs \
    examples/prensa.origo.rs

cargo check --example prensa
```


## Comandos para publicação

### Validação pré-publicação

```bash
cargo fmt --check
cargo check
cargo check --examples
cargo test
cargo clippy --all-targets -- -D warnings
cargo package --list
cargo package
cargo publish --dry-run
```

### Git e tag

```bash
git status --short
git add .
git commit -m "release: prepara Origo Overlay 0.3.0"
git tag -a v0.3.0 -m "Origo Overlay 0.3.0"
git push origin main
git push origin v0.3.0
```

### Release no GitHub

```bash
gh auth login
gh release create v0.3.0 \
    --verify-tag \
    --draft \
    --title "Origo Overlay 0.3.0" \
    --notes-file RELEASE_NOTES.md

gh release view v0.3.0
```

### crates.io

```bash
cargo login
cargo publish --dry-run
cargo publish
cargo info origo-overlay
```

### Instalação pública

```bash
cargo install origo-overlay --version 0.3.0
origo-overlay scan examples/prensa.rs
```

### Retirada de uma versão problemática

```bash
cargo yank --version 0.3.0
cargo yank --version 0.3.0 --undo
```

A referência detalhada está em `docs/PUBLISHING.md`. Problemas frequentes estão em `docs/TROUBLESHOOTING.md`.
