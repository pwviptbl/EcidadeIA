## cadastro.iptuisen

> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptuisen`
> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_iptuisen_classe.php`

### Resumo tecnico

- Descricao: cadastro de isencoes de IPTU por matricula, com periodo de vigencia, percentual e historico.
- Chave primaria: `j46_codigo`
- Chave de negocio: `j46_codigo`
- Coluna de tempo: `j46_dtini`, `j46_dtfim`, `j46_dtinc`
- Grao: uma linha por isencao cadastrada; algumas consultas ampliam o resultado com tipo, lote, contribuinte e taxas isentas
- Recomendada: sim
- Significado da contagem: conta isencoes cadastradas, nao matriculas.
- Candidatas a chave de negocio: `j46_codigo`, `j46_matric`, `j46_tipo`
- Candidatas a coluna de tempo: `j46_dtini`, `j46_dtfim`, `j46_dtinc`

### Relacionamentos

- `j46_matric` -> `cadastro.iptubase` (`j01_matric`) [iptuisen_matric_fk]
- `j46_tipo` -> `cadastro.tipoisen` (`j45_tipo`) [iptuisen_tipo_fk]
- `j46_codigo` -> `cadastro.isenexe` (`j47_codigo`) [isenexe_isencao_fk]
- `j46_codigo` -> `cadastro.isentaxa` (`j56_codigo`) [isentaxa_isencao_fk]

### Perguntas que esta tabela ajuda a responder

- Qual isencao esta cadastrada para uma matricula?
- Qual o periodo de vigencia de uma isencao?
- Qual o percentual de desconto/isencao aplicado?
- Quais matriculas possuem isencao vigente no exercicio?
- Qual a descricao do tipo de isencao usada em certidao ou emissao?
- Quais taxas foram vinculadas a uma isencao?

### Filtros e regras reaproveitaveis

#### Filtros padrao

- Isencao especifica: `j46_codigo = :codigo_isencao`
- Matricula especifica: `j46_matric = :matricula`
- Tipo de isencao: `j46_tipo = :tipo_isencao`
- Exercizio da isencao: `j47_anousu = :anousu` quando o filtro passa por `isenexe`

#### Semantica de filtros

- `j46_matric` liga a isencao ao imovel cadastrado em `iptubase`.
- `j46_tipo` liga a isencao ao motivo/regra cadastrada em `tipoisen`.
- `j46_dtini`, `j46_dtfim` e `j46_dtinc` delimitam vigencia e inclusao.
- `j46_arealo` aparece como area de lote em metros quadrados e deve ser tratado como dado complementar, nao como medida universal da isencao.

### Consulta: `sql_query`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptuisen_classe.php`
- **Objetivo:** ler a isencao com enriquecimento cadastral do imovel, tipo e eventuais taxas isentas.
- **Tabelas:** `iptuisen`, `iptubase`, `tipoisen`, `lote`, `cgm`, `isentaxa`
- **Grau do resultado:** uma linha por isencao, podendo multiplicar por linhas de `isentaxa` quando houver mais de uma taxa vinculada
- **Parametros:** `j46_codigo` filtra a isencao; `campos` escolhe colunas; `ordem` define ordenacao; `dbwhere` substitui o filtro por codigo
- **Juncoes:**
  - `iptubase.j01_matric = iptuisen.j46_matric` `inner join`
  - `tipoisen.j45_tipo = iptuisen.j46_tipo` `inner join`
  - `lote.j34_idbql = iptubase.j01_idbql` `inner join`
  - `cgm.z01_numcgm = iptubase.j01_numcgm` `inner join`
  - `isentaxa.j56_codigo = iptuisen.j46_codigo` `left join`
- **Filtros e regras:**
  - Quando `dbwhere` esta vazio e `j46_codigo` foi informado, filtra `iptuisen.j46_codigo = <codigo>`.
  - Os `inner join` exigem matricula, tipo, lote e contribuinte validos para a linha aparecer.
  - O `left join` com `isentaxa` preserva a isencao mesmo sem taxa vinculada, mas pode multiplicar linhas quando houver mais de uma isentaxa.
