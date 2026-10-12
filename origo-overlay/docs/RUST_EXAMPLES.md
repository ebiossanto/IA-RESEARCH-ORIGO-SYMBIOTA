# Exemplos de uso em Rust

Os exemplos deste diretório mostram duas formas de integração:

1. código Rust hospedeiro contendo uma política Origo Overlay;
2. programas Rust que usam a biblioteca `origo_overlay` diretamente.

## Exemplo industrial hospedeiro

```bash
cargo run --example prensa
```

O arquivo `examples/prensa.rs` contém um programa Rust comum e um bloco Overlay em comentários. Para analisá-lo com a CLI:

```bash
cargo run -- rust-check examples/prensa.rs
cargo run -- rust-plan examples/prensa.rs
cargo run -- integrity-check examples/prensa.rs
```

## API básica

```bash
cargo run --example api_basica
```

Esse exemplo:

- extrai o overlay de uma string Rust;
- valida as capacidades;
- cria eventos;
- serializa o plano como `origo-overlay-events/v1`.

## Adaptador Rust

```bash
cargo run --example analisar_rust
```

Esse exemplo:

- analisa uma assinatura multilinha;
- preserva um tipo genérico com vírgula;
- resolve parâmetro, variável e retorno;
- gera `origo-overlay-rust-plan/v1`;
- produz uma cópia instrumentada em memória.

## Integridade SHA-256

```bash
cargo run --example integridade_sha256
```

Esse exemplo:

- calcula o hash do host canônico;
- constrói uma declaração `integrity hash`;
- verifica o conteúdo original;
- altera o código em memória;
- demonstra a detecção da alteração.

## Usar como dependência local

No `Cargo.toml` de outro projeto:

```toml
[dependencies]
origo-overlay = { path = "../origo-overlay" }
```

No código:

```rust
use std::path::Path;
use origo_overlay::{load, rust_adapter};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = Path::new("src/main.rs");
    let source = std::fs::read_to_string(path)?;
    let overlays = load(path)?;
    let analysis = rust_adapter::analyze(&source, &overlays);
    rust_adapter::validate(&analysis)?;
    println!("{}", rust_adapter::analysis_json(&analysis));
    Ok(())
}
```
