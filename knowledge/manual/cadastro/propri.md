# e-Cidade — Cadastro Imobiliário

## Tabela principal: `propri`

| Campo | Tipo | Descrição | Observações |
|---|---:|---|---|
| `j42_matric` | `int4` | Matrícula | Parte da chave lógica. Relaciona com `iptubase.j01_matric`. |
| `j42_numcgm` | `int4` | Numcgm | Parte da chave lógica. Relaciona com `cgm.z01_numcgm`. |
| `j42_fracaoproprietario` | `float8` | Fração por proprietário | Valor padrão `0` quando não informado. |
| `j42_arealoteproprietario` | `float8` | Área do lote por proprietário | Valor padrão `0` quando não informado. |
| `j42_tipoproprietario` | `int4` | Tipo de proprietário | Existe no CRUD/auditoria, embora não esteja listado em `$campos`; padrão `0` quando não informado. Relaciona com `tipoproprietario.j163_tipoproprietario`. |

## Chave e identidade

A classe trabalha com chave lógica composta:

```sql
j42_matric + j42_numcgm
```

Não há geração por sequence nesta classe. A inclusão exige que matrícula e CGM sejam recebidos como parâmetros de `incluir($j42_matric, $j42_numcgm)`.

## Tabelas relacionadas

| Tabela/View | Relação | Uso |
|---|---|---|
| `iptubase` | `iptubase.j01_matric = propri.j42_matric` | Matrícula principal do imóvel. |
| `cgm` | `cgm.z01_numcgm = propri.j42_numcgm` | Dados cadastrais do coproprietário. |
| `lote` | `lote.j34_idbql = iptubase.j01_idbql` | Dados do lote da matrícula. |
| `cgm as a` | `a.z01_numcgm = iptubase.j01_numcgm` | CGM do proprietário principal na matrícula base. |
| `iptuender` | `iptuender.j43_matric = iptubase.j01_matric` | Endereço de entrega vinculado à matrícula. |
| `tipoproprietario` | `tipoproprietario.j163_tipoproprietario = propri.j42_tipoproprietario` | Descrição do tipo de proprietário. |

## Métodos relevantes

| Método | Finalidade |
|---|---|
| `incluir($j42_matric, $j42_numcgm)` | Insere coproprietário/outro proprietário na matrícula. |
| `alterar($j42_matric = null, $j42_numcgm = null)` | Atualiza dados do coproprietário. |
| `excluir($j42_matric = null, $j42_numcgm = null, $dbwhere = null)` | Remove vínculo de proprietário. |
| `sql_record($sql)` | Executa SQL e controla estado de erro/quantidade. |
| `sql_query(...)` | Consulta `propri` com joins em `iptubase`, `cgm`, `lote` e CGM principal. |
| `sql_query_file(...)` | Consulta direta na tabela `propri`. |
| `sql_query_enderecoEntrega(...)` | Busca dados de proprietários com possível endereço de entrega. |
| `sql_outrosProprietarios($matricula)` | Lista proprietários da matrícula com descrição do tipo de proprietário. |

## SQLs prontos

### 1. Buscar coproprietário por matrícula e CGM

```sql
select *
  from propri
 where j42_matric = :matricula
   and j42_numcgm = :numcgm;
```

### 2. Buscar todos os coproprietários de uma matrícula

```sql
select propri.*
  from propri
 where j42_matric = :matricula
 order by j42_numcgm;
```

### 3. Buscar coproprietários com dados do CGM

```sql
select
    propri.j42_matric,
    propri.j42_numcgm,
    cgm.z01_nome,
    propri.j42_fracaoproprietario,
    propri.j42_arealoteproprietario,
    propri.j42_tipoproprietario
from propri
inner join cgm
        on cgm.z01_numcgm = propri.j42_numcgm
where propri.j42_matric = :matricula
order by cgm.z01_nome;
```

### 4. Buscar coproprietários com dados da matrícula e lote