- **Campos relevantes:**
  - `j46_codigo` identifica a isencao.
  - `j46_matric`, `j46_tipo`, `j46_dtini`, `j46_dtfim`, `j46_perc`, `j46_dtinc`, `j46_idusu`, `j46_hist`, `j46_arealo`.
  - `j45_descr` e `j56_receit`, `j56_perc` sao usados nas telas para explicar motivo e taxa isenta.
- **SQL normalizada:**

  ```sql
  select /* campos dinamicos */
    from iptuisen
    inner join iptubase on iptubase.j01_matric = iptuisen.j46_matric
    inner join tipoisen on tipoisen.j45_tipo = iptuisen.j46_tipo
    inner join lote on lote.j34_idbql = iptubase.j01_idbql
    inner join cgm on cgm.z01_numcgm = iptubase.j01_numcgm
    left join isentaxa on isentaxa.j56_codigo = iptuisen.j46_codigo
   where /* j46_codigo ou dbwhere dinamico */
   order by /* ordem dinamica */
  ```

- **Cuidados:**
  - Como `isentaxa` e `left join`, o resultado pode duplicar a mesma isencao por receita/taxa.
  - Se a analise for apenas da isencao cadastrada, `sql_query_file()` e mais segura.
  - A consulta depende de dados de `iptubase` e `tipoisen`; sem eles a isencao nao aparece.
- **Evidencia adicional:** usada em `cad4_iptuisen002.php` para carregar o cadastro completo da isencao.

### Consulta: `sql_query_file`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptuisen_classe.php`
- **Objetivo:** leitura direta da tabela `iptuisen` por codigo ou por filtro livre.
- **Tabelas:** `iptuisen`
- **Grau do resultado:** uma linha por isencao cadastrada
- **Parametros:** `j46_codigo`, `campos`, `ordem`, `dbwhere`
- **Juncoes:** nenhuma
- **Filtros e regras:**
  - Quando `dbwhere` esta vazio e `j46_codigo` foi informado, filtra `iptuisen.j46_codigo = <codigo>`.
  - Nao enriquece com lote, contribuinte, tipo ou taxas.
- **Campos relevantes:**
  - Todos os campos brutos da isencao.
- **SQL normalizada:**

  ```sql
  select /* campos dinamicos */
    from iptuisen
   where /* j46_codigo ou dbwhere dinamico */
   order by /* ordem dinamica */
  ```

- **Cuidados:**
  - Consulta util para manutenção e validação de persistencia.
  - Nao responde sozinha qual e o motivo da isencao, porque isso vem de `tipoisen`.

### Consulta: `sql_query_isen`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptuisen_classe.php`
- **Objetivo:** montar uma visao mais ampla da isencao com tipo, proprietario, promitente, processo e condominio.
- **Tabelas:** `iptuisen`, `tipoisen`, `proprietario`, `isenproc`, `promitente`, `cgm`, `iptubasecondominio`, `condominio`
- **Grau do resultado:** uma linha por isencao, podendo ampliar por relacionamentos opcionais de proprietario, promitente e condominio
- **Parametros:** `j46_codigo`, `campos`, `ordem`, `dbwhere`
- **Juncoes:**
  - `j45_tipo = j46_tipo` `inner join` com `tipoisen`
  - `j01_matric = j46_matric` `inner join` com `proprietario`
  - `j61_codigo = j46_codigo` `left join` com `isenproc`
  - `promitente.j41_matric = j46_matric` `left join`
  - `promitente.j41_numcgm = cgm.z01_numcgm` `left join`
  - `proprietario.z01_numcgm = cgm_propri.z01_numcgm` `left join`
  - `j108_matric = j46_matric` `left join` com `iptubasecondominio`
  - `j108_condominio = j107_sequencial` `left join` com `condominio`
- **Filtros e regras:**
  - Quando `dbwhere` esta vazio e `j46_codigo` foi informado, filtra `iptuisen.j46_codigo = <codigo>`.
  - Os dados de promitente e condominio sao opcionais; o registro continua aparecendo sem eles.
  - O join com proprietario parece assumir o conceito de proprietario principal da matricula.
