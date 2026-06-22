## contabilidade.conlancamval

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_conlancamval_classe.php`

Registra os valores e partidas de cada lancamento contabil. Cada linha aponta a conta reduzida de debito, a conta reduzida de credito, o historico, o valor, a data e a ordem interna dentro do lancamento.

### Estrutura e interpretacao

- **Classe:** `cl_conlancamval`
- **Tabela principal:** `contabilidade.conlancamval`
- **Chave primaria:** `c69_sequen`
- **Chave de agrupamento de negocio:** `c69_codlan`
- **Grau basico:** uma linha por partida contabil dentro de um lancamento

Campos de negocio confirmados:

- `c69_codlan`: codigo do lancamento pai em `conlancam`
- `c69_codhist`: historico contabil em `conhist`
- `c69_debito`: conta reduzida debitada
- `c69_credito`: conta reduzida creditada
- `c69_valor`: valor da partida
- `c69_data`: data da partida
- `c69_ordem`: ordem da partida dentro do lancamento

Interpretacao segura:

- `c69_debito` e `c69_credito` nao sao o codigo estrutural completo da conta; sao reduzidos, resolvidos via `conplanoreduz`.
- Um mesmo `c69_codlan` pode ter varias linhas em `conlancamval`.
- A ordem `c69_ordem` e usada por consultas consumidoras para identificar a partida principal em varios contextos.

### Consulta: `sql_query`

- **Objetivo:** Recuperar a partida contabil com metadados do lancamento, documento, historico e instituicao.
- **Tabelas:** `conlancamval`, `conhist`, `conlancam`, `conlancamdoc`, `conhistdoc`, `conlancaminstit`, `conlancamdig`
- **Grau do resultado:** uma linha por combinacao de partida contabil e linha de documento do lancamento

```sql
select /* campos dinamicos */
  from conlancamval
       left join conhist
          on conhist.c50_codhist = conlancamval.c69_codhist
       inner join conlancam
          on conlancam.c70_codlan = conlancamval.c69_codlan
       inner join conlancamdoc
          on conlancamdoc.c71_codlan = conlancam.c70_codlan
       inner join conhistdoc
          on conhistdoc.c53_coddoc = conlancamdoc.c71_coddoc
       left join conlancaminstit
          on conlancaminstit.c02_codlan = conlancam.c70_codlan
       left outer join conlancamdig
          on conlancamdig.c78_codlan = conlancam.c70_codlan
 where conlancamval.c69_sequen = :sequencial
 order by /* ordenacao dinamica */
```

Regras observadas:

- O documento do lancamento e obrigatorio nesta consulta por causa do `inner join conlancamdoc`.
- O historico interno da partida (`conhist`) e opcional.
- A existencia de mais de um documento em `conlancamdoc` pode multiplicar a mesma linha de `conlancamval`.

### Consulta: `sql_queryComplemento`

- **Objetivo:** Igual a `sql_query`, mas exigindo complemento e conta corrente do lancamento quando existirem.
- **Tabelas adicionais:** `conlancamcompl`, `conlancamcorrente`

```sql
select /* campos dinamicos */
  from conlancamval
       left join conhist on c50_codhist = c69_codhist
       inner join conlancam on c70_codlan = c69_codlan
       inner join conlancamcompl on c72_codlan = c70_codlan
       inner join conlancamdoc on c71_codlan = c70_codlan
       inner join conhistdoc on c53_coddoc = c71_coddoc
       left join conlancaminstit on c02_codlan = c70_codlan
       left join conlancamcorrente on c86_conlancam = c70_codlan
       left outer join conlancamdig on c78_codlan = c70_codlan
 where conlancamval.c69_sequen = :sequencial
