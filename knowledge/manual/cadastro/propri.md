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

## Regras operacionais recorrentes
### 1. Buscar coproprietário por matrícula e CGM


### 2. Buscar todos os coproprietários de uma matrícula


### 3. Buscar coproprietários com dados do CGM


### 4. Buscar coproprietários com dados da matrícula e lote


### 5. Buscar matrículas em que um CGM aparece como coproprietário


### 6. Buscar endereço de entrega por CGM proprietário


### 7. Listar outros proprietários com tipo


### 8. Conferir total de fração por matrícula


### 9. Conferir área proporcional por proprietário contra área do lote


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
