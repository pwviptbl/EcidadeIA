# e-Cidade — Cadastro Imobiliário

## Resumo
- A classe representa a tabela `iptucale`, usada para armazenar dados financeiros/secundários do cálculo de IPTU por construção/edificação de uma matrícula.
- Cada registro representa o cálculo de uma construção específica de uma matrícula em um exercício.

## Tabela principal `cl_iptucale`

| Item | Valor |
|---|---|
| Tabela | `iptucale` |
| Classe PHP | `cl_iptucale` |
| Módulo | `cadastro` |
| Prefixo dos campos | `j22` |
| Entidade | Cálculo por edificação/construção |
| Chave primária lógica | `j22_anousu`, `j22_matric`, `j22_idcons` |
| Grão | 1 registro por exercício + matrícula + construção |
| Operações da classe | incluir, alterar, excluir, consultar |

## Resumo funcional

A tabela `iptucale` guarda o detalhamento do cálculo do valor venal por construção.

Ela se conecta à construção cadastrada em `iptuconstr`, à matrícula em `iptubase` e ao logradouro da construção em `ruas`.

É uma tabela secundária em relação a `iptucalc`, pois `iptucalc` consolida o cálculo do imóvel/matrícula, enquanto `iptucale` detalha o cálculo por edificação.

## Colunas

| Coluna | Tipo | Papel | Métrica | Descrição |
|---|---:|---|---|---|
| `j22_anousu` | `int4` | chave | dimensão temporal | Exercício do cálculo |
| `j22_matric` | `int4` | chave / FK lógica | dimensão | Matrícula do imóvel |
| `j22_idcons` | `int4` | chave / FK lógica | dimensão | Código da construção |
| `j22_areaed` | `float8` | atributo | sim | Área construída usada no cálculo |
| `j22_vm2` | `float8` | atributo | sim | Valor do metro quadrado da construção |
| `j22_pontos` | `int4` | atributo | sim | Pontuação da construção |
| `j22_valor` | `float8` | atributo | sim | Valor venal calculado da construção |

## Chaves e identificadores

### Chave primária lógica

```sql
(j22_anousu, j22_matric, j22_idcons)
```

### Chaves de negócio candidatas

| Chave | Uso |
|---|---|
| `j22_anousu + j22_matric + j22_idcons` | Identifica o cálculo de uma construção específica em um exercício |

### Observação

A classe não usa sequence. Os três campos da chave são recebidos como parâmetros no método `incluir($j22_anousu, $j22_matric, $j22_idcons)`.

## Relacionamentos inferidos da classe

| Tabela relacionada | Relação | Tipo | Origem |
|---|---|---|---|
| `iptuconstr` | `iptuconstr.j39_matric = iptucale.j22_matric` e `iptuconstr.j39_idcons = iptucale.j22_idcons` | INNER JOIN | `sql_query` |
| `ruas` | `ruas.j14_codigo = iptuconstr.j39_codigo` | INNER JOIN | `sql_query` |
| `iptubase` | `iptubase.j01_matric = iptuconstr.j39_matric` | INNER JOIN | `sql_query` |

## Relação com outras tabelas do cálculo IPTU

| Tabela | Relação funcional |
|---|---|
| `iptucalc` | Consolida o cálculo da matrícula por exercício |
| `iptucale` | Detalha o cálculo por construção/edificação |
| `iptucalv` | Detalha valores por receita/histórico |
| `iptunump` | Liga exercício/matrícula ao `numpre` gerado no arrecadamento |
| `iptuconstr` | Cadastro das construções da matrícula |
| `iptubase` | Cadastro principal da matrícula |

## Operações SQL extraídas e normalizadas

### 4. Consulta simples por chave

```sql
SELECT *
FROM iptucale
WHERE j22_anousu = :anousu
  AND j22_matric = :matric
  AND j22_idcons = :idcons;
```

### 5. Consulta com relacionamento da construção

```sql
SELECT *
FROM iptucale
INNER JOIN iptuconstr
        ON iptuconstr.j39_matric = iptucale.j22_matric
       AND iptuconstr.j39_idcons = iptucale.j22_idcons
INNER JOIN ruas
        ON ruas.j14_codigo = iptuconstr.j39_codigo
INNER JOIN iptubase
        ON iptubase.j01_matric = iptuconstr.j39_matric
WHERE iptucale.j22_anousu = :anousu
  AND iptucale.j22_matric = :matric
  AND iptucale.j22_idcons = :idcons;
```

