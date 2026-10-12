# Limitações conhecidas

1. `alpha_ast_hash` mede equivalência alfa-estrutural, não equivalência semântica.
2. O perfil v1 é específico de Python/CPython AST; schema e versão entram no identificador.
3. O adaptador Rust 0.3.0 é lexical e possui cobertura limitada de sintaxe e escopos.
4. SHA-256 fornece integridade, não autoria ou não repúdio.
5. A instrumentação Rust é declarativa: insere comentários e não executa telemetria.
6. O Overlay não inicia processos, acessa rede, lê segredos ou interpreta payloads invisíveis.
7. O pacote Python possui CI de matriz declarada; a execução local desta entrega foi feita em Python 3.12.
8. Os artefatos são locais; nenhuma publicação externa foi realizada.
9. O formato de configuração de políticas ainda é mais simples que um sistema completo de configuração de produto.
10. Mudanças incompatíveis no normalizador ou schema exigem novo perfil e novos vetores.
