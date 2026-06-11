# e-Cidade — Cadastro Imobiliário 

## Resumo

- Classe analisada: `cl_iptubase`
- Tabela principal: `iptubase`
- Domínio funcional: Cadastro Imobiliário
- Foco da classe: manutenção cadastral de matrículas imobiliárias, vínculos com lote, proprietário, endereço, construção, registro imobiliário e consultas auxiliares para localização e titularidade.
- Operações principais: consultas SQL.

---

## Tabela Principal: `iptubase`

Cadastro de matrículas de imóveis no IPTU. Cada registro representa uma matrícula imobiliária. A matrícula (`j01_matric`) é a chave principal para vincular lote, proprietário, construções, cálculo, endereço de entrega, baixas e dados de registro imobiliário.

| Coluna | Tipo | Descrição |
|---|---:|---|
| `j01_matric` | int4 | **PK** — Matrícula do imóvel |
| `j01_numcgm` | int4 | **FK lógica** → `cgm.z01_numcgm` — CGM do contribuinte/proprietário principal |
| `j01_idbql` | int4 | **FK lógica** → `lote.j34_idbql` — lote vinculado à matrícula |
| `j01_baixa` | date | Data de baixa da matrícula. `NULL` indica matrícula ativa |
| `j01_codave` | int4 | Código da averbação |
| `j01_fracao` | float8 | Fração ideal da matrícula |
| `j01_tipoproprietario` | int4 | Tipo do proprietário. Relaciona com `tipoproprietario.j163_tipoproprietario` |
| `j01_tipoimovel` | int4 | Tipo de imóvel |
| `j01_distrito` | char(4) | Distrito |
| `j01_hectare` | float8 | Área em hectares para imóvel rural |
| `j01_situcad` | varchar(50) | Situação cadastral |
| `j01_datacad` | date | Data de cadastro |
| `j01_processo` | int4 | Processo relacionado |
| `j01_incra` | int4 | Inscrição INCRA |
| `j01_descrlocal` | varchar(255) | Descrição da localização |
| `j01_unidade` | int8 | Unidade. Default usado pela classe: `1` |
| `j01_areaprivativa` | float8 | Área privativa do lote |
| `j01_fracaoproprietario` | float8 | Fração por proprietário. Default usado pela classe: `100` |

**Sequence:** `iptubase_j01_matric_seq`

Usada na inclusão quando `j01_matric` não é informado. A classe chama `nextval('iptubase_j01_matric_seq')`.

---

## Regras operacionais

## Tabelas Relacionadas

### Pessoas / Entidades

| Tabela | Chave principal / campo | Relação com `iptubase` | Descrição |
|---|---|---|---|
| `cgm` / `protocolo.cgm` | `z01_numcgm` | `j01_numcgm = z01_numcgm` | Cadastro Geral do Município; proprietário principal |
| `propri` | `j42_matric`, `j42_numcgm` | `j42_matric = j01_matric` | Outros proprietários / coproprietários |
| `promitente` | `j41_matric`, `j41_numcgm` | `j41_matric = j01_matric` | Promitentes compradores |
| `imobil` | `j44_matric`, `j44_numcgm` | `j44_matric = j01_matric` | Imobiliárias vinculadas à matrícula |
| `tipoproprietario` | `j163_tipoproprietario` | `j163_tipoproprietario = j01_tipoproprietario` | Tipo do proprietário |
| `tipopromitente` | `j164_promitipo` | `j164_promitipo = j41_promitipo` | Tipo do promitente |
| `tipoproprietariopromitente` | variável | usado em consultas de tipo | Vínculo entre tipos de proprietário e promitente |

### Localização / Lote

