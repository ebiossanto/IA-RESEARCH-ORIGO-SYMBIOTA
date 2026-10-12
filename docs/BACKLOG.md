# Backlog pós-release

## Prioridade alta

- migrar o adaptador Rust para Tree-sitter ou parser equivalente;
- adicionar matriz local automatizada para Python 3.10–3.13;
- executar lint, mypy, auditoria de dependências e scan de segurança no CI;
- adicionar fuzzing para parser, carrier e normalizador;
- definir diagnóstico JSON estável entre Overlay e `alpha_ast_hash`.

## Prioridade média

- sidecar `.oro` ligado por hash;
- assinaturas Ed25519 para autenticidade;
- exportação W3C PROV JSON-LD e integração SLSA/in-toto;
- benchmarks de normalização, hashing e resolução;
- adaptadores AST para JavaScript/TypeScript e Python integrado ao Overlay.

## Prioridade baixa / pesquisa

- runtime de telemetria isolado e fail-safe;
- codificação binária canônica alternativa ao JSON;
- perfis adicionais de watermark detectável, sem comandos;
- suporte a ambientes industriais com garantias temporais demonstradas.

Nenhum item deve ser iniciado sem especificação, teste de regressão e justificativa arquitetural.
