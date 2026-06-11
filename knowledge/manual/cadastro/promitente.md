# e-Cidade — Cadastro Imobiliário 

## Resumo

A tabela `promitente` representa os promitentes vinculados a uma matrícula imobiliária. Em termos de negócio, registra o CGM do promitente, se ele é o responsável, o tipo/abreviação do promitente e a fração associada.

Esta referência foi estruturada para uso por IA e por consultas SQL diretas, sem depender da leitura do PHP original.

## Tabela principal: `promitente`

| Campo | Tipo | Descrição | Observações |
|---|---:|---|---|
| `j41_matric` | `int4` | Matricula | Parte da chave lógica. Referencia `iptubase.j01_matric`. |
| `j41_numcgm` | `int4` | Numcgm | Parte da chave lógica. Referencia `cgm.z01_numcgm`. |
| `j41_tipopro` | `bool` | Responsável | Indica se é responsável/principal (`t`/`f`). |
| `j41_promitipo` | `char(1)` | Abreviação do tipo do promitente | Abreviação textual do tipo; usada no vínculo com `tipopromitente.j164_promitipo`. |
| `j41_tipopromitente` | `int4` | Tipo do promitente | Código numérico do tipo; pode ser `null` quando não informado. |
| `j41_fracao` | `float` | Fração por Promitente | Obrigatória quando `j41_tipopro = 't'`; caso contrário pode ser `null`. |

## Regras extraídas da classe

| Regra | Detalhe |
|---|---|
| Chave lógica | `j41_matric + j41_numcgm`. |
| Inclusão | Recebe `j41_matric` e `j41_numcgm` por parâmetro. |
| Responsável | `j41_tipopro` é obrigatório. |
| Tipo abreviado | `j41_promitipo` é obrigatório. |
| Tipo numérico | `j41_tipopromitente` vira `null` quando vazio. |
| Fração | `j41_fracao` é obrigatória quando o promitente é principal/responsável (`j41_tipopro = 't'`). Se não for principal, pode virar `null`. |
| Exclusão | Pode excluir por `j41_matric + j41_numcgm` ou por `$dbwhere`. |
| Auditoria | Não foi extraída rotina explícita de `db_acount` nesta classe, diferente de outras classes antigas do mesmo módulo. |

## Tabelas relacionadas extraídas dos SQLs

| Tabela | Relação/uso |
|---|---|
| `promitente` | Tabela principal. |
| `tipopromitente` | Relaciona o tipo do promitente por `j41_promitipo = j164_promitipo` ou `j41_tipopromitente = j164_tipopromitente`. |
| `iptubase` | Vínculo da matrícula: `iptubase.j01_matric = promitente.j41_matric`. |
| `cgm` | Vínculo do promitente: `cgm.z01_numcgm = promitente.j41_numcgm`. |
| `lote` | Vínculo via base imobiliária: `lote.j34_idbql = iptubase.j01_idbql`. |
| `cgm as a` | CGM do proprietário/base do imóvel: `a.z01_numcgm = iptubase.j01_numcgm`. |
| `iptuender` | Endereço de entrega do imóvel, por matrícula: `iptuender.j43_matric = iptubase.j01_matric`. |

## Prefixos de campos

| Prefixo | Tabela provável | Contexto |
|---|---|---|
| `j41_` | `promitente` | Dados do promitente. |
| `j01_` | `iptubase` | Cadastro base da matrícula. |
| `j164_` | `tipopromitente` | Tipo de promitente. |
| `z01_` | `cgm` | Cadastro geral municipal. |
| `j34_` | `lote` | Dados físicos do lote. |
| `j43_` | `iptuender` | Endereço de entrega. |

## SQLs normalizados

### Consulta principal com joins

```sql
select
    {campos}
from promitente
inner join tipopromitente
        on promitente.j41_promitipo = tipopromitente.j164_promitipo
        or tipopromitente.j164_tipopromitente = promitente.j41_tipopromitente
inner join iptubase
        on iptubase.j01_matric = promitente.j41_matric
inner join cgm
        on cgm.z01_numcgm = promitente.j41_numcgm
inner join lote
        on lote.j34_idbql = iptubase.j01_idbql
inner join cgm as a
        on a.z01_numcgm = iptubase.j01_numcgm
where promitente.j41_matric = :matricula
  and promitente.j41_numcgm = :numcgm;
```