| Tabela | Chave principal / campo | Relação | Descrição |
|---|---|---|---|
| `lote` | `j34_idbql` | `j34_idbql = j01_idbql` | Lote/terreno vinculado à matrícula |
| `bairro` | `j13_codi` | `j13_codi = lote.j34_bairro` | Bairro do lote |
| `setor` | `j30_codi` | `j30_codi = lote.j34_setor` | Setor cadastral/fiscal |
| `zonas` | `j50_zona` | `j50_zona = lote.j34_zona` | Zona de valor |
| `testpri` | `j49_idbql`, `j49_face` | `j49_idbql = j01_idbql` | Testada principal do lote |
| `testada` | `j36_idbql`, `j36_face` | `j36_idbql = j49_idbql` e `j36_face = j49_face` | Testadas do lote |
| `testadanumero` | `j15_idbql`, `j15_face` | `j15_idbql = j36_idbql` e `j15_face = j36_face` | Numeração predial pela testada |
| `face` | `j37_face` | `j37_face = j36_face` | Face de quadra |
| `ruas` | `j14_codigo` | `j14_codigo = j49_codigo` | Logradouro |
| `ruastipo` | `j88_codigo` | `j88_codigo = ruas.j14_tipo` | Tipo do logradouro |
| `loteloc` | `j06_idbql` | `j06_idbql = j01_idbql` | Localização alternativa |
| `setorloc` | `j05_codigo` | `j05_codigo = loteloc.j06_setorloc` | Setor de localização |
| `lotesetorfiscal` | `j91_idbql` | `j91_idbql = j01_idbql` | Setor fiscal do lote |
| `setorfiscal` | `j90_codigo` | `j90_codigo = j91_codigo` | Setores fiscais |
| `loteloteam` / `loteam` | `j34_idbql`, `j34_loteam` | via lote | Loteamentos |

### Construções / Edificações

| Tabela | Chave principal / campo | Relação | Descrição |
|---|---|---|---|
| `iptuconstr` | `j39_matric`, `j39_idcons` | `j39_matric = j01_matric` | Construções/edificações da matrícula |
| `iptuant` | `j40_matric` | `j40_matric = j01_matric` | Dados anteriores / referência anterior |
| `carconstr` | `j48_matric`, `j48_idcons`, `j48_caract` | via `iptuconstr` | Características da construção |
| `caracter` | `j31_codigo` | `j31_codigo = j48_caract` | Descrição das características |
| `iptubasecondominio` | `j108_matric` | `j108_matric = j01_matric` | Vínculo da matrícula com condomínio |
| `condominio` | `j107_sequencial` | `j107_sequencial = j108_condominio` | Condomínios |
| `iptubasepredio` | `j109_matric` | `j109_matric = j01_matric` | Vínculo da matrícula com prédio |
| `predio` | `j111_sequencial` | `j111_sequencial = j109_predio` | Prédios |

### Registro de Imóveis / Baixa / Endereço

| Tabela | Chave principal / campo | Relação | Descrição |
|---|---|---|---|
| `iptubaseregimovel` | `j04_matric` | `j04_matric = j01_matric` | Dados de registro imobiliário/cartório |
| `setorregimovel` | `j69_sequencial` | `j69_sequencial = j04_setorregimovel` | Setor no registro de imóveis |
| `iptubaixa` | `j02_matric` | `j02_matric = j01_matric` | Baixas da matrícula |
| `iptuender` | `j43_matric` | `j43_matric = j01_matric` | Endereço de entrega/carnê |

### Cálculo IPTU / Arrecadação

| Tabela | Chave principal / campo | Relação | Descrição |
|---|---|---|---|
| `iptucalc` | `j23_anousu`, `j23_matric` | `j23_matric = j01_matric` | Cálculo principal do IPTU por exercício |
| `iptucale` | `j22_anousu`, `j22_matric`, `j22_idcons` | `j22_matric = j01_matric` | Cálculo por edificação |
| `iptucalv` | `j21_anousu`, `j21_matric` | `j21_matric = j01_matric` | Valores calculados por matrícula |
| `iptunump` | `j20_anousu`, `j20_matric` | `j20_matric = j01_matric` | Número de débito/numpre relacionado ao cálculo |
| `cfiptu` | `j18_anousu` | ano da sessão | Configuração anual do IPTU |

### Histórico / Observações

| Tabela | Relação | Descrição |
|---|---|---|
| `histocorrenciamatric` | `ar25_matric = j01_matric` | Ocorrências da matrícula |
| `histocorrencia` | `ar23_sequencial = ar25_histocorrencia` | Descrição da ocorrência |

### Views / fontes auxiliares

| View / Fonte | Uso |
|---|---|
| `proprietario` | Consolida proprietário, imóvel, lote, endereço e construção |
| `proprietario_ender` | Endereço completo do proprietário/matrícula |
| `fc_iptu_fracionalote(matric, anousu, ...)` | Função usada para calcular fração/área proporcional do lote |

