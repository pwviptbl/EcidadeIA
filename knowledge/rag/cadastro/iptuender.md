## cadastro.iptuender

> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptuender`
> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_iptuender_classe.php`

### Resumo tecnico

- Descricao: cadastro de endereco de entrega dos carnes de IPTU por matricula.
- Chave primaria: `j43_matric`
- Chave de negocio: `j43_matric`
- Coluna de tempo: Nao informada
- Grao: uma linha por matricula com endereco de entrega cadastrado
- Recomendada: nao
- Significado da contagem: conta matriculas com endereco de entrega proprio; nao conta imoveis ativos em geral
- Candidatas a chave de negocio: `j43_matric`, `j43_iptuendergrupo`
- Candidatas a coluna de tempo: nenhuma inferida automaticamente

### Relacionamentos

- `j43_matric` -> `cadastro.iptubase` (`j01_matric`) [iptuender_matric_fk]
- `j43_iptuendergrupo` -> `cadastro.iptuendergrupo` (`j135_sequencial`) [grupo_endereco_fk, observado no codigo]

### Perguntas que esta tabela ajuda a responder

- Qual o endereco de entrega de um carnê de IPTU para uma matricula?
- Quais matriculas compartilham o mesmo grupo de endereco de entrega?
- Qual o endereco de entrega cadastrado para uma matricula especifica?
- Como listar o endereco de entrega com dados da matricula, lote e contribuinte?

### Filtros e regras reaproveitaveis

#### Filtros padrao

- Matricula especifica: `j43_matric = :matricula`
- Grupo de endereco de entrega: `j43_iptuendergrupo = :grupo_endereco`

#### Semantica de filtros

- `j43_matric` identifica o cadastro de entrega ligado a uma matricula do IPTU.
- `j43_iptuendergrupo` representa o agrupamento de matriculas com o mesmo endereco de entrega, conforme uso na RPC `cad4_iptuendergrupo.RPC.php`.

### Consulta: `sql_query`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptuender_classe.php`
- **Objetivo:** ler o endereco de entrega da matricula enriquecendo com dados do imovel, lote e contribuinte.
- **Tabelas:** `iptuender`, `iptubase`, `lote`, `cgm`
- **Grau do resultado:** uma linha por matricula com endereco de entrega, desde que exista correspondencia em `iptubase`, `lote` e `cgm`
- **Parametros:** `j43_matric` filtra a matricula; `campos` escolhe as colunas; `ordem` define ordenacao; `dbwhere` substitui o filtro por matricula
- **Juncoes:**
  - `iptubase.j01_matric = iptuender.j43_matric` `inner join`
  - `lote.j34_idbql = iptubase.j01_idbql` `inner join`
  - `cgm.z01_numcgm = iptubase.j01_numcgm` `inner join`
- **Filtros e regras:**
  - Quando `dbwhere` esta vazio e `j43_matric` foi informado, o filtro aplicado e `iptuender.j43_matric = <matricula>`.
  - Se qualquer uma das tabelas vinculadas nao existir para a matricula, a linha nao aparece por causa dos `inner join`.
- **Campos relevantes:**
  - `j43_matric` identifica a matricula do endereco de entrega.
  - `j43_dest`, `j43_ender`, `j43_numimo`, `j43_comple`, `j43_bairro`, `j43_munic`, `j43_uf`, `j43_cep`, `j43_cxpost` descrevem o endereco de entrega.
  - `j01_idbql` e `j01_numcgm` permitem conectar o endereco ao lote e ao contribuinte.
- **SQL normalizada:**

  ```sql
  select /* campos dinamicos */
    from iptuender
    inner join iptubase on iptubase.j01_matric = iptuender.j43_matric
    inner join lote on lote.j34_idbql = iptubase.j01_idbql
    inner join cgm on cgm.z01_numcgm = iptubase.j01_numcgm
   where /* j43_matric ou dbwhere dinamico */
   order by /* ordem dinamica */
  ```

- **Cuidados:**
  - Esta consulta exclui enderecos de entrega sem correspondencia em `iptubase`, `lote` ou `cgm`.
  - Se a pergunta for apenas sobre o endereco cadastrado, `sql_query_file()` e mais direta.
  - Evite usar esta saida como contagem de imoveis, porque o grao aqui e o endereco de entrega por matricula.
- **Evidencia adicional:** consumo direto da matricula em telas legadas e uso do grupo de enderecos na RPC `cad4_iptuendergrupo.RPC.php`.

### Consulta: `sql_query_file`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptuender_classe.php`
- **Objetivo:** leitura direta da tabela `iptuender` por matricula ou por `dbwhere`.
- **Tabelas:** `iptuender`
- **Grau do resultado:** uma linha por matricula na tabela de endereco de entrega
- **Parametros:** `j43_matric`, `campos`, `ordem`, `dbwhere`
- **Juncoes:** nenhuma
- **Filtros e regras:**
  - Quando `dbwhere` esta vazio e `j43_matric` foi informado, filtra `iptuender.j43_matric = <matricula>`.
  - Nao enriquece com `iptubase`, `lote` ou `cgm`.
- **Campos relevantes:**
  - Todos os campos de endereco de entrega da tabela.
