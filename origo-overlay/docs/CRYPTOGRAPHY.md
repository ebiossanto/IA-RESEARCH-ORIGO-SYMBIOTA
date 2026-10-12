# Integridade criptográfica

## Algoritmo

A Origo Overlay 0.3 usa SHA-256 por meio da crate `sha2` da comunidade RustCrypto.

## Canonicalização

O hash não inclui nenhum bloco delimitado por `@origo-begin` e `@origo-end`. Isso evita autorreferência: o valor do hash pode ser declarado dentro do próprio overlay sem alterar o digest.

A forma canônica:

1. remove blocos Overlay completos;
2. preserva a ordem das demais linhas;
3. remove espaços no fim de cada linha;
4. normaliza a terminação de cada linha para `\n`;
5. codifica o resultado como UTF-8;
6. calcula SHA-256;
7. representa o digest como 64 dígitos hexadecimais minúsculos com prefixo `sha256:`.

## Comandos

```bash
cargo run -- hash examples/prensa.rs
cargo run -- integrity-check examples/prensa.rs
```

Copie o resultado do primeiro comando para:

```origo
integrity hash "sha256:...";
```

Depois, `integrity-check` falhará se o programa hospedeiro tiver sido alterado.

## Limites

Hash comprova identidade de conteúdo, não autoria. Assinaturas digitais e gestão de chaves serão uma camada posterior. SHA-256 não deve ser usado como senha ou KDF.