```

Regra comprovada:

- So retorna partidas de lancamentos que possuem registro em `conlancamcompl`.

### Consulta: `sql_query_contacorrentedetalhe`

- **Objetivo:** Recuperar os vinculos entre a partida contabil e os detalhes de conta corrente.
- **Tabelas:** `conlancamval`, `contacorrentedetalheconlancamval`, `contacorrentedetalhe`
- **Grau do resultado:** uma linha por vinculo entre partida e detalhe de conta corrente

```sql
select /* campos dinamicos */
  from conlancamval
       inner join contacorrentedetalheconlancamval
          on contacorrentedetalheconlancamval.c28_conlancamval = conlancamval.c69_sequen
       inner join contacorrentedetalhe
          on contacorrentedetalhe.c19_sequencial =
             contacorrentedetalheconlancamval.c28_contacorrentedetalhe
 where conlancamval.c69_sequen = :sequencial
```

### Consulta: `sql_query_contacorrentedetalhe_tce`

- **Objetivo:** Montar a visao mais completa do vinculo de conta corrente para exportacao/analise TCE.
- **Parametro de negocio:** `sTipo = 'D'` usa `c69_debito`; `sTipo = 'C'` usa `c69_credito`.
- **Tabelas principais:** `conlancamval`, `contacorrentedetalheconlancamval`, `contacorrentedetalhe`, `conlancaminstit`, `conlancamdoc`, `conplanoreduz`, `conplano`

Regra comprovada:

- O tipo escolhido define qual lado da partida sera comparado com `conplanoreduz`.
- O join em `conplanoreduz` exige simultaneamente:
  - reduzido igual a debito ou credito escolhido;
  - mesma instituicao de `conlancaminstit`;
  - mesmo exercicio de `conlancamval`.

Cuidados:

- A consulta adiciona muitas relacoes opcionais de caixa, grupo corrente, slip, pagamento e placa de caixa.
- O grao real depende dos vinculos auxiliares e pode multiplicar a partida.

### Consulta: `sql_query_conta_documento`

- **Objetivo:** Relacionar a partida contabil ao documento do lancamento.

```sql
select /* campos dinamicos */
  from conlancamval
       inner join conlancamdoc
          on conlancamdoc.c71_codlan = conlancamval.c69_codlan
 where /* filtro dinamico */
```

Uso seguro:

- descobrir qual documento contabil esta associado a uma partida;
- filtrar partidas por documento sem ainda resolver conta reduzida ou plano completo.

### Consulta: `sql_query_lancamentos_documento`

- **Objetivo:** Projetar debito e credito de um reduzido especifico em uma lista fechada de lancamentos.
- **Parametros:** `reduzido`, `lista_lancamentos`
- **Campos calculados:**
  - `valor_debito`: recebe `c69_valor` quando `c69_debito = :reduzido`
  - `valor_credito`: recebe `c69_valor` quando `c69_credito = :reduzido`

```sql
select c69_codlan as codigo_lancamento,
       c71_coddoc as documento,
       c53_descr  as descricao_documento,
       case when c69_debito = :reduzido then c69_valor else 0 end as valor_debito,
       case when c69_credito = :reduzido then c69_valor else 0 end as valor_credito,
       c69_data as data
  from conlancamval
       inner join conlancamdoc on c71_codlan = c69_codlan
       inner join conhistdoc on c53_coddoc = c71_coddoc
 where c69_codlan in (:lista_lancamentos)
   and (c69_debito = :reduzido or c69_credito = :reduzido)
 order by c69_data, c69_codlan
