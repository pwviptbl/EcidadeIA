## caixa.arrepaga

> Fonte de código: `/var/www/html/e-cidade-php74/classes/db_arrepaga_classe.php`

Registra componentes financeiros de pagamentos realizados. A classe relaciona os pagamentos a receitas, contribuinte, origem do débito, instituição e, em relatórios específicos, descontos concedidos, correção, juros e multa.

### Resumo técnico

- **Classe:** `cl_arrepaga`
- **Tabela principal:** `arrepaga`
- **Módulo:** caixa
- **Identificador técnico usado pela classe:** `oid`
- **Número de arrecadação:** `k00_numpre`
- **Parcela:** `k00_numpar`
- **Receita de tesouraria:** `k00_receit`
- **Contribuinte:** `k00_numcgm`
- **Valor do componente:** `k00_valor`
- **Data de pagamento:** `k00_dtpaga`
- **Data de vencimento original:** `k00_dtvenc`
- **Data de operação/lançamento:** `k00_dtoper`
- **Histórico de cálculo:** `k00_hist`
- **Conta:** `k00_conta`
- **Grão:** Componente de receita pago para um número de arrecadação e parcela. Um mesmo `k00_numpre` pode possuir várias linhas e receitas.

### Relacionamentos observados

- `arrepaga.k00_numcgm = cgm.z01_numcgm`
- `arrepaga.k00_receit = tabrec.k02_codigo`
- `arrepaga.k00_receit = taborc.k02_codigo`
- `arrepaga.k00_numpre = arreinstit.k00_numpre`
- `arrepaga.k00_numpre = arrematric.k00_numpre`
- `arrepaga.k00_numpre = arreinscr.k00_numpre`
- `(arrepaga.k00_numpre, arrepaga.k00_numpar) = (arrecant.k00_numpre, arrecant.k00_numpar)`

---

### Leitura direta: `sql_query` e `sql_query_file`

- **Objetivo:** Consultar campos físicos de `arrepaga`.
- **Filtro de `sql_query`:** `arrepaga.oid = :oid`, quando o identificador é informado e não há `$dbwhere`.
- **Diferença:** `sql_query_file` ignora o parâmetro `$oid`; somente aplica o `$dbwhere`.
- **Campos e ordenação:** São recebidos dinamicamente e separados por `#`.
- **Cuidados:** Para localizar um pagamento de negócio, normalmente filtrar pela composição `k00_numpre`, `k00_numpar`, `k00_receit` e/ou `k00_dtpaga`, não apenas por `oid`.

```sql
SELECT /* campos dinâmicos */
FROM arrepaga
WHERE arrepaga.oid = :oid
ORDER BY /* ordenação dinâmica */;
```

---

### Descontos concedidos por regra: `sql_queryDescontoConcedidoPorRegra`

- **Objetivo:** Identificar pagamentos com desconto e reconstruir o valor histórico, correção, juros, multa, valor sem desconto e valor efetivamente pago.
- **Parâmetros:**
  - `:data_inicial` e `:data_final` - período considerado pelas diferentes origens.
  - `:tipos` - lista opcional de códigos `arrecant.k00_tipo`.
- **Instituição:** Usa `DB_instit` da sessão.
- **Exercício orçamentário:** Usa `DB_anousu` da sessão para `taborc.k02_anousu`.
- **Exercícios das dívidas:** São derivados dos anos existentes entre a data inicial e a data final.
- **Grão final:** Número de arrecadação, receita e classificações de tipo/procedência.
- **Filtro final:** Mantém apenas grupos com `ABS(SUM(valor_desconto)) > 0`.
- **Ordenação:** Nome do contribuinte.

#### Regra dos valores em `arrepaga`

- **Desconto:** Soma somente `k00_valor < 0`.
- **Valor sem desconto:** Soma somente `k00_valor > 0`.
- **Valor pago:** Soma algébrica de todos os componentes `k00_valor`.
- **Consequência:** O campo `desconto` pode permanecer negativo no resultado. Usar `ABS(desconto)` apenas quando a apresentação exigir magnitude positiva.

