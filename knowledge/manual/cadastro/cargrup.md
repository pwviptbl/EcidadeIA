# Referência da Classe `cl_cargrup`

## 1. Identificação

A classe `cl_cargrup` representa a entidade `cargrup`, utilizada para cadastrar grupos de características do cadastro imobiliário. Esses grupos organizam características (`caracter`) por tipo e descrição, sendo usados em rotinas de características de construção, matrícula e parametrizações relacionadas ao IPTU.

- **Módulo:** `cadastro`
- **Tabela principal:** `cargrup`
- **Chave primária:** `j32_grupo`
- **Sequência:** `cargrup_j32_grupo_seq`
- **Classe PHP:** `cl_cargrup`

## 2. Tabela principal

### `cargrup`

| Campo | Tipo | Descrição |
|---|---:|---|
| `j32_grupo` | `int4` | Código do grupo |
| `j32_descr` | `varchar(40)` | Descrição |
| `j32_tipo` | `char(1)` | Tipo |
| `j32_data_limite` | `date` | Data limite |

## 3. Campos da classe

A classe declara as seguintes propriedades de dados:

| Propriedade | Campo | Observação |
|---|---|---|
| `$j32_grupo` | `j32_grupo` | Código identificador do grupo |
| `$j32_descr` | `j32_descr` | Nome/descrição do grupo |
| `$j32_tipo` | `j32_tipo` | Tipo do grupo |
| `$j32_data_limite` | `j32_data_limite` | Data limite para uso/validade |

## 4. Regras de inclusão

Método: `incluir($j32_grupo)`

Campos obrigatórios na inclusão:

| Campo | Regra |
|---|---|
| `j32_descr` | Obrigatório |
| `j32_tipo` | Obrigatório |
| `j32_grupo` | Obrigatório; gerado pela sequência quando não informado |

Quando `j32_grupo` não é informado, a classe busca o próximo valor em `cargrup_j32_grupo_seq`.

Quando `j32_grupo` é informado manualmente, a classe consulta o `last_value` da sequência e bloqueia a inclusão se o código informado for maior que o último valor da sequência.

A inclusão grava apenas:

```sql
insert into cargrup (
  j32_grupo,
  j32_descr,
  j32_tipo
)
values (
  :j32_grupo,
  :j32_descr,
  :j32_tipo
);
```

Observação: apesar de `j32_data_limite` existir em `$campos` e ser tratado na alteração, ele não é incluído no `INSERT` desta classe.

## 5. Regras de alteração

Método: `alterar($j32_grupo = null)`

A alteração monta dinamicamente um `UPDATE cargrup SET ... WHERE j32_grupo = ...`.

Campos alteráveis pela classe:

| Campo | Regra |
|---|---|
| `j32_grupo` | Aceita alteração se enviado |
| `j32_descr` | Obrigatório quando enviado |
| `j32_tipo` | Obrigatório quando enviado |
| `j32_data_limite` | Se vazia, grava `null`; se informada, deve ser menor ou igual à data atual |

Regra específica de `j32_data_limite`:

- A data é validada com `DateTime::createFromFormat('d/m/Y', $this->j32_data_limite)`.
- Se a data limite for futura, a alteração é abortada.
- Se vazia, o campo é atualizado para `null`.

SQL equivalente:

```sql
update cargrup
   set j32_descr = :descricao,
       j32_tipo = :tipo,
       j32_data_limite = :data_limite
 where j32_grupo = :grupo;
```

## 6. Regras de exclusão

Método: `excluir($j32_grupo = null, $dbwhere = null)`

A exclusão remove registros de `cargrup` por chave ou por condição livre.

```sql
delete from cargrup
 where j32_grupo = :grupo;
```

Se `$dbwhere` for informado, ele substitui o filtro por chave.

## 7. Consultas geradas pela classe

### `sql_query($j32_grupo = null, $campos = "*", $ordem = null, $dbwhere = "")`

Consulta a tabela `cargrup`.

```sql
select *
  from cargrup
 where cargrup.j32_grupo = :grupo
 order by :ordem;
```

### `sql_query_file($j32_grupo = null, $campos = "*", $ordem = null, $dbwhere = "")`

Consulta direta para leitura/auditoria da tabela `cargrup`.

```sql
select *
  from cargrup
 where cargrup.j32_grupo = :grupo
 order by :ordem;
```

## 8. Relacionamentos conhecidos

Embora a classe `cl_cargrup` não faça `JOIN` diretamente em suas consultas, ela se relaciona funcionalmente com a tabela `caracter`.

| Tabela relacionada | Relação | Uso |
|---|---|---|
| `caracter` | `caracter.j31_grupo = cargrup.j32_grupo` | Características pertencem a grupos |
| `carconstr` | Via `caracter.j31_codigo = carconstr.j48_caract` | Características aplicadas a construções |
| `constrcar` | Via características/grupos | Caracterização de construção |
| `cfiptu` | Usa grupos/características em parametrizações específicas | Configurações do IPTU |

## 9. Papel no cadastro imobiliário

`cargrup` é uma tabela de domínio para organizar características. No fluxo do cadastro imobiliário, ela costuma ser usada para:

- agrupar características de construção;
- classificar características por tipo;
- facilitar pontuação, filtros e regras por grupo;
- permitir controle de validade por `j32_data_limite`;
- apoiar consultas de características já vinculadas a construções.

## 10. Perguntas que esta tabela ajuda a responder

- Quais grupos de características existem no cadastro imobiliário?
- Qual descrição e tipo de um grupo de características?
- Um grupo de características está com data limite definida?
- Quais características pertencem a determinado grupo?
- Quais grupos são usados para classificar características de construção?

## 11. Cuidados e riscos

- A classe concatena valores diretamente em SQL.
- `$dbwhere` é aceito livremente em consultas e exclusões.
- `j32_data_limite` é tratado como `d/m/Y` na validação, embora o campo seja `date`.
- O campo `j32_data_limite` não aparece no `INSERT`, apenas na alteração.
- A alteração permite atualizar a própria chave `j32_grupo`, o que pode impactar registros relacionados em `caracter`.
- A inclusão manual de chave depende do `last_value` da sequência.

## 12. Resumo para IA

Use `cargrup` quando a pergunta envolver grupos de características do cadastro imobiliário. A chave é `j32_grupo`. A tabela armazena descrição, tipo e data limite. Ela se relaciona principalmente com `caracter` pelo campo `caracter.j31_grupo = cargrup.j32_grupo`. Para características aplicadas a construções, o caminho usual é `cargrup -> caracter -> carconstr`.
