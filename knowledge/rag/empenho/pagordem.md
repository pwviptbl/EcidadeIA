## empenho.pagordem

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_pagordem_classe.php`

Cadastro das ordens de pagamento ligadas a empenhos. A classe guarda os dados básicos da ordem e oferece diversas consultas para recuperar cheques, movimentos de pagamento, contas, elementos, notas de liquidação, agenda e vínculo com restos a pagar.

### Estrutura e interpretacao

- **Classe:** `cl_pagordem`
- **Tabela principal:** `pagordem`
- **Chave primaria:** `e50_codord`
- **Grau basico:** uma linha por ordem de pagamento

Campos de negocio confirmados:

- `e50_codord`: codigo da ordem de pagamento
- `e50_numemp`: empenho associado
- `e50_data`: data de emissao da ordem
- `e50_obs`: observacao textual
- `e50_id_usuario`: usuario que registrou a ordem
- `e50_hora`: hora do registro
- `e50_anousu`: ano da ordem

Interpretacao segura:

- A ordem de pagamento e um passo operacional posterior ao empenho.
- `e50_numemp` conecta a ordem ao empenho principal.
- `e50_anousu` representa o ano da ordem, que pode ser relevante para trilhas de pagamento e RP.

### Consulta: `sql_query`

- **Objetivo:** recuperar a ordem com enriquecimento do usuario, empenho, CGM, instituicao, dotacao, tipo de compra, tipo de empenho e caracteristica peculiar.
- **Tabelas:** `pagordem`, `db_usuarios`, `empempenho`, `cgm`, `db_config`, `orcdotacao`, `pctipocompra`, `emptipo`, `concarpeculiar`

```sql
select /* campos dinamicos */
  from pagordem
       inner join db_usuarios on db_usuarios.id_usuario = pagordem.e50_id_usuario
       inner join empempenho on empempenho.e60_numemp = pagordem.e50_numemp
       inner join cgm on cgm.z01_numcgm = empempenho.e60_numcgm
       inner join db_config on db_config.codigo = empempenho.e60_instit
       inner join orcdotacao
          on orcdotacao.o58_anousu = empempenho.e60_anousu
         and orcdotacao.o58_coddot = empempenho.e60_coddot
       inner join pctipocompra on pctipocompra.pc50_codcom = empempenho.e60_codcom
       inner join emptipo on emptipo.e41_codtipo = empempenho.e60_codtipo
       left join concarpeculiar on concarpeculiar.c58_sequencial = empempenho.e60_concarpeculiar
 where pagordem.e50_codord = :codord
 order by /* ordenacao dinamica */
```

Interpretacao segura:

- Esta e a consulta base para responder "o que e esta ordem" com contexto do empenho.

### Consulta: `sql_query_file`

- **Objetivo:** ler apenas a tabela fisica `pagordem`.

```sql
select /* campos dinamicos */
  from pagordem
 where pagordem.e50_codord = :codord
 order by /* ordenacao dinamica */