```sql
SUM(fc_iif(arrepaga.k00_valor < 0, arrepaga.k00_valor, 0::float8))
  AS valor_desconto,
SUM(fc_iif(arrepaga.k00_valor > 0, arrepaga.k00_valor, 0::float8))
  AS valor_sem_desconto,
SUM(arrepaga.k00_valor)
  AS valor_pago
```

#### Valores reconstruídos

- **Valor histórico:** `SUM(arrecant.k00_valor)`.
- **Valor corrigido:** Calculado por `fc_corre(...)`.
- **Juros:** Valor histórico multiplicado pelo fator retornado por `fc_juros(...)`.
- **Multa:** Valor histórico multiplicado pelo fator retornado por `fc_multa(...)`.
- **Total:** `valor_corrigido + juros + multa`.
- **Origem do débito:** `fc_origem_numpre(k00_numpre, 1)`.
- **Receita orçamentária:** `taborc.k02_codrec` e estrutura `taborc.k02_estorc`.
- **Procedência:** `divida.v01_proced -> proced.v03_codigo`.
- **Tipo de procedência:** `proced.v03_tributaria -> tipoproced.v07_sequencial`.
- **Fallbacks textuais:** Sem vínculo, retorna `SEM PROCEDÊNCIA` e `SEM TIPO DE PROCEDÊNCIA`.

#### Origens de pagamento consolidadas

O método combina três caminhos com `UNION ALL`:

1. **Parcelamento, prioridade 1**
   - Origem em `termo`.
   - Pagamento em `arrepaga` por `termo.v07_numpre`.
   - Instituição em `termo.v07_instit = DB_instit`.
   - Exclui receitas cujo `tabrec.k02_tabrectipo` esteja em `(2, 3, 5)`.
   - Calcula o desconto proporcional a partir de `v07_valor`, `v07_vlrcor`, `v07_vlrjur` e `v07_vlrmul`.

2. **Retorno bancário, prioridade 2**
   - Origem em `disbanco -> arreidret -> arrepaga`.
   - Período por `disbanco.dtpago`.
   - Instituição por `disbanco.instit = DB_instit`.
   - Exige recibo web de tipo `1`, `2` ou `3` relacionado a `recibopaga`.

3. **Cobrança registrada, prioridade 3**
   - Origem em `cornump -> arrepaga`.
   - Período por `cornump.k12_data`.
   - Exige `db_reciboweb.k99_tipo IN (1, 2, 3)`.
   - A instituição é validada por `db_reciboweb -> arreinstit`.

#### Deduplicação entre origens

A mesma combinação de número de arrecadação e receita pode aparecer em mais de uma origem. A consulta aplica:

```sql
ROW_NUMBER() OVER (
  PARTITION BY k00_numpre, k00_receit
  ORDER BY prioridade
) AS rn
```

Depois mantém somente `rn = 1`. Portanto, a preferência é:

1. Parcelamento.
2. Retorno bancário.
3. Cobrança registrada.

Não somar diretamente os três blocos sem reproduzir essa deduplicação.

#### Filtro opcional por tipo de débito

Quando `:tipos` é informado, os três blocos exigem uma linha em `arrecant` com:

```sql
c.k00_numpre = arrepaga.k00_numpre
AND c.k00_numpar = arrepaga.k00_numpar
AND c.k00_tipo IN (:tipos)
```

O filtro é aplicado ao tipo histórico da parcela, não ao texto da receita.

#### Origem das dívidas parceladas

Antes de retornar a consulta principal, o método executa `CREATE TEMP TABLE w_origem_dividas` e cria dois índices. A tabela temporária unifica:

- Certidão de parcelamento de dívida sem inicial vinculada.
- Parcelamento de inicial de certidão de parcelamento.
- Parcelamento de inicial de certidão de dívida.

Os caminhos usam `certter`, `termoini`, `inicialcert`, `termodiv`, `certdiv` e `divida`. As dívidas são restringidas à instituição da sessão e aos exercícios compreendidos no período solicitado.