```sql
select
    propri.*,
    iptubase.j01_idbql,
    lote.j34_setor,
    lote.j34_quadra,
    lote.j34_lote,
    lote.j34_area,
    cgm.z01_nome as nome_coproprietario,
    a.z01_nome as nome_proprietario_principal
from propri
inner join iptubase
        on iptubase.j01_matric = propri.j42_matric
inner join cgm
        on cgm.z01_numcgm = propri.j42_numcgm
inner join lote
        on lote.j34_idbql = iptubase.j01_idbql
inner join cgm as a
        on a.z01_numcgm = iptubase.j01_numcgm
where propri.j42_matric = :matricula;
```

### 5. Buscar matrículas em que um CGM aparece como coproprietário

```sql
select
    propri.j42_matric,
    propri.j42_numcgm,
    propri.j42_fracaoproprietario,
    propri.j42_arealoteproprietario,
    propri.j42_tipoproprietario
from propri
where propri.j42_numcgm = :numcgm
order by propri.j42_matric;
```

### 6. Buscar endereço de entrega por CGM proprietário

```sql
select
    propri.*,
    iptubase.j01_matric,
    iptubase.j01_idbql,
    iptuender.*
from propri
inner join iptubase
        on iptubase.j01_matric = propri.j42_matric
left join iptuender
       on iptuender.j43_matric = iptubase.j01_matric
where propri.j42_numcgm = :numcgm;
```

### 7. Listar outros proprietários com tipo

```sql
select
    cgm.z01_numcgm,
    cgm.z01_nome,
    propri.j42_tipoproprietario || ' - ' || tipoproprietario.j163_descricao as tipoproprietario
from propri
inner join cgm
        on cgm.z01_numcgm = propri.j42_numcgm
inner join tipoproprietario
        on tipoproprietario.j163_tipoproprietario = propri.j42_tipoproprietario
where propri.j42_matric = :matricula;
```

### 8. Conferir total de fração por matrícula

```sql
select
    j42_matric,
    sum(coalesce(j42_fracaoproprietario, 0)) as total_fracao
from propri
where j42_matric = :matricula
group by j42_matric;
```

### 9. Conferir área proporcional por proprietário contra área do lote

```sql
select
    propri.j42_matric,
    iptubase.j01_idbql,
    lote.j34_area,
    sum(coalesce(propri.j42_arealoteproprietario, 0)) as total_area_proprietarios
from propri
inner join iptubase
        on iptubase.j01_matric = propri.j42_matric
inner join lote
        on lote.j34_idbql = iptubase.j01_idbql
where propri.j42_matric = :matricula
group by
    propri.j42_matric,
    iptubase.j01_idbql,
    lote.j34_area;
```

## Relação com o cadastro imobiliário

A tabela `propri` complementa `iptubase`.

- `iptubase.j01_numcgm` indica o proprietário principal da matrícula.
- `propri.j42_numcgm` indica outros proprietários/coparticipantes da matrícula.
- `propri.j42_fracaoproprietario` permite representar a fração do proprietário.
- `propri.j42_arealoteproprietario` permite representar a área proporcional do lote.
- `propri.j42_tipoproprietario` classifica o tipo de vínculo proprietário.

## Perguntas que esta referência ajuda a responder

- Quais CGMs são coproprietários de uma matrícula?
- Em quais matrículas um CGM aparece como coproprietário?
- Qual a fração de propriedade de cada coproprietário?
- Qual a área do lote atribuída a cada coproprietário?
- Qual o tipo de proprietário vinculado a cada CGM?
- Existe endereço de entrega para matrícula associada ao coproprietário?
- A soma das frações dos coproprietários está coerente?

## Cuidados e riscos

- A classe possui `j42_tipoproprietario` como propriedade e campo persistido, mas o campo não aparece no texto de `$campos`. Para IA/SQL, considerar o campo como existente porque ele é usado no `INSERT`, `UPDATE`, auditoria e consultas.
- O construtor está no padrão antigo `cl_propri()`, não em `__construct()`.
- A exclusão por `dbwhere` aceita SQL livre; usar apenas filtros controlados.
- `sql_query` une duas vezes a tabela `cgm`: uma para o coproprietário (`propri.j42_numcgm`) e outra para o proprietário principal da matrícula (`iptubase.j01_numcgm`).
- `sql_outrosProprietarios` usa sintaxe antiga com tabelas separadas por vírgula; para consultas novas, prefira `JOIN` explícito.
