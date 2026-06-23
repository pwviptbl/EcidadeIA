## empenho.empresto

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_empresto_classe.php`

Cadastro de restos a pagar por empenho e exercicio. A classe guarda os valores base do RP por empenho e oferece consultas para enriquecimento com tipo de recurso, tipo de resto, dotacao, elemento, funcao e movimentacao contabil do periodo.

### Estrutura e interpretacao

- **Classe:** `cl_empresto`
- **Tabela principal:** `empresto`
- **Chave primaria composta:** `e91_anousu`, `e91_numemp`
- **Grau basico:** uma linha por empenho inscrito em restos a pagar dentro de um exercicio

Campos de negocio confirmados:

- `e91_anousu`: exercicio do registro de resto a pagar
- `e91_numemp`: numero do empenho
- `e91_vlremp`: valor original do empenho levado ao RP
- `e91_vlranu`: valor anulado
- `e91_vlrliq`: valor liquidado
- `e91_vlrpag`: valor pago
- `e91_elemento`: elemento antigo textual
- `e91_recurso`: tipo de recurso vinculado a `orctiporec`
- `e91_codtipo`: tipo de resto a pagar vinculado a `emprestotipo`
- `e91_rpcorreto`: flag booleana de consistencia do RP

Interpretacao segura:

- `e91_numemp` aponta para o empenho que originou o resto a pagar.
- Os campos `e91_vlremp`, `e91_vlranu`, `e91_vlrliq` e `e91_vlrpag` guardam um retrato base do RP, mas varias consultas da classe recalculam movimentos do periodo a partir de lancamentos contabeis.
- `e91_recurso` referencia o tipo de recurso orcamentario, nao o codigo textual final da fonte.
- `e91_codtipo` classifica o RP pelo cadastro `emprestotipo`.

### Consulta: `sql_query`

- **Objetivo:** recuperar o RP com enriquecimento por tipo de recurso, complemento da fonte e tipo de RP.
- **Tabelas:** `empresto`, `orctiporec`, `complementofonterecurso`, `emprestotipo`

```sql
select /* campos dinamicos */
  from empresto
       inner join orctiporec
          on orctiporec.o15_codigo = empresto.e91_recurso
       inner join complementofonterecurso
          on complementofonterecurso.o200_sequencial = orctiporec.o15_complemento
       inner join emprestotipo
          on emprestotipo.e90_codigo = empresto.e91_codtipo
 where empresto.e91_anousu = :exercicio
   and empresto.e91_numemp = :numemp
 order by /* ordenacao dinamica */
```

Interpretacao segura:

- Use esta consulta quando precisar do cadastro do RP com o caminho antigo de complemento da fonte.
- O retorno continua em nivel de um RP por empenho, desde que os joins de recurso e tipo estejam consistentes.

### Consulta: `sql_query2`

- **Objetivo:** versao atualizada da consulta base usando `fonterecurso`.
- **Tabelas:** `empresto`, `orctiporec`, `fonterecurso`, `complementofonterecurso`, `emprestotipo`

```sql
select /* campos dinamicos */
  from empresto
       join orctiporec
         on orctiporec.o15_codigo = empresto.e91_recurso
       join fonterecurso
         on fonterecurso.orctiporec_id = orctiporec.o15_codigo
        and fonterecurso.exercicio = empresto.e91_anousu
       join complementofonterecurso
         on complementofonterecurso.o200_sequencial = orctiporec.o15_complemento
       join emprestotipo
         on emprestotipo.e90_codigo = empresto.e91_codtipo
 where empresto.e91_anousu = :exercicio
   and empresto.e91_numemp = :numemp
```

Interpretacao segura:

- Quando a pergunta envolver a fonte de recurso no modelo mais novo, prefira `sql_query2`.
- O join com `fonterecurso` depende do mesmo exercicio do RP.

### Consulta: `sql_query_file`

- **Objetivo:** ler apenas a tabela fisica `empresto`.

```sql
select /* campos dinamicos */
  from empresto
 where empresto.e91_anousu = :exercicio
   and empresto.e91_numemp = :numemp
 order by /* ordenacao dinamica */