- **Campos relevantes:**
  - `j45_tipo`, `j45_descr`, `j45_obscertidao`
  - `j41_tipopro`
  - `j61_codigo`
  - `j107_nome`
  - `proprietario.*`, `cgm_propri.z01_cgccpf`, `cgm.z01_nome`, `cgm.z01_cgccpf`
- **SQL normalizada:**

  ```sql
  select /* campos dinamicos */
    from iptuisen
    inner join tipoisen on j45_tipo = j46_tipo
    inner join proprietario on j01_matric = j46_matric
    left join isenproc on j61_codigo = j46_codigo
    left join promitente on promitente.j41_matric = j46_matric
    left join cgm on promitente.j41_numcgm = cgm.z01_numcgm
    left join cgm as cgm_propri on proprietario.z01_numcgm = cgm_propri.z01_numcgm
    left join iptubasecondominio on j46_matric = j108_matric
    left join condominio on j108_condominio = j107_sequencial
   where /* j46_codigo ou dbwhere dinamico */
   order by /* ordem dinamica */
  ```

- **Cuidados:**
  - Esta consulta e mais ampla e depende de varios relacionamentos opcionais.
  - Se faltar dado em `promitente`, `isenproc` ou condominio, parte do enriquecimento vira `null`.
  - Como a query nao qualifica todos os aliases de forma explicita, convem manter o filtro simples quando for usar em documento ou tela nova.

### Consulta: `sql_queryIsencao`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptuisen_classe.php`
- **Objetivo:** recuperar o tipo e a descricao da isencao no exercicio informado.
- **Tabelas:** `iptuisen`, `isenexe`, `tipoisen`
- **Grau do resultado:** uma linha por isencao no exercicio da matricula; se nao houver isencao no exercicio, nao retorna registro
- **Parametros:** `iAnousu`, `iMatricula`
- **Juncoes:**
  - `j46_codigo = j47_codigo` `inner join` com `isenexe`
  - `j46_tipo = j45_tipo` `inner join` com `tipoisen`
- **Filtros e regras:**
  - Filtra pela matricula e pelo exercicio do ano vigente informado.
  - O retorno fica limitado ao tipo de isencao e sua descricao.
- **Campos relevantes:**
  - `j45_tipo`
  - `j45_descr`
- **SQL normalizada:**

  ```sql
  select j45_tipo, j45_descr
    from iptuisen
    inner join isenexe on j46_codigo = j47_codigo
    inner join tipoisen on j46_tipo = j45_tipo
   where j46_matric = :matricula
     and j47_anousu = :anousu
  ```

- **Cuidados:**
  - Este metodo e o melhor contrato para responder "qual isencao vale neste exercicio?".
  - A ausencia de linha pode significar que a isencao nao vale no ano consultado, nao apenas que a matricula nao existe.
- **Evidencia adicional:** consumido por `model/cadastro/Imovel.model.php`, `cad2_certisen002.php`, `cad4_emissaogeralisencao002.php` e `app/Domain/Tributario/Cadastro/Services/CadastroIsencaoIptuService.php`.

### Regras de manutencao observadas

1. `j46_codigo` e a chave principal operacional da isencao.
2. `sql_query()` e a melhor consulta para detalhamento cadastral, mas pode multiplicar linhas quando ha varias `isentaxa`.
3. `sql_query_file()` serve como base bruta de manutencao.
4. `sql_query_isen()` e a visao analitica ampla com proprietario, promitente e condominio.
5. `sql_queryIsencao()` e o helper mais apropriado para verificacao da isencao do exercicio corrente.

### Cuidados / riscos

- Nao confundir isencao de IPTU com isencao de taxa: a classe permite amarrar ambas, mas o significado muda conforme a consulta.
- Nao assumir que toda matricula tem isencao vigente.
- Nao usar `sql_query()` como contagem simples de isencoes sem considerar a multiplicacao por `isentaxa`.
- Em certidoes, a regra do promitente pode alterar o nome exibido; isso vem dos consumidores, nao da classe sozinha.
- Se a fonte aparecer sem `isenexe`, a leitura anual nao e segura.
