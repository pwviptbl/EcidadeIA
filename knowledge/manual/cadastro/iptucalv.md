# e-Cidade — Cadastro Imobiliário

## Tabela Principal: `cadastro.iptucalv`

Tabela de valores gerados no cálculo do IPTU por exercício, matrícula, receita e histórico de cálculo.

Cada registro representa um valor calculado para uma matrícula em determinado exercício, associado a uma receita (`j21_receit`) e a um histórico de cálculo (`j21_codhis`).

> Importante: `iptucalv` não deve ser tratada como “valor total de IPTU” sem classificação. Ela pode conter valores de IPTU, taxas, isenções e outros componentes do cálculo, dependendo do histórico e da receita.

## Resumo técnico

| Item | Valor |
|---|---|
| Classe PHP | `cl_iptucalv` |
| Tabela | `cadastro.iptucalv` |
| Módulo | `cadastro` |
| Finalidade | Valores financeiros gerados pelo cálculo de IPTU |
| Chave primária | Não declarada na classe; operações de alteração/exclusão usam `oid` |
| Chave de negócio recomendada | `j21_anousu`, `j21_matric`, `j21_receit`, `j21_codhis` |
| Coluna temporal | `j21_anousu` |
| Grão | Uma linha por valor calculado de matrícula/exercício/receita/histórico |
| Recomendada para análise | Sim, para valores de cálculo e comparação entre exercícios |

## Colunas

| Coluna | Tipo | Papel | Descrição |
|---|---:|---|---|
| `j21_anousu` | `int4` | exercício / tempo | Exercício do cálculo |
| `j21_matric` | `int4` | chave de negócio / FK | Matrícula do imóvel |
| `j21_receit` | `int4` | classificação arrecadatória / FK | Código da receita |
| `j21_valor` | `float8` | métrica | Valor gerado no cálculo |
| `j21_quant` | `float8` | métrica auxiliar | Quantidade associada ao valor |
| `j21_codhis` | `int8` | classificação de histórico / FK | Código do histórico do cálculo |

## Relacionamentos principais

| Origem | Destino | Relação | Uso |
|---|---|---|---|
| `iptucalv.j21_matric` | `iptubase.j01_matric` | matrícula do imóvel | Identificar o imóvel calculado |
| `iptucalv.j21_codhis` | `iptucalh.j17_codhis` | histórico do cálculo | Classificar se o valor é IPTU, taxa, isenção etc. |
| `iptucalv.j21_receit` | `tabrec.k02_codigo` | receita | Classificação arrecadatória/contábil |
| `iptucalv.j21_anousu`, `j21_matric` | `iptunump.j20_anousu`, `j20_matric` | número do débito gerado | Conectar cálculo com arrecadação/pagamento |
| `iptucalv.j21_matric` | `iptutaxacalv` via `iptutaxanump` | taxas calculadas separadamente | Usado em consulta que une IPTU e taxas |

## Operações CRUD mapeadas

| Método | Operação | Observação |
|---|---|---|
| `sql_query()` | Consulta genérica | Não aplica filtro por `oid`; usa `dbwhere` quando informado |
| `sql_query_file()` | Consulta genérica da tabela | Sem joins |
| `sql_query_hist()` | Consulta pretendida com histórico | Contém indício de join com `iptucalh`, mas o SQL sobrescreve `$sql2` e perde o join |
| `sql_queryValoresCalculoIptu($iAnoCalculo)` | Relatório financeiro por receita | Consolida calculado, isento, cancelado, compensado, pago, a pagar e importado |
| `sql_queryIptuDiversos($iAno, $iTipo)` | Relatório de diversos por receita | Usa arrecadação/diversos e status financeiro |
| `sql_query_taxa($j21_anousu, $j21_matric)` | União de valores IPTU + taxas | Une `iptucalv` e `iptutaxacalv` |

## Regras de negócio extraídas

### 1. Valor calculado não é necessariamente IPTU puro

`j21_valor` representa um valor gerado no cálculo. Para saber se é IPTU, taxa, isenção ou outro componente, deve-se classificar por:

1. `j21_codhis` → `cadastro.iptucalh.j17_codhis`; e/ou
2. `j21_receit` → `caixa.tabrec.k02_codigo`.

Regra prática:

> Não responder “valor total do IPTU” usando apenas `sum(j21_valor)` sem filtrar/classificar histórico ou receita.

### 2. Valores negativos podem representar isenção

Na consulta `sql_queryValoresCalculoIptu`, o valor isento é calculado quando `j21_valor < 0` e existe correspondência com configurações de histórico/isencão em:

- `iptucalhconf`
- `iptuisen`
- `isenexe`
- `tipoisen`

### 3. Situação financeira depende da arrecadação

A tabela `iptucalv` guarda o valor calculado. Para saber se foi pago, cancelado, compensado ou está em aberto, a classe cruza com tabelas de arrecadação:

- `iptunump`
- `arrecad`
- `arrecant`
- `arrepaga`
- `cancdebitosreg`
- `cancdebitosprocreg`
- `abatimento`
- `abatimentoarreckey`
- `abatimentoutilizacao`
- `abatimentoutilizacaodestino`

### 4. Quantidade de matrículas calculadas por receita

A consulta `sql_queryValoresCalculoIptu` conta registros de `iptucalv` por exercício e receita onde `j21_valor > 0`.

Isso não é necessariamente “quantidade de imóveis únicos”, porque a mesma matrícula pode ter mais de uma linha por histórico/receita.

Para contar imóveis únicos, usar:

```sql
count(distinct j21_matric)
```

## Consultas SQL prontas

### 1. Buscar valores de cálculo por matrícula e exercício

```sql
SELECT
  v.j21_anousu,
  v.j21_matric,
  v.j21_receit,
  r.k02_descr AS receita_descricao,
  v.j21_codhis,
  h.j17_descr AS historico_descricao,
  v.j21_valor,
  v.j21_quant
FROM cadastro.iptucalv v
LEFT JOIN cadastro.iptucalh h
       ON h.j17_codhis = v.j21_codhis
LEFT JOIN caixa.tabrec r
       ON r.k02_codigo = v.j21_receit
WHERE v.j21_anousu = :ano
  AND v.j21_matric = :matricula
ORDER BY v.j21_receit, v.j21_codhis;
```

### 2. Somar valores calculados por exercício e receita

```sql
SELECT
  v.j21_anousu AS ano,
  v.j21_receit AS codigo_receita,
  r.k02_descr AS descricao_receita,
  count(*) AS quantidade_linhas,
  count(DISTINCT v.j21_matric) AS quantidade_matriculas,
  round(sum(v.j21_valor)::numeric, 2) AS valor_total
FROM cadastro.iptucalv v
LEFT JOIN caixa.tabrec r
       ON r.k02_codigo = v.j21_receit
WHERE v.j21_anousu = :ano
GROUP BY
  v.j21_anousu,
  v.j21_receit,
  r.k02_descr
ORDER BY v.j21_receit;
```

### 3. Somar somente valores positivos calculados

```sql
SELECT
  v.j21_anousu AS ano,
  v.j21_receit AS codigo_receita,
  r.k02_descr AS descricao_receita,
  count(DISTINCT v.j21_matric) AS quantidade_matriculas,
  round(sum(CASE WHEN v.j21_valor > 0 THEN v.j21_valor ELSE 0 END)::numeric, 2) AS valor_calculado
FROM cadastro.iptucalv v
LEFT JOIN caixa.tabrec r
       ON r.k02_codigo = v.j21_receit
WHERE v.j21_anousu = :ano
GROUP BY
  v.j21_anousu,
  v.j21_receit,
  r.k02_descr
ORDER BY v.j21_receit;
```

### 4. Identificar valores por histórico de cálculo

```sql
SELECT
  v.j21_anousu AS ano,
  v.j21_codhis AS codigo_historico,
  h.j17_descr AS historico_descricao,
  count(*) AS quantidade_linhas,
  count(DISTINCT v.j21_matric) AS quantidade_matriculas,
  round(sum(v.j21_valor)::numeric, 2) AS valor_total
FROM cadastro.iptucalv v
LEFT JOIN cadastro.iptucalh h
       ON h.j17_codhis = v.j21_codhis
WHERE v.j21_anousu = :ano
GROUP BY
  v.j21_anousu,
  v.j21_codhis,
  h.j17_descr
ORDER BY v.j21_codhis;
```

### 5. Consulta para “somente IPTU” por histórico

```sql
SELECT
  v.j21_anousu AS ano,
  count(DISTINCT v.j21_matric) AS quantidade_matriculas,
  round(sum(v.j21_valor)::numeric, 2) AS valor_iptu
FROM cadastro.iptucalv v
JOIN cadastro.iptucalh h
  ON h.j17_codhis = v.j21_codhis
WHERE v.j21_anousu = :ano
  AND position('iptu' IN lower(h.j17_descr)) > 0
GROUP BY v.j21_anousu;
```

> Validar no município se o histórico do IPTU sempre contém a palavra `iptu`. Em bases customizadas, o filtro pode exigir código fixo de histórico ou receita.

### 6. Comparar valores entre dois exercícios por matrícula

```sql
WITH base AS (
  SELECT
    v.j21_matric,
    v.j21_anousu,
    sum(v.j21_valor) AS valor_total
  FROM cadastro.iptucalv v
  WHERE v.j21_anousu IN (:ano_anterior, :ano_atual)
  GROUP BY v.j21_matric, v.j21_anousu
)
SELECT
  coalesce(a.j21_matric, b.j21_matric) AS matricula,
  coalesce(a.valor_total, 0) AS valor_ano_anterior,
  coalesce(b.valor_total, 0) AS valor_ano_atual,
  coalesce(b.valor_total, 0) - coalesce(a.valor_total, 0) AS diferenca_valor,
  CASE
    WHEN coalesce(a.valor_total, 0) = 0 THEN NULL
    ELSE round(((coalesce(b.valor_total, 0) - a.valor_total) / a.valor_total * 100)::numeric, 2)
  END AS variacao_percentual
FROM base a
FULL JOIN base b
       ON b.j21_matric = a.j21_matric
      AND b.j21_anousu = :ano_atual
WHERE a.j21_anousu = :ano_anterior
   OR b.j21_anousu = :ano_atual
ORDER BY abs(coalesce(b.valor_total, 0) - coalesce(a.valor_total, 0)) DESC;
```

