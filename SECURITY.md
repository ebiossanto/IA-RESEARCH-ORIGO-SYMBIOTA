# Segurança

## Garantias de projeto

- overlays são visíveis, versionáveis e extraídos somente por comando explícito;
- caracteres invisíveis ou bidirecionais suspeitos geram diagnóstico;
- validação de política e integridade falha fechada;
- o core não executa comandos, rede, leitura de segredos ou payloads ocultos;
- o hash inclui perfil, linguagem, schema e algoritmo;
- selectors ausentes, ambíguos ou incompatíveis não são aproximados silenciosamente.

## Não confundir

SHA-256 não comprova autoria. O hash alfa-estrutural não certifica segurança nem comportamento. O adaptador lexical Rust não é um parser completo.

## Reporte

Não publique segredos, arquivos de credenciais ou amostras sensíveis nas issues. Registre um relatório reproduzível contendo versão, comando, entrada mínima e saída. Para vulnerabilidades de distribuição, interrompa o release até revisão.
