# Origo — Documento Consolidado de Desenvolvimento

**Data da auditoria:** 2026-10-11  
**Escopo:** Origo Overlay e perfil Python `alpha_ast_hash`  
**Estado do material auditado:** artefatos ZIP compartilhados; o diretório não contém um checkout Git

## 1. Objetivo deste documento

Este documento organiza o desenvolvimento do Origo em uma sequência lógica, registra o estado real dos artefatos disponíveis, separa fatos verificados de resultados apenas declarados pelos pacotes e define o caminho de conclusão sem expansão desnecessária de escopo.

O objetivo técnico final é um produto seguro e explícito para:

1. transportar metadados declarativos em código hospedeiro;
2. analisar e validar esses metadados sem execução implícita;
3. resolver seletores de forma determinística;
4. produzir planos de eventos e diagnósticos úteis para CI/CD;
5. disponibilizar o perfil versionado `alpha_ast_hash` para equivalência alfa-estrutural de funções Python;
6. manter documentação, testes, artefatos e processo de release reproduzíveis.

> **Regra de segurança preservada:** nada invisível executa e nada executa apenas pela presença de um overlay.

---

## 2. Resultado executivo

O material contém duas linhas técnicas relacionadas, porém ainda não unificadas:

| Linha | Artefato mais completo | Estado identificado |
|---|---|---|
| Overlay | `origo-overlay-0.3.0-technical.zip` e variantes 0.3.0 | Protótipo Rust funcional documentado, com parser de overlay, política, scanner, hash SHA-256, CLI e adaptador Rust lexical |
| Alpha AST Hash | `origo-alpha-ast-final-1.0.0.zip` | Pacote Python instalável, versão 1.0.0, classificado como beta, com API, CLI, CI, wheel e 130 vetores no pacote final |

A principal conclusão é que o `alpha_ast_hash` está mais próximo de uma entrega utilizável localmente. O Overlay Rust ainda deve ser tratado como protótipo técnico até que seja compilado e testado em uma máquina com toolchain Rust.

Não foi possível identificar commit, branch ou histórico Git final: `/home/ubuntu/projects/origo-78ade9cf` não é um repositório Git. Consequentemente, a entrega atual não pode declarar um commit final sem criar ou recuperar um checkout versionado.

---

## 3. Inventário do material disponível

### 3.1 Pacotes de implementação

- `origo-alpha-ast-final-1.0.0.zip`
- `origo-alpha-ast-python.zip`
- `origo-alpha-ast-python-advanced-vectors.zip`
- `origo-alpha-ast-python-async-closures.zip`
- `origo-alpha-ast-python-comprehensions-decorators.zip`
- `origo-alpha-ast-python-decorator-dict-literals.zip`
- `origo-alpha-ast-python-mixed-decorators-recursive-generators.zip`
- `origo-alpha-ast-python-nested-async-chained-decorators.zip`
- `origo-alpha-ast-python-yield-from-star-kwargs.zip`
- `origo-alpha-ast-python-yield-parameterized-decorators.zip`
- `origo-overlay-0.1.0.zip`
- `origo-overlay-0.2.0.zip`
- `origo-overlay-0.3.0.zip`
- variantes `origo-overlay-0.3.0-technical.zip`, `-rust-command-table.zip`, `-rust-examples.zip` e `-publishing-guide.zip`

### 3.2 Vetores compartilhados

Foram encontrados oito arquivos JSON de vetores externos, com **635 casos no total**:

| Arquivo | Casos |
|---|---:|
| `ORIGO_ALPHA_AST_TEST_VECTORS.json` | 25 |
| `ORIGO_ALPHA_AST_TEST_VECTORS_ADVANCED.json` | 40 |
| `ORIGO_ALPHA_AST_TEST_VECTORS_ASYNC_CLOSURES.json` | 56 |
| `ORIGO_ALPHA_AST_TEST_VECTORS_DECORATOR_DICT_LITERALS.json` | 130 |
| `ORIGO_ALPHA_AST_TEST_VECTORS_MIXED_DECORATORS_RECURSIVE_GENERATORS.json` | 120 |
| `ORIGO_ALPHA_AST_TEST_VECTORS_NESTED_ASYNC_CHAINED_DECORATORS.json` | 72 |
| `ORIGO_ALPHA_AST_TEST_VECTORS_YIELD_FROM_STAR_KWARGS.json` | 104 |
| `ORIGO_ALPHA_AST_TEST_VECTORS_YIELD_PARAMETERIZED_DECORATORS.json` | 88 |

O pacote final Python contém um conjunto interno de **130 vetores** e seus resultados registrados indicam 20 testes automatizados aprovados.

### 3.3 Documentação de evolução

- `ler primeiro Origo Overlay desenvolvimento.md`: reformulação segura da ideia original, arquitetura Carrier → Decoder/Parser → Validator → Policy → Instrumenter → Runtime e scanner contra Unicode/Trojan Source.
- `ler segundo desenvolvimento 2 origo.md`: avaliação de maturidade, proposta de Tree-sitter, assinaturas, telemetria, W3C PROV, SLSA e planos alternativos de foco.
- `ORIGO_OVERLAY_TECHNICAL_README.md`: referência operacional do Overlay 0.3.0.
- `ORIGO_OVERLAY_RUST_COMMANDS.md`: tabela de comandos, códigos de saída e sequência recomendada.

---

## 4. Arquitetura final recomendada

A arquitetura deve manter módulos independentes e contratos versionados.

```text
Código hospedeiro / sidecar
        |
        v
Carrier (extração visível)
        |
        v
Parser do Overlay -> Overlay AST / IR
        |
        +--> Scanner Unicode e segurança lexical
        |
        v
Validator (schema, versão, capacidades, integridade)
        |
        v
Resolver de bindings e seletores
        |
        v
Policy Engine (allow / warn / reject; fail-closed)
        |
        v
Planner de eventos -> JSON versionado
        |
        +--> CLI / relatório CI
        +--> Adaptador AST da linguagem hospedeira
        +--> Instrumentação declarativa, quando explicitamente habilitada
```

O `alpha_ast_hash` deve ser um componente separado do Overlay, com esta decomposição:

```text
Fonte Python
   -> parser CPython AST
   -> seleção de exatamente uma função/lambda
   -> escopos léxicos e slots de bindings
   -> normalização estrutural
   -> JSON canônico UTF-8
   -> domain separator + metadados
   -> SHA-256
   -> identificador versionado
```

### Contratos que não devem ser misturados

- **Integridade** do arquivo não é **autenticidade** do autor.
- **Equivalência alfa-estrutural** não é equivalência semântica ou comportamental.
- **Plano declarativo** não é execução de código.
- **Digest** sem perfil, linguagem e schema não é comparável de forma segura.
- **Analisador lexical Rust** não deve ser apresentado como AST completa ou como substituto do compilador.

---

## 5. Estado do Overlay 0.3.0

### 5.1 Capacidades observadas

A documentação e o código empacotado indicam:

- carrier por comentários com `@origo-begin` / `@origo-end`;
- parser de uma linguagem declarativa de overlays;
- modelo de capacidades e ações `trace`, `record`, `emit`, `warn` e `reject`;
- scanner defensivo de Unicode;
- canonicalização do hospedeiro para SHA-256;
- verificação de integridade sem autorreferência do bloco overlay;
- geração de plano `origo-overlay-events/v1`;
- CLI com `scan`, `inspect`, `verify`, `plan`, `hash`, `integrity-check`, `rust-check`, `rust-plan` e `rust-instrument`;
- adaptador Rust que indexa funções, parâmetros, variáveis simples e retornos;
- instrumentação que insere comentários `@origo-site`, sem executar código.

### 5.2 Limitações técnicas confirmadas pela leitura

