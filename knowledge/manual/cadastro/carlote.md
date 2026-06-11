# ecidade-carlote-schema-referencia

## Metadados

| Item | Valor |
|---|---|
| Classe | `cl_carlote` |
| Entidade / tabela principal | `carlote` |
| Módulo | `cadastro` |
| Arquivo sugerido | `ecidade-carlote-schema-referencia.md` |
| Finalidade | Registrar características associadas a um lote imobiliário. |

## Resumo

A tabela `carlote` representa o vínculo entre um lote (`lote`) e uma característica cadastral (`caracter`). Ela funciona como tabela associativa para qualificar o lote com atributos previamente cadastrados, agrupados em `cargrup`.

O vínculo principal é composto por:

```sql
j35_idbql + j35_caract
```

Na prática, a classe permite consultar quais características estão associadas a um lote e, por meio dos joins, recuperar também o grupo da característica, dados do lote, bairro e setor.

## Tabela principal

### `carlote`

| Coluna | Tipo | Descrição | Observações |
|---|---:|---|---|
| `j35_idbql` | `int4` | Id lote | Parte da chave lógica. Referencia `lote.j34_idbql`. |
| `j35_caract` | `int4` | Característica | Parte da chave lógica. Referencia `caracter.j31_codigo`. |
| `j35_dtlanc` | `date` | Data de lançamento | Campo opcional no insert; pode ser `null`. |

## Chave lógica

A classe trata como chave lógica a combinação:

```sql
carlote.j35_idbql = :id_lote
and carlote.j35_caract = :caracteristica
```

Não há sequence própria na classe. Os dois identificadores são recebidos por parâmetro em `incluir($j35_idbql, $j35_caract)`.

## Relacionamentos identificados

| Origem | Destino | Condição | Tipo |
|---|---|---|---|
| `carlote` | `caracter` | `caracter.j31_codigo = carlote.j35_caract` | `inner join` |
| `carlote` | `lote` | `lote.j34_idbql = carlote.j35_idbql` | `inner join` |
| `caracter` | `cargrup` | `cargrup.j32_grupo = caracter.j31_grupo` | `inner join` |
| `lote` | `bairro` | `bairro.j13_codi = lote.j34_bairro` | `inner join` |
| `lote` | `setor` | `setor.j30_codi = lote.j34_setor` | `inner join` |

## Métodos relevantes

| Método | Papel |
|---|---|
| `__construct()` | Inicializa rótulos da tabela `carlote` e página de retorno. |
| `erro($mostra, $retorna)` | Exibe mensagem de erro e opcionalmente retorna para a página. |
| `atualizacampos($exclusao=false)` | Alimenta propriedades a partir de `HTTP_POST_VARS`; em exclusão atualiza apenas chave. |
| `incluir($j35_idbql, $j35_caract)` | Insere vínculo entre lote e característica. |
| `alterar($j35_idbql=null, $j35_caract=null)` | Atualiza vínculo existente, principalmente `j35_dtlanc`. |
| `excluir($j35_idbql=null, $j35_caract=null, $dbwhere=null)` | Remove vínculo por chave ou por cláusula customizada. |
| `sql_record($sql)` | Executa SQL e controla `numrows`/erro. |
| `sql_query(...)` | Consulta completa com joins para lote, característica, grupo, bairro e setor. |
| `sql_query_file(...)` | Consulta simples diretamente em `carlote`. |

## Regras de validação e defaults

### Inclusão

`incluir($j35_idbql, $j35_caract)` exige:

| Campo | Regra |
|---|---|
| `j35_idbql` | Obrigatório. Se vazio, retorna erro de chave primária zerada. |
| `j35_caract` | Obrigatório. Se vazio, retorna erro de chave primária zerada. |
| `j35_dtlanc` | Opcional. Se vazio ou `"null"`, grava `null`. |

### Alteração

`alterar($j35_idbql, $j35_caract)` pode alterar:

| Campo | Regra |
|---|---|
| `j35_idbql` | Se informado/postado, não pode ser nulo. |
| `j35_caract` | Se informado/postado, não pode ser nulo. |
| `j35_dtlanc` | Se data postada, grava a data; se o campo de data foi postado vazio, grava `null`, mas a validação interna ainda trata ausência como erro em alguns cenários. |

## Auditoria

A classe registra auditoria nas operações de inclusão, alteração e exclusão usando `db_acount`.

| Código | Campo |
|---:|---|
| `96` | `j35_idbql` |
| `97` | `j35_caract` |
| `8069` | `j35_dtlanc` |

Código da tabela na auditoria: `23`.

Operações usadas:

| Operação | Marcador |
|---|---|
| Inclusão | `I` |
| Alteração | `A` |
| Exclusão | `E` |

## SQLs extraídos e normalizados

### Consulta completa da classe

```sql
select *
from carlote
inner join caracter
        on caracter.j31_codigo = carlote.j35_caract
inner join lote
        on lote.j34_idbql = carlote.j35_idbql
inner join cargrup
        on cargrup.j32_grupo = caracter.j31_grupo
inner join bairro
        on bairro.j13_codi = lote.j34_bairro
inner join setor
        on setor.j30_codi = lote.j34_setor
where carlote.j35_idbql = :id_lote
  and carlote.j35_caract = :caracteristica
order by :ordem;
```

### Consulta simples da tabela

```sql
select *
from carlote
where carlote.j35_idbql = :id_lote
  and carlote.j35_caract = :caracteristica
order by :ordem;
```

### Inserção normalizada

```sql
insert into carlote (
  j35_idbql,
  j35_caract,
  j35_dtlanc
) values (
  :id_lote,
  :caracteristica,
  :data_lancamento
);
```

### Exclusão por chave

```sql
delete from carlote
where j35_idbql = :id_lote
  and j35_caract = :caracteristica;
```

## Perguntas que esta tabela ajuda a responder

- Quais características estão associadas a determinado lote?
- Quais lotes possuem determinada característica?
- Qual grupo (`cargrup`) organiza uma característica vinculada ao lote?
- Quais características de lote podem ser cruzadas com bairro e setor?
- Quando uma característica foi lançada no lote?

## Filtros seguros para IA/SQL

Use preferencialmente filtros explícitos por chave:

```sql
where carlote.j35_idbql = :id_lote
```

ou:

```sql
where carlote.j35_idbql = :id_lote
  and carlote.j35_caract = :caracteristica
```

Para análises cadastrais por grupo:

```sql
where caracter.j31_grupo = :grupo
```

Para recortes territoriais:

```sql
where lote.j34_bairro = :bairro
```

```sql
where lote.j34_setor = :setor
```

## Cuidados e riscos

- `carlote` é uma tabela de associação; não descreve a característica por si só. Para obter descrição, grupo e pontos, juntar com `caracter`.
- A classe permite `dbwhere` livre em consultas e exclusões; isso exige cuidado para evitar filtros inseguros ou amplos demais.
- `j35_dtlanc` é opcional na inclusão, mas a alteração tem lógica sensível ao envio dos campos de data separados (`dia`, `mes`, `ano`).
- A chave lógica depende da combinação lote + característica; repetir a mesma característica no mesmo lote tende a gerar erro de duplicidade.
- A data é montada manualmente no formato `YYYY-MM-DD` a partir de campos separados.

## Convenção de prefixo

| Prefixo | Tabela principal provável |
|---|---|
| `j35_` | `carlote` |
| `j31_` | `caracter` |
| `j32_` | `cargrup` |
| `j34_` | `lote` |
| `j13_` | `bairro` |
| `j30_` | `setor` |

## Uso recomendado para IA

Ao responder perguntas sobre características de lote, tratar `carlote` como tabela ponte entre `lote` e `caracter`.

Caminho típico:

```sql
lote
  -> carlote
  -> caracter
  -> cargrup
```

Para contextualização territorial, incluir:

```sql
lote
  -> bairro
  -> setor
```