**Cuidado operacional:** Este método não é apenas um gerador puro de SQL. Ele executa DDL temporário via `db_query()` antes de retornar o `SELECT`. A conexão que executar a consulta retornada precisa ser a mesma conexão onde `w_origem_dividas` foi criada.

#### SQL normalizada da consolidação

```sql
SELECT
  k00_numpre AS numpre,
  z01_nome AS contribuinte,
  fc_origem_numpre(k00_numpre, 1) AS origem,
  k00_receit AS receit,
  k03_tipo AS tipo,
  k00_descr AS descrtipo,
  k02_estorc AS receitorcamentoestrutural,
  ROUND(SUM(valor_sem_desconto), 2) AS valor_pagar,
  ROUND(SUM(valor_pago), 2) AS valor_pago,
  ROUND(SUM(valor_desconto), 2) AS desconto,
  ROUND(SUM(vlrhist), 2) AS vlrhist,
  ROUND(SUM(corrigido), 2) AS vlrcorr,
  ROUND(SUM(juros), 2) AS juros,
  ROUND(SUM(multa), 2) AS multa,
  ROUND(SUM(corrigido + juros + multa), 2) AS total
FROM (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY k00_numpre, k00_receit
           ORDER BY prioridade
         ) AS rn
  FROM (
    /* parcelamento: prioridade 1 */
    UNION ALL
    /* retorno bancário: prioridade 2 */
    UNION ALL
    /* cobrança registrada: prioridade 3 */
  ) AS todas
) AS x
WHERE rn = 1
GROUP BY /* número, contribuinte, receita e classificações */
HAVING ABS(SUM(valor_desconto)) > 0
ORDER BY z01_nome;
```

---

### Descontos agrupados por receita: `sql_queryDescontoConcedidoPorRegraAgrupado`

- **Objetivo:** Consolidar o resultado detalhado por receita orçamentária e receita de tesouraria.
- **Fonte:** Usa integralmente `sql_queryDescontoConcedidoPorRegra`.
- **Grão:** Estrutura da receita orçamentária, código e descrição da receita de tesouraria.
- **Agregações:** Juros, multa, desconto, valor histórico, corrigido, valor a pagar, valor pago e total.
- **Ordenação:** Receita orçamentária, receita de tesouraria e descrição.
- **Cuidados:**
  - O método declara `SUM(desconto) AS desconto` duas vezes no `SELECT`; consumidores por nome normalmente enxergam a mesma informação, mas a duplicidade deve ser evitada ao reescrever a consulta.
  - A assinatura do método recebe apenas duas datas. Chamadores legados podem passar argumento extra, que não altera a SQL construída.

```sql
SELECT
  receitorcamentoestrutural AS receita_orcamento,
  receit AS receita_tesouraria,
  descrreceit AS descricao_receita_tesouraria,
  SUM(juros) AS juros,
  SUM(multa) AS multa,
  SUM(desconto) AS desconto,
  SUM(vlrhist) AS valor_historico,
  SUM(vlrcorr) AS valor_corrigido,
  SUM(valor_pagar) AS valor_pagar,
  SUM(valor_pago) AS valor_pago,
  SUM(total) AS total
FROM (
  /* sql_queryDescontoConcedidoPorRegra */
) AS descontos
GROUP BY
  receitorcamentoestrutural,
  receit,
  descrreceit;
```

---

### Pagamentos por período e origem: `sql_queryPagamentosPorPeriodo`

- **Objetivo:** Consolidar pagamentos por receita orçamentária e receita de tesouraria, rateando o valor conforme a origem imobiliária ou mobiliária.
- **Período:** `arrepaga.k00_dtpaga BETWEEN :data_inicial AND :data_final`.
- **Instituição:** Exige `arreinstit.k00_instit = DB_instit`.
- **Exercício orçamentário:** Exige `taborc.k02_anousu = DB_anousu`.
- **Grão final:** Receita orçamentária, receita de tesouraria e descrição da receita.