---

## Métodos relevantes da classe

| Método | Finalidade |
|---|---|
| `atualizacampos()` | Carrega atributos a partir de `HTTP_POST_VARS` |
| `incluir($j01_matric)` | Insere matrícula em `iptubase` |
| `alterar($j01_matric)` | Atualiza matrícula em `iptubase` |
| `excluir($j01_matric, $dbwhere)` | Exclui matrícula(s) |
| `sql_record($sql)` | Executa consulta e controla erros/numrows |
| `sql_query()` | Consulta completa de `iptubase` com lote, CGM, bairro, setor, zonas e tipo proprietário |
| `sql_query_file()` | Consulta direta em `iptubase` |
| `sql_query_regmovel()` | Consulta ampla com dados de lote, testada, construção, registro e baixa |
| `proprietario_query()` | Consulta na view `proprietario` |
| `sqlmatriculas_setor()` | Busca matrículas por setor |
| `sqlmatriculas_ruas()` | Busca matrículas por rua/número/tipo |
| `sqlmatriculas_nome()` | Busca matrículas por CGM, incluindo proprietário, coproprietário e promitente |
| `sqlmatriculas_nome_numero()` | Busca por CGM com regras distintas de titularidade |
| `sqlmatriculas_imobiliaria()` | Busca matrículas por imobiliária |
| `sqlmatriculas_bairros()` | Busca matrículas por bairro |
| `sqlmatriculas_IDBQL()` | Busca matrícula por lote (`j01_idbql`) |
| `sqlmatriculas_setorQuadra()` | Busca por setor e quadra |
| `sql_query_constr()` | Consulta matrícula com construções |
| `sql_query_enderecoEntrega()` | Consulta endereço de entrega da matrícula |
| `sql_query_area_total()` | Soma área de lotes ativos por setor/quadra/lote |
| `sql_query_area_contruida()` | Soma área construída ativa por matrícula |
| `sql_query_imobiliaria()` | Consulta imobiliária vinculada à matrícula |
| `sql_query_setorfiscal()` | Consulta setor fiscal da matrícula |
| `sql_query_proprietariolote()` | Consulta detalhada de proprietário/lote |
| `sql_query_promitentes()` | Lista promitentes da matrícula |
| `sql_query_proprietarios()` | Lista proprietário principal e, opcionalmente, coproprietários |
| `sql_query_construcoes()` | Consulta construções da matrícula |
| `sql_queryCalculoMatricula()` | Consulta cálculo IPTU da matrícula/ano |
| `consultaDebitosMatricula()` | Consulta débitos relacionados à matrícula |
| `findBydId()` | Busca direta por matrícula |
| `sql_query_area_contruida_lote()` | Soma área construída ativa por lote |
| `sql_query_tipos_promitentes()` | Consulta tipos de promitente da matrícula |
| `sql_query_envolvidos_matricula()` | Consolida proprietário, coproprietários e promitentes |
| `sql_query_buscaOcorrenciasMatricula()` | Busca ocorrências da matrícula |
| `sql_query_informacoesImovel()` | Consulta consolidada de dados do imóvel |
| `sql_query_buscaConstrucoesMatricula()` | Busca construções por matrícula/ano |
| `sql_query_construcoesMatricula()` | Consulta construções da matrícula e permite filtrar códigos de área irregular |

---

## Queries SQL prontas

### 1. Busca completa por matrícula

```sql
SELECT :campos
FROM iptubase
INNER JOIN lote
        ON lote.j34_idbql = iptubase.j01_idbql
INNER JOIN cgm
        ON cgm.z01_numcgm = iptubase.j01_numcgm
INNER JOIN bairro
        ON bairro.j13_codi = lote.j34_bairro
INNER JOIN setor
        ON setor.j30_codi = lote.j34_setor
INNER JOIN zonas
        ON zonas.j50_zona = lote.j34_zona
INNER JOIN tipoproprietario
        ON tipoproprietario.j163_tipoproprietario = iptubase.j01_tipoproprietario
WHERE iptubase.j01_matric = :matricula;
```

### 2. Busca simples na tabela principal

```sql
SELECT :campos
FROM iptubase
WHERE iptubase.j01_matric = :matricula;
```