```

Uso seguro:

- validar a existencia da ordem;
- ler apenas os campos gravados no cadastro.

### Consulta: `sql_query_cheques`

- **Objetivo:** recuperar a ordem junto dos elementos pagos, movimento financeiro, configuracao de cheque, conta vinculada e dados auxiliares.
- **Tabelas principais:** `pagordem`, `pagordemele`, `empempenho`, `cgm`, `db_config`, `orcdotacao`, `orctiporec`, `emptipo`, `empord`, `empagemov`, `empagemovforma`, `empage`, `corempagemov`, `empageconf`, `empageconfche`, `pagordemconta`, `empageconfgera`

Interpretacao segura:

- Use quando a pergunta depender do meio de pagamento, cheque ou conta da ordem.
- O metodo aceita `sJoin` adicional para extensoes locais.

### Consulta: `sql_query_emp`

- **Objetivo:** recuperar a ordem em conjunto com o empenho e os elementos da ordem.
- **Tabelas:** `pagordem`, `empempenho`, `cgm`, `pagordemele`

Uso seguro:

- consultas simples de ordem + empenho + distribuicao por elemento.

### Consulta: `sql_query_empagemovforma`

- **Objetivo:** montar o encadeamento completo da ordem com movimento de pagamento, forma de pagamento, fonte de recurso, conta, cheque, notas e grupo de corrente.
- **Tabelas principais:** `empage`, `empagemov`, `empord`, `pagordem`, `pagordemele`, `empempenho`, `cgm`, `db_config`, `orcdotacao`, `orctiporec`, `fonterecurso`, `emptipo`, `empresto`, `empageconcarpeculiar`, `corempagemov`, `empagemovconta`, `empageconf`, `empageconfche`, `pagordemconta`, `empagemovforma`, `empagepag`, `empagetipo`, `pagordemnota`, `empnota`, `empageconfgera`, `corgrupocorrente`

Interpretacao segura:

- Esta e uma das consultas mais ricas da classe para auditoria completa do pagamento.
- Quando a ordem estiver ligada a resto a pagar no ano corrente de sessao, o metodo tambem puxa `empresto`.
- Para analise de fonte atual, este metodo ja usa `fonterecurso`.

### Consulta: `sql_query_notaliquidacao`

- **Objetivo:** recuperar a ordem vinculada a notas de liquidacao.
- **Tabelas:** `pagordem`, `db_usuarios`, `empempenho`, `cgm`, `db_config`, `orcdotacao`, `pctipocompra`, `emptipo`, `concarpeculiar`, `pagordemnota`, `empnota`

Regras observadas:

- o metodo retorna um array com `sql` e `params`;
- usa placeholder posicional para `e50_codord`, evitando concatenacao direta nesse caso.

Interpretacao segura:

- Prefira este metodo quando a pergunta envolver nota de liquidacao da ordem.

### Consulta: `sql_query_pag`

- **Objetivo:** recuperar a ordem junto dos lancamentos contabeis de pagamento, historico documental, plano reduzido/plano contabil e conta associada.
- **Tabelas principais:** `pagordem`, `empempenho`, `cgm`, `db_config`, `orcdotacao`, `pctipocompra`, `emptipo`, `conlancamord`, `conlancampag`, `conlancam`, `conlancamdoc`, `conhistdoc`, `conplanoreduz`, `conplano`, `pagordemconta`

Interpretacao segura:

- Use para responder sobre contabilizacao do pagamento da ordem.
- O tipo do movimento/documento vem do caminho `conlancamdoc -> conhistdoc`.

### Consultas por agenda e elementos

Metodos principais:

- `sql_query_pagordemagenda`
- `sql_query_pagordemele`
- `sql_query_pagordemele2`
- `sql_query_pagordemeleempage`

Leituras de negocio confirmadas:

- todos partem de `pagordem` e conectam a ordem a `pagordemele`, `empempenho` e dimensoes orcamentarias;
- as variantes `...ele2` e `...eleempage` trazem agregacao/estado de `empord`, `empagemov`, `empageconf` e `empageconfgera`;
- `sql_query_pagordemagenda` ainda liga a agenda de pagamento via `empage`.

Interpretacao segura:

- Use estas consultas quando a unidade de analise for a distribuicao da ordem por elemento ou o estado operacional da ordem na rotina de pagamento.

### Consulta: `sql_query_pagDiversos`

- **Objetivo:** recuperar pagamentos diversos da ordem com lancamento contabil, plano, conta e elementos.

Interpretacao segura:

- E uma variante de `sql_query_pag` com foco mais direto em pagamentos diversos e composicao por elemento.

### Consulta: `sql_query_movimento`

- **Objetivo:** ligar a ordem diretamente ao movimento financeiro.
- **Tabelas:** `pagordem`, `empord`, `empagemov`

Uso seguro:

- verificar rapidamente qual movimento financeiro esta associado a uma ordem;
- bom ponto de entrada para trilhas de cancelamento ou conciliação.

### Consulta: `sql_query_empenho_rp`

- **Objetivo:** verificar o vinculo entre a ordem e restos a pagar.
- **Tabelas:** `pagordem`, `empresto`

```sql
select /* campos dinamicos */
  from pagordem
       inner join empresto
          on pagordem.e50_numemp = empresto.e91_numemp
 where pagordem.e50_codord = :codord
```

Cuidados:

- O join mostrado na classe usa apenas o numero do empenho; se a analise depender do exercicio do RP, o filtro precisa ser complementado fora do metodo.

### Regras de manutencao observadas

1. `incluir()` exige `e50_numemp`, `e50_data`, `e50_id_usuario`, `e50_hora` e `e50_anousu`.
2. Quando `e50_codord` nao e informado, a classe usa a sequence `pagordem_e50_codord_seq`.
3. Se o codigo informado for maior que o ultimo valor da sequence, a inclusao e bloqueada.
4. Inclusao, alteracao e exclusao registram auditoria em `db_acount*`.

### Relacionamentos de negocio confirmados no catalogo

- `pagordem.e50_id_usuario -> db_usuarios.id_usuario`
- `pagordem.e50_numemp -> empempenho.e60_numemp`
- `pagordem.e50_codord -> empord.e82_codord`
- `pagordem.e50_codord -> pagordemconta.e49_codord`
- `pagordem.e50_codord -> pagordemdesconto.e34_codord`

Interpretacao segura:

- `pagordem` e a entidade central da fase de pagamento do empenho.
- Quase todas as trilhas de movimento ou conta passam primeiro por `empord`.

### Cuidados para consultas do agente

- Nao confunda ordem de pagamento com movimento de pagamento: a ordem e o documento operacional; o movimento real costuma vir por `empord` e `empagemov`.
- Para perguntas sobre contabilizacao, prefira `sql_query_pag`.
- Para perguntas sobre nota de liquidacao, prefira `sql_query_notaliquidacao`.
- Para perguntas sobre cheque, conta, forma de pagamento ou fonte, prefira `sql_query_cheques` ou `sql_query_empagemovforma`.
- Para perguntas sobre RP, complemente `sql_query_empenho_rp` com filtro de exercicio quando necessario.
