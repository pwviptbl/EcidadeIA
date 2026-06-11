# Referência da classe `cl_caracter`

## 1. Identificação

A classe `cl_caracter` representa a entidade `caracter`, usada no cadastro imobiliário para manter características classificadas por grupo. Essas características aparecem principalmente em vínculos com construções e podem influenciar pontuação, composição de características da edificação e identificação de características irregulares.

Tabela principal:

```sql
caracter
```

Chave primária lógica:

```sql
j31_codigo
```

## 2. Colunas da tabela principal

| Campo | Tipo | Descrição |
|---|---:|---|
| `j31_codigo` | `int8` | Código da característica |
| `j31_descr` | `varchar(40)` | Descrição da característica |
| `j31_grupo` | `int4` | Grupo da característica |
| `j31_pontos` | `int4` | Pontuação associada |
| `j31_data_limite` | `date` | Data limite da característica |

## 3. Campos da classe

A classe declara propriedades equivalentes aos campos da tabela:

```php
j31_codigo
j31_descr
j31_grupo
j31_pontos
j31_data_limite
```

Observação: o `INSERT` da classe grava `j31_codigo`, `j31_descr`, `j31_grupo` e `j31_pontos`. O campo `j31_data_limite` é tratado na alteração, mas não aparece no `INSERT` da classe analisada.

## 4. Regras de inclusão

Método:

```php
incluir($j31_codigo)
```

Campos obrigatórios na inclusão:

| Campo | Regra |
|---|---|
| `j31_descr` | obrigatório |
| `j31_grupo` | obrigatório |
| `j31_pontos` | obrigatório |
| `j31_codigo` | chave; gerada por sequência se não informada |

Sequência utilizada:

```sql
caracter_j31_codigo_seq
```

Se o código for informado manualmente, a classe compara com `last_value` da sequência e rejeita valores maiores que o último número da sequência.

SQL base da inclusão:

```sql
insert into caracter (
  j31_codigo,
  j31_descr,
  j31_grupo,
  j31_pontos
) values (
  :j31_codigo,
  :j31_descr,
  :j31_grupo,
  :j31_pontos
);
```

## 5. Regras de alteração

Método:

```php
alterar($j31_codigo = null)
```

A alteração monta dinamicamente o `UPDATE` apenas com campos recebidos. Campos numéricos vazios podem ser normalizados para `0`.

Tratamento especial:

| Campo | Regra |
|---|---|
| `j31_data_limite` | se informada, deve ser menor ou igual à data atual |
| `j31_data_limite` | se vazia, é gravada como `null` |

SQL base:

```sql
update caracter
   set j31_descr = :descricao,
       j31_grupo = :grupo,
       j31_pontos = :pontos,
       j31_data_limite = :data_limite
 where j31_codigo = :codigo;
```

## 6. Regras de exclusão

Método:

```php
excluir($j31_codigo = null, $dbwhere = null)
```

A exclusão pode ocorrer por código ou por uma cláusula livre recebida em `$dbwhere`.

SQL equivalente:

```sql
delete from caracter
 where j31_codigo = :codigo;
```

## 7. Consulta principal

Método:

```php
sql_query($j31_codigo = null, $campos = "*", $ordem = null, $dbwhere = "")
```

Consulta a tabela `caracter` com junção ao grupo da característica:

```sql
select *
  from caracter
 inner join cargrup
         on cargrup.j32_grupo = caracter.j31_grupo
 where caracter.j31_codigo = :codigo;
```

## 8. Consulta direta da tabela

Método:

```php
sql_query_file($j31_codigo = null, $campos = "*", $ordem = null, $dbwhere = "")
```

Consulta apenas a tabela principal:

```sql
select *
  from caracter
 where caracter.j31_codigo = :codigo;
```

## 9. Consulta de característica por construção

Método:

```php
sql_query_carconstr($iMatric, $iIdConstr, $sCaracter)
```

Esse método recebe uma matrícula, um identificador de construção e uma lista de características. Ele identifica o grupo das características informadas e verifica se a construção já possui característica daquele mesmo grupo vinculada em `carconstr`.

Estrutura lógica:

```sql
with buscagrupo as (
  select j31_grupo as grupo,
         j31_codigo as caract
    from caracter
   where j31_codigo in (:caracteristicas)
),
buscacaracter as (
  select j48_caract as caractmatric,
         j31_grupo as grupomatric,
         j48_matric as matricula
    from caracter
    join carconstr
      on j48_matric = :matricula
     and j48_idcons = :id_construcao
     and j48_caract = caracter.j31_codigo
   where j31_grupo in (select j31_grupo from buscagrupo)
)
select caract,
       coalesce(caractmatric, 0) as caractmatric
  from buscagrupo
  left join buscacaracter
         on grupomatric = grupo;
```

Uso provável:

- verificar substituição ou conflito de características por grupo;
- evitar múltiplas características do mesmo grupo em uma mesma construção;
- apoiar telas de seleção de características da edificação.

## 10. Relacionamentos identificados

| Tabela | Relação | Uso |
|---|---|---|
| `cargrup` | `cargrup.j32_grupo = caracter.j31_grupo` | Grupo da característica |
| `carconstr` | `carconstr.j48_caract = caracter.j31_codigo` | Características vinculadas a construções |

Relacionamentos funcionais observados no conjunto de classes do cadastro imobiliário:

| Origem | Relação | Destino |
|---|---|---|
| `caracter.j31_codigo` | característica selecionada | `carconstr.j48_caract` |
| `caracter.j31_grupo` | grupo de classificação | `cargrup.j32_grupo` |
| `cfiptu.j18_caracterirregular` | pode armazenar códigos relacionados a características irregulares | `caracter.j31_codigo` |
| `lote.sql_query_construcoesLote()` | usa lista de características irregulares para verificar regularidade da construção | `carconstr` + `caracter` |

## 11. Auditoria

Diferente de várias classes legadas do e-Cidade, esta classe não executa inserts em `db_acount`, `db_acountkey` ou `db_acountacesso` nos métodos de inclusão, alteração e exclusão.

## 12. Consultas úteis

### Buscar característica com grupo

```sql
select caracter.j31_codigo,
       caracter.j31_descr,
       caracter.j31_grupo,
       cargrup.j32_descr,
       caracter.j31_pontos,
       caracter.j31_data_limite
  from caracter
 inner join cargrup
         on cargrup.j32_grupo = caracter.j31_grupo
 where caracter.j31_codigo = :codigo;
```

### Listar características de um grupo

```sql
select j31_codigo,
       j31_descr,
       j31_pontos,
       j31_data_limite
  from caracter
 where j31_grupo = :grupo
 order by j31_descr;
```

### Verificar características vinculadas a uma construção

```sql
select carconstr.j48_matric,
       carconstr.j48_idcons,
       caracter.j31_codigo,
       caracter.j31_descr,
       caracter.j31_grupo,
       caracter.j31_pontos
  from carconstr
 inner join caracter
         on caracter.j31_codigo = carconstr.j48_caract
 where carconstr.j48_matric = :matricula
   and carconstr.j48_idcons = :id_construcao;
```

## 13. Perguntas que esta referência ajuda a responder

- Quais características existem cadastradas?
- A qual grupo pertence uma característica?
- Qual pontuação uma característica adiciona?
- Uma construção já possui característica do mesmo grupo?
- A característica possui data limite?
- Quais características podem ser usadas para identificar área irregular?

## 14. Cuidados e riscos

- A classe concatena valores diretamente em SQL.
- O método `excluir()` aceita `$dbwhere` livre.
- `j31_data_limite` é validado apenas no método de alteração.
- `j31_data_limite` está no `$campos`, mas não aparece no `INSERT`.
- A validação da data limite usa `DateTime::createFromFormat('d/m/Y', ...)`, enquanto a propriedade é declarada como campo `date`; conferir o formato enviado pela interface.
- A classe não registra auditoria via `db_acount`.

## 15. Resumo para IA

Use `caracter` para representar características cadastrais usadas principalmente em construções do cadastro imobiliário. A chave é `j31_codigo`. O campo `j31_grupo` classifica a característica em `cargrup`; `j31_pontos` indica pontuação; `j31_data_limite` controla limite temporal. Para saber se uma construção já possui característica de determinado grupo, use a lógica de `sql_query_carconstr`, combinando `caracter` e `carconstr`.
