# e-Cidade — Cadastro Imobiliário

## Tabela principal: `bairro`

A tabela `bairro` representa o cadastro básico de bairros. É usada como dimensão territorial para lote, logradouro e consultas por CEP.

| Campo | Tipo | Descrição | Observações |
|---|---:|---|---|
| `j13_codi` | `int4` | Cód. do Bairro | Chave primária lógica. Gerada pela sequência `bairro_j13_codi_seq` quando não informada. |
| `j13_descr` | `varchar(40)` | Bairro | Nome/descrição do bairro. Obrigatório na inclusão. |
| `j13_codant` | `varchar(10)` | Código Anterior | Código legado/anterior. Opcional. |
| `j13_rural` | `bool` | Rural | Indica se o bairro é rural. Obrigatório na inclusão. Valor padrão inicial da classe: `'f'`. |

## Chave e sequência

- **Chave principal:** `j13_codi`
- **Sequência:** `bairro_j13_codi_seq`
- Se `j13_codi` não for informado na inclusão, a classe usa `nextval('bairro_j13_codi_seq')`.
- Se `j13_codi` for informado manualmente, a classe compara com `last_value` da sequência e bloqueia valores maiores que o último número da sequência.

## Tabelas relacionadas identificadas

### `ruasbairro`

Tabela de vínculo entre logradouro e bairro, usada em `sql_getBairroByCodRua()`.

Relacionamento identificado:

```sql
ruasbairro.j16_bairro = bairro.j13_codi
ruasbairro.j16_lograd = ruas.j14_codigo
```

Uso principal: descobrir o bairro associado a um código de rua/logradouro.

### `ruas`

Tabela de logradouros, usada na consulta por código de rua.

Relacionamento identificado:

```sql
ruas.j14_codigo = ruasbairro.j16_lograd
```

### `cepbairrosfaixa`

Tabela de faixas de CEP por bairro, usada em `sql_buscaBairroPorCep()`.

Campos usados:

| Campo | Papel |
|---|---|
| `cp02_codbairro` | Código do bairro associado à faixa. |
| `cp02_faixa` | Identificador da faixa. |
| `cp02_cepinicial` | CEP inicial da faixa. |
| `cp02_cepfinal` | CEP final da faixa. |

A classe não faz `JOIN` explícito com `bairro` nessa query, mas o campo `cp02_codbairro` deve ser tratado como referência ao código do bairro.

## Métodos relevantes

| Método | Finalidade |
|---|---|
| `atualizacampos($exclusao=false)` | Atualiza propriedades da classe a partir de `HTTP_POST_VARS`. |
| `incluir($j13_codi)` | Insere novo bairro, gerando código pela sequência quando necessário. |
| `alterar($j13_codi=null)` | Atualiza bairro por `j13_codi`. |
| `excluir($j13_codi=null, $dbwhere=null)` | Exclui bairro por código ou condição customizada. |
| `sql_record($sql)` | Executa consulta e atualiza `numrows`/erros. |
| `sql_query($j13_codi=null, $campos='*', $ordem=null, $dbwhere='')` | Consulta principal na tabela `bairro`. |
| `sql_query_file($j13_codi=null, $campos='*', $ordem=null, $dbwhere='')` | Consulta direta na tabela `bairro`, usada para auditoria e leitura simples. |
| `sql_getBairroByCodRua($iCodRua)` | Busca bairro vinculado a uma rua/logradouro. |
| `sql_buscaBairroPorCep($cep)` | Busca faixa de CEP que contém o CEP informado. |

## SQLs prontos para uso por IA

### 1. Buscar bairro por código

```sql
select
    bairro.*
from bairro
where bairro.j13_codi = :codigo_bairro;
```

Parâmetros:

| Placeholder | Descrição |
|---|---|
| `:codigo_bairro` | Código `j13_codi` do bairro. |

### 2. Listar bairros por nome

```sql
select
    bairro.j13_codi,
    bairro.j13_descr,
    bairro.j13_codant,
    bairro.j13_rural
from bairro
where bairro.j13_descr ilike '%' || :nome_bairro || '%'
order by bairro.j13_descr;
```

Parâmetros:

| Placeholder | Descrição |
|---|---|
| `:nome_bairro` | Parte do nome do bairro. |

### 3. Listar bairros rurais ou urbanos

```sql
select
    bairro.j13_codi,
    bairro.j13_descr,
    bairro.j13_codant,
    bairro.j13_rural
from bairro
where bairro.j13_rural = :rural
order by bairro.j13_descr;
```

Parâmetros:

| Placeholder | Descrição |
|---|---|
| `:rural` | `true`/`false` ou representação booleana equivalente usada pelo banco. |

### 4. Buscar bairro por código de logradouro

```sql
select
    bairro.*
from ruasbairro
inner join ruas
        on ruas.j14_codigo = ruasbairro.j16_lograd
inner join bairro
        on bairro.j13_codi = ruasbairro.j16_bairro
where ruas.j14_codigo = :codigo_rua;
```

Parâmetros:

| Placeholder | Descrição |
|---|---|
| `:codigo_rua` | Código do logradouro em `ruas.j14_codigo`. |

### 5. Buscar bairro por CEP dentro de faixa

```sql
select
    cepbairrosfaixa.cp02_codbairro,
    cepbairrosfaixa.cp02_faixa,
    cepbairrosfaixa.cp02_cepinicial,
    cepbairrosfaixa.cp02_cepfinal
from cepbairrosfaixa
where cepbairrosfaixa.cp02_cepinicial::int <= :cep::int
  and cepbairrosfaixa.cp02_cepfinal::int >= :cep::int;
```

Parâmetros:

| Placeholder | Descrição |
|---|---|
| `:cep` | CEP numérico, sem máscara. |

### 6. Buscar dados completos do bairro por CEP com descrição

```sql
select
    bairro.j13_codi,
    bairro.j13_descr,
    bairro.j13_codant,
    bairro.j13_rural,
    cepbairrosfaixa.cp02_faixa,
    cepbairrosfaixa.cp02_cepinicial,
    cepbairrosfaixa.cp02_cepfinal
from cepbairrosfaixa
inner join bairro
        on bairro.j13_codi = cepbairrosfaixa.cp02_codbairro
where cepbairrosfaixa.cp02_cepinicial::int <= :cep::int
  and cepbairrosfaixa.cp02_cepfinal::int >= :cep::int
order by bairro.j13_descr;
```

Parâmetros:

| Placeholder | Descrição |
|---|---|
| `:cep` | CEP numérico, sem pontos ou hífen. |

### 7. Contar lotes por bairro

```sql
select
    bairro.j13_codi,
    bairro.j13_descr,
    count(lote.j34_idbql) as quantidade_lotes
from bairro
left join lote
       on lote.j34_bairro = bairro.j13_codi
group by
    bairro.j13_codi,
    bairro.j13_descr
order by bairro.j13_descr;
```

Observação: a tabela `lote` não aparece diretamente nesta classe, mas é uma relação importante no cadastro imobiliário, pois `lote.j34_bairro` referencia `bairro.j13_codi` em outras classes extraídas.

## Convenção de prefixos

| Prefixo | Tabela provável | Observação |
|---|---|---|
| `j13_` | `bairro` | Campos do cadastro de bairros. |
| `j14_` | `ruas` | Campos de logradouro. |
| `j16_` | `ruasbairro` | Vínculo rua/bairro. |
| `cp02_` | `cepbairrosfaixa` | Faixas de CEP por bairro. |
| `j34_` | `lote` | Lotes vinculados ao bairro por `j34_bairro`. |

## Perguntas que esta classe ajuda a responder

- Qual é o nome de um bairro pelo código `j13_codi`?
- Um bairro é rural ou urbano?
- Qual bairro está associado a um logradouro?
- Qual bairro atende um determinado CEP?
- Quais bairros possuem código anterior/legado?
- Quais bairros estão associados a lotes no cadastro imobiliário?

## Filtros seguros recomendados

| Caso | Filtro recomendado |
|---|---|
| Buscar por código | `bairro.j13_codi = :codigo_bairro` |
| Buscar por nome | `bairro.j13_descr ilike '%' || :nome_bairro || '%'` |
| Buscar por logradouro | `ruas.j14_codigo = :codigo_rua` |
| Buscar por CEP | `cp02_cepinicial::int <= :cep::int and cp02_cepfinal::int >= :cep::int` |
| Buscar rural/urbano | `bairro.j13_rural = :rural` |

## Cuidados e riscos

- A classe monta SQL por interpolação direta de variáveis. Em uso externo, substitua por parâmetros preparados.
- `sql_buscaBairroPorCep()` faz cast de CEP para inteiro. Remova máscara antes de consultar.
- `sql_getBairroByCodRua()` pode retornar mais de um bairro para o mesmo logradouro caso a tabela `ruasbairro` permita múltiplos vínculos.
- `j13_rural` é booleano, mas a classe manipula valores textuais como `'f'`; validar compatibilidade conforme driver/PostgreSQL.
- A exclusão por `dbwhere` permite condições arbitrárias; use com restrição.

