# Origo Overlay 0.3.0

**Origo Overlay** é uma linguagem declarativa transversal para anexar políticas explícitas de proveniência, observação, auditoria, integridade e validação a programas escritos em outras linguagens.

O projeto foi concebido para permitir que metadados semânticos “peguem carona” em código hospedeiro sem alterar sua execução normal. Os overlays são transportados em comentários visíveis, inspecionáveis e versionáveis.

> **Princípio de segurança:** nada invisível executa e nada executa sem ativação explícita.

## Estado do projeto

A versão `0.3.0` é um protótipo técnico funcional e inclui:

- linguagem declarativa própria;
- carrier por comentários;
- parser e AST de overlays;
- sistema de capacidades;
- política de validação;
- scanner defensivo de Unicode;
- planejamento determinístico de eventos;
- adaptador Rust lexical;
- suporte a assinaturas Rust multilinhas;
- resolução de funções, parâmetros, variáveis e retornos;
- instrumentação declarativa não executável;
- integridade SHA-256 real;
- canonicalização do código hospedeiro;
- CLI;
- testes unitários e de integração;
- documentação formal.

A implementação ainda é experimental. Ela não substitui o parser do compilador Rust e não deve ser considerada pronta para instrumentação de produção sem validação adicional.

---

## Visão geral

Um overlay é transportado dentro de comentários do arquivo hospedeiro:

```rust
// @origo-begin
// overlay "prensa-quality" {
// version "0.1";
// target "examples/prensa.rs";
// capability observe;
// capability emit;
// integrity hash "sha256:7c61dab41f1837deecd14c4017c9057861295851997c1461d172c4498cde8e83";
// observe variable "temperatura" -> trace "sensor_temperatura";
// observe return "calcular_indice" -> emit "quality.calculated";
// }
// @origo-end

fn calcular_indice(
    forca: f64,
    temperatura: f64,
) -> f64 {
    forca / temperatura
}
```

Para o compilador Rust, o overlay é apenas comentário. Para a ferramenta `origo-overlay`, ele é uma política declarativa que pode ser extraída, analisada, validada e vinculada aos símbolos do programa.

---

## Objetivos

A Origo Overlay busca oferecer:

1. **proveniência transversal:** aplicar rastreabilidade a código já existente;
2. **adoção incremental:** dispensar reescrita integral na linguagem Origo;
3. **transparência:** manter políticas visíveis em revisão de código;
4. **ativação explícita:** impedir efeitos apenas pela presença do overlay;
5. **falha fechada:** rejeitar versões, capacidades, hashes e símbolos inválidos;
6. **interoperabilidade:** produzir planos de eventos consumíveis por outras ferramentas;
7. **simplicidade:** usar uma sintaxe mínima e declarativa.

---

## Não objetivos

A versão atual não pretende:

- executar comandos ocultos;
- interpretar payloads invisíveis;
- iniciar processos;
- acessar rede;
- ler segredos do sistema;
- modificar silenciosamente o arquivo original;
- substituir o compilador Rust;
- fornecer uma linguagem de propósito geral;
- provar autoria apenas com hash.

---

## Estrutura do projeto

```text
origo-overlay/
├── Cargo.toml
├── CHANGELOG.md
├── README.md
├── ROADMAP.md
├── SECURITY.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CRYPTOGRAPHY.md
│   ├── FORMAL_SPEC.md
│   ├── RUST_ADAPTER.md
│   └── SPEC.md
├── examples/
│   └── prensa.rs
├── policies/
│   └── strict.txt
├── src/
│   ├── carrier.rs
│   ├── crypto.rs
│   ├── engine.rs
│   ├── error.rs
│   ├── lib.rs
│   ├── main.rs
│   ├── model.rs
│   ├── output.rs
│   ├── parser.rs
│   ├── policy.rs
│   ├── rust_adapter.rs
│   └── security.rs
└── tests/
    └── overlay.rs
```

---

## Requisitos

- Rust compatível com a edição 2024;
- Cargo;
- acesso inicial ao registro de crates para baixar `sha2`;
- sistema operacional capaz de manipular arquivos UTF-8.

Verifique:

```bash
rustc --version
cargo --version
```

---

## Instalação

Extraia o projeto e entre no diretório:

```bash
unzip origo-overlay-0.3.0.zip
cd origo-overlay
```

Baixe as dependências:

```bash
cargo fetch
```

Compile:

```bash
cargo build
```

Compile em modo otimizado:

```bash
cargo build --release
```

O binário será criado em:

```text
target/release/origo-overlay
```

---

## Validação do projeto

Execute a sequência completa:

```bash
cargo fmt --check
cargo check
cargo test
cargo clippy --all-targets -- -D warnings
```

---

## Sintaxe mínima

```origo
overlay "nome" {
    version "0.1";
    target "arquivo.rs";

    capability observe;
    capability emit;

    integrity hash "sha256:...";

    observe variable "temperatura"
        -> trace "sensor_T3";

    observe parameter "calcular::forca"
        -> record "sensor_P1";

    observe return "calcular"
        -> emit "quality.calculated";
}
```

### Declarações

```text
overlay
version
target
capability
integrity hash
observe
```

### Seletores

```text
variable
function
return
parameter
```

O seletor de parâmetro usa:

```text
funcao::parametro
```

Exemplo:

```origo
observe parameter "calcular_indice::temperatura"
    -> trace "entrada_termica";
```

### Ações

```text
trace
record
emit
warn
reject
```

### Capacidades

```text
observe
emit
export
warn
reject
```

Uma ação sem a capacidade correspondente é inválida.

---

## Carrier em comentários

O bloco começa com:

```text
@origo-begin
```

E termina com:

```text
@origo-end
```

Exemplo Rust:

```rust
// @origo-begin
// overlay "quality" {
// capability observe;
// observe variable "temperatura" -> trace "T3";
// }
// @origo-end
```

O carrier reconhece prefixos comuns:

```text
//
#
/*
*
```

Blocos aninhados, encerramentos sem início e blocos não encerrados são rejeitados.

---

## Comandos da CLI

### Scanner Unicode

```bash
cargo run -- scan examples/prensa.rs
```

Saída esperada:

```text
OK: nenhum Unicode perigoso detectado
```

### Inspeção do overlay

```bash
cargo run -- inspect examples/prensa.rs
```

Saída aproximada:

```text
overlay=prensa-quality linhas=1-12 regras=2
```

### Validação declarativa

```bash
cargo run -- verify examples/prensa.rs
```

### Plano genérico de eventos

```bash
cargo run -- plan examples/prensa.rs
```

### Hash SHA-256 do hospedeiro

```bash
cargo run -- hash examples/prensa.rs
```

Saída do exemplo entregue:

```text
sha256:7c61dab41f1837deecd14c4017c9057861295851997c1461d172c4498cde8e83
```

### Verificação de integridade

```bash
cargo run -- integrity-check examples/prensa.rs
```

Saída esperada:

```text
OK: integridade SHA-256 verificada para 1 overlay(s)
```

### Validação dos seletores Rust

```bash
cargo run -- rust-check examples/prensa.rs
```

### Plano Rust com localização

```bash
cargo run -- rust-plan examples/prensa.rs
```

### Instrumentação declarativa

```bash
cargo run -- rust-instrument \
    examples/prensa.rs \
    examples/prensa.origo.rs
```

Se o destino for omitido, será usado:

```text
examples/prensa.origo.rs
```

---

## Adaptador Rust

O adaptador atual indexa:

- funções;
- retornos lógicos;
- parâmetros simples;
- variáveis declaradas com `let`;
- variáveis declaradas com `let mut`;
- posição em linha e coluna;
- função proprietária da variável.

### Assinaturas multilinhas

```rust
fn calcular<T>(
    forca: f64,
    temperatura: f64,
    transformacao: Option<Result<T, String>>,
) -> f64
where
    T: Clone,
{
    let indice = forca / temperatura;
    indice
}
```

O adaptador acompanha delimitadores balanceados:

```text
(...)
[...]
{...}
<...>
```

Assim, a vírgula de `Result<T, String>` não é tratada como uma divisão entre parâmetros.

### Plano Rust