### 3. Busca ampla com registro imobiliário, testada, construção e baixa

```sql
SELECT :campos
FROM iptubase
INNER JOIN lote
        ON lote.j34_idbql = iptubase.j01_idbql
INNER JOIN cgm
        ON cgm.z01_numcgm = iptubase.j01_numcgm
LEFT JOIN testpri
       ON testpri.j49_idbql = iptubase.j01_idbql
LEFT JOIN testada
       ON testada.j36_idbql = testpri.j49_idbql
      AND testada.j36_face = testpri.j49_face
      AND testada.j36_codigo = testpri.j49_codigo
LEFT JOIN testadanumero
       ON testadanumero.j15_idbql = testada.j36_idbql
      AND testadanumero.j15_face = testada.j36_face
LEFT JOIN face
       ON face.j37_face = testada.j36_face
LEFT JOIN ruas
       ON ruas.j14_codigo = testpri.j49_codigo
LEFT JOIN iptuconstr
       ON iptuconstr.j39_matric = iptubase.j01_matric
LEFT JOIN iptuant
       ON iptuant.j40_matric = iptubase.j01_matric
LEFT JOIN iptubaseregimovel
       ON iptubaseregimovel.j04_matric = iptubase.j01_matric
LEFT JOIN setorregimovel
       ON setorregimovel.j69_sequencial = iptubaseregimovel.j04_setorregimovel
LEFT JOIN loteloc
       ON loteloc.j06_idbql = iptubase.j01_idbql
LEFT JOIN setorloc
       ON setorloc.j05_codigo = loteloc.j06_setorloc
LEFT JOIN iptubaixa
       ON iptubaixa.j02_matric = iptubase.j01_matric
LEFT JOIN lotesetorfiscal
       ON lotesetorfiscal.j91_idbql = iptubase.j01_idbql
LEFT JOIN setorfiscal
       ON setorfiscal.j90_codigo = lotesetorfiscal.j91_codigo
WHERE iptubase.j01_matric = :matricula;
```

### 4. Busca por CGM — proprietário principal, coproprietário e promitente

```sql
SELECT DISTINCT dados.*
FROM (
    SELECT
        j01_matric,
        'PROPRIETARIO'::varchar(12) AS proprietario,
        j01_idbql,
        cgm.z01_nome,
        j01_baixa
    FROM iptubase
    INNER JOIN cgm ON j01_numcgm = z01_numcgm
    WHERE j01_numcgm = :numcgm

    UNION

    SELECT
        j01_matric,
        'OUTRO PROPR'::varchar(12) AS proprietario,
        j01_idbql,
        cgm.z01_nome,
        j01_baixa
    FROM propri
    INNER JOIN iptubase ON j42_matric = j01_matric
    INNER JOIN cgm ON j42_numcgm = z01_numcgm
    WHERE j42_numcgm = :numcgm

    UNION

    SELECT
        j01_matric,
        'PROMITENTE'::varchar(12) AS proprietario,
        j01_idbql,
        cgm.z01_nome,
        j01_baixa
    FROM promitente
    INNER JOIN iptubase ON j41_matric = j01_matric
    INNER JOIN cgm ON j41_numcgm = z01_numcgm
    WHERE j41_numcgm = :numcgm
) AS dados
INNER JOIN lote ON j34_idbql = j01_idbql
LEFT JOIN testpri ON j49_idbql = j01_idbql
LEFT JOIN ruas ON j49_codigo = j14_codigo
LEFT JOIN ruastipo ON j88_codigo = j14_tipo
LEFT JOIN bairro ON j34_bairro = j13_codi;
```

### 5. Busca por imobiliária

```sql
SELECT DISTINCT *
FROM (
    SELECT
        j01_matric,
        c.z01_nome AS proprietario,
        j01_idbql,
        cgm.z01_nome
    FROM imobil
    INNER JOIN iptubase ON j44_matric = j01_matric
    INNER JOIN cgm ON j01_numcgm = cgm.z01_numcgm
    INNER JOIN cgm c ON j44_numcgm = c.z01_numcgm
    WHERE j44_numcgm = :numcgm_imobiliaria
) AS dados
INNER JOIN lote ON j34_idbql = j01_idbql
LEFT JOIN testpri ON j49_idbql = j01_idbql
LEFT JOIN ruas ON j49_codigo = j14_codigo
LEFT JOIN bairro ON j34_bairro = j13_codi;
```

