# Adaptador Rust

## Objetivo

O adaptador Rust vincula seletores Overlay a símbolos reais encontrados no arquivo hospedeiro, sem compilar ou executar o programa.

## Comandos

```bash
cargo run -- rust-check examples/prensa.rs
cargo run -- rust-plan examples/prensa.rs
cargo run -- rust-instrument examples/prensa.rs examples/prensa.origo.rs
```

## `rust-check`

Indexa funções, parâmetros, variáveis e retornos e exige que todos os seletores encontrem ao menos um símbolo.

## `rust-plan`

Produz `origo-overlay-rust-plan/v1`, incluindo linha, coluna e símbolo encontrado.

## `rust-instrument`

Cria uma nova cópia com comentários `@origo-site`. Não altera o original e não injeta comportamento executável.

## Filosofia

## Assinaturas multilinhas

A versão 0.3 acompanha parênteses balanceados através de várias linhas e separa parâmetros apenas em vírgulas de nível superior. Assim, tipos genéricos como `Option<Result<T, E>>` não quebram a lista de parâmetros.

Suporta também cláusulas `where` entre a assinatura e o corpo, desde que exista um corpo `{ ... }`.

## Limitações restantes

Métodos, macros, padrões destruturados e semântica de tipos ainda exigirão Tree-sitter ou `rustc`.

A versão lexical mantém o protótipo simples e sem dependências. Para produção, o adaptador deve migrar para Tree-sitter ou para a AST do compilador Rust, preservando a mesma API de `RustAnalysis`.