#### Percentual da origem

```sql
CASE
  WHEN arrematric.k00_numpre IS NOT NULL THEN arrematric.k00_perc
  WHEN arreinscr.k00_numpre IS NOT NULL THEN arreinscr.k00_perc
  ELSE 100
END AS percentual_origem
```

- Se houver vínculo com matrícula, usa `arrematric.k00_perc`.
- Sem matrícula e com inscrição, usa `arreinscr.k00_perc`.
- Sem ambos, atribui `100%`.
- Se matrícula e inscrição coexistirem, a matrícula tem precedência pela ordem do `CASE`.

#### Valores retornados

- **Valor histórico:** `arrepaga.k00_valor * percentual_origem / 100`.
- **Valor corrigido:** Sempre zero nesta implementação.
- **Juros:** Sempre zero nesta implementação.
- **Multas:** Sempre zero nesta implementação.
- **Valor de desconto:** Sempre zero nesta implementação.

O nome do método é genérico, mas esta implementação não recompõe acréscimos ou descontos. Ela distribui somente `arrepaga.k00_valor`.

```sql
SELECT
  receita_orcamento,
  receita_tesouraria,
  descricao_receita,
  ROUND(SUM(juros), 2) AS juros,
  ROUND(SUM(multas), 2) AS multas,
  ROUND(SUM(valor_historico * percentual_origem / 100), 2)
    AS valor_historico,
  ROUND(SUM(valor_corrigido * percentual_origem / 100), 2)
    AS valor_corrigido,
  ROUND(SUM(valor_desconto * percentual_origem / 100), 2)
    AS valor_desconto
FROM (
  SELECT
    taborc.k02_estorc AS receita_orcamento,
    tabrec.k02_codigo AS receita_tesouraria,
    tabrec.k02_descr AS descricao_receita,
    arrepaga.k00_valor AS valor_historico,
    0 AS valor_corrigido,
    0 AS juros,
    0 AS multas,
    0 AS valor_desconto,
    CASE
      WHEN arrematric.k00_numpre IS NOT NULL THEN arrematric.k00_perc
      WHEN arreinscr.k00_numpre IS NOT NULL THEN arreinscr.k00_perc
      ELSE 100
    END AS percentual_origem
  FROM arrepaga
  JOIN arreinstit
    ON arreinstit.k00_numpre = arrepaga.k00_numpre
   AND arreinstit.k00_instit = :instituicao
  JOIN tabrec
    ON tabrec.k02_codigo = arrepaga.k00_receit
  JOIN taborc
    ON taborc.k02_codigo = arrepaga.k00_receit
   AND taborc.k02_anousu = :exercicio
  LEFT JOIN arrematric
    ON arrematric.k00_numpre = arrepaga.k00_numpre
  LEFT JOIN arreinscr
    ON arreinscr.k00_numpre = arrepaga.k00_numpre
  WHERE arrepaga.k00_dtpaga BETWEEN :data_inicial AND :data_final
) AS pagamentos
GROUP BY
  receita_orcamento,
  receita_tesouraria,
  descricao_receita;
```

### Cuidados gerais

- `k00_valor` pode representar componentes positivos ou negativos; não assumir que toda linha é valor principal pago.
- Somar `arrepaga` sem agrupar por receita pode misturar principal, desconto e outros componentes.
- A data usada para relatórios de pagamento é `k00_dtpaga`, salvo nos blocos que usam datas operacionais de `cornump` ou `disbanco`.
- `taborc` é filtrada pelo exercício da sessão, não automaticamente pelo ano de cada pagamento.
- `arrematric` e `arreinscr` podem alterar o grão e ratear valores por percentual.
- Para contar pagamentos ou parcelas, não contar linhas de `arrepaga` sem antes definir a entidade: número de arrecadação, parcela, receita ou componente.
- Para a visão conceitual do ciclo de arrecadação, consultar `knowledge/rag/caixa/arrecadacao_e_pagamentos.md`.