O adaptador em `src/rust_adapter.rs` faz descoberta manual por texto, mascarando comentários e strings e procurando padrões de `fn`, parâmetros e `let`. Portanto:

- não é uma AST Rust completa;
- não substitui `rustc` nem um parser oficial;
- pode falhar em macros, padrões complexos, bindings destruturados, sintaxe incomum, escopos avançados e construções que não correspondam aos padrões implementados;
- pode produzir resolução múltipla para nomes iguais, em vez de um diagnóstico de seletor ambíguo semanticamente completo;
- o roadmap propõe Tree-sitter, mas a dependência não está presente no `Cargo.toml` 0.3.0 auditado.

Também foi observada uma inconsistência de manutenção: o cabeçalho produzido pelo adaptador ainda informa `Rust Adapter 0.2.0` dentro do pacote 0.3.0.

### 5.3 Segurança e fronteiras

A política de segurança correta para a linha 0.3.x é:

- nenhum gatilho por caractere invisível;
- nenhum processo, rede ou leitura de segredo no core;
- validação estática em modo fail-closed;
- instrumentação apenas declarativa até que um runtime isolado, política explícita e testes de segurança existam;
- scanner de Unicode executado no arquivo inteiro, não somente no bloco overlay.

Telemetria industrial ativa, assinaturas Ed25519, exportação W3C PROV/SLSA e injeção real de código são temas de evolução, não capacidades que devem ser consideradas entregues no 0.3.0.

---

## 6. Especificação do `alpha_ast_hash` v1

### 6.1 Identificador

Formato especificado:

```text
origo-alpha-ast-v1:python:cpython-ast-X.Y:sha256:<digest>
```

A implementação também expõe os campos estruturados `profile`, `language`, `language_version`, `ast_schema`, `digest_algorithm`, `digest` e `canonical_size`.

### 6.2 Pipeline normativo

1. Fazer parse com `ast` oficial do CPython.
2. Resolver exatamente um seletor de função, método/lambda conforme a convenção do pacote.
3. Construir escopos léxicos e slots estáveis.
4. Substituir nomes de parâmetros e locais ligados por referências de profundidade, tipo e slot.
5. Preservar referências externas, atributos, literais, operadores, controle de fluxo e ordem das instruções.
6. Remover posições de origem, formatação e comentários comuns.
7. Serializar a árvore normalizada em JSON UTF-8 determinístico.
8. Prefixar metadados do perfil e `ORIGO\0ALPHA_AST\0V1\0`.
9. Calcular SHA-256.

### 6.3 Política de bindings

| Categoria | Tratamento no perfil v1 |
|---|---|
| Parâmetros | slots lexicais |
| Variáveis locais | slots lexicais |
| Alvos de comprehensions | slots próprios |
| Capturas / `nonlocal` | referência de captura preservando nome |
| Globais e externas | nome preservado |
| Atributos | nome do atributo preservado |
| Literais | codificação determinística por tipo |
| Decorators | preservados e ordenados |
| `async`, `await`, `yield`, `yield from` | nós distintos e significativos |
| Dicionários | ordem dos pares preservada |

### 6.4 Limite de equivalência

Um hash igual significa apenas equivalência alfa-estrutural sob o perfil, linguagem e schema informados. Não prova:

- equivalência semântica geral;
- equivalência de efeitos colaterais;
- segurança do código;
- autoria;
- comportamento em dependências externas;
- compatibilidade entre versões diferentes do schema AST.

Uma mudança incompatível na normalização exige novo identificador de perfil. Nunca comparar apenas o digest nu entre schemas diferentes.

### 6.5 Seletores

O pacote falha explicitamente quando:

- não há função ou lambda selecionável;
- há mais de uma função e o seletor foi omitido;
- um seletor curto corresponde a múltiplos candidatos;
- o seletor não é encontrado.

A listagem observada inclui caminhos como `outer`, `outer::inner` e `outer::lambda#1`.

---

## 7. Evidências de qualidade executadas

### 7.1 Python — verificado neste ambiente

