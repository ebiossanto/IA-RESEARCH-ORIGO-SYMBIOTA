# Arquitetura

1. Carrier extrai blocos declarativos.
2. Parser cria Overlay AST.
3. Scanner Unicode examina o arquivo completo.
4. Validator verifica versão, capacidades e limites.
5. Planner converte regras em eventos neutros.
6. Policy Engine permite, alerta ou rejeita.
7. Output serializa `origo-overlay-events/v1`.

## Próximos adaptadores
- Rust: comentários e atributos.
- Python: comentários, decorators e AST.
- C/C++: comentários e Clang AST.
- JavaScript/TypeScript: comentários e ESTree.
- Sidecar: arquivo `.oro` ligado por hash.

## Interoperabilidade de proveniência
O modelo futuro deve mapear eventos para Entity, Activity e Agent e permitir exportação compatível com W3C PROV. Atestações de build podem usar envelope e proveniência alinhados ao ecossistema SLSA/in-toto.