### 7. Unir valores de IPTU e taxas da classe `sql_query_taxa`

```sql
SELECT
  calv.j21_valor
FROM (
  SELECT
    j21_valor
  FROM cadastro.iptucalv
  WHERE j21_anousu = :ano
    AND j21_matric = :matricula

  UNION

  SELECT
    j152_valor AS j21_valor
  FROM cadastro.iptutaxacalv
  INNER JOIN cadastro.iptutaxanump
          ON j151_codigo = j152_iptutaxanump
  INNER JOIN cadastro.iptucadtaxaexe
          ON j08_iptucadtaxaexe = j151_iptucadtaxaexe
  WHERE j08_anousu = :ano
    AND j151_matric = :matricula
) calv;
```

### 8. Relatório financeiro consolidado por receita

Versão simplificada da intenção de `sql_queryValoresCalculoIptu`:

```sql
SELECT
  v.j21_anousu AS ano_calculo,
  v.j21_receit AS codigo_receita,
  r.k02_descr AS descricao_receita,
  coalesce(round(sum(CASE WHEN v.j21_valor > 0 THEN v.j21_valor ELSE 0 END)::numeric, 2), 0) AS valor_calculado,
  coalesce(round(sum(CASE WHEN v.j21_valor < 0 THEN v.j21_valor * -1 ELSE 0 END)::numeric, 2), 0) AS valor_negativo,
  count(DISTINCT v.j21_matric) AS quantidade_matriculas
FROM cadastro.iptucalv v
LEFT JOIN caixa.tabrec r
       ON r.k02_codigo = v.j21_receit
WHERE v.j21_anousu = :ano
GROUP BY
  v.j21_anousu,
  v.j21_receit,
  r.k02_descr
ORDER BY v.j21_receit;
```

## Perguntas que esta tabela ajuda a responder

- Qual foi o valor calculado por matrícula em determinado exercício?
- Quanto foi calculado por receita no exercício?
- Quais matrículas tiveram maior variação entre 2026 e 2027?
- Qual a composição do cálculo por histórico?
- Qual valor calculado, isento, pago, cancelado, compensado ou em aberto por receita?
- Quantas matrículas tiveram valor calculado positivo em uma receita?
- Quais receitas compõem o cálculo de uma matrícula?

## Filtros recomendados

| Filtro | SQL |
|---|---|
| Por exercício | `v.j21_anousu = :ano` |
| Por matrícula | `v.j21_matric = :matricula` |
| Por receita | `v.j21_receit = :receita` |
| Por histórico | `v.j21_codhis = :codhis` |
| Valores positivos | `v.j21_valor > 0` |
| Valores negativos/isentos potenciais | `v.j21_valor < 0` |
| Imóveis únicos | `count(distinct v.j21_matric)` |

## Cuidados / riscos

1. **Não somar `j21_valor` cru para responder IPTU total**, pois a tabela pode misturar IPTU, taxas, isenções e outros históricos.
2. **`sql_query_hist()` tem possível bug/legado:** o código monta um `inner join iptucalh`, mas em seguida sobrescreve `$sql2 = ""`, descartando o join.
4. **Quantidade de linhas não é quantidade de imóveis:** usar `count(distinct j21_matric)` quando a pergunta for sobre imóveis/matrículas.
5. **Receita e histórico respondem perguntas diferentes:** receita serve para classificação arrecadatória; histórico serve para composição do cálculo.
6. **Situação de pagamento não está em `iptucalv`:** precisa cruzar com arrecadação (`arrecad`, `arrecant`, `arrepaga`, cancelamentos e abatimentos).
7. **Valores negativos exigem interpretação:** podem representar isenções ou ajustes, dependendo de `iptucalh`, `iptucalhconf` e regras do município.

## Uso recomendado para análise 2026 × 2027

Para comparação de impacto do recadastramento e nova fórmula de cálculo:

1. Usar `iptucalv` como tabela de valores calculados.
2. Filtrar os exercícios comparados em `j21_anousu`.
3. Classificar por `j21_codhis` e/ou `j21_receit` antes de agregar.
4. Usar `count(distinct j21_matric)` para quantidade de imóveis.
5. Cruzar com `iptubase`, `lote`, `bairro`, `setor`, `zonas` e `iptuconstr` para explicar impacto por localização e características.
6. Usar `iptucalc` para métricas estruturais do cálculo, como área, valor venal, alíquota e área edificada.