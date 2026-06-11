# e-Cidade — Cadastro Imobiliário

## Resumo

A tabela `iptunump` vincula o cálculo/lançamento de IPTU de uma matrícula em um exercício ao `numpre`, que é o número do débito utilizado pelo módulo de arrecadação.

Em termos práticos, ela faz a ponte entre:

- matrícula imobiliária (`iptubase.j01_matric`);
- exercício do cálculo (`j20_anousu`);
- débito gerado no arrecadamento (`j20_numpre`).

Essa tabela é importante para análises financeiras porque permite sair do cadastro/cálculo de IPTU e chegar nas tabelas de cobrança, pagamento, cancelamento e dívida.

## Tabela principal

`cadastro.iptunump`

### Grao

Um registro por matrícula e exercício de IPTU, associado a um `numpre`.

### Chave primária / chave lógica

| Campo | Papel |
|---|---|
| `j20_anousu` | Parte da chave lógica. Exercício do IPTU. |
| `j20_matric` | Parte da chave lógica. Matrícula do imóvel. |

Observação: a classe trata `j20_anousu + j20_matric` como chave composta nas operações de inclusão, alteração, exclusão e busca.

## Colunas

| Coluna | Tipo | Descrição | Obrigatório na classe | Observações |
|---|---:|---|---|---|
| `j20_anousu` | int4 | Exercício | Sim | Ano de uso/cálculo do IPTU. |
| `j20_matric` | int4 | Matrícula | Sim | FK lógica para `iptubase.j01_matric`. |
| `j20_numpre` | int4 | Numpre | Sim | Número do débito gerado no arrecadamento. |

## Relacionamentos identificados na classe

### Relacionamentos diretos

| Tabela | Join | Finalidade |
|---|---|---|
| `iptubase` | `iptubase.j01_matric = iptunump.j20_matric` | Recuperar dados cadastrais da matrícula. |
| `lote` | `lote.j34_idbql = iptubase.j01_idbql` | Recuperar dados do lote/terreno. |
| `cgm` | `cgm.z01_numcgm = iptubase.j01_numcgm` | Recuperar contribuinte principal da matrícula. |

### Relacionamentos de endereço

Usados nas consultas `sql_query_ender` e `sql_query_ender_taxa`.

| Tabela | Join | Finalidade |
|---|---|---|
| `testada` | `j34_idbql = j36_idbql` | Obter testadas do lote. |
| `testpri` | `j49_idbql = j36_idbql AND j49_face = j36_face AND j49_codigo = j36_codigo` | Identificar testada principal. |
| `bairro` | `j34_bairro = j13_codi` | Bairro do lote. |
| `ruas` | `j14_codigo = j36_codigo` | Logradouro da testada. |
| `zonas` | `j50_zona = j34_zona` | Zona fiscal. |
| `setor` | `j30_codi = j34_setor` | Setor do lote. |

### Relacionamentos com taxas

A consulta `sql_query_ender_taxa` une os `numpre` de IPTU principal (`iptunump`) com os `numpre` de taxas separadas (`iptutaxanump`).

| Tabela | Join | Finalidade |
|---|---|---|
| `iptutaxanump` | `j151_matric` como matrícula e `j151_numpre` como numpre | Incluir débitos de taxas separadas. |
| `iptucadtaxaexe` | `j08_iptucadtaxaexe = j151_iptucadtaxaexe` | Identificar exercício da taxa (`j08_anousu`). |

## Métodos relevantes

| Método | Tipo | Descrição |
|---|---|---|
| `incluir($j20_anousu, $j20_matric)` | Escrita | Insere vínculo entre exercício, matrícula e numpre. |
| `alterar($j20_anousu = null, $j20_matric = null)` | Escrita | Atualiza registro pela chave composta. |
| `excluir($j20_anousu = null, $j20_matric = null, $dbwhere = null)` | Escrita | Exclui por exercício/matrícula ou por `dbwhere`. |
| `sql_record($sql)` | Leitura | Executa SQL e atualiza `numrows`. |
| `sql_query(...)` | Leitura | Consulta `iptunump` com joins básicos para imóvel, lote e CGM. |
| `sql_query_ender(...)` | Leitura | Consulta `iptunump` com dados de endereço/localização. |
| `sql_query_file(...)` | Leitura | Consulta direta na tabela `iptunump`, sem joins. |
| `sql_query_ender_taxa(...)` | Leitura | Consulta endereço incluindo numpres de IPTU e taxas. |

## SQLs extraídos e normalizados

### 1. Buscar vínculo IPTU → numpre por exercício e matrícula

```sql
SELECT *
FROM iptunump
WHERE j20_anousu = :ano
  AND j20_matric = :matricula;
```

### 2. Buscar numpre com dados cadastrais básicos

Extraído de `sql_query`.

```sql
SELECT *
FROM iptunump
INNER JOIN iptubase
        ON iptubase.j01_matric = iptunump.j20_matric
INNER JOIN lote
        ON lote.j34_idbql = iptubase.j01_idbql
INNER JOIN cgm
        ON cgm.z01_numcgm = iptubase.j01_numcgm
WHERE iptunump.j20_anousu = :ano
  AND iptunump.j20_matric = :matricula;
```

### 3. Buscar numpre com endereço principal do imóvel

Extraído de `sql_query_ender`.

