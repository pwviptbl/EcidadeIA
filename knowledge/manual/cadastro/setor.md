# e-Cidade — Referência de Schema: `setor`

## Resumo

Classe PHP: `cl_setor`  
Módulo: `cadastro`  
Entidade/tabela principal: `setor`  
Finalidade: cadastro de setores do cadastro imobiliário, com descrição e alíquotas predial/territorial associadas ao setor.

A tabela `setor` é usada como dimensão territorial/localizacional do cadastro imobiliário. Ela aparece vinculada principalmente a lotes, faces e valores por zona/setor.

## Tabela principal

| Campo | Tipo | Descrição | Observações |
|---|---:|---|---|
| `j30_codi` | `char(4)` | Setor | Chave lógica/primária da tabela. Informado manualmente no `incluir`. |
| `j30_descr` | `varchar(40)` | Descrição | Obrigatório na inclusão e alteração quando enviado. |
| `j30_alipre` | `float8` | Alíquota Predial | Obrigatório. Usado como parâmetro fiscal do setor. |
| `j30_aliter` | `float8` | Alíquota Territorial | Obrigatório. Usado como parâmetro fiscal do setor. |

## Chave

Chave principal/lógica:


Não há uso de sequence na inclusão. O código do setor é recebido como parâmetro em `incluir($j30_codi)`.

## Métodos principais

| Método | Finalidade |
|---|---|
| `__construct()` | Inicializa rótulos da tabela `setor` e página de retorno. |
| `erro($mostra, $retorna)` | Exibe mensagem de erro/sucesso em JavaScript. |
| `atualizacampos($exclusao=false)` | Atualiza atributos da classe a partir de `HTTP_POST_VARS`. |
| `incluir($j30_codi)` | Insere registro em `setor`. Exige descrição e alíquotas. |
| `alterar($j30_codi=null)` | Atualiza dinamicamente campos enviados. |
| `excluir($j30_codi=null, $dbwhere=null)` | Remove registros por setor ou condição customizada. |
| `sql_record($sql)` | Executa SQL e armazena contagem em `numrows`. |
| `sql_query($j30_codi=null, $campos="*", $ordem=null, $dbwhere="")` | Monta consulta da tabela `setor`. |
| `sql_query_file($j30_codi=null, $campos="*", $ordem=null, $dbwhere="")` | Monta consulta simples da tabela `setor`. |
| `vinculosSetor(array $aCampos, array $aWhere)` | Consulta vínculos do setor com faces, lotes e valores por zona/setor. |

## Regras de inclusão

Campos obrigatórios:

| Campo | Regra |
|---|---|
| `j30_codi` | Deve ser informado no parâmetro `incluir($j30_codi)`. |
| `j30_descr` | Não pode ser nulo. |
| `j30_alipre` | Não pode ser nulo. |
| `j30_aliter` | Não pode ser nulo. |

SQL base de inclusão:


## Regras de alteração

A alteração monta o `UPDATE` dinamicamente conforme os campos informados. Quando enviados, estes campos são validados:

| Campo | Regra |
|---|---|
| `j30_codi` | Não pode ser nulo. |
| `j30_descr` | Não pode ser nulo. |
| `j30_alipre` | Não pode ser nulo. |
| `j30_aliter` | Não pode ser nulo. |

SQL lógico:


## Exclusão

A exclusão remove por `j30_codi` ou por `$dbwhere` customizado.


## Auditoria

A classe grava auditoria em `db_acount*`, exceto quando a sessão `DB_desativar_account` estiver ativa.

| Campo | Código de auditoria |
|---|---:|
| `j30_codi` | `71` |
| `j30_descr` | `72` |
| `j30_alipre` | `651` |
| `j30_aliter` | `652` |

Código da tabela na auditoria: `16`.

## SQLs extraídos e normalizados

### Consulta principal da tabela


### Consulta de vínculos do setor

Método: `vinculosSetor(array $aCampos, array $aWhere)`


Esse método é útil para verificar se determinado setor possui vínculos em cadastros dependentes antes de manutenção ou exclusão.

## Relacionamentos identificados

| Tabela relacionada | Relação | Origem |
|---|---|---|
| `face` | `face.j37_setor = setor.j30_codi` | `vinculosSetor` |
| `lote` | `lote.j34_setor = setor.j30_codi` | `vinculosSetor` e uso recorrente no cadastro imobiliário |
| `zonassetorvalor` | `zonassetorvalor.j141_setor = setor.j30_codi` | `vinculosSetor` |

## Consultas úteis para IA

### Buscar setor por código


### Listar setores com quantidade de lotes


### Verificar vínculos antes de excluir setor


## Convenções de prefixo

| Prefixo | Tabela provável |
|---|---|
| `j30_` | `setor` |
| `j34_` | `lote` |
| `j37_` | `face` |
| `j141_` | `zonassetorvalor` |

## Perguntas que esta tabela ajuda a responder

- Qual é a descrição de um setor imobiliário?
- Quais são as alíquotas predial e territorial configuradas para o setor?
- Um setor possui lotes vinculados?
- Um setor possui faces ou valores fiscais por zona/setor vinculados?
- O setor pode ser removido sem afetar registros dependentes?

## Cuidados e riscos

- `j30_codi` é `char(4)`, então comparações podem exigir atenção a zeros à esquerda e espaços.
- A classe permite alteração de `j30_codi`, o que pode ser perigoso se houver vínculos em `lote`, `face` ou `zonassetorvalor`.
- A exclusão por `$dbwhere` permite remoção ampla; deve ser usada com filtros explícitos.
- O método `vinculosSetor` aceita arrays de campos e condições já montadas; deve-se evitar interpolação insegura de entrada externa.

## Nome de arquivo recomendado

`ecidade-setor-schema-referencia.md`