```

Uso seguro:

- confirmar existencia do RP;
- ler somente os valores gravados na tabela;
- evitar multiplicacao por joins ao validar o cadastro base.

### Consulta: `sql_query_empenho`

- **Objetivo:** enriquecer o RP com tipo de recurso, tipo de RP e o empenho de origem.
- **Tabelas:** `empresto`, `orctiporec`, `emprestotipo`, `empempenho`

```sql
select /* campos dinamicos */
  from empresto
       inner join orctiporec on orctiporec.o15_codigo = empresto.e91_recurso
       inner join emprestotipo on emprestotipo.e90_codigo = empresto.e91_codtipo
       inner join empempenho on empempenho.e60_numemp = empresto.e91_numemp
 where /* filtro dinamico */
 order by /* ordenacao dinamica */
```

Cuidados:

- O join com `empempenho` usa apenas `e60_numemp = e91_numemp`, entao em cenarios multi-exercicio o filtro por ano deve estar bem amarrado no `where`.
- O metodo aceita lista de campos e ordenacao separadas por `#`.

### Consultas analiticas de restos a pagar

Metodos principais:

- `sql_rp`
- `sql_rp2`
- `sql_rp_novo`
- `sql_rp_novo_com_processo_administrativo`
- `sql_query_restosPag`
- `sql_query_restos`
- `sql_query_restosPagarPorPeriodo`

Leituras de negocio confirmadas:

- A classe recalcula anulacoes, liquidacoes e pagamentos por meio de `conlancamemp`, `conlancamdoc`, `conhistdoc` e `conlancam`.
- As consultas `sql_rp*` cruzam o RP com `empempenho`, `orcdotacao`, `orcorgao`, `orcunidade`, `orcfuncao`, `orcsubfuncao`, `orcprograma`, `orcprojativ`, `orcelemento`, `cgm` e metadados institucionais.
- `sql_rp_novo` e `sql_rp_novo_com_processo_administrativo` usam `fonterecurso` e expõem campos adicionais como `gestao`, programa, projeto/atividade e dados institucionais.
- A variante `sql_rp_novo_com_processo_administrativo` ainda traz `e150_numeroprocesso`.

Regras contabeis observadas nos somatorios:

- `c53_tipo = 11` entra como anulacao.
- `c53_tipo = 20` e `21` compoem liquidacao com sinal positivo/negativo.
- Pagamentos processados e nao processados usam codigos documentais distintos, inclusive variantes novas como `6008`, `6009`, `6010` e `6011` nas consultas mais recentes.

### Regras de manutencao observadas

1. `incluir()` exige `e91_vlremp`, `e91_vlranu`, `e91_vlrliq`, `e91_vlrpag`, `e91_recurso` e `e91_codtipo`.
2. `e91_elemento` e opcional.
3. `e91_rpcorreto` nasce com default `'f'` quando nao informado.
4. Inclusao, alteracao e exclusao registram auditoria em `db_acount*` quando a sessao nao desativa account.

### Relacionamentos de negocio confirmados no catalogo

- `empresto.e91_codtipo -> emprestotipo.e90_codigo`
- `empresto.e91_recurso -> orctiporec.o15_codigo`

Interpretacao segura:

- `emprestotipo` classifica a natureza do resto a pagar.
- `orctiporec` resolve o recurso/origem orcamentaria usado nas analises por fonte e gestao.

### Cuidados para consultas do agente

- Nao tratar `empresto` como valor realizado definitivo sem considerar os lancamentos recalculados nas consultas `sql_rp*`.
- Para perguntas por periodo, preferir as consultas de RP que usam data e movimentos contabeis, nao apenas a leitura crua da tabela.
- Para perguntas sobre fonte de recurso no modelo atual, prefira os metodos baseados em `fonterecurso`.
- Em joins com empenho, amarre exercicio e instituicao explicitamente para evitar ambiguidade por numero de empenho.
