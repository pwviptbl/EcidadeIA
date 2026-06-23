## contabilidade.conlancamemp

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_conlancamemp_classe.php`

Relaciona lancamentos contabeis a empenhos. A classe funciona como ponte entre `conlancam` e `empempenho`, permitindo recuperar pagamentos, documentos, dados do empenho, contratos e desdobramentos da despesa a partir de um codigo de lancamento.

### Estrutura e interpretacao

- **Classe:** `cl_conlancamemp`
- **Tabela principal:** `conlancamemp`
- **Chave primaria:** `c75_codlan`
- **Grau basico:** uma linha por lancamento vinculado a um empenho

Campos de negocio confirmados:

- `c75_codlan`: codigo do lancamento contabil
- `c75_numemp`: numero do empenho vinculado
- `c75_data`: data do vinculo/lancamento

Interpretacao segura:

- `c75_codlan` aponta para `conlancam.c70_codlan` e ancora o registro contabil.
- `c75_numemp` aponta para o empenho afetado pelo lancamento.
- A tabela e de ligacao: o significado contabil completo vem dos joins com `conlancam`, `conhistdoc`, `conlancamdoc`, `empempenho` e tabelas orcamentarias.

### Consulta: `sql_query`

- **Objetivo:** recuperar o vinculo entre lancamento e empenho junto do cabecalho de `conlancam`.
- **Tabelas:** `conlancamemp`, `conlancam`

```sql
select /* campos dinamicos */
  from conlancamemp
       inner join conlancam
          on conlancam.c70_codlan = conlancamemp.c75_codlan
 where conlancamemp.c75_codlan = :codlan
 order by /* ordenacao dinamica */
```

Uso seguro:

- confirmar que um lancamento esta vinculado a empenho;
- ler dados basicos do lancamento com baixa chance de multiplicacao.

### Consulta: `sql_query_file`

- **Objetivo:** ler apenas a tabela fisica `conlancamemp`.

```sql
select /* campos dinamicos */
  from conlancamemp
 where conlancamemp.c75_codlan = :codlan
 order by /* ordenacao dinamica */
```

Uso seguro:

- validar o vinculo bruto entre lancamento e empenho;
- obter apenas `c75_codlan`, `c75_numemp` e `c75_data`.

### Consulta: `sql_query_pagamentoEmpenho`

- **Objetivo:** recuperar pagamentos de empenho com ordem de pagamento e conta contabil associada.
- **Tabelas principais:** `conlancamemp`, `conlancam`, `conlancamord`, `pagordem`, `empempenho`, `cgm`, `conlancamdoc`, `orcdotacao`, `conhistdoc`, `conlancampag`, `conplanoreduz`, `conplano`

Interpretacao segura:

- O metodo foi desenhado para exportacao/arquivo do TCE Sigfis.
- O caminho de pagamento passa por ordem de pagamento (`pagordem`) e reduzido contabil (`conplanoreduz`).

### Consulta: `sql_query_pagamentoEmpenhoSemOP`

- **Objetivo:** variacao da consulta de pagamento sem depender de ordem de pagamento.

Interpretacao segura:

- Use quando o pagamento precisa ser rastreado pelo lancamento e empenho, mas sem amarrar o fluxo a `pagordem`.

### Consulta: `sql_query_empenho_contrato`

- **Objetivo:** enriquecer o lancamento com contrato/acordo vinculado ao empenho.
- **Tabelas principais:** `conlancamemp`, `conlancam`, `conlancamdoc`, `empempenho`, `empempenhocontrato`, `acordo`, `conhistdoc`, `conlancamnota`

Interpretacao segura:

- O lancamento precisa passar por um empenho que esteja ligado a contrato.
- `conlancamnota` entra como `left join`, entao a nota e opcional.

### Consulta: `sql_query_dadoslancamento`

- **Objetivo:** montar um contexto mais completo do lancamento, com complemento, empenho, CGM e elemento.
- **Tabelas:** `conlancamemp`, `conlancam`, `conlancamcompl`, `empempenho`, `conlancamcgm`, `conlancamele`

Interpretacao segura:

- Boa consulta para auditoria operacional do lancamento sem entrar ainda em toda a arvore orcamentaria.

### Consulta: `sql_query_documentos`

- **Objetivo:** recuperar os documentos/historicos associados ao lancamento de empenho.
- **Tabelas:** `conlancamemp`, `conlancam`, `conlancamdoc`, `conhistdoc`, `conlancamordem`

Interpretacao segura:

- Use quando a pergunta depender do tipo documental do lancamento.
- O tipo do movimento costuma vir de `conhistdoc`.

### Consulta: `sql_query_arquivo_lancamento`

- **Objetivo:** montar o encadeamento completo de lancamento bancario/corrente para geracao de arquivo.
- **Tabelas principais:** `conlancamemp`, `conlancam`, `conlancamdoc`, `conhistdoc`, `conlancamordem`, `conlancamcorgrupocorrente`, `corgrupocorrente`, `corrente`, `corempagemov`, `empagemov`, `empageconfgera`, `empagegera`

Interpretacao segura:

- Esta consulta e especializada em trilha de geracao de arquivo/pagamento.
- O encadeamento passa da contabilidade para corrente bancaria e configuracao de geracao.

### Consulta: `sql_query_dados_empenho`

- **Objetivo:** consolidar dados amplos do lancamento de empenho com dimensoes orcamentarias, autorizacao e, opcionalmente, restos a pagar.
- **Tabelas principais:** `conlancam`, `conlancamemp`, `conlancamdoc`, `conhistdoc`, `empempenho`, `cgm`, `empempaut`, `empautoriza`, `empautorizaprocesso`, `orcdotacao`, `orcorgao`, `orcunidade`, `orcprograma`, `orcprojativ`, `orcfuncao`, `orcsubfuncao`, `orcelemento`, `orctiporec`, `conlancampag`, `conplanoreduz`, `conplanocontabancaria`, `contabancaria`, `bancoagencia`

Regras observadas:

- Quando `resto = true`, a consulta ainda faz `join` com `empenho.empresto` filtrando `e91_anousu = :anoResto`.
- O metodo aceita `where`, `group` e `order` livres, entao serve como consulta analitica ampla.

Interpretacao segura:

- E a consulta mais completa da classe para responder sobre um lancamento de empenho com contexto orcamentario e bancario.
- Para perguntas sobre restos a pagar ligados ao lancamento, este e o caminho mais forte dentro da classe.

### Consulta: `sql_query_despesa_desdobramento`

- **Objetivo:** agregar valores de empenhado, anulado, liquidado e pago por elemento de despesa em um periodo.
- **Tabelas principais:** `conlancamele`, `conlancam`, `conlancamemp`, `empempenho`, `orcdotacao`, `conlancamdoc`, `conhistdoc`, `orcelemento`

Regras contabeis confirmadas:

- `c53_tipo = 10` representa empenhado.
- `c53_tipo = 11` representa anulado.
- `c53_tipo = 20` e `21` compoem liquidado com sinal.
- `c53_tipo = 30` e `31` compoem pago com sinal.

Interpretacao segura:

- A consulta resume a despesa por elemento (`o56_elemento`) e periodo.
- E apropriada para analise agregada, nao para leitura de um unico lancamento.

### Consulta: `sql_query_dados`

- **Objetivo:** recuperar o lancamento com instituicao contabil associada.
- **Tabelas:** `conlancamemp`, `conlancam`, `conlancaminstit`

Uso seguro:

- identificar a instituicao responsavel pelo lancamento;
- complementar filtros institucionais em analises.

### Regra utilitaria: `getSsqlBuscaPagamentos`

- **Objetivo:** buscar pagamentos por periodo, agrupando ordens, reduzidos e contas por empenho/data.

Regras observadas:

- filtra `conhistdoc.c53_tipo in (30, 31)`;
- exclui codigos documentais especiais de pagamento no calculo de `valor_pago`;
- agrupa por empenho, data, orgao e unidade.

### Regras de manutencao observadas

1. `incluir()` exige `c75_numemp` e `c75_data`.
2. A data pode ser montada a partir de dia/mes/ano vindos do POST.
3. Inclusao, alteracao e exclusao registram auditoria em `db_acount*`.

### Relacionamentos de negocio confirmados no catalogo

- `conlancamemp.c75_codlan -> conlancam.c70_codlan`

Interpretacao segura:

- `conlancamemp` e uma extensao do lancamento contabil para o dominio de empenho.
- A maior parte dos demais caminhos parte primeiro de `conlancam`.

### Cuidados para consultas do agente

- Nao interpretar `conlancamemp` isoladamente como fato contabil completo; ela so vincula o lancamento ao empenho.
- Em consultas por pagamento, o tipo contabil do movimento vem de `conhistdoc.c53_tipo`, nao apenas da existencia do vinculo.
- Quando a pergunta exigir contexto orcamentario completo, prefira `sql_query_dados_empenho` em vez de `sql_query` simples.
- Em agregacoes por periodo, respeite a semantica de sinal dos tipos `10/11/20/21/30/31`.
