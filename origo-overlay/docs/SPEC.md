# Origo Overlay 0.1 - Especificação

## Objetivo
Origo Overlay é uma linguagem declarativa transversal para anexar políticas de proveniência, observação, auditoria e rejeição a código hospedeiro. Ela nunca executa comandos arbitrários e exige invocação explícita da ferramenta.

## Sintaxe mínima
```origo
overlay "nome" {
  version "0.1";
  target "arquivo.rs";
  capability observe;
  capability emit;
  observe variable "temperatura" -> trace "sensor_T3";
  observe return "calcular" -> emit "quality.calculated";
  integrity hash "sha256:...";
}
```

## Seletores
`variable`, `function`, `return`, `parameter "funcao::nome"`.

## Ações
`trace`, `record`, `warn`, `reject`, `emit`.

## Capacidades
`observe`, `emit`, `export`, `warn`, `reject`. Uma ação é inválida sem sua capacidade correspondente.

## Carrier em comentários
Um bloco inicia em `@origo-begin` e termina em `@origo-end`. Linhas podem usar comentários `//`, `#`, `/*` ou `*`.

## Segurança normativa
- Conteúdo invisível não é sintaxe.
- Ativação é sempre explícita.
- Sem rede, subprocessos ou acesso arbitrário a arquivos.
- `scan` bloqueia controles bidirecionais, caracteres invisíveis e seletores de variação.
- Implementações futuras devem adotar perfil de identificadores e detecção de confusáveis alinhados ao UTS #39.

## Comandos
```text
origo-overlay scan arquivo.rs
origo-overlay inspect arquivo.rs
origo-overlay verify arquivo.rs
origo-overlay plan arquivo.rs
```

## Códigos de saída
`0` sucesso; `1` erro de parsing/overlay; `2` Unicode perigoso; `3` política negada; `64` uso; `66` arquivo indisponível.