- **SQL normalizada:**

  ```sql
  select /* campos dinamicos */
    from iptuender
   where /* j43_matric ou dbwhere dinamico */
   order by /* ordem dinamica */
  ```

- **Cuidados:**
  - Consulta util como base de cadastro, mas sem contexto territorial ou do contribuinte.

### Consulta: `sql_query_endereco`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptuender_classe.php`
- **Objetivo:** tentar devolver a matricula com endereco de entrega e, na ausencia de dados de entrega, considerar o endereco do CGM.
- **Tabelas:** `iptubase`, `iptuender`, `cgm`
- **Grau do resultado:** pretendido como uma linha por matricula, mas a montagem atual parece estruturalmente fragil
- **Parametros:** `j43_matric`, `campos`, `ordem`, `dbwhere`
- **Juncoes:**
  - `iptuender.j43_matric = iptubase.j01_matric` `left join`
  - `cgm.z01_numcgm = iptubase.j01_numcgm` `inner join`
- **Filtros e regras:**
  - O codigo tenta restringir por `iptubase.j01_matric = <matricula>` quando `dbwhere` esta vazio.
  - O bloco `where_ender` exige ou endereco/caixa postal em `iptuender` ou endereco/caixa postal em `cgm`.
  - O SQL final usa `select * from ($sql and $sql2) as x where $where_ender`, o que aparenta ser incorreto ou ao menos muito arriscado.
- **Campos relevantes:**
  - `j43_ender`, `j43_cxpost`, `z01_ender`, `z01_cxpostal`
- **SQL normalizada:**

  ```sql
  select * from (
    select /* campos dinamicos */
      from iptubase
      left join iptuender on iptuender.j43_matric = iptubase.j01_matric
      inner join cgm on cgm.z01_numcgm = iptubase.j01_numcgm
     where /* filtro dinamico */
  ) as x
  where /* regra de endereco dinamica */
  ```

- **Cuidados:**
  - Nao encontrei chamada externa para este metodo no checkout, entao ele deve ser tratado como candidato interno, nao como regra consolidada.
  - A concatenacao final parece gerar SQL invalida em alguns caminhos, entao nao use esta consulta como referencia confiavel sem revalidar a classe em runtime.
  - Se a intencao for buscar matrículas com grupo de endereco, a RPC usa `sql_queryMatriculasAgrupadas()`, nao este metodo.

### Consulta: `sql_queryMatriculasAgrupadas`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptuender_classe.php`
- **Objetivo:** listar todas as matriculas que compartilham o mesmo grupo de endereco de entrega.
- **Tabelas:** `iptuender`
- **Grau do resultado:** uma linha por matricula dentro do grupo de endereco
- **Parametros:** `iGrupoEndereco`, `sCampos`, `sWhere`
- **Juncoes:** nenhuma
- **Filtros e regras:**
  - Aplica `where j43_iptuendergrupo = <grupo>`.
  - Se `sWhere` vier preenchido, acrescenta restricoes adicionais com `and`.
  - A RPC `cad4_iptuendergrupo.RPC.php` passa `j43_matric <> <matricula>`, entao a matricula base fica fora do retorno agrupado.
- **Campos relevantes:**
  - `j43_iptuendergrupo` identifica o grupo de endereco de entrega.
  - `j43_matric`, `j43_ender`, `j43_numimo`, `j43_comple`, `j43_munic` formam o conjunto reutilizado na tela de agrupamento.
- **SQL normalizada:**

  ```sql
  select /* campos dinamicos */
    from iptuender
   where j43_iptuendergrupo = :grupo_endereco
     and /* filtro adicional opcional */
  ```

- **Cuidados:**
  - O significado de negocio do grupo nao esta descrito em um manual proprio, mas o uso real mostra que ele serve para agrupar matriculas com o mesmo endereco de entrega.
  - Como o metodo aceita filtro extra livre, o resultado pode ser reduzido alem do grupo original.
- **Evidencia adicional:** consumido por `cad4_iptuendergrupo.RPC.php` ao carregar as matriculas do mesmo grupo.

### Regras de manutencao observadas

1. A classe trata `j43_matric` como identificador principal do cadastro de endereco de entrega.
2. `sql_query()` e a consulta mais rica para consumo de negocio, porque combina endereco com `iptubase`, `lote` e `cgm`.
3. `sql_query_file()` e a leitura direta do cadastro, sem enriquecimento.
4. `sql_query_endereco()` aparenta ter montagem fragil e deve ser tratada com cautela.
5. `sql_queryMatriculasAgrupadas()` e a consulta que suporta o agrupamento de enderecos de entrega.

### Cuidados / riscos

- Nao confundir endereco de entrega com endereco cadastral do contribuinte.
- Nao tratar `sql_query()` como lista de imoveis; o grao segue sendo a matricula com endereco de entrega.
- Nao assumir que `sql_query_endereco()` esteja funcional sem validar a sintaxe gerada.
- Nao inferir que toda matricula tenha grupo de endereco; o grupo e opcional.
- Se a pergunta for sobre entrega de carnes em massa, revisar tambem a RPC `cad4_iptuendergrupo.RPC.php`, porque ela mostra como o grupo e usado na pratica.
