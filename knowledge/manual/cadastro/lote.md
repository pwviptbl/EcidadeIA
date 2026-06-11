# e-Cidade — Cadastro Imobiliário

## 1. Resumo da extração

Este documento segue o padrão de extração usado para as demais classes do cadastro imobiliário: descrição objetiva da tabela principal, campos, regras operacionais, relacionamentos inferidos dos SQLs e consultas prontas para uso por IA ou por apoio técnico.

| Item | Valor |
|---|---|
| Classe | `cl_lote` |
| Entidade/Tabela principal | `lote` |
| Módulo | `Cadastro` |
| Chave primária/lógica | `j34_idbql` |
| Sequence usada na inclusão | `lote_j34_idbql_seq` |
| Função principal da tabela | Cadastro físico/localizacional do lote imobiliário: setor, quadra, lote, área, bairro, zona fiscal e áreas complementares. |

A tabela `lote` é uma das bases centrais do cadastro imobiliário. Ela identifica o lote por `j34_idbql` e guarda os atributos territoriais usados por `iptubase`, cálculo de IPTU, georreferenciamento, localização, testadas e emissão de relatórios/cartões.

---

## 2. Tabela principal: `lote`

| Campo | Tipo | Descrição | Observações de uso |
|---|---:|---|---|
| `j34_idbql` | `int4` | Cód. Lote | Chave principal do lote. Gerada por `lote_j34_idbql_seq` quando não informada. |
| `j34_setor` | `char(4)` | Setor | Obrigatório na inclusão. Relaciona com `setor.j30_codi`. |
| `j34_quadra` | `char(4)` | Quadra | Obrigatório na inclusão. |
| `j34_lote` | `char(4)` | Lote | Obrigatório na inclusão. |
| `j34_area` | `float8` | Área M2 | Obrigatório. Área oficial do lote. |
| `j34_bairro` | `int4` | Cód. Bairro | Obrigatório. Relaciona com `bairro.j13_codi`. |
| `j34_areal` | `float8` | Área Medida | Se nulo na inclusão, assume `0`. |
| `j34_totcon` | `float8` | Total construído no lote | Se nulo na inclusão, assume `0`. |
| `j34_zona` | `int8` | Zona Fiscal | Obrigatório. Relaciona com `zonas.j50_zona`. |
| `j34_quamat` | `int4` | Matrículas cadastradas | Se nulo na inclusão, assume `0`. |
| `j34_areapreservada` | `float8` | Área Preservada | Se nulo na inclusão, assume `0`. |
| `j34_areaprivativa` | `float8` | Área Privativa | Obrigatório na inclusão. |
| `j34_areausocomum` | `float8` | Área Uso Comum | Se nulo na inclusão, assume `0`. |
| `j34_zonadesurb` | `int4` | Zona Des. Urbano | Se nulo na inclusão, grava `NULL`. |

---

## 4. Tabelas relacionadas

### Relacionamentos diretos do método `sql_query`

| Tabela | Ligação | Papel |
|---|---|---|
| `bairro` | `bairro.j13_codi = lote.j34_bairro` | Bairro do lote. |
| `setor` | `setor.j30_codi = lote.j34_setor` | Setor fiscal/local do lote. |
| `zonas` | `zonas.j50_zona = lote.j34_zona` | Zona fiscal do lote. |

### Relacionamentos com matrícula e proprietário

| Tabela | Ligação | Papel |
|---|---|---|
| `iptubase` | `iptubase.j01_idbql = lote.j34_idbql` | Matrículas imobiliárias vinculadas ao lote. |
| `cgm` | `cgm.z01_numcgm = iptubase.j01_numcgm` | Proprietário principal da matrícula. |
| `iptuant` | `iptuant.j40_matric = iptubase.j01_matric` | Referências anteriores da matrícula. |

### Relacionamentos de endereço e testada

