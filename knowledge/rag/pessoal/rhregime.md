## pessoal.rhregime

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_rhregime_classe.php`

Cadastro de regime e vinculo funcional. A classe define o tipo de regime do servidor e e usada como referencia central por `rhpessoal`, `rhpessoalmov`, rescisao e rotinas de folha que dependem de situacao funcional.

### Resumo tecnico

- **Tipo de fonte:** classe DAO + consultas analiticas de pessoal
- **Tabela principal:** `pessoal.rhregime`
- **Chave operacional:** `rh30_codreg`
- **Grau base:** uma linha por regime/vinculo cadastrado
- **Uso funcional:** classificar o servidor como ativo, pensionista ou inativo e amarrar regras de folha

Interpretacao segura:

- `rhregime` nao representa a movimentacao do servidor, mas o catalogo do regime usado pela movimentacao.
- A classe carrega o regime, o vinculo, a natureza e os parametros de utilizacao ligados a ferias, admissao e provimento.
- Quase todas as consultas relevantes dependem deste cadastro para classificar a situacao do servidor.

### Campos de negocio confirmados

- `rh30_codreg`: codigo do vinculo/regime.
- `rh30_vinculomanad`: vinculo para Manad.
- `rh30_descr`: descricao.
- `rh30_regime`: codigo do regime.
- `rh30_vinculo`: situacao do vinculo.
- `rh30_instit`: instituicao.
- `rh30_naturezaregime`: natureza do regime.
- `rh30_utilizacao`: utilizacao.
- `rh30_periodoaquisitivo`: duracao do periodo aquisitivo.
- `rh30_periodogozoferias`: periodo de gozo.
- `rh30_vinculoemprego`: indica trabalhador com vinculo de emprego.
- `rh30_codigocategoria`: codigo de categoria.
- `rh30_admissao`: tipo de admissao.
- `rh30_provimento`: tipo de provimento.

### Regras de manutencao

- `incluir()` exige vinculo Manad, descricao, regime, situacao, instituicao, natureza, utilizacao, periodo aquisitivo, periodo de gozo, flag de vinculo de emprego e categoria.
- A chave `rh30_codreg` pode vir por parametro ou pela sequencia `rhregime_rh30_codreg_seq`.
- `alterar()` e `excluir()` trabalham diretamente sobre `rh30_codreg`.
- O cadastro registra auditoria em `db_acount*` quando a sessao nao desativa esse fluxo.

### Consulta: `sql_query`

#### Objetivo

Recuperar o regime com contexto cadastral da instituicao e classificacao administrativa.

#### Tabelas

- `pessoal.rhregime`
- `db_config`
- `pessoal.rhcadregime`
- `pessoal.rhnaturezaregime`
- `pessoal.vinculomanad`
- `cgm`
- `db_tipoinstit`

#### Juncoes principais

- `db_config.codigo = rhregime.rh30_instit` `inner join`
- `rhcadregime.rh52_regime = rhregime.rh30_regime` `inner join`
- `rhnaturezaregime.rh71_sequencial = rhregime.rh30_naturezaregime` `inner join`
- `vinculomanad.rh84_sequencial = rhregime.rh30_vinculomanad` `inner join`
- `cgm.z01_numcgm = db_config.numcgm` `inner join`
- `db_tipoinstit.db21_codtipo = db_config.db21_tipoinstit` `inner join`

#### Grau do resultado

- Uma linha por regime cadastrado.
- Como ha varios `inner join`, o registro precisa ter configuracao completa na instituicao para aparecer.

### Consulta: `sql_query_file`

- **Objetivo:** leitura bruta do cadastro de regime.
- **Uso seguro:** manutencao, auditoria e consultas simples sem enriquecimento.

### Consulta: `sql_query_servidorerPorVinculo`

- **Objetivo:** listar servidores por tipo de vinculo na competencia informada.
- **Tabelas:** `rhpessoalmov`, `rhpessoal`, `rhregime`, `rhpesrescisao`, `rhtipoapos`.
- **Regras chave:**
  - competencia e instituicao sao obrigatorias
  - vinculo `A` retorna ativos
  - vinculos `P` e `I` filtram inativos/pensionistas conforme o tipo informado
  - exige `rh05_seqpes is null`
- **Uso seguro:** recorte de servidores por situacao funcional.

### Consulta: `sql_query_rescisao`

- **Objetivo:** cruzar o regime com a tabela de rescisao da competencia atual.
- **Tabelas:** `rhregime` e `rescisao`.
- **Uso seguro:** verificar configuracao de rescisao associada ao regime.

### Consulta: `sql_query_servidores`

- **Objetivo:** listar servidores por tipo de regime na competencia.
- **Tabelas:** `rhpessoalmov` e `rhregime`.
- **Uso seguro:** base simples para recortes por regime na folha.

### Cuidados

- Nao confundir regime com movimentacao de pessoal: o regime e a classificacao, a movimentacao esta em `rhpessoalmov`.
- Este cadastro aparece como dependencia em consultas de folha, rescisao e situacao funcional; uma configuracao ausente pode derrubar joins.
- `sql_query_servidorerPorVinculo()` trata os vinculos ativos e inativos de forma diferente; isso importa na leitura das regras de folha.

### Perguntas que ela responde bem

- Qual e o regime cadastrado para este vinculo?
- O servidor e ativo, pensionista ou inativo?
- Quais servidores pertencem a um tipo de vinculo na competencia?
- Qual configuracao de ferias, admissao e provimento acompanha o regime?
- Qual regime a folha usa para classificar a situacao funcional?