```sql
SELECT *
FROM iptunump
INNER JOIN iptubase
        ON iptubase.j01_matric = iptunump.j20_matric
INNER JOIN lote
        ON lote.j34_idbql = iptubase.j01_idbql
INNER JOIN testada
        ON j34_idbql = j36_idbql
INNER JOIN testpri
        ON j49_idbql = j36_idbql
       AND j49_face = j36_face
       AND j49_codigo = j36_codigo
INNER JOIN bairro
        ON j34_bairro = j13_codi
INNER JOIN ruas
        ON j14_codigo = j36_codigo
INNER JOIN zonas
        ON j50_zona = j34_zona
INNER JOIN setor
        ON j30_codi = j34_setor
WHERE iptunump.j20_anousu = :ano
  AND iptunump.j20_matric = :matricula;
```

### 4. Buscar endereço considerando IPTU principal e taxas separadas

Extraído de `sql_query_ender_taxa`.

```sql
SELECT *
FROM iptubase
INNER JOIN (
    SELECT
        j20_matric,
        j20_anousu,
        j20_numpre
    FROM iptunump
    WHERE j20_anousu = :ano

    UNION

    SELECT
        j151_matric AS j20_matric,
        j08_anousu AS j20_anousu,
        j151_numpre AS j20_numpre
    FROM iptutaxanump txnump
    INNER JOIN iptucadtaxaexe txexe
            ON txexe.j08_iptucadtaxaexe = txnump.j151_iptucadtaxaexe
    WHERE txexe.j08_anousu = :ano
) nump
        ON iptubase.j01_matric = nump.j20_matric
INNER JOIN lote
        ON lote.j34_idbql = iptubase.j01_idbql
INNER JOIN testada
        ON j34_idbql = j36_idbql
INNER JOIN testpri
        ON j49_idbql = j36_idbql
       AND j49_face = j36_face
       AND j49_codigo = j36_codigo
INNER JOIN bairro
        ON j34_bairro = j13_codi
INNER JOIN ruas
        ON j14_codigo = j36_codigo
INNER JOIN zonas
        ON j50_zona = j34_zona
INNER JOIN setor
        ON j30_codi = j34_setor
WHERE nump.j20_anousu = :ano
  AND nump.j20_matric = :matricula;
```

### 5. Inserir vínculo de numpre

Extraído de `incluir`.

```sql
INSERT INTO iptunump (
    j20_anousu,
    j20_matric,
    j20_numpre
)
VALUES (
    :ano,
    :matricula,
    :numpre
);
```

### 6. Alterar numpre

Extraído de `alterar`.

```sql
UPDATE iptunump
SET j20_numpre = :numpre
WHERE j20_anousu = :ano
  AND j20_matric = :matricula;
```

### 7. Excluir vínculo

Extraído de `excluir`.

```sql
DELETE FROM iptunump
WHERE j20_anousu = :ano
  AND j20_matric = :matricula;
```

## Perguntas que esta tabela ajuda a responder

- Qual `numpre` foi gerado para uma matrícula em determinado exercício?
- Quais matrículas tiveram débito gerado em determinado exercício?
- Como vincular o cálculo do IPTU às tabelas de arrecadação?
- Qual endereço/localização deve ser usado para emissão ou análise do débito?
- Como considerar, em uma mesma consulta, débitos de IPTU principal e taxas separadas?

## Filtros seguros

| Filtro | Uso recomendado |
|---|---|
| `j20_anousu = :ano` | Sempre filtrar por exercício em análises anuais. |
| `j20_matric = :matricula` | Usar para análise individual de imóvel. |
| `j20_numpre = :numpre` | Usar para rastrear o débito no arrecadamento. |

## Cuidados / riscos

- `iptunump` não contém valor calculado. Para valores do cálculo, usar `iptucalc`, `iptucalv` e/ou tabelas de arrecadação.
- `j20_numpre` é ponte para cobrança/arrecadação, não é matrícula.
- A chave prática usada pela classe é `j20_anousu + j20_matric`.
- Para taxas separadas, `iptunump` sozinho pode ser insuficiente; usar a lógica de união com `iptutaxanump`.
- Consultas de endereço dependem de `testpri`; se a testada principal não estiver cadastrada, o `INNER JOIN` pode eliminar a matrícula do resultado.
- A classe usa SQL concatenado com variáveis; em implementação nova, substituir por parâmetros/bind para evitar risco de injeção.

## Convenções de prefixo

| Prefixo | Tabela / contexto |
|---|---|
| `j20_` | `iptunump` |
| `j01_` | `iptubase` |
| `j34_` | `lote` |
| `z01_` | `cgm` |
| `j36_` | `testada` |
| `j49_` | `testpri` |
| `j13_` | `bairro` |
| `j14_` | `ruas` |
| `j50_` | `zonas` |
| `j30_` | `setor` |
| `j151_` | `iptutaxanump` |
| `j08_` | `iptucadtaxaexe` |

## Uso recomendado para IA

Use `iptunump` quando a pergunta envolver geração de débito, vínculo com arrecadação, `numpre`, emissão/cobrança ou rastreamento financeiro do IPTU.

Não use `iptunump` como fonte principal para valor venal, áreas, alíquotas ou valores por receita. Para isso, prefira:

- `iptucalc` para resumo do cálculo;
- `iptucalv` para valores por receita;
- `iptucale` para valores por construção;
- tabelas de arrecadação para situação financeira do débito.