| Tabela | Ligação | Papel |
|---|---|---|
| `testada` | `testada.j36_idbql = lote.j34_idbql` | Testadas do lote. |
| `testpri` | `testpri.j49_idbql = testada.j36_idbql` e `testpri.j49_face = testada.j36_face` | Testada principal. |
| `testadanumero` | `testadanumero.j15_idbql = testpri.j49_idbql` e `j15_face = j49_face` | Número predial por testada. |
| `ruas` | `ruas.j14_codigo = testpri.j49_codigo` | Logradouro vinculado à testada. |
| `ruastipo` | `ruastipo.j88_codigo = ruas.j14_tipo` | Tipo/sigla do logradouro. |
| `ruascep` | `ruascep.j29_codigo = ruas.j14_codigo` | CEP do logradouro. |

### Relacionamentos de localização complementar

| Tabela | Ligação | Papel |
|---|---|---|
| `loteloc` | `loteloc.j06_idbql = lote.j34_idbql` | Localização interna/setor local do lote. |
| `setorloc` | `setorloc.j05_codigo = loteloc.j06_setorloc` | Descrição do setor de localização. |
| `loteloteam` | `loteloteam.j34_idbql = lote.j34_idbql` | Vínculo lote-loteamento. |
| `loteam` | `loteam.j34_loteam = loteloteam.j34_loteam` | Loteamento. |

### Relacionamentos com construções

| Tabela | Ligação | Papel |
|---|---|---|
| `iptuconstr` | `iptuconstr.j39_matric = iptubase.j01_matric` | Construções da matrícula/lote. |
| `carconstr` | `carconstr.j48_matric = iptuconstr.j39_matric` e `carconstr.j48_idcons = iptuconstr.j39_idcons` | Características da construção. Usada para identificar área irregular. |
| `caracter` | `caracter.j31_codigo = carconstr.j48_caract` | Cadastro de características. |

---

## 5. Métodos relevantes da classe

| Método | Finalidade |
|---|---|
| `atualizacampos($exclusao = false)` | Preenche atributos da classe com valores vindos de `HTTP_POST_VARS`. |
| `incluir($j34_idbql)` | Insere novo lote. Usa sequence quando `j34_idbql` não é informado. |
| `alterar($j34_idbql = null)` | Atualiza lote existente por `j34_idbql`. |
| `excluir($j34_idbql = null, $dbwhere = null)` | Exclui lote por chave ou condição dinâmica. |
| `sql_record($sql)` | Executa SQL e atualiza contador `numrows`. |
| `sql_query(...)` | Consulta `lote` com `bairro`, `setor` e `zonas`. |
| `sql_query_file(...)` | Consulta somente a tabela `lote`. |
| `sql_query_refant(...)` | Consulta referência anterior do imóvel com matrícula, CGM, construção principal, testada e localização. |
| `sql_query_loteloc(...)` | Consulta lote com localização (`loteloc`, `setorloc`). |
| `sql_query_loteloc_cartao_numerico(...)` | Consulta lote, matrícula, CGM, endereço e localização para cartão numérico. |
| `sql_query_lote($iCodigoLote)` | Consulta detalhada do lote, endereço, CEP, testada e loteamento. |
| `sql_queryGeodados()` | Lista lotes ativos com dados mínimos para georreferenciamento. |
| `sql_query_dados_lote(...)` | Consulta dados completos do lote com matrícula, proprietário, construção principal, testada e referências anteriores. |
| `sql_query_construcoesLote($lote, $codigosAreaIrregular = [])` | Lista construções ativas de um lote e marca se são regulares conforme características informadas. |

---

## 6. SQLs prontos

### 6.1. Buscar lote por código com bairro, setor e zona

```sql
SELECT
  lote.*,
  bairro.j13_descr AS bairro_descricao,
  setor.j30_descr  AS setor_descricao,
  zonas.*
FROM lote
INNER JOIN bairro ON bairro.j13_codi = lote.j34_bairro
INNER JOIN setor  ON setor.j30_codi  = lote.j34_setor
INNER JOIN zonas  ON zonas.j50_zona  = lote.j34_zona
WHERE lote.j34_idbql = :idbql;
```

### 6.2. Buscar somente dados da tabela `lote`

```sql
SELECT *
FROM lote
WHERE lote.j34_idbql = :idbql;
```

### 6.3. Buscar lotes por setor, quadra e lote

```sql
SELECT *
FROM lote
WHERE j34_setor  = :setor
  AND j34_quadra = :quadra
  AND j34_lote   = :lote;
```

### 6.4. Buscar lote com matrícula e proprietário

```sql
SELECT
  lote.*,
  iptubase.j01_matric,
  iptubase.j01_numcgm,
  cgm.z01_nome
FROM lote
INNER JOIN iptubase ON iptubase.j01_idbql = lote.j34_idbql
INNER JOIN cgm      ON cgm.z01_numcgm     = iptubase.j01_numcgm
WHERE lote.j34_idbql = :idbql;
```

### 6.5. Buscar dados de referência anterior do lote

```sql
SELECT
  lote.*,
  iptubase.j01_matric,
  cgm.z01_nome,
  iptuconstr.j39_idcons,
  iptuconstr.j39_area,
  ruas.j14_nome,
  iptuant.*,
  loteloc.*
FROM lote
INNER JOIN iptubase        ON iptubase.j01_idbql  = lote.j34_idbql
INNER JOIN cgm             ON cgm.z01_numcgm      = iptubase.j01_numcgm
LEFT JOIN iptuconstr       ON iptuconstr.j39_matric = iptubase.j01_matric
                           AND iptuconstr.j39_idprinc IS TRUE
LEFT JOIN testpri          ON testpri.j49_idbql   = iptubase.j01_idbql
LEFT JOIN ruas             ON ruas.j14_codigo     = testpri.j49_codigo
LEFT JOIN iptuant          ON iptuant.j40_matric  = iptubase.j01_matric
LEFT JOIN loteloc          ON loteloc.j06_idbql   = lote.j34_idbql
WHERE lote.j34_idbql = :idbql;
```

### 6.6. Buscar lote com localização complementar

```sql
SELECT
  lote.*,
  bairro.j13_descr,
  setor.j30_descr,
  zonas.*,
  loteloc.*,
  setorloc.*
FROM lote
INNER JOIN bairro   ON bairro.j13_codi    = lote.j34_bairro
INNER JOIN setor    ON setor.j30_codi     = lote.j34_setor
INNER JOIN zonas    ON zonas.j50_zona     = lote.j34_zona
LEFT JOIN loteloc   ON loteloc.j06_idbql  = lote.j34_idbql
LEFT JOIN setorloc  ON setorloc.j05_codigo = loteloc.j06_setorloc
WHERE lote.j34_idbql = :idbql;
```

### 6.7. Buscar lote para cartão numérico

```sql
SELECT
  lote.*,
  iptubase.j01_matric,
  cgm.z01_nome,
  bairro.j13_descr,
  setor.j30_descr,
  ruas.j14_nome,
  loteloc.*,
  setorloc.*
FROM lote
INNER JOIN iptubase ON iptubase.j01_idbql = lote.j34_idbql
INNER JOIN cgm      ON cgm.z01_numcgm     = iptubase.j01_numcgm
INNER JOIN bairro   ON bairro.j13_codi    = lote.j34_bairro
INNER JOIN setor    ON setor.j30_codi     = lote.j34_setor
INNER JOIN zonas    ON zonas.j50_zona     = lote.j34_zona
LEFT JOIN testpri   ON testpri.j49_idbql  = lote.j34_idbql
LEFT JOIN ruas      ON ruas.j14_codigo    = testpri.j49_codigo
LEFT JOIN loteloc   ON loteloc.j06_idbql  = lote.j34_idbql
LEFT JOIN setorloc  ON setorloc.j05_codigo = loteloc.j06_setorloc
WHERE lote.j34_idbql = :idbql;
```

### 6.8. Buscar lote detalhado com testada, rua, CEP e loteamento