### 6. Busca por setor

```sql
SELECT
    lote.j34_idbql AS db_lote,
    j34_setor,
    j34_quadra,
    j34_lote,
    j34_area,
    j34_areal,
    j01_matric,
    ruas.j14_nome,
    bairro.j13_descr
FROM lote
INNER JOIN bairro ON j13_codi = j34_bairro
INNER JOIN iptubase ON j01_idbql = j34_idbql
LEFT JOIN testpri ON j34_idbql = j49_idbql
LEFT JOIN ruas ON j14_codigo = j49_codigo
WHERE j34_setor = :setor;
```

### 7. Busca por setor e quadra

```sql
SELECT
    lote.j34_idbql AS db_lote,
    j34_setor,
    j34_quadra,
    j34_lote,
    j34_area,
    j34_areal,
    j01_matric,
    ruas.j14_nome,
    bairro.j13_descr
FROM lote
INNER JOIN bairro ON j13_codi = j34_bairro
INNER JOIN iptubase ON j01_idbql = j34_idbql
LEFT JOIN testpri ON j34_idbql = j49_idbql
LEFT JOIN ruas ON j14_codigo = j49_codigo
WHERE j34_setor = :setor
  AND j34_quadra = :quadra;
```

### 8. Busca por bairro

```sql
SELECT
    iptubase.j01_matric,
    cgm.z01_nome,
    cgm.z01_ender,
    cgm.z01_munic,
    cgm.z01_cep,
    cgm.z01_uf,
    lote.*
FROM lote
INNER JOIN iptubase ON j34_idbql = j01_idbql
INNER JOIN cgm ON z01_numcgm = j01_numcgm
WHERE j34_bairro = :bairro;
```

### 9. Área total de lotes ativos por setor/quadra/lote

```sql
SELECT COALESCE(SUM(j34_area), 0) AS area_total
FROM (
    SELECT DISTINCT j34_idbql, j34_area
    FROM lote
    INNER JOIN iptubase ON j01_idbql = j34_idbql
    WHERE j34_setor = :setor
      AND j34_quadra = :quadra
      AND j34_lote = :lote
      AND j01_baixa IS NULL
) AS x;
```

### 10. Área construída ativa por matrícula

```sql
SELECT COALESCE(SUM(j39_area), 0) AS area_construida
FROM iptuconstr
INNER JOIN iptubase ON j01_matric = j39_matric
WHERE j39_matric = :matricula
  AND j39_dtdemo IS NULL
  AND j01_baixa IS NULL;
```

### 11. Endereço de entrega por proprietário ou filtro customizado

```sql
SELECT :campos
FROM iptubase
LEFT JOIN iptuender ON j43_matric = j01_matric
WHERE j01_numcgm = :numcgm;
```

### 12. Promitentes da matrícula

```sql
SELECT
    j41_numcgm,
    z01_nome,
    j41_tipopro AS principal,
    j41_promitipo
FROM promitente
INNER JOIN cgm ON z01_numcgm = j41_numcgm
WHERE j41_matric = :matricula;
```

### 13. Proprietário principal e coproprietários

```sql
SELECT
    j01_numcgm,
    z01_nome,
    TRUE AS principal
FROM iptubase
INNER JOIN cgm ON z01_numcgm = j01_numcgm
WHERE j01_matric = :matricula

UNION

SELECT
    j42_numcgm AS j01_numcgm,
    z01_nome,
    FALSE AS principal
FROM propri
INNER JOIN cgm ON z01_numcgm = j42_numcgm
WHERE j42_matric = :matricula;
```

### 14. Cálculo IPTU por matrícula e exercício

```sql
SELECT
    *
FROM iptucalc
INNER JOIN iptubase ON j01_matric = j23_matric
WHERE j23_matric = :matricula
  AND j23_anousu = :ano;
```

### 15. Ocorrências da matrícula

```sql
SELECT
    ar23_ocorrencia
FROM histocorrenciamatric
INNER JOIN histocorrencia
        ON histocorrencia.ar23_sequencial = histocorrenciamatric.ar25_histocorrencia
WHERE ar25_matric = :matricula
  AND ar23_tipo = 1;
```