### Consulta simples da tabela

```sql
select
    *
from promitente
where j41_matric = :matricula
  and j41_numcgm = :numcgm;
```

### Inserção normalizada

```sql
insert into promitente (
    j41_matric,
    j41_numcgm,
    j41_tipopro,
    j41_promitipo,
    j41_tipopromitente,
    j41_fracao
) values (
    :matricula,
    :numcgm,
    :responsavel,
    :promitipo,
    :tipopromitente,
    :fracao
);
```

### Endereço de entrega do promitente

```sql
select
    {campos}
from promitente
inner join iptubase
        on iptubase.j01_matric = promitente.j41_matric
left join iptuender
       on iptuender.j43_matric = iptubase.j01_matric
where promitente.j41_numcgm = :numcgm_promitente;
```

### Atualização normalizada

```sql
update promitente
   set j41_tipopro = :responsavel,
       j41_promitipo = :promitipo,
       j41_tipopromitente = :tipopromitente,
       j41_fracao = :fracao
 where j41_matric = :matricula
   and j41_numcgm = :numcgm;
```

### Exclusão normalizada

```sql
delete from promitente
 where j41_matric = :matricula
   and j41_numcgm = :numcgm;
```

## Métodos relevantes

| Método | Finalidade |
|---|---|
| `cl_promitente()` | Construtor legado; inicializa rótulos da tabela `promitente`. |
| `atualizacampos($exclusao=false)` | Carrega campos do POST/global antigo do e-Cidade. |
| `incluir($j41_matric,$j41_numcgm)` | Insere promitente da matrícula. |
| `alterar($j41_matric=null,$j41_numcgm=null)` | Altera dados do promitente. |
| `excluir($j41_matric=null,$j41_numcgm=null,$dbwhere=null)` | Exclui por chave lógica ou condição livre. |
| `sql_record($sql)` | Executa SQL e guarda `numrows`. |
| `sql_query(...)` | Retorna consulta com joins de tipo, matrícula, CGM e lote. |
| `sql_query_file(...)` | Retorna consulta simples da tabela `promitente`. |
| `sql_query_enderecoEntrega(...)` | Consulta endereço de entrega associado à matrícula do promitente. |

## Perguntas que este schema ajuda a responder

| Pergunta | Campos/tabelas úteis |
|---|---|
| Quem são os promitentes de uma matrícula? | `promitente.j41_matric`, `promitente.j41_numcgm`, `cgm.z01_*`. |
| Qual promitente é responsável? | `j41_tipopro = 't'`. |
| Qual é a fração do promitente principal? | `j41_fracao`, com regra de obrigatoriedade quando `j41_tipopro = 't'`. |
| Qual é o tipo do promitente? | `j41_promitipo`, `j41_tipopromitente`, `tipopromitente`. |
| Qual endereço de entrega está associado? | `promitente`, `iptubase`, `iptuender`. |

## Filtros seguros recomendados

| Cenário | Filtro |
|---|---|
| Buscar promitentes de uma matrícula | `where j41_matric = :matricula` |
| Buscar promitente específico | `where j41_matric = :matricula and j41_numcgm = :numcgm` |
| Buscar responsáveis | `where j41_tipopro = 't'` |
| Buscar por tipo numérico | `where j41_tipopromitente = :tipo` |
| Buscar por abreviação do tipo | `where j41_promitipo = :promitipo` |

## Cuidados de uso

- O campo `j41_fracao` tem regra condicional: é obrigatório quando o registro representa promitente principal/responsável.
- O join com `tipopromitente` usa `OR`; isso pode duplicar registros se as duas condições baterem em linhas diferentes.
- A classe permite `$dbwhere` livre em consultas e exclusões; em uso moderno, preferir parâmetros SQL.
- O construtor usa padrão legado `cl_promitente()` em vez de `__construct()`.