```sql
SELECT
  lote.j34_setor,
  setor.j30_descr,
  lote.j34_quadra,
  lote.j34_lote,
  lote.j34_area,
  lote.j34_bairro,
  bairro.j13_descr,
  lote.j34_areal,
  lote.j34_totcon,
  lote.j34_zona,
  lote.j34_quamat,
  lote.j34_areapreservada,
  lote.j34_areaprivativa,
  lote.j34_areausocomum,
  lote.j34_zonadesurb,
  lote.j34_idbql,
  ruas.j14_codigo,
  ruas.j14_nome,
  ruascep.j29_cep,
  testada.j36_testad,
  loteam.j34_loteam,
  loteam.j34_descr,
  ruastipo.j88_codigo,
  ruastipo.j88_sigla
FROM lote
INNER JOIN setor         ON setor.j30_codi          = lote.j34_setor
INNER JOIN bairro        ON bairro.j13_codi         = lote.j34_bairro
INNER JOIN testada       ON testada.j36_idbql       = lote.j34_idbql
INNER JOIN testpri       ON testpri.j49_idbql       = testada.j36_idbql
                         AND testpri.j49_face       = testada.j36_face
LEFT JOIN testadanumero  ON testadanumero.j15_idbql = testpri.j49_idbql
INNER JOIN ruas          ON ruas.j14_codigo         = testpri.j49_codigo
LEFT JOIN ruastipo       ON ruastipo.j88_codigo     = ruas.j14_tipo
LEFT JOIN ruascep        ON ruascep.j29_codigo      = ruas.j14_codigo
LEFT JOIN loteloteam     ON loteloteam.j34_idbql    = lote.j34_idbql
LEFT JOIN loteam         ON loteam.j34_loteam       = loteloteam.j34_loteam
WHERE lote.j34_idbql = :idbql;
```

### 6.9. Listar lotes ativos com dados para georreferenciamento

```sql
SELECT DISTINCT j01_idbql
FROM iptubase
INNER JOIN lote    ON lote.j34_idbql   = iptubase.j01_idbql
INNER JOIN bairro  ON lote.j34_bairro  = bairro.j13_codi
INNER JOIN testada ON testada.j36_idbql = lote.j34_idbql
INNER JOIN testpri ON testpri.j49_idbql = testada.j36_idbql
                  AND testpri.j49_face  = testada.j36_face
INNER JOIN ruas    ON ruas.j14_codigo   = testpri.j49_codigo
WHERE iptubase.j01_baixa IS NULL;
```

### 6.10. Buscar dados completos do lote

```sql
SELECT
  lote.*,
  iptubase.j01_matric,
  iptubase.j01_numcgm,
  cgm.z01_nome,
  iptuconstr.j39_idcons,
  iptuconstr.j39_area,
  ruas.j14_nome,
  iptuant.*,
  loteloc.*,
  testada.*,
  testadanumero.*
FROM lote
INNER JOIN iptubase           ON iptubase.j01_idbql  = lote.j34_idbql
INNER JOIN cgm                ON cgm.z01_numcgm      = iptubase.j01_numcgm
LEFT JOIN iptuconstr          ON iptuconstr.j39_matric = iptubase.j01_matric
                              AND iptuconstr.j39_idprinc IS TRUE
LEFT JOIN testpri             ON testpri.j49_idbql   = iptubase.j01_idbql
LEFT JOIN ruas                ON ruas.j14_codigo     = testpri.j49_codigo
LEFT JOIN iptuant             ON iptuant.j40_matric  = iptubase.j01_matric
LEFT JOIN loteloc             ON loteloc.j06_idbql   = lote.j34_idbql
LEFT JOIN testada             ON testada.j36_idbql   = lote.j34_idbql
LEFT JOIN testadanumero       ON testadanumero.j15_idbql = testpri.j49_idbql
                              AND testadanumero.j15_face = testpri.j49_face
WHERE lote.j34_idbql = :idbql;
```

### 6.11. Listar construções ativas de um lote

```sql
SELECT
  iptubase.j01_matric,
  iptuconstr.*
FROM lote
INNER JOIN iptubase    ON iptubase.j01_idbql = lote.j34_idbql
INNER JOIN iptuconstr  ON iptuconstr.j39_matric = iptubase.j01_matric
WHERE iptubase.j01_baixa IS NULL
  AND iptuconstr.j39_dtdemo IS NULL
  AND lote.j34_idbql = :idbql;
```

### 6.12. Listar construções ativas de um lote marcando área irregular

Use quando houver uma lista de códigos de características consideradas irregulares.

```sql
SELECT
  (
    (
      SELECT COUNT(carconstr.j48_caract)
      FROM carconstr
      INNER JOIN caracter ON caracter.j31_codigo = carconstr.j48_caract
      WHERE carconstr.j48_idcons = iptuconstr.j39_idcons
        AND carconstr.j48_matric = iptuconstr.j39_matric
        AND carconstr.j48_caract IN (:codigos_caracteristicas)
    ) = 0
  ) AS regular,
  iptubase.j01_matric,
  iptuconstr.*
FROM lote
INNER JOIN iptubase   ON iptubase.j01_idbql = lote.j34_idbql
INNER JOIN iptuconstr ON iptuconstr.j39_matric = iptubase.j01_matric
WHERE iptubase.j01_baixa IS NULL
  AND iptuconstr.j39_dtdemo IS NULL
  AND lote.j34_idbql = :idbql;
```

---

## 7. Convenção de prefixos

| Prefixo | Tabela/Contexto |
|---|---|
| `j34_` | `lote` |
| `j01_` | `iptubase` |
| `z01_` | `cgm` |
| `j13_` | `bairro` |
| `j30_` | `setor` |
| `j50_` | `zonas` |
| `j36_` | `testada` |
| `j49_` | `testpri` |
| `j14_` | `ruas` |
| `j88_` | `ruastipo` |
| `j29_` | `ruascep` |
| `j06_` | `loteloc` |
| `j05_` | `setorloc` |
| `j39_` | `iptuconstr` |
| `j48_` | `carconstr` |
| `j31_` | `caracter` |
| `j40_` | `iptuant` |

---

## 8. Perguntas que esta classe ajuda a responder

- Qual é o setor, quadra e lote de um `idbql`?
- Qual bairro e zona fiscal pertencem a um lote?
- Qual é a área oficial, área medida, área privativa, área comum e área preservada do lote?
- Quais matrículas estão vinculadas a um lote?
- Quem é o proprietário principal da matrícula vinculada ao lote?
- Qual é o endereço/testada principal do lote?
- Qual é o CEP e tipo de logradouro associado ao lote?
- O lote possui loteamento vinculado?
- Quais construções ativas existem no lote?
- Quais lotes ativos têm dados mínimos para georreferenciamento?

---

## 9. Filtros seguros e recomendados

Use preferencialmente filtros por:

| Filtro | Uso recomendado |
|---|---|
| `lote.j34_idbql = :idbql` | Busca direta por lote. |
| `j34_setor = :setor` | Busca por setor. |
| `j34_setor = :setor AND j34_quadra = :quadra` | Busca por quadra dentro do setor. |
| `j34_setor = :setor AND j34_quadra = :quadra AND j34_lote = :lote` | Busca precisa por inscrição territorial. |
| `iptubase.j01_baixa IS NULL` | Apenas matrículas ativas. |
| `iptuconstr.j39_dtdemo IS NULL` | Apenas construções não demolidas. |

---

## 10. Cuidados e riscos

1. A classe monta SQL por concatenação de strings. Em uso moderno, parâmetros devem ser tratados com prepared statements ou sanitização rigorosa.
2. O campo `j34_idbql` pode ser informado manualmente, mas a classe valida contra a sequence e pode bloquear valores superiores ao último número.
3. `j34_setor`, `j34_quadra` e `j34_lote` são campos `char(4)`. Comparações podem exigir atenção com zeros à esquerda e espaços.
4. `j34_zonadesurb` recebe `NULL` quando não informado, mas na alteração a classe pode gravar como string dependendo do fluxo. Validar comportamento no banco antes de automações.
5. Algumas consultas com testada usam `INNER JOIN`, o que pode ocultar lotes sem testada cadastrada.
6. Em consultas de lote com matrícula, pode haver mais de uma matrícula para o mesmo `j34_idbql`.
7. Para cálculos e relatórios de área construída, considere sempre filtrar `iptuconstr.j39_dtdemo IS NULL` quando o objetivo for construção ativa.