Foi criado um ambiente virtual temporário e instalado o pacote final com `pip install --no-deps` a partir do diretório extraído.

Resultado:

- instalação do pacote `origo-alpha-ast==1.0.0`: **aprovada**;
- `python -m unittest discover -s tests -v`: **20 testes aprovados**;
- execução dos vetores internos: **aprovada**;
- CLI instalada `origo-alpha-ast`: **executada** e listou o seletor `f` do exemplo;
- `scripts/release_check.py`: **aprovado**, com 130 vetores.

Observação: executar a suíte diretamente no checkout extraído, sem instalação e sem `PYTHONPATH=src`, falha com `ModuleNotFoundError: origo_alpha_ast`. O CI fornecido instala o pacote em modo editável antes dos testes, portanto o fluxo documentado corrige essa condição.

### 7.2 Rust — não verificado neste ambiente

A sequência prevista é:

```bash
cargo fmt --check
cargo check
cargo check --examples
cargo test
cargo clippy --all-targets -- -D warnings
```

Ela não pôde ser executada porque o ambiente atual não possui `cargo` (`cargo: command not found`). Isso deve ser registrado como **pendência de validação**, não como aprovação.

### 7.3 CI/CD existente

O pacote Python contém:

- CI em push e pull request;
- matriz Python 3.10, 3.11, 3.12 e 3.13;
- instalação editável;
- `release_check.py`;
- build de wheel;
- workflow de release disparado por tag `v*`;
- `twine check` e upload de artefato.

O CI Python ainda não executa explicitamente `ruff`, `mypy`, auditoria de dependências ou scanner de segurança, embora essas ferramentas apareçam como dependências opcionais de desenvolvimento. Não há workflow Rust no material do pacote final auditado.

---

## 8. Sequência lógica para finalizar o produto

### Fase 0 — Recuperar versionamento

1. Localizar o repositório Git original ou criar um checkout inicial a partir do artefato final.
2. Preservar os ZIPs originais como evidência, sem misturá-los automaticamente ao código-fonte.
3. Registrar a origem, checksum e data de cada artefato.
4. Criar branch de integração, por exemplo `origo/finalization`.
5. Adicionar este documento ao repositório.

**Critério de saída:** branch e commit identificáveis, com histórico ou registro explícito da ausência dele.

### Fase 1 — Separar produtos e contratos

1. Manter `origo-overlay` como crate Rust.
2. Manter `origo-alpha-ast` como pacote Python.
3. Definir se haverá monorepo ou dois repositórios; não duplicar código por cópia de ZIP.
4. Versionar separadamente o Overlay, a API Python e o perfil de hash.
5. Definir um contrato comum apenas para identificadores, planos e diagnósticos, sem forçar a mesma implementação entre linguagens.

**Critério de saída:** estrutura de diretórios única e sem protótipos concorrentes ativos.

### Fase 2 — Consolidar `alpha_ast_hash`

1. Instalar a árvore Python como pacote em ambiente limpo.
2. Fazer os testes importarem de modo consistente tanto em checkout quanto em instalação (`pytest`/`pythonpath` ou configuração equivalente).
3. Incorporar os 635 vetores externos ao conjunto de conformidade ou documentar formalmente quais 130 são o subconjunto normativo atual.
4. Testar todos os Python suportados na matriz 3.10–3.13.
5. Fixar e publicar o schema AST efetivamente usado em cada versão.
6. Adicionar testes de erro para selector ausente, ambíguo, inexistente e fonte sem função.
7. Adicionar lint, tipos e auditoria de dependências ao CI.
8. Gerar wheel e sdist em ambiente limpo e comparar conteúdo/manifesto; não declarar reprodutibilidade sem essa verificação.

**Critério de saída:** API, CLI, vetores, metadados e erros estáveis; build reproduzível demonstrado.

### Fase 3 — Validar e endurecer o Overlay

1. Instalar toolchain Rust compatível com edição 2024.
2. Executar fmt, check, exemplos, testes e Clippy estrito.
3. Corrigir a identificação do adaptador `0.2.0` para a versão correta.
4. Adicionar casos de seletor ausente, não resolvido, ambíguo e incompatível.
5. Delimitar no README quais construções Rust o analisador lexical suporta.
6. Decidir e implementar Tree-sitter ou retirar essa promessa do roadmap imediato.
7. Adicionar CI Rust em pull requests e tags.
8. Validar que `rust-instrument` só gera marcadores declarativos e não altera a semântica do arquivo.

**Critério de saída:** suíte Rust aprovada em ambiente com Cargo e limitações do adaptador explicitamente testadas.

### Fase 4 — Integração e relatórios CI

1. Definir formato de diagnóstico estável com código, severidade, arquivo, linha, coluna e remediação.
2. Definir formato JSON versionado para planos e resultados.
3. Criar comando de relatório para CI com saída humana e máquina.
4. Padronizar códigos de saída para parsing, política, Unicode, seletor e integridade.
5. Integrar `alpha_ast_hash` ao fluxo de seleção Python somente após definir o contrato de linguagem/schema.
6. Adicionar fixtures cross-platform e testes de encoding UTF-8.

**Critério de saída:** uma pipeline consegue falhar de modo determinístico e explicar a causa.

### Fase 5 — Release explícito

1. Atualizar CHANGELOG e guia de migração.
2. Criar tag somente após aprovação dos gates.
3. Gerar wheel, sdist, binário Rust e checksums.
4. Executar verificações de conteúdo e licença.
5. Publicar somente por ação explícita e revisão humana.
6. Arquivar relatório de release e vetores usados.

**Critério de saída:** artefatos versionados, checksums, documentação e procedimento de rollback disponíveis.

---

## 9. Backlog pós-release, fora do bloqueio atual

- Adaptadores baseados em AST oficial/Tree-sitter para Rust, Python e JavaScript.
- Sidecar `.oro` ligado por integridade.
- Assinaturas Ed25519 para autenticidade de políticas e atestações.
- Exportação W3C PROV JSON-LD e envelope alinhado a SLSA/in-toto.
- Benchmarks de custo do hashing e resolução de seletores.
- Runtime de telemetria isolado, com buffers não bloqueantes e testes fail-safe.
- Codificação binária canônica alternativa ao JSON, mediante novo perfil.
- Scanner Unicode baseado em regras documentadas de UTS #39.
- Testes de fuzzing para parser, carrier, normalizador e resolução.

Esses itens não devem ser implementados antes de fechar os bloqueadores de versionamento, instalação, testes, integração e CI.

---

## 10. Limitações e riscos restantes

1. **Sem repositório Git no material atual:** não há commit ou branch final verificável.
2. **Rust não validado localmente:** falta `cargo`; os resultados do ZIP não substituem uma execução independente.
3. **Parser Rust lexical:** não oferece a precisão de uma AST completa.
4. **Produtos ainda não integrados:** Overlay Rust e `alpha_ast_hash` Python são distribuídos separadamente.
5. **Python beta:** o pacote é utilizável, mas a própria documentação não o classifica como prova de equivalência semântica.
6. **Schema CPython:** mudanças de versão/schema exigem identificadores distintos; a compatibilidade precisa ser testada por matriz.
7. **Reprodutibilidade de build não demonstrada:** há wheel no ZIP e foi possível construir outro wheel, mas não foi executada comparação formal de conteúdo/byte a byte.
8. **CI incompleto para segurança e tipos:** lint, mypy, auditoria de dependências e Rust CI não estão demonstrados nos workflows auditados.
9. **Configuração parcial:** o Overlay possui política `strict.txt`, mas não há evidência de um formato de configuração completo e unificado para todo o ecossistema.
10. **Autenticidade ausente no perfil atual:** SHA-256 fornece integridade do conteúdo normalizado, não autoria nem não repúdio.

---

## 11. Comandos de instalação, teste e execução