---

## Convenção de prefixos observada

| Prefixo | Tabela / fonte provável |
|---|---|
| `j01_` | `iptubase` |
| `j34_` | `lote` |
| `z01_` | `cgm` / `protocolo.cgm` |
| `j13_` | `bairro` |
| `j30_` | `setor` |
| `j50_` | `zonas` |
| `j49_` | `testpri` |
| `j36_` | `testada` |
| `j15_` | `testadanumero` |
| `j37_` | `face` |
| `j14_` | `ruas` |
| `j88_` | `ruastipo` |
| `j39_` | `iptuconstr` |
| `j40_` | `iptuant` |
| `j41_` | `promitente` |
| `j42_` | `propri` |
| `j44_` | `imobil` |
| `j04_` | `iptubaseregimovel` |
| `j69_` | `setorregimovel` |
| `j06_` | `loteloc` |
| `j05_` | `setorloc` |
| `j02_` | `iptubaixa` |
| `j91_` | `lotesetorfiscal` |
| `j90_` | `setorfiscal` |
| `j43_` | `iptuender` |
| `j23_` | `iptucalc` |
| `j22_` | `iptucale` |
| `j21_` | `iptucalv` |
| `j20_` | `iptunump` |
| `j18_` | `cfiptu` |
| `j163_` | `tipoproprietario` |
| `j164_` | `tipopromitente` |

---

## Perguntas que esta classe ajuda a responder

- Qual proprietário principal de uma matrícula?
- Quais coproprietários ou promitentes estão vinculados a uma matrícula?
- Qual lote está vinculado à matrícula?
- A matrícula está ativa ou baixada?
- Qual endereço/logradouro/bairro/setor/quadra/lote de uma matrícula?
- Quais construções existem para a matrícula?
- Qual área total do lote e área construída ativa?
- Quais matrículas pertencem a um CGM?
- Quais matrículas estão associadas a uma imobiliária?
- Quais matrículas existem em um setor, quadra, bairro ou rua?
- Quais dados de registro imobiliário existem para a matrícula?
- Qual cálculo de IPTU foi gerado para matrícula/ano?
- Quais ocorrências estão registradas para a matrícula?

---

## Filtros seguros e recomendados

| Filtro | Campo / expressão | Observação |
|---|---|---|
| Matrícula específica | `j01_matric = :matricula` | Filtro mais seguro para detalhe |
| Matrículas ativas | `j01_baixa IS NULL` | Usado para excluir baixadas |
| Proprietário principal | `j01_numcgm = :numcgm` | Apenas proprietário principal |
| Coproprietário | `propri.j42_numcgm = :numcgm` | Exige join/union com `propri` |
| Promitente | `promitente.j41_numcgm = :numcgm` | Exige join/union com `promitente` |
| Lote | `j01_idbql = :idbql` | Busca por vínculo técnico do lote |
| Setor/quadra/lote | `j34_setor`, `j34_quadra`, `j34_lote` | Requer join com `lote` |
| Construção ativa | `j39_dtdemo IS NULL` | Evita construções demolidas |
| Ano do cálculo | `j23_anousu = :ano` | Requer `iptucalc` |

---

## Cuidados / riscos

- `j01_numcgm` representa o proprietário principal. Para listar todos os envolvidos, é necessário incluir `propri` e `promitente`.
- `j01_baixa IS NULL` deve ser usado quando a análise exigir apenas matrículas ativas.
- Construções devem considerar `j39_dtdemo IS NULL` para evitar incluir construções demolidas.
- A classe usa SQL por concatenação de strings; em uso moderno, substituir variáveis por placeholders parametrizados.
- Nem toda relação aparece como foreign key explícita no código PHP; algumas são relações lógicas inferidas pelos joins.
- `proprietario` e `proprietario_ender` são views/fontes auxiliares e podem carregar regras internas não visíveis nesta classe.
- A consulta por CGM muda conforme a regra aplicada: proprietário principal, coproprietário e promitente podem ou não ser considerados.
- `cfiptu` depende do ano da sessão (`DB_anousu`), portanto consultas de cálculo devem sempre explicitar o exercício quando usadas fora do e-Cidade.