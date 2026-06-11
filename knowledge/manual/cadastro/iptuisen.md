# e-Cidade — Cadastro Imobiliário

## Resumo

Esta referência foi extraída da classe PHP `cl_iptuisen`, entidade `iptuisen`, do módulo `cadastro`.

A tabela `iptuisen` registra isenções de IPTU vinculadas a uma matrícula imobiliária. O registro identifica o tipo de isenção, período de vigência, percentual, usuário de inclusão, histórico textual e área de lote usada no contexto da isenção.

## Tabela principal: `iptuisen`

Chave principal operacional: `j46_codigo`.

Sequência usada para geração automática: `iptuisen_j46_codigo_seq`.

| Campo | Tipo | Descrição |
|---|---:|---|
| `j46_codigo` | `int4` | Codigo Isencao |
| `j46_matric` | `int4` | Matrícula |
| `j46_tipo` | `int4` | Tipo Isencao |
| `j46_dtini` | `date` | Data Inicio |
| `j46_dtfim` | `date` | Data Final |
| `j46_perc` | `float8` | Percentual |
| `j46_dtinc` | `date` | Data inclusao |
| `j46_idusu` | `int4` | Codigo do Usuario |
| `j46_hist` | `text` | Historico |
| `j46_arealo` | `float8` | Área do lote M2 |

## Relacionamentos identificados

| Tabela | Relação extraída | Uso |
|---|---|---|
| `iptubase` | `iptubase.j01_matric = iptuisen.j46_matric` | Vincula a isenção à matrícula imobiliária. |
| `tipoisen` | `tipoisen.j45_tipo = iptuisen.j46_tipo` | Descreve o tipo de isenção. |
| `lote` | `lote.j34_idbql = iptubase.j01_idbql` | Permite acesso aos dados físicos do lote. |
| `cgm` | `cgm.z01_numcgm = iptubase.j01_numcgm` | Recupera o CGM do proprietário principal da matrícula. |
| `isentaxa` | `isentaxa.j56_codigo = iptuisen.j46_codigo` | Vincula taxas relacionadas à isenção. |
| `isenexe` | `isenexe.j47_codigo = iptuisen.j46_codigo` | Relaciona isenção a exercício. |
| `proprietario` | `proprietario.j01_matric = iptuisen.j46_matric` | Consulta ampliada do responsável/proprietário. |
| `isenproc` | `isenproc.j61_codigo = iptuisen.j46_codigo` | Processo associado à isenção. |
| `promitente` | `promitente.j41_matric = iptuisen.j46_matric` | Promitente relacionado à matrícula. |
| `iptubasecondominio` | `iptubasecondominio.j108_matric = iptuisen.j46_matric` | Vínculo com condomínio. |
| `condominio` | `condominio.j107_sequencial = iptubasecondominio.j108_condominio` | Dados do condomínio. |

## Prefixos de campos

| Prefixo | Tabela provável | Observação |
|---|---|---|
| `j46` | `iptuisen` | Campos da isenção. |
| `j01` | `iptubase` / visão `proprietario` | Matrícula e proprietário base. |
| `j45` | `tipoisen` | Tipo/descrição da isenção. |
| `j47` | `isenexe` | Exercício da isenção. |
| `j56` | `isentaxa` | Taxas associadas à isenção. |
| `j61` | `isenproc` | Processo da isenção. |
| `j108` | `iptubasecondominio` | Vínculo matrícula-condomínio. |
| `j107` | `condominio` | Cadastro de condomínio. |

## Métodos relevantes

| Método | Finalidade |
|---|---|
| `__construct` | Inicializa rótulos da entidade `iptuisen`. |
| `atualizacampos` | Preenche propriedades a partir de `HTTP_POST_VARS`, incluindo montagem das datas `j46_dtini`, `j46_dtfim` e `j46_dtinc`. |
| `incluir($j46_codigo)` | Insere isenção; gera código pela sequência `iptuisen_j46_codigo_seq` quando não informado. |
| `alterar($j46_codigo)` | Atualiza registro de isenção por `j46_codigo`, com auditoria prévia. |
| `excluir($j46_codigo, $dbwhere)` | Remove isenção por código ou condição dinâmica, registrando auditoria. |
| `sql_query` | Consulta isenção com joins de matrícula, tipo de isenção, lote, CGM e taxas isentas. |
| `sql_query_file` | Consulta direta na tabela `iptuisen`. |
| `sql_query_isen` | Consulta ampliada de isenção com proprietário, promitente, processo e condomínio. |
| `sql_queryIsencao($iAnousu, $iMatricula)` | Lista tipos de isenção de uma matrícula em um exercício via `isenexe`. |

## SQLs de referência normalizados

### Consultar isenção com dados cadastrais principais

```sql
select
  iptuisen.*,
  iptubase.*,
  tipoisen.*,
  lote.*,
  cgm.*,
  isentaxa.*
from iptuisen
inner join iptubase on iptubase.j01_matric = iptuisen.j46_matric
inner join tipoisen on tipoisen.j45_tipo = iptuisen.j46_tipo
inner join lote on lote.j34_idbql = iptubase.j01_idbql
inner join cgm on cgm.z01_numcgm = iptubase.j01_numcgm
left join isentaxa on isentaxa.j56_codigo = iptuisen.j46_codigo
where iptuisen.j46_codigo = :codigo;
```

### Consultar isenções por exercício e matrícula

```sql
select
  j45_tipo,
  j45_descr
from iptuisen
inner join isenexe on j46_codigo = j47_codigo
inner join tipoisen on j46_tipo = j45_tipo
where j46_matric = :matricula
  and j47_anousu = :exercicio;
```

### Consulta ampliada de isenção

```sql
select
  iptuisen.*,
  tipoisen.*,
  proprietario.*,
  isenproc.*,
  promitente.*,
  cgm.*,
  cgm_propri.*,
  iptubasecondominio.*,
  condominio.*
from iptuisen
inner join tipoisen on j45_tipo = j46_tipo
inner join proprietario on j01_matric = j46_matric
left join isenproc on j61_codigo = j46_codigo
left join promitente on promitente.j41_matric = j46_matric
left join cgm on promitente.j41_numcgm = cgm.z01_numcgm
left join cgm as cgm_propri on proprietario.z01_numcgm = cgm_propri.z01_numcgm
left join iptubasecondominio on j46_matric = j108_matric
left join condominio on j108_condominio = j107_sequencial
where iptuisen.j46_codigo = :codigo;
```

## Perguntas que esta referência ajuda a responder

| Pergunta | Caminho principal |
|---|---|
| Quais isenções uma matrícula possui? | `iptuisen.j46_matric = :matricula`. |
| Qual tipo de isenção está ativo no exercício? | `iptuisen` + `isenexe` + `tipoisen`. |
| Qual percentual de isenção foi registrado? | Campo `j46_perc`. |
| Qual período de vigência da isenção? | Campos `j46_dtini` e `j46_dtfim`. |
| Quem cadastrou a isenção? | Campo `j46_idusu`. |
| Qual histórico justificou a isenção? | Campo `j46_hist`. |
| A isenção está ligada a taxas específicas? | Join com `isentaxa` por `j56_codigo = j46_codigo`. |
| A matrícula isenta pertence a condomínio? | Joins `iptubasecondominio` e `condominio`. |

## Filtros seguros sugeridos

```sql
-- Por código da isenção
where iptuisen.j46_codigo = :codigo

-- Por matrícula
where iptuisen.j46_matric = :matricula

-- Por tipo de isenção
where iptuisen.j46_tipo = :tipo_isencao

-- Por vigência em uma data
where iptuisen.j46_dtini <= :data_referencia
  and (iptuisen.j46_dtfim is null or iptuisen.j46_dtfim >= :data_referencia)

-- Por exercício, usando isenexe
where isenexe.j47_anousu = :exercicio
```

## Cuidados de uso

Não confundir `j46_codigo`, que identifica o registro de isenção, com `j46_tipo`, que identifica o tipo da isenção.

`j46_dtfim` pode ser nulo. Em consultas de vigência, considerar nulo como ausência de data final.

A classe usa SQL montado por concatenação. Para uso em IA, integrações ou consultas novas, sempre substituir valores por parâmetros.

`j46_perc` pode ser zero, mas isso não significa necessariamente ausência de isenção; pode depender de regras externas, tipo de isenção, `isenexe` ou taxas associadas.
