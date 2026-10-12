# Origo Overlay 0.2 - Especificação formal

## 1. Escopo

Origo Overlay é uma linguagem declarativa de metaprogramação **não executável**. Um programa Overlay descreve observações e decisões de política sobre símbolos de um programa hospedeiro. Sua avaliação produz um plano de eventos, nunca comandos de sistema.

## 2. Domínios semânticos

- `Host`: texto-fonte hospedeiro.
- `Overlay`: módulo declarativo extraído do host.
- `Symbol`: símbolo reconhecido por um adaptador.
- `Selector`: predicado que seleciona símbolos.
- `Action`: intenção declarativa.
- `Capability`: autorização estática requerida por uma ação.
- `Event`: resultado neutro do planejamento.
- `Policy`: limites fornecidos pelo usuário ou organização.
- `Diagnostic`: resultado de erro, alerta ou segurança.

## 3. Léxico

### 3.1 Codificação

Arquivos devem ser UTF-8. Caracteres de controle bidirecional, zero-width e seletores de variação não fazem parte da sintaxe e devem ser diagnosticados antes do parsing.

### 3.2 Identificadores

Na versão 0.2, nomes estruturais são palavras ASCII reservadas. Nomes de símbolos hospedeiros são strings UTF-8 entre aspas e são interpretados pelo adaptador.

### 3.3 Strings

```ebnf
string = '"' , { escaped_quote | escaped_backslash | unicode_scalar } , '"' ;
escaped_quote = '\\"' ;
escaped_backslash = '\\\\' ;
```

A implementação 0.2 suporta escape de aspas. Escape completo será estabilizado em versão posterior.

### 3.4 Comentários hospedeiros

O carrier reconhece um envelope explícito:

```text
@origo-begin
...
@origo-end
```

Marcadores devem ocorrer em linhas distintas. Blocos aninhados são inválidos.

## 4. Gramática concreta

```ebnf
module          = "overlay" string "{" { declaration } "}" ;

declaration     = version_decl
                | target_decl
                | capability_decl
                | integrity_decl
                | observe_decl ;

version_decl    = "version" string ";" ;
target_decl     = "target" string ";" ;
capability_decl = "capability" capability ";" ;
integrity_decl  = "integrity" "hash" string ";" ;
observe_decl    = "observe" selector "->" action ";" ;

capability      = "observe" | "emit" | "export" | "warn" | "reject" ;

selector        = "variable" string
                | "function" string
                | "return" string
                | "parameter" string ;

action          = "trace" string
                | "record" string
                | "emit" string
                | "warn" string
                | "reject" string ;
```

Para `parameter`, a string usa a forma `funcao::parametro`.

## 5. AST abstrata

```text
Overlay = {
  name: String,
  version: Version,
  target: Path?,
  capabilities: Set<Capability>,
  rules: List<Rule>,
  integrity: Integrity?
}

Rule = Selector × Action

Selector =
    Variable(Name)
  | Function(Name)
  | Return(FunctionName)
  | Parameter(FunctionName, ParameterName)

Action =
    Trace(Label)
  | Record(Label)
  | Emit(EventName)
  | Warn(Message)
  | Reject(Message)
```

## 6. Sistema de capacidades

Defina `required(a)`:

```text
required(Trace(_))  = observe
required(Record(_)) = observe
required(Emit(_))   = emit
required(Warn(_))   = warn
required(Reject(_)) = reject
```

Regra de boa formação:

```text
required(action) ∈ overlay.capabilities
─────────────────────────────────────── WF-RULE
overlay ⊢ selector -> action ok
```

Uma ação sem capacidade correspondente é erro de validação.

## 7. Resolução pelos adaptadores

Cada adaptador define um índice:

```text
index_L : Host → Set<Symbol_L>
```

E uma relação de correspondência:

```text
matches_L : Selector × Symbol_L → Bool
```

Uma regra é resolvida quando existe ao menos um símbolo correspondente:

```text
s ∈ index_L(host)    matches_L(selector, s)
──────────────────────────────────────────── RESOLVE
host ⊢ selector ⇓ s
```

Ausência de correspondência é erro no comando de verificação específico da linguagem.

## 8. Planejamento

A função de planejamento é pura:

```text
plan : Overlay × HostIndex → List<Event>
```

Para cada regra e cada símbolo correspondente:

```text
Event {
  overlay,
  action,
  selector,
  payload,
  location,
  symbol
}
```

Planejamento não possui efeitos externos além de produzir dados.

## 9. Política

Uma política define:

```text
Policy = {
  allowed_capabilities,
  max_rules,
  require_integrity
}
```

Validação:

```text
capabilities(overlay) ⊆ allowed(policy)
|rules(overlay)| ≤ max_rules(policy)
require_integrity(policy) ⇒ integrity(overlay) ≠ ∅
```

## 10. Semântica das ações

- `trace`: marca um símbolo como origem ou ponto de derivação.
- `record`: solicita registro de ocorrência.
- `emit`: produz evento de domínio nomeado.
- `warn`: produz diagnóstico não bloqueante em runtime futuro.
- `reject`: torna a política inválida quando avaliada por `verify`.

Nenhuma ação contém linguagem de expressão geral, shell, rede ou carregamento dinâmico.

## 11. Propriedades desejadas

### Transparência do host

Remover blocos Overlay não deve alterar a semântica do compilador hospedeiro.

### Ativação explícita

A presença do bloco não causa execução. Apenas a invocação de `origo-overlay` produz análise.

### Monotonicidade de observação

Adicionar uma regra de observação não pode alterar o código hospedeiro original.

### Falha fechada

Versão desconhecida, capacidade ausente, Unicode perigoso ou seletor irresolvido devem causar diagnóstico, não comportamento implícito.

### Reprodutibilidade

Para mesmo host, overlay, adaptador e política, o plano serializado deve ser determinístico.

## 12. Adaptador Rust 0.2

Símbolos reconhecidos:

- funções `fn nome(...)`;
- parâmetros simples `nome: Tipo`;
- variáveis simples `let nome` e `let mut nome`;
- retorno lógico de uma função, localizado na assinatura.

Limitações deliberadas:

- não resolve padrões de desestruturação;
- não expande macros;
- não resolve módulos ou tipos semanticamente;
- não interpreta aliases, traits ou métodos com precisão de compilador;
- assinaturas multilinhas ainda são limitadas;
- o instrumento gerado adiciona comentários `@origo-site`, não chamadas executáveis.

## 13. Instrumentação declarativa

`rust-instrument` produz uma cópia do arquivo e insere marcadores antes das linhas resolvidas:

```rust
// @origo-site overlay="quality" action="trace" selector="variable:temperatura" payload="T3"
let temperatura = 188.7;
```

O marcador é intencionalmente inerte. Uma futura fase de instrumentação executável deverá exigir runtime explícito, diff visível e política assinada.

## 14. Integridade criptográfica

`integrity hash` usa SHA-256 sobre o host canônico. O host canônico exclui blocos Overlay, remove espaços finais e normaliza linhas com `\n`. A verificação compara o valor declarado com `sha256(canonical_host)`.

Hash garante detecção de alteração acidental ou adversarial do conteúdo, mas não autentica o autor. Assinaturas digitais ficam fora do escopo 0.3.

## 15. Códigos de saída

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
