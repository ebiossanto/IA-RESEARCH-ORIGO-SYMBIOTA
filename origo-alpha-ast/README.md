# Origo Overlay `alpha_ast_hash` para Python

Implementação de referência do perfil `origo-alpha-ast-v1` para AST do Python.

## Características

- usa a AST oficial do Python;
- remove influência de formatação e comentários comuns;
- normaliza parâmetros e variáveis locais por slots léxicos;
- preserva atributos, literais, operadores e referências externas;
- preserva capturas por nome no perfil v1;
- inclui separação de domínio e metadados do schema no SHA-256;
- falha para seletores ausentes ou ambíguos;
- inclui vetores positivos e negativos.

## Executar os testes

```bash
python -m unittest discover -s tests -v
python run_vectors.py
```

## Usar pela CLI

Listar funções selecionáveis:

```bash
python src/alpha_ast_hash.py exemplo.py --list
```

Calcular o hash:

```bash
python src/alpha_ast_hash.py exemplo.py --selector modulo::funcao
```

Exibir a árvore normalizada:

```bash
python src/alpha_ast_hash.py exemplo.py \
    --selector modulo::funcao \
    --show-normalized
```

## Usar como módulo

```python
from src.alpha_ast_hash import alpha_ast_hash

result, normalized, canonical = alpha_ast_hash(
    "lambda valor: valor * 2"
)

print(result.compact)
print(result.to_dict())
```

## Perfil de bindings

```text
parâmetros      -> slots lexicais
variáveis locais -> slots lexicais
capturas         -> nome preservado
externas/globais -> nome preservado
atributos        -> nome preservado
```

## Limites

Esta é uma implementação de referência, não uma prova de equivalência semântica. Ela cobre a AST do Python e não implementa JavaScript/ESTree. A forma canônica usa JSON determinístico para facilitar inspeção; uma especificação futura pode adotar codificação binária canônica.


## Vetores adicionais: comprehensions e decorators

A suíte inclui agora casos para:

- list, set e dict comprehensions;
- generator expressions;
- generators aninhados;
- filtros de comprehension;
- renomeação alfa dos alvos de comprehension;
- mudanças de atributos e filtros;
- decorators simples;
- decorators com argumentos;
- ordem de decorators;
- caminhos de atributos em decorators.

Os alvos das comprehensions recebem slots lexicais próprios. A ordem dos
generators, condições, atributos e expressões permanece significativa.
Decorators integram a identidade da função na ordem em que aparecem.

## Vetores avançados

A suíte cobre também:

- comprehensions aninhadas em elementos, chaves e valores;
- captura de bindings da comprehension externa pela interna;
- generator expressions aninhadas;
- mudança de filtros, atributos e ordem estrutural entre níveis;
- decorators que são chamadas;
- lambdas posicionais e nomeadas em decorators;
- chamadas aninhadas dentro de decorators;
- mudanças de factory, callee, literal e captura livre.

Decorators são normalizados no escopo léxico externo à função decorada, pois suas expressões são avaliadas antes do binding da função decorada. Lambdas declaradas dentro do decorator possuem escopo próprio e recebem a mesma normalização alfa aplicada às demais funções anônimas.

## Async comprehensions e decorators com closures

A suíte inclui casos para:

- list comprehensions assíncronas;
- generator expressions assíncronas;
- filtros em async comprehensions;
- níveis assíncronos aninhados;
- combinação de generators assíncronos e síncronos;
- diferença estrutural entre `async for` e `for`;
- closures de dois e três níveis em decorators;
- closures em argumentos posicionais e nomeados;
- captura de bindings externos;
- mudanças de literal, operador, ordem de bindings e referência livre.

O campo `is_async` de cada generator faz parte da representação canônica. Portanto, substituir `async for` por `for` altera o `alpha_ast_hash`.

## Async generators aninhados e decorators encadeados

A suíte agora cobre:

- generator expressions assíncronas em múltiplos níveis;
- referências do nível interno ao binding assíncrono externo;
- `await` dentro do elemento de uma async comprehension;
- mistura de `async for` e `for` em níveis sucessivos;
- alterações no modo assíncrono de apenas um nível;
- filtros e atributos em generators assíncronos internos;
- dois ou três decorators encadeados contendo closures;
- manutenção da ordem de aplicação dos decorators;
- closures independentes por decorator;
- mudanças de factory, literal, operador, referência livre e ordem de bindings.

A lista de decorators permanece ordenada na representação canônica. Isso é necessário porque a ordem de aplicação de decorators é semanticamente relevante. Cada lambda ou closure dentro de uma expressão decoradora recebe seu próprio escopo normalizado.

## Async generators com `yield` e decorators parametrizados em cadeia

A suíte cobre agora:

- funções `async def` que produzem valores com `yield`;
- `yield` dentro de laços `async for`;
- `yield await chamada(...)`;
- async generators aninhados como funções locais;
- distinção entre `yield` e `return`;
- preservação da ordem de múltiplos `yield`;
- cadeias de decorators com argumentos posicionais e nomeados;
- decorators parametrizados com chamadas e lambdas aninhadas;
- mudanças de ordem, factory, literal, keyword e chamada interna.

Os nós `Yield`, `Await`, `Return`, `AsyncFor` e a lista ordenada de decorators permanecem distintos na representação canônica.

## `yield from` e decorators com `*args` e `**kwargs`

A suíte cobre também:

- delegação simples com `yield from`;
- delegação para variável local e chamada externa;
- generators aninhados delegados;
- múltiplos `yield from` e sua ordem;
- distinção entre `yield`, `yield from` e `return`;
- decorators com argumentos expandidos por `*args`;
- decorators com keywords expandidas por `**kwargs`;
- combinação e encadeamento de ambas as expansões;
- distinção entre expansão e argumento regular;
- mudanças das referências externas usadas nas expansões.

Na AST do Python, `yield from` é representado por um nó distinto de `yield`. Chamadas decoradoras preservam nós `Starred` para `*args`; keywords expandidas por `**kwargs` preservam uma entrada keyword sem nome explícito. Essas diferenças entram na representação canônica.

## Decorators com argumentos mistos e generators recursivos

A suíte cobre agora:

- decorators que combinam argumento posicional, `*args`, keyword explícita e `**kwargs`;
- cadeias contendo múltiplas chamadas decoradoras mistas;
- mudanças isoladas de literal, origem expandida, keyword e tipo do argumento;
- generators diretamente recursivos com `yield from`;
- generators recursivos com acumuladores e condições de parada;
- generator recursivo definido como função local;
- alterações de atributo, callee, condição de parada e passo recursivo.

Chamadas recursivas mantêm o nome da função como referência externa ou binding léxico conforme o contexto. Parâmetros e variáveis locais continuam alfa-normalizados; operadores, atributos, chamadas e literais permanecem significativos.

## Decorators com dicionários literais

A suíte cobre:

- dicionários literais simples usados como argumentos de decorators;
- dicionários aninhados;
- lambdas e chamadas como valores;
- desempacotamento com `**mapping` dentro do literal;
- mudanças em chaves, valores, chamadas e fontes de desempacotamento;
- ordem dos pares chave-valor.

No perfil `origo-alpha-ast-v1`, a ordem dos itens do dicionário é preservada. Embora dois dicionários possam terminar com conteúdo semelhante, a avaliação das expressões de chave e valor ocorre em ordem e pode produzir efeitos observáveis. Por isso, reordenar os pares altera o hash estrutural.

## Pacote finalizado

Instalação local:

```bash
python -m pip install .
```

CLI instalada:

```bash
origo-alpha-ast arquivo.py --list
origo-alpha-ast arquivo.py --selector caminho::funcao
```

API pública:

```python
from origo_alpha_ast import alpha_ast_hash

result, normalized, canonical = alpha_ast_hash("lambda valor: valor * 2")
print(result.compact)
```

Validação de release:

```bash
python scripts/release_check.py
```

O projeto é uma implementação de referência em estado beta. Um hash igual indica
equivalência alfa-estrutural sob o perfil e schema informados, não equivalência
semântica geral nem certificação de segurança.
