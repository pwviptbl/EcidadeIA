# e-Cidade — Cadastro Imobiliário — `averba`

A classe pertence ao módulo `cadastro` e representa a entidade `averba`. No contexto do cadastro imobiliário, a tabela registra averbações vinculadas a matrículas imobiliárias, com data, registro de imóvel, cidade e CGM associado.

## 2. Tabela principal: `averba`

Cada registro representa uma averbação associada a uma matrícula do IPTU.

| Coluna | Tipo | Papel | Descrição |
|---|---:|---|---|
| `j55_codave` | `int4` | PK | Código da averbação |
| `j55_matric` | `int4` | FK provável → `iptubase.j01_matric` | Matrícula do imóvel |
| `j55_data` | `date` | Data do evento | Data da averbação |
| `j55_regimo` | `varchar(20)` | Atributo cartorial | Registro de imóvel |
| `j55_cidade` | `varchar(20)` | Atributo cartorial/localidade | Cidade do registro de imóvel |
| `j55_numcgm` | `int4` | FK provável → `cgm.z01_numcgm` | Número do CGM associado à averbação |

## 3. Campos extraídos da propriedade `$campos`

| Campo | Tipo | Rótulo original |
|---|---:|---|
| `j55_codave` | `int4` | Codigo Averbacao |
| `j55_matric` | `int4` | Matricula |
| `j55_data` | `date` | Data |
| `j55_regimo` | `varchar(20)` | Registro Imovel |
| `j55_cidade` | `varchar(20)` | Cidade |
| `j55_numcgm` | `int4` | Número Cgm |


## 6. Relacionamentos extraídos dos SQLs

### 6.1 Relacionamentos diretos

| Tabela | Relação | Uso |
|---|---|---|
| `iptubase` | `iptubase.j01_matric = averba.j55_matric` | Vincula a averbação à matrícula imobiliária |
| `cgm` | `cgm.z01_numcgm = averba.j55_numcgm` | Recupera o CGM associado à averbação |
| `lote` | `lote.j34_idbql = iptubase.j01_idbql` | Recupera o lote da matrícula |
| `cgm as a` | `a.z01_numcgm = iptubase.j01_numcgm` | Recupera o CGM do proprietário principal da matrícula |

### 6.2 Interpretação dos vínculos

- `j55_matric` aponta para a matrícula do imóvel em `iptubase`.
- `j55_numcgm` representa o CGM vinculado à averbação.
- A consulta principal também busca o proprietário atual/principal da matrícula por `iptubase.j01_numcgm`.
- A tabela pode envolver troca ou registro de titularidade, mas a classe isolada não prova a regra completa de alteração de proprietário.

## 7. Operações CRUD

## 8. Consultas SQL extraídas e normalizadas

### 8.1 Consulta completa por averbação

Equivalente ao método `sql_query()`:

```sql
select *
  from averba
       inner join iptubase on iptubase.j01_matric = averba.j55_matric
       inner join cgm on cgm.z01_numcgm = averba.j55_numcgm
       inner join lote on lote.j34_idbql = iptubase.j01_idbql
       inner join cgm as a on a.z01_numcgm = iptubase.j01_numcgm
 where averba.j55_codave = :codave;
```

Uso recomendado: obter dados completos da averbação, matrícula, lote, CGM vinculado à averbação e CGM principal da matrícula.

### 8.2 Consulta direta da tabela

Equivalente ao método `sql_query_file()`:

```sql
select *
  from averba
 where averba.j55_codave = :codave;
```

Uso recomendado: buscar apenas os dados brutos da averbação.

### 8.3 Consulta do nome anterior / CGM associado

Equivalente ao método `sql_query_nomeant()`:

```sql
select *
  from averba
       inner join cgm on cgm.z01_numcgm = averba.j55_numcgm
 where averba.j55_codave = :codave;
```

Uso recomendado: recuperar dados cadastrais do CGM vinculado à averbação.

## 10. Perguntas que esta tabela ajuda a responder

- Quais averbações existem para uma matrícula?
- Qual CGM está associado a uma averbação?
- Em que data uma averbação foi registrada?
- Qual registro de imóvel e cidade estão associados à averbação?
- Quais averbações estão ligadas a determinado CGM?
- Quais averbações ocorreram em determinado período?

## 11. Consultas úteis para análise

### 11.1 Averbações por matrícula

```sql
select *
  from averba
 where j55_matric = :matricula
 order by j55_data, j55_codave;
```

### 11.2 Averbações por CGM

```sql
select *
  from averba
 where j55_numcgm = :numcgm
 order by j55_data, j55_codave;
```

### 11.3 Averbações por período

```sql
select *
  from averba
 where j55_data between :data_inicial and :data_final
 order by j55_data, j55_codave;
```

### 11.4 Averbações com dados da matrícula e proprietário principal

```sql
select
  averba.j55_codave,
  averba.j55_matric,
  averba.j55_data,
  averba.j55_regimo,
  averba.j55_cidade,
  averba.j55_numcgm,
  cgm.z01_nome as nome_cgm_averbacao,
  iptubase.j01_numcgm as numcgm_proprietario_atual,
  proprietario_atual.z01_nome as nome_proprietario_atual,
  lote.j34_idbql
from averba
     inner join iptubase on iptubase.j01_matric = averba.j55_matric
     inner join lote on lote.j34_idbql = iptubase.j01_idbql
     inner join cgm on cgm.z01_numcgm = averba.j55_numcgm
     inner join cgm as proprietario_atual on proprietario_atual.z01_numcgm = iptubase.j01_numcgm
where averba.j55_codave = :codave;
```

## 12. Cuidados e riscos

- A classe usa SQL concatenado diretamente; em uso moderno, converter para placeholders parametrizados.
- `j55_data` é montado manualmente a partir de dia, mês e ano, sem validação forte de data.
- `sql_query()` faz dois joins com `cgm`: um para o CGM da averbação e outro para o CGM do proprietário principal da matrícula.
- O método `sql_query_nomeant()` sugere consulta de “nome anterior”, mas a classe sozinha não comprova que `j55_numcgm` é sempre proprietário anterior; validar com a regra funcional da averbação.
- A alteração permite atualizar a própria chave `j55_codave`, o que pode causar inconsistência se usado sem cuidado.
- A exclusão aceita `dbwhere` livre; risco alto se a condição for montada com entrada externa.

## 13. Resumo para IA

Use `averba` quando a pergunta envolver averbações de matrícula, eventos cartoriais ligados ao imóvel, data de averbação, registro de imóvel, cidade e CGM associado à averbação.

Prefira juntar com:

- `iptubase` para chegar à matrícula/imóvel;
- `lote` para dados territoriais;
- `cgm` para nomes dos envolvidos;
- tabelas do grupo `averbacao`, `averbatipo`, `averbacgm`, quando a pergunta exigir regra moderna/completa de troca de titularidade.

Não inferir apenas por esta classe que houve troca efetiva de proprietário. Ela registra dados de averbação, mas a efetivação da titularidade pode depender de outras tabelas e rotinas.