```

Interpretacao segura:

- uma mesma partida pode aparecer como debito ou credito para o reduzido analisado;
- o valor nao e somado na propria consulta, apenas projetado por natureza.

### Consulta: `sql_query_lancamentos`

- **Objetivo:** Resolver o lancamento completo com contas reduzidas e plano contabil de debito e credito.
- **Tabelas:** `conlancamval`, `conlancam`, `conlancamdoc`, `conlancaminstit`, `conplanoreduz`, `conplano`
- **Grau do resultado:** uma linha por partida contabil, sujeita a multiplicacao pelos documentos do lancamento

```sql
select /* campos dinamicos */
  from contabilidade.conlancamval
       inner join contabilidade.conlancam on c70_codlan = c69_codlan
       inner join contabilidade.conlancamdoc on c70_codlan = c71_codlan
       inner join contabilidade.conlancaminstit on c70_codlan = c02_codlan
       inner join contabilidade.conplanoreduz reduzdebito
          on reduzdebito.c61_reduz = c69_debito
         and reduzdebito.c61_anousu = c69_anousu
       inner join contabilidade.conplano planodebito
          on planodebito.c60_codcon = reduzdebito.c61_codcon
         and planodebito.c60_anousu = reduzdebito.c61_anousu
       inner join contabilidade.conplanoreduz reduzcredito
          on reduzcredito.c61_reduz = c69_credito
         and reduzcredito.c61_anousu = c69_anousu
       inner join contabilidade.conplano planocredito
          on planocredito.c60_codcon = reduzcredito.c61_codcon
         and planocredito.c60_anousu = reduzcredito.c61_anousu
 where /* filtro dinamico */
 order by /* ordenacao dinamica */
```

Regras comprovadas:

- Debito e credito sempre sao resolvidos separadamente contra `conplanoreduz` e `conplano`.
- O exercicio da partida (`c69_anousu`) controla a resolucao dos dois lados.

### Consulta: `sql_recurso_lancamento_por_natureza`

- **Objetivo:** Buscar o recurso orcamentario associado ao lado debito ou credito da partida.
- **Regra:** `natureza = 'C'` usa `c69_credito`; qualquer outro valor usa `c69_debito`.

```sql
select /* campos dinamicos */
  from contabilidade.conlancamval
       join contabilidade.conplanoreduz
         on c61_reduz = /* credito ou debito */
        and c61_anousu = c69_anousu
       join recurso_exercicio
         on recurso_exercicio.o15_codigo = conplanoreduz.c61_codigo
        and recurso_exercicio.exercicio = c69_anousu
 where /* filtro dinamico */
```

Cuidados:

- A implementacao referencia `$order` no final, mas o metodo nao recebe esse parametro.
- Portanto, nao conte com ordenacao gerada por essa funcao sem corrigir o codigo consumidor.

### Consulta: `sql_query_lancamentos_novo`

- **Objetivo:** Expandir a visao de lancamentos com origem de empenho, receita, elemento e dotacao.
- **Tabelas adicionais:** `conlancamemp`, `conlancamrec`, `orcreceita`, `conlancamele`, `orcelemento`, `conlancamdot`, `orcdotacao`
- **Regra estrutural:** usa `DISTINCT` para tentar reduzir duplicacoes geradas pelos varios caminhos opcionais.

Cuidados:

- `DISTINCT` mascara parte da multiplicacao, mas nao substitui definicao clara de grao.
- A ausencia ou presenca de vinculos de empenho, receita, elemento e dotacao altera bastante a cardinalidade efetiva.

### Regras de negocio confirmadas

1. Um lancamento contabil (`c69_codlan`) pode possuir varias partidas em `conlancamval`.
2. Cada partida carrega os dois lados contabeis: debito e credito.
3. O historico da partida (`c69_codhist`) e independente do documento contabil (`conlancamdoc -> conhistdoc`).
4. A ordem `c69_ordem` e relevante e usada em consumidores para selecionar a conta principal do lancamento.
5. O valor da linha (`c69_valor`) e o valor da partida, nao um saldo agregado do lancamento inteiro.

### Cuidados para consultas do agente

- Nao trate `c69_debito` e `c69_credito` como codigo estrutural; resolva via `conplanoreduz` e `conplano`.
- Se a pergunta for por documento contabil, o join com `conlancamdoc` pode multiplicar a partida.
- Se a pergunta for por valor total do lancamento, defina antes se a soma deve considerar todas as partidas ou apenas `c69_ordem = 1`.
- Em consultas por recurso, a natureza D/C muda completamente o lado da conta analisada.
- Para analise de contas exibidas ao usuario, o padrao consumidor observado e ordenar por `c69_ordem, c69_sequen`.