### 11.1 Python alpha_ast_hash

A partir do diretório do pacote Python:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
python -m unittest discover -s tests -v
python run_vectors.py
python scripts/release_check.py
```

Uso da CLI:

```bash
origo-alpha-ast exemplo.py --list
origo-alpha-ast exemplo.py --selector caminho::funcao
origo-alpha-ast exemplo.py --selector caminho::funcao --show-normalized
```

Uso da API:

```python
from origo_alpha_ast import alpha_ast_hash

result, normalized, canonical = alpha_ast_hash(
    "lambda valor: valor * 2"
)
print(result.compact)
```

### 11.2 Overlay Rust

A partir do diretório da crate:

```bash
cargo fetch
cargo fmt --check
cargo check
cargo check --examples
cargo test
cargo clippy --all-targets -- -D warnings
cargo run -- scan examples/prensa.rs
cargo run -- verify examples/prensa.rs
cargo run -- rust-plan examples/prensa.rs
cargo run -- rust-instrument examples/prensa.rs examples/prensa.origo.rs
```

### 11.3 Instalação futura em ambiente limpo

O procedimento de release deve testar, no mínimo:

```bash
python -m pip install --no-cache-dir origo_alpha_ast-<versao>-py3-none-any.whl
origo-alpha-ast --help
```

E, para Rust:

```bash
cargo install --path . --locked
origo-overlay --help
```

---

## 12. Decisões arquiteturais registradas

1. **Execução explícita:** abrir, compilar ou visualizar código não ativa o Origo.
2. **Comentários visíveis como carrier inicial:** favorecem revisão, versionamento e compatibilidade com compiladores hospedeiros.
3. **Fail-closed na validação:** hash divergente, Unicode perigoso, política negada ou seletor inválido impedem o plano aprovado.
4. **Instrumentação declarativa no protótipo:** a geração de comentários não deve ser confundida com injeção executável.
5. **Perfil de hash versionado:** perfil, linguagem, schema AST e algoritmo entram no identificador.
6. **Preservação de ordem:** operadores, literais, decorators, generators, statements, atributos e referências externas permanecem significativos.
7. **Separação de integridade e autenticidade:** assinatura digital é evolução posterior, não deve ser simulada por SHA-256.
8. **Escopo controlado:** Tree-sitter, runtime industrial, W3C PROV e SLSA ficam condicionados aos critérios da fase de integração.

---

## 13. Conclusão de auditoria

O Origo possui uma base conceitual coerente e uma implementação Python `alpha_ast_hash` que foi instalada e executada com sucesso em ambiente virtual limpo, com 20 testes e 130 vetores do pacote final aprovados. O perfil documenta corretamente a fronteira entre equivalência alfa-estrutural e equivalência semântica e inclui metadados de schema no identificador.

O Overlay 0.3.0 possui documentação e código suficientes para um protótipo técnico, mas sua validação final está pendente de toolchain Rust. O maior risco técnico conhecido é o adaptador Rust baseado em análise lexical, que não deve ser promovido a parser AST completo sem migração ou delimitação mais rigorosa.

A próxima ação correta não é adicionar funcionalidades: é recuperar o versionamento, consolidar os dois produtos, executar os gates de qualidade em ambientes suportados, corrigir o CI e só então preparar um release com artefatos e checksums. Até essa sequência ser concluída, o estado honesto do projeto é **alpha_ast_hash utilizável em beta; Overlay Rust 0.3.0 protótipo não homologado**.

## Atualização de conclusão — 2026-10-11

A consolidação foi executada no workspace `origo-product`. Foram adicionados os 635 vetores externos, a suíte integrada, os scripts de validação, workflows de CI/release, documentação raiz e artefatos locais. A toolchain Rust foi instalada e os gates completos passaram: `cargo fmt`, `cargo check`, exemplos, testes, doc-tests e Clippy estrito. O estado final é executável localmente e pronto para revisão/publicação futura, sem publicação externa automática.