### 6. Consulta de valor venal por construção em um exercício

```sql
SELECT
    j22_anousu,
    j22_matric,
    j22_idcons,
    j22_areaed,
    j22_vm2,
    j22_pontos,
    j22_valor
FROM iptucale
WHERE j22_anousu = :anousu
  AND j22_matric = :matric
ORDER BY j22_idcons;
```

### 7. Total de valor venal das construções por matrícula

```sql
SELECT
    j22_anousu,
    j22_matric,
    SUM(j22_areaed) AS area_construida_total,
    SUM(j22_valor)  AS valor_venal_construcoes
FROM iptucale
WHERE j22_anousu = :anousu
GROUP BY
    j22_anousu,
    j22_matric;
```

### 8. Comparação de valor venal de construções entre exercícios

```sql
SELECT
    atual.j22_matric,
    atual.j22_idcons,
    anterior.j22_valor AS valor_anterior,
    atual.j22_valor    AS valor_atual,
    atual.j22_valor - anterior.j22_valor AS diferenca_valor,
    CASE
        WHEN anterior.j22_valor = 0 THEN NULL
        ELSE ROUND(((atual.j22_valor - anterior.j22_valor) / anterior.j22_valor)::numeric * 100, 2)
    END AS variacao_percentual
FROM iptucale atual
LEFT JOIN iptucale anterior
       ON anterior.j22_matric = atual.j22_matric
      AND anterior.j22_idcons = atual.j22_idcons
      AND anterior.j22_anousu = :ano_anterior
WHERE atual.j22_anousu = :ano_atual;
```

### 9. Imóveis com maior valor venal de construção

```sql
SELECT
    j22_anousu,
    j22_matric,
    SUM(j22_valor) AS valor_venal_construcoes
FROM iptucale
WHERE j22_anousu = :anousu
GROUP BY
    j22_anousu,
    j22_matric
ORDER BY valor_venal_construcoes DESC
LIMIT :limite;
```

### 10. Construções com maior valor de m²

```sql
SELECT
    j22_anousu,
    j22_matric,
    j22_idcons,
    j22_areaed,
    j22_vm2,
    j22_valor
FROM iptucale
WHERE j22_anousu = :anousu
ORDER BY j22_vm2 DESC
LIMIT :limite;
```

## Auditoria

A classe registra operações em tabelas de auditoria do e-Cidade:

| Operação | Tabelas usadas |
|---|---|
| Inclusão | `db_acountacesso`, `db_acountkey`, `db_acount` |
| Alteração | `db_acountacesso`, `db_acountkey`, `db_acount` |
| Exclusão | `db_acountacesso`, `db_acountkey`, `db_acount` |

### Códigos de auditoria usados

| Campo | Código |
|---|---:|
| `j22_anousu` | `661` |
| `j22_matric` | `662` |
| `j22_idcons` | `663` |
| `j22_areaed` | `664` |
| `j22_vm2` | `665` |
| `j22_pontos` | `666` |
| `j22_valor` | `667` |

| Código do grupo/tabela na auditoria | Valor |
|---|---:|
| `iptucale` | `123` |

## Perguntas que esta tabela ajuda a responder

- Qual foi o valor venal calculado para cada construção de uma matrícula?
- Qual a área construída considerada no cálculo do IPTU?
- Qual o valor do metro quadrado de construção usado no exercício?
- Quais construções tiveram maior variação de valor entre dois exercícios?
- Quanto do valor venal do imóvel vem das construções?
- Quais imóveis concentram maior valor venal edificado?
- Quais matrículas tiveram alteração relevante na área construída ou no valor venal das edificações?

## Filtros e regras reaproveitáveis

### Filtros padrão

```sql
j22_anousu = :anousu
```

```sql
j22_matric = :matric
```

```sql
j22_idcons = :idcons
```

### Filtro por exercício e matrícula

```sql
j22_anousu = :anousu
AND j22_matric = :matric
```

### Filtro por construção específica

```sql
j22_anousu = :anousu
AND j22_matric = :matric
AND j22_idcons = :idcons
```

## Regras de negócio inferidas

- `iptucale` não representa o imóvel inteiro; representa o cálculo de uma construção específica.
- Para totalizar por matrícula, é necessário agrupar por `j22_anousu` e `j22_matric`.
- Para comparar exercícios, a chave de pareamento deve incluir matrícula e construção: `j22_matric + j22_idcons`.
- `j22_valor` é o valor venal calculado da construção, não necessariamente o IPTU lançado.
- `j22_vm2` é o valor unitário por m² aplicado à construção.
- `j22_areaed` é a área construída considerada no cálculo, podendo diferir de áreas cadastrais de outras tabelas.
- `j22_pontos` indica pontuação usada na composição do cálculo, quando a regra municipal utiliza pontuação por construção.

## Cuidados e riscos

- Não somar `iptucale.j22_valor` com `iptucalc.j23_vlrter` sem entender a fórmula municipal, pois um representa construção e outro terreno.
- Não usar `j22_valor` como valor de imposto. Para imposto/taxa por receita, usar `iptucalv`.
- Não usar `iptucale` para identificar proprietário. Para isso, usar `iptubase` + `cgm` ou views de proprietário.
- A classe usa SQL dinâmico sem parametrização nativa; ao reaproveitar as queries, substituir por placeholders seguros.
- A consulta `sql_query` contém joins duplicados com aliases (`ruas as a`, `iptubase as b`) que podem ser redundantes para análise.
- Registros ausentes em `iptucale` não significam necessariamente ausência de construção; pode indicar ausência de cálculo para o exercício.
- A comparação entre anos deve considerar que uma construção pode existir em um ano e não existir em outro.

## Uso recomendado em análise de impacto do recadastramento/IPTU

A tabela `iptucale` é útil para decompor o impacto do recadastramento sobre as construções.

### Métricas recomendadas

| Métrica | Expressão |
|---|---|
| Área construída total | `SUM(j22_areaed)` |
| Valor venal edificado | `SUM(j22_valor)` |
| Valor médio por m² | `SUM(j22_valor) / NULLIF(SUM(j22_areaed), 0)` |
| Quantidade de construções calculadas | `COUNT(*)` |
| Pontuação média | `AVG(j22_pontos)` |
| Variação de valor venal edificado | `valor_atual - valor_anterior` |
| Variação percentual | `(valor_atual - valor_anterior) / valor_anterior` |

### Consulta base para impacto entre exercícios

```sql
WITH anterior AS (
    SELECT
        j22_matric,
        SUM(j22_areaed) AS area_construida_anterior,
        SUM(j22_valor)  AS valor_edificado_anterior
    FROM iptucale
    WHERE j22_anousu = :ano_anterior
    GROUP BY j22_matric
),
atual AS (
    SELECT
        j22_matric,
        SUM(j22_areaed) AS area_construida_atual,
        SUM(j22_valor)  AS valor_edificado_atual
    FROM iptucale
    WHERE j22_anousu = :ano_atual
    GROUP BY j22_matric
)
SELECT
    COALESCE(atual.j22_matric, anterior.j22_matric) AS matricula,
    anterior.area_construida_anterior,
    atual.area_construida_atual,
    atual.area_construida_atual - anterior.area_construida_anterior AS diferenca_area,
    anterior.valor_edificado_anterior,
    atual.valor_edificado_atual,
    atual.valor_edificado_atual - anterior.valor_edificado_anterior AS diferenca_valor
FROM atual
FULL JOIN anterior
       ON anterior.j22_matric = atual.j22_matric;
```

## Convenção de prefixos

| Prefixo | Tabela provável | Significado |
|---|---|---|
| `j22` | `iptucale` | Cálculo por edificação/construção |
| `j39` | `iptuconstr` | Construções do imóvel |
| `j01` | `iptubase` | Matrícula imobiliária |
| `j14` | `ruas` | Logradouro |
| `db_acount*` | auditoria | Log de alterações |

## Resumo para IA

Use `iptucale` quando a pergunta envolver cálculo de IPTU por construção, área construída calculada, valor de m² da construção, pontuação da edificação ou valor venal edificado.

Não use `iptucale` como fonte principal para valor lançado por receita, pagamento, débito, proprietário ou lote. Para esses casos, combine com `iptucalv`, `iptunump`, `iptubase`, `lote` e `cgm`.
