# ecidade-carconstr-schema-referencia

## Resumo

Classe PHP: `cl_carconstr`  
Entidade/tabela principal: `carconstr`  
Módulo: `cadastro`  
Finalidade: representar o vínculo entre uma construção de uma matrícula imobiliária e suas características cadastrais.

A tabela funciona como associação N:N entre `iptuconstr` e `caracter`, identificando quais características foram atribuídas a uma construção específica.

## Tabela principal

| Campo | Tipo | Descrição |
|---|---:|---|
| `j48_matric` | `int4` | Matrícula do imóvel |
| `j48_idcons` | `int4` | Código da construção |
| `j48_caract` | `int4` | Código da característica |

## Chave lógica

A chave lógica da tabela é composta por:


Ela identifica uma característica aplicada a uma construção específica de uma matrícula.

## Relacionamentos identificados

| Tabela relacionada | Condição | Papel |
|---|---|---|
| `iptuconstr` | `iptuconstr.j39_matric = carconstr.j48_matric` e `iptuconstr.j39_idcons = carconstr.j48_idcons` | Construção vinculada à matrícula |
| `caracter` | `caracter.j31_codigo = carconstr.j48_caract` | Característica atribuída |
| `cargrup` | `cargrup.j32_grupo = caracter.j31_grupo` | Grupo da característica |
| `ruas` | `ruas.j14_codigo = iptuconstr.j39_codigo` | Logradouro da construção |
| `iptubase` | `iptubase.j01_matric = iptuconstr.j39_matric` | Cadastro base do imóvel |
| `carpadrao` | `carpadrao.j33_codcaracter = caracter.j31_codigo` | Características padrão usadas na seleção |

## Métodos relevantes

| Método | Finalidade |
|---|---|
| `__construct()` | Inicializa rótulos da tabela `carconstr` e página de retorno |
| `erro($mostra, $retorna)` | Exibe mensagens de erro/sucesso |
| `atualizacampos($exclusao=false)` | Atualiza propriedades a partir do POST |
| `incluir($j48_matric, $j48_idcons, $j48_caract)` | Insere vínculo entre construção e característica |
| `alterar($j48_matric=null, $j48_idcons=null, $j48_caract=null)` | Altera característica vinculada |
| `excluir($j48_matric=null, $j48_idcons=null, $j48_caract=null, $dbwhere=null)` | Remove vínculos por chave ou condição customizada |
| `sql_record($sql)` | Executa SQL e controla número de linhas/erro |
| `sql_query(...)` | Consulta `carconstr` com joins para construção, rua e base imobiliária |
| `sql_query_file(...)` | Consulta direta na tabela `carconstr` |
| `sql_queryCaracteristicas($iMatricula, $iCodigoConstrucao)` | Lista características de uma construção |
| `sql_querySelecaoCaracteristicas($iMatricula, $iIdConstrucao)` | Monta seleção de características disponíveis/selecionadas por construção |
| `sql_caracteristicas_selecionadas($iMatric, $iIdConstr, $sGrupo)` | Retorna características selecionadas, opcionalmente filtradas por grupo |

## Regras de inclusão

O método `incluir()` exige os três campos da chave:

| Campo | Regra |
|---|---|
| `j48_matric` | Obrigatório |
| `j48_idcons` | Obrigatório |
| `j48_caract` | Obrigatório |

Não há geração automática de sequência. Todos os valores da chave são informados por parâmetro.

## Auditoria

A classe grava auditoria em `db_acount`, `db_acountkey` e `db_acountacesso`.

| Código | Campo |
|---:|---|
| `159` | `j48_matric` |
| `160` | `j48_idcons` |
| `161` | `j48_caract` |

Código de tabela na auditoria: `31`.

Operações auditadas: inclusão (`I`), alteração (`A`) e exclusão (`E`).

## SQL principal normalizado


## Consulta direta da tabela


## Características da construção


## Seleção de características disponíveis

A consulta `sql_querySelecaoCaracteristicas()` lista grupos e características do tipo construção (`j32_tipo = 'C'`) e indica se cada característica está selecionada para a construção.

A regra considera:

- características já existentes em `carconstr`;
- características padrão em `carpadrao`;
- grupos e características sem `data_limite` vencida;
- apenas grupos do tipo `C`.

## Características selecionadas por grupo


## Perguntas que esta tabela ajuda a responder

- Quais características estão atribuídas a uma construção?
- Quais grupos de características existem para construção?
- Uma característica específica está vinculada a uma construção?
- Quais características padrão devem aparecer como selecionadas?
- Quais características de construção estão vigentes, considerando `data_limite` de grupo/característica?

## Filtros seguros para IA

Use preferencialmente:


Para listas de grupos:


## Cuidados e riscos

- A tabela não possui coluna de sequência própria; a identidade é composta pelos três campos.
- `alterar()` atualiza apenas `j48_caract`, mas usa a chave completa no `where`.
- `sql_querySelecaoCaracteristicas()` usa lógica de característica padrão via `carpadrao`; isso pode marcar uma característica como selecionada mesmo sem registro explícito em `carconstr`.
- As consultas de seleção filtram características e grupos vencidos por `data_limite`.
- O código monta SQL por concatenação; entradas externas devem ser parametrizadas em reimplementações modernas.

## Convenção de prefixo

Prefixo principal da tabela: `j48`.

| Prefixo | Tabela provável |
|---|---|
| `j48` | `carconstr` |
| `j39` | `iptuconstr` |
| `j31` | `caracter` |
| `j32` | `cargrup` |
| `j14` | `ruas` |
| `j01` | `iptubase` |

## Uso recomendado para IA

Use `carconstr` como tabela de associação entre construção imobiliária e características. Para enriquecer a resposta, junte com `caracter` e `cargrup`; para contexto físico da construção, junte com `iptuconstr`; para contexto do imóvel, junte com `iptubase`.
