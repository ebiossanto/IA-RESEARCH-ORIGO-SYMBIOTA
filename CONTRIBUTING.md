# Contribuição e release

## Desenvolvimento

1. Crie branch a partir de `main`.
2. Faça a mudança em um componente e documente a decisão.
3. Adicione teste antes de ampliar comportamento.
4. Execute `./scripts/validate.sh`.
5. Revise `git diff`, licenças e arquivos temporários.
6. Faça commit com mensagem objetiva.

## Release

1. Atualize `CHANGELOG.md` e a documentação afetada.
2. Execute a validação completa e smoke tests.
3. Gere os artefatos em `artifacts/`.
4. Verifique `SHA256SUMS` em ambiente limpo.
5. Crie tag somente após revisão humana.
6. O workflow de release gera artefatos, mas não publica automaticamente.

## Regra de escopo

Não adicione runtime executável, rede, assinaturas ou novos carriers sem especificação de segurança, testes e revisão arquitetural.
