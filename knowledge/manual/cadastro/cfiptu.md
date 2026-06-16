# Tabela de negocio: `cadastro.cfiptu`

## Identidade

- Nome humano: configuracao anual do calculo de IPTU.
- O que representa: configuracoes gerais usadas pelo calculo de IPTU em determinado exercicio.
- Quando usar:
  - entender parametros globais do calculo por ano;
  - verificar configuracoes de vencimento, historico de isencao, formatacao cadastral e funcoes de calculo;
  - apoiar explicacoes sobre mudanca de regra quando a pergunta envolver configuracao anual.
- Quando evitar:
  - para valor calculado por matricula, usar `iptucalc` ou `iptucalv`;
  - para pagamento/arrecadacao, usar tabelas financeiras;
  - para explicar aumento por fator cadastral sem cruzar com resultados por matricula.

## Grao e chaves

- Grao: uma linha por exercicio/configuracao anual.
- Entidade principal: configuracao de IPTU do exercicio.
- Chave de negocio:
  - `j18_anousu`
- Coluna temporal:
  - `j18_anousu`

## Colunas principais

- `j18_anousu`: exercicio.
- `j18_dtoper`: data de operacao/configuracao, quando preenchida.
- `j18_iptuhistisen`: historico de isencao do IPTU.
- `j18_infla`: parametro de inflacao/correcao, quando usado.
- `j18_perccorrepadrao`: percentual de correcao padrao, quando usado.
- `j18_calcvenc`: configuracao de vencimento.
- `j18_formatlote`, `j18_formatquadra`, `j18_formatsetor`: formatos cadastrais.

## Metricas atomicas

- Parametros percentuais e valores de referencia dependem da configuracao municipal e nao devem ser tratados como causa unica sem validacao.

## Filtros de negocio

- Exercicio: `j18_anousu`.

## Regra de contagem

- Contar linhas de `cfiptu` conta configuracoes anuais, nao imoveis ou calculos.

## Regra de agregacao

- Normalmente nao deve ser agregada; usar como dimensao/configuracao por exercicio.

## Relacionamentos importantes

- `cfiptu.j18_anousu` se relaciona logicamente com exercicios de calculo em `iptucalc`, `iptucalv`, `iptucale` e outras tabelas de IPTU.

## Riscos de duplicidade

- Baixo risco quando usada por exercicio, mas nao deve ser juntada sem necessidade a tabelas de fato que tenham muitas linhas.

## O que nao inferir

- Nao atribuir aumento de IPTU a uma configuracao anual sem comparar os resultados calculados.
- Nao assumir que todo campo percentual esta ativo ou aplicado em todas as matriculas.

## Cuidados

- Configuracao explica contexto, mas nao substitui a analise dos valores e parametros calculados por matricula.