```json
{
  "schema": "origo-overlay-rust-plan/v1",
  "resolved": [
    {
      "overlay": "prensa-quality",
      "action": "trace",
      "selector": "variable:temperatura",
      "payload": "sensor_temperatura",
      "line": 18,
      "column": 9,
      "symbol": "main::temperatura"
    }
  ],
  "unresolved": []
}
```

### Instrumentação gerada

```rust
// @origo-site overlay="prensa-quality" action="trace" selector="variable:temperatura" payload="sensor_temperatura"
let temperatura = 188.7;
```

O marcador é somente comentário. Ele não executa código e não altera a semântica do programa hospedeiro.

---

## Integridade criptográfica

A Origo Overlay usa SHA-256 por meio da dependência:

```toml
sha2 = "0.11.0"
```

### Formato

```text
sha256:<64 dígitos hexadecimais minúsculos>
```

### Canonicalização

O hash é calculado sobre uma forma canônica do arquivo:

1. blocos entre `@origo-begin` e `@origo-end` são removidos;
2. o restante do código mantém a ordem original;
3. espaços no fim das linhas são removidos;
4. terminações de linha são normalizadas para `\n`;
5. o texto é codificado em UTF-8;
6. SHA-256 é calculado.

A exclusão do overlay evita autorreferência. Assim, o próprio digest pode ser declarado dentro do bloco sem alterar o valor calculado.

### Fluxo recomendado

Calcule:

```bash
cargo run -- hash src/programa.rs
```

Copie o resultado:

```origo
integrity hash "sha256:...";
```

Verifique:

```bash
cargo run -- integrity-check src/programa.rs
```

### Garantias

O hash auxilia na detecção de:

- alteração do código hospedeiro;
- arquivo incorreto;
- corrupção acidental;
- divergência entre política e programa.

### Limites

SHA-256 não comprova:

- autoria;
- identidade do mantenedor;
- momento de criação;
- legitimidade da política;
- ausência de vulnerabilidades.

Assinaturas digitais serão necessárias para autenticação e não estão implementadas nesta versão.

---

## Scanner de segurança Unicode

O scanner rejeita ou diagnostica:

```text
OO-UNICODE-001  controles bidirecionais
OO-UNICODE-002  caracteres invisíveis
OO-UNICODE-003  seletores de variação
```

A presença desses caracteres não constitui sintaxe Overlay e nunca ativa ações.

---

## Sistema de capacidades

Relação entre ações e capacidades:

```text
trace   -> observe
record  -> observe
emit    -> emit
warn    -> warn
reject  -> reject
```

Exemplo inválido:

```origo
overlay "x" {
    observe return "calcular" -> emit "done";
}
```

Exemplo válido:

```origo
overlay "x" {
    capability emit;
    observe return "calcular" -> emit "done";
}
```

---

## Política padrão

A política valida:

- versão do overlay;
- capacidades permitidas;
- limite máximo de regras;
- exigência opcional de integridade;
- correspondência ação-capacidade.

O perfil conceitual estrito está em:

```text
policies/strict.txt
```

Ele proíbe:

```text
network
subprocess
hidden_payload_execution
```

---

## Formatos de saída

### Plano genérico

```text
origo-overlay-events/v1
```

### Plano Rust

```text
origo-overlay-rust-plan/v1
```

Esses identificadores devem ser verificados por consumidores antes de interpretar o conteúdo.

---

## Códigos de saída

```text
0   sucesso
1   parsing, validação geral ou escrita
2   segurança Unicode
3   política Overlay negada
4   seletor do adaptador não resolvido
5   integridade criptográfica divergente
64  uso incorreto
66  arquivo indisponível
```

Exemplo:

```bash
cargo run -- integrity-check examples/prensa.rs
echo $?
```

---

## Testes

Execute tudo:

```bash
cargo test
```

Casos cobertos incluem:

- parsing da sintaxe mínima;
- extração em comentários;
- Unicode invisível;
- capacidade ausente;
- indexação Rust;
- resolução de seletores;
- instrumentação declarativa;
- assinaturas multilinhas;
- tipos genéricos com vírgulas;
- cláusula `where`;
- vetor SHA-256 conhecido;
- canonicalização sem o overlay;
- verificação de hash válido.

---

## API Rust

Módulos públicos:

```rust
origo_overlay::carrier
origo_overlay::crypto
origo_overlay::engine
origo_overlay::error
origo_overlay::model
origo_overlay::output
origo_overlay::parser
origo_overlay::policy
origo_overlay::rust_adapter
origo_overlay::security
```

Exemplo:

```rust
use std::path::Path;
use origo_overlay::{load, rust_adapter};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = Path::new("examples/prensa.rs");
    let source = std::fs::read_to_string(path)?;
    let overlays = load(path)?;

    let analysis = rust_adapter::analyze(
        &source,
        &overlays,
    );

    rust_adapter::validate(&analysis)?;
    println!("{}", rust_adapter::analysis_json(&analysis));

    Ok(())
}
```

---

## Limitações atuais

O adaptador Rust é lexical, não semântico. Ainda não cobre completamente:

- expansão de macros;
- funções produzidas por macros;
- resolução de módulos;
- caminhos completos;
- métodos de traits;
- aliases de tipos;
- todos os padrões de parâmetros;
- desestruturação em `let`;
- closures;
- inferência de tipos;
- associação semântica de símbolos;
- atributos procedurais;
- AST completa do compilador;
- assinaturas digitais.

Para precisão de produção, o adaptador deverá migrar para Tree-sitter ou para interfaces do compilador Rust.

---

## Modelo de segurança

A Origo Overlay estabelece:

- conteúdo invisível não é sintaxe;
- presença do overlay não causa execução;
- análise depende de comando explícito;
- o original não é modificado por padrão;
- instrumentação vai para outro arquivo;
- eventos são dados, não comandos;
- capacidades são declaradas;
- falhas relevantes bloqueiam a validação;
- rede e subprocessos não fazem parte do runtime.

Leia:

```text
SECURITY.md
```

---

## Documentação

- `docs/SPEC.md`: especificação resumida;
- `docs/FORMAL_SPEC.md`: gramática e semântica formal;
- `docs/ARCHITECTURE.md`: arquitetura do sistema;
- `docs/RUST_ADAPTER.md`: adaptador Rust;
- `docs/CRYPTOGRAPHY.md`: canonicalização e SHA-256;
- `SECURITY.md`: modelo de segurança;
- `ROADMAP.md`: evolução planejada;
- `CHANGELOG.md`: histórico de versões.

---

## Roadmap resumido

### Próxima etapa

- parser Rust baseado em Tree-sitter;
- sidecars `.oro`;
- validação real de `target`;
- política configurável por arquivo;
- seleção por caminho qualificado;
- diagnóstico com spans completos.

### Etapas posteriores

- exportação W3C PROV;
- atestações de build;
- assinaturas digitais;
- adaptador Python;
- adaptador JavaScript/TypeScript;
- adaptador C/C++;
- runtime de eventos opcional;
- suíte de conformidade;
- auditoria de segurança.

---

## Changelog da versão 0.3.0

- suporte a assinaturas Rust multilinhas;
- parâmetros com tipos genéricos e vírgulas aninhadas;
- suporte básico a cláusulas `where`;
- SHA-256 real;
- canonicalização do host;
- comando `hash`;
- comando `integrity-check`;
- código de saída `5`;
- testes criptográficos;
- documentação técnica ampliada.

---

## Licença

O manifesto declara:

```text
MIT OR Apache-2.0
```

Antes de publicar oficialmente, inclua os arquivos completos:

```text
LICENSE-MIT
LICENSE-APACHE
```

---

## Aviso de maturidade

A Origo Overlay 0.3.0 é um protótipo de pesquisa funcional. Use-a para estudo, experimentação, desenho de políticas e validação de arquitetura. Antes de uso industrial, são necessárias compilação multiplataforma, CI, fuzzing, análise de dependências, auditoria de segurança e estabilização da especificação.

---

## Exemplos de uso em Rust

A pasta `examples/` contém quatro cenários executáveis.

### 1. Programa hospedeiro industrial

```bash
cargo run --example prensa
```

Analise o mesmo arquivo pela CLI:

```bash
cargo run -- rust-check examples/prensa.rs
cargo run -- rust-plan examples/prensa.rs
cargo run -- integrity-check examples/prensa.rs
```

### 2. Extração e planejamento pela API

```bash
cargo run --example api_basica
```

O exemplo usa:

```rust
use origo_overlay::{
    carrier,
    engine,
    output,
    policy::{self, Policy},
};
```

Fluxo executado:

```text
fonte Rust em memória
        ↓
extração do bloco Overlay
        ↓
validação da política
        ↓
planejamento de eventos
        ↓
JSON origo-overlay-events/v1
```

### 3. Resolução de símbolos Rust

```bash
cargo run --example analisar_rust
```

O arquivo demonstra:

- assinatura multilinha;
- parâmetro genérico `Option<Result<T, String>>`;
- resolução de `calcular::forca`;
- resolução da variável `indice`;
- resolução do retorno de `calcular`;
- geração do plano Rust;
- instrumentação declarativa em memória.

Trecho principal:

```rust
let overlays = carrier::extract_from_host(
    Path::new("analise.rs"),
    source,
)?;

let analysis = rust_adapter::analyze(
    source,
    &overlays,
);

rust_adapter::validate(&analysis)?;
println!("{}", rust_adapter::analysis_json(&analysis));
```

### 4. Integridade SHA-256

```bash
cargo run --example integridade_sha256
```

O exemplo calcula um digest real, verifica o conteúdo original e demonstra a falha depois de uma alteração em memória:

```rust
let digest = crypto::source_hash(source)?;
let overlay = parser::parse_overlay(&overlay_source)?;
crypto::verify_overlay_hash(source, &overlay)?;

let modified = source.replace(
    "processo industrial",
    "processo alterado",
);

assert!(
    crypto::verify_overlay_hash(&modified, &overlay)
        .is_err()
);
```

### Usar como biblioteca local

Adicione ao projeto consumidor:

```toml
[dependencies]
origo-overlay = { path = "../origo-overlay" }
```

Exemplo mínimo:

```rust
use std::path::Path;
use origo_overlay::{load, rust_adapter};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = Path::new("src/main.rs");
    let source = std::fs::read_to_string(path)?;
    let overlays = load(path)?;

    let analysis = rust_adapter::analyze(
        &source,
        &overlays,
    );

    rust_adapter::validate(&analysis)?;
    println!("{}", rust_adapter::analysis_json(&analysis));
    Ok(())
}
```

A documentação ampliada está em `docs/RUST_EXAMPLES.md`.

---

## Tabela de comandos Rust

A referência consolidada de comandos está em:

```text
docs/RUST_COMMANDS.md
```

Ela reúne:

- preparação e compilação com Cargo;
- formatação, testes, Clippy e documentação;
- comandos da Origo Overlay aplicados a arquivos Rust;
- exemplos executáveis;
- códigos de saída;
- sequências recomendadas para CI, validação e instrumentação.

### Validação completa recomendada

```bash
cargo fmt --check
cargo check
cargo check --examples
cargo test
cargo clippy --all-targets -- -D warnings
```

### Análise completa do exemplo industrial

```bash
cargo run -- scan examples/prensa.rs
cargo run -- integrity-check examples/prensa.rs
cargo run -- rust-check examples/prensa.rs
cargo run -- rust-plan examples/prensa.rs
```

---

## Solução de erros comuns e publicação

A documentação operacional foi dividida em duas referências:

```text
docs/TROUBLESHOOTING.md
docs/PUBLISHING.md
```

### Diagnóstico completo

```bash
cargo fmt --check
cargo check
cargo check --examples
cargo test
cargo clippy --all-targets -- -D warnings
cargo package --list
cargo publish --dry-run
```

### Publicação resumida

```bash
cargo package
cargo publish --dry-run

git tag -a v0.3.0 -m "Origo Overlay 0.3.0"
git push origin v0.3.0

gh release create v0.3.0 \
    --verify-tag \
    --draft \
    --title "Origo Overlay 0.3.0" \
    --notes-file RELEASE_NOTES.md

cargo login
cargo publish
```

Antes da primeira publicação, complete os metadados reais do `Cargo.toml`, inclua `LICENSE-MIT` e `LICENSE-APACHE`, revise `cargo package --list` e não publique tokens ou placeholders.
