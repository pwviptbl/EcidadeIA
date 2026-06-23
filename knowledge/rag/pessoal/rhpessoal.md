## pessoal.rhpessoal

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_rhpessoal_classe.php`

Cadastro mestre do servidor. Esta classe representa a ficha principal da pessoa vinculada ao RH e cruza, na competencia atual, com `rhpessoalmov` para recuperar lotacao, cargo, regime, rescisao e contexto de folha.

### Resumo tecnico

- **Tipo de fonte:** classe DAO + consultas analiticas de pessoal
- **Tabela principal:** `pessoal.rhpessoal`
- **Chave operacional:** `rh01_regist`
- **Vinculo base:** `rh01_numcgm`
- **Grau base:** uma linha por servidor
- **Grau analitico comum:** servidor + competencia atual quando cruza com `rhpessoalmov`

Interpretacao segura:

- `rhpessoal` e o cadastro mestre, nao a movimentacao de competencia.
- A maioria das consultas importantes junta `rhpessoal` com `rhpessoalmov` para saber a situacao vigente na folha.
- A classe e usada como base para folha, ferias, rescisao, cedencia, consignacao, previdencia e eSocial.

### Campos de negocio confirmados

- `rh01_regist`: matricula.
- `rh01_numcgm`: vinculo com cadastro geral.
- `rh01_funcao`: cargo principal.
- `rh01_lotac`: lotacao de cadastro.
- `rh01_admiss`: data de admissao.
- `rh01_nasc`: data de nascimento.
- `rh01_nacion`: nacionalidade.
- `rh01_anoche`: ano de chegada.
- `rh01_instru`: grau de instrucao.
- `rh01_sexo`: sexo.
- `rh01_estciv`: estado civil.
- `rh01_tipadm`: tipo de admissao.
- `rh01_natura`: naturalidade.
- `rh01_raca`: raca/cor.
- `rh01_clas1`, `rh01_clas2`: classificacoes livres.
- `rh01_trienio`: marco de trienio.
- `rh01_progres`: marco de progressao.
- `rh01_instit`: instituicao.
- `rh01_vale`: adiantamento.
- `rh01_ponto`: numero do ponto.
- `rh01_depirf`: dependentes IRRF.
- `rh01_depsf`: dependentes salario familia.
- `rh01_observacao`: observacoes.
- `rh01_rhsindicato`: sindicato.
- `rh01_reajusteparidade`: tipo de reajuste.
- `rh01_registrapontoeletronico`: registra ponto eletronico.
- `rh01_matriculaanterior`: matricula anterior eSocial.

### Regras de manutencao

- `incluir()` exige `rh01_numcgm`, `rh01_admiss`, `rh01_nasc` e `rh01_nacion` como bases obrigatorias.
- `rh01_funcao` e `rh01_lotac` podem entrar como nulo/0 em alguns fluxos, mas a classe valida a maior parte dos campos essenciais.
- A chave primaria operacional e `rh01_regist`; nao ha chave sequencial como em `rhpessoalmov`.
- O cadastro grava auditoria em `db_acount*` quando a sessao nao desativa esse fluxo.
- `alterar()` e `excluir()` trabalham pelo registro e, opcionalmente, por `dbwhere`.

### Consulta: `sql_query`

#### Objetivo

Recuperar o cadastro do servidor com o contexto da competencia atual da folha.

#### Tabelas

- `pessoal.rhpessoal`
- `pessoal.rhpessoalmov`
- `pessoal.rhlota`
- `cgm`
- `db_config`
- `pessoal.rhestcivil`
- `pessoal.rhraca`
- `pessoal.rhfuncao`
- `pessoal.rhinstrucao`
- `pessoal.rhnacionalidade`
- `pessoal.rhpesrescisao`
- `pessoal.rhsindicato`
- `pessoal.rhreajusteparidade`

#### Juncoes principais

- `rhpessoalmov.rh02_regist = rhpessoal.rh01_regist` `left join`
- `rhpessoalmov.rh02_anousu = DBPessoal::getAnoFolha()` e `rh02_mesusu = DBPessoal::getMesFolha()` `left join`
- `rhpessoalmov.rh02_instit = db_getsession("DB_instit")` `left join`
- `rhlota.r70_codigo = rhpessoalmov.rh02_lota and r70_instit = rhpessoalmov.rh02_instit` `left join`
- `cgm.z01_numcgm = rhpessoal.rh01_numcgm` `inner join`
- `db_config.codigo = rhpessoal.rh01_instit` `inner join`
- `rhestcivil.rh08_estciv = rhpessoal.rh01_estciv` `inner join`
- `rhraca.rh18_raca = rhpessoal.rh01_raca` `inner join`
- `rhfuncao.rh37_funcao = rhpessoalmov.rh02_funcao and rh37_instit = rhpessoalmov.rh02_instit` `left join`
- `rhinstrucao.rh21_instru = rhpessoal.rh01_instru` `inner join`
- `rhnacionalidade.rh06_nacionalidade = rhpessoal.rh01_nacion` `inner join`
- `rhpesrescisao.rh05_seqpes = rhpessoalmov.rh02_seqpes` `left join`
- `rhsindicato.rh116_sequencial = rhpessoal.rh01_rhsindicato` `left join`
- `rhreajusteparidade.rh148_sequencial = rhpessoal.rh01_reajusteparidade` `inner join`

#### Grau do resultado

- Uma linha por servidor, enriquecida com o contexto da folha atual quando existe movimentacao na competencia.
- Se o servidor nao tiver movimento na competencia atual, parte do contexto funcional pode vir nula por causa dos `left join`.

### Consulta: `sql_query_file`

- **Objetivo:** leitura bruta do cadastro de servidor.
- **Uso seguro:** base simples para manutencao, listagens e auditoria.

### Consulta: `sql_query_cgm`

- **Objetivo:** trazer servidor com o contexto de CGM, lotacao e movimentacao atual.
- **Uso seguro:** consultas de ficha funcional e identificacao.

### Consulta: `sql_query_cgm_instituicoes`

- **Objetivo:** listar o servidor considerando um conjunto de instituicoes.
- **Uso seguro:** cenarios multi-instituicao.

### Consulta: `sql_query_matriculas_ativas`

- **Objetivo:** resolver matriculas ativas do mesmo CGM na competencia.
- **Regras chave:**
  - usa CTE para achar o CGM da matricula base
  - cruza com `rhpessoalmov` da competencia
  - descarta regime do tipo `I`
  - retorna apenas vinculos sem rescisao vigente
- **Uso seguro:** descobrir matriculas vigentes e duplo vinculo.

### Consulta: `sql_query_rescisao`

- **Objetivo:** trazer rescisao associada ao cadastro na competencia atual.
- **Tabelas:** `rhpessoal`, `rhpessoalmov`, `rhregime`, `cgm`, `rhpesrescisao`.
- **Uso seguro:** verificacao de desligamento/amarracao de rescisao.

### Consulta: `sql_query_cedencia`

- **Objetivo:** trazer dados de cedencia do servidor.
- **Tabelas:** `rhpessoal` e `rhcedencia`.

### Consulta: `sql_query_pesdoc`

- **Objetivo:** cruzar servidor com documentos pessoais.
- **Tabelas:** `rhpessoal`, `rhpesdoc`, `rhpessoalmov`, `rhpesrescisao`.

### Consulta: `sql_query_ferias`

- **Objetivo:** listar dados de ferias com contexto funcional da competencia atual.
- **Tabelas:** `rhpessoal`, `rhpessoalmov`, `rhlota`, `cgm`, `rhfuncao`, `rhregime`, `rhpesrescisao`, `cadferia`, `rhiperegist`, `rhipe`.

### Consulta: `sql_query_pesquisa`

- **Objetivo:** base de pesquisa ampla do servidor com regime, cargo, padrao, rescisao e tabela de previdencia.
- **Uso seguro:** telas de busca e relatorios analiticos.

### Consulta: `sql_query_afasta`

- **Objetivo:** montar base para afastamentos e situacoes relacionadas.
- **Tabelas:** `rhpessoal`, `rhpessoalmov`, `rhlota`, `cgm`, `rhfuncao`, `rhregime`, `rhpesrescisao`, `cadferia`, `afasta`.

### Consulta: `sql_query_cgmmov`

- **Objetivo:** cruzar `rhpessoal` com a movimentacao corrente e regime.
- **Uso seguro:** consultas de identificacao funcional na folha.

### Consulta: `sql_query_relPREVID`

- **Objetivo:** montar base para relatorios previdenciarios a partir de arquivos de calculo.
- **Uso seguro:** extracoes de previdencia e bases de folha.

### Consulta: `sql_query_lotafuncres`

- **Objetivo:** recuperar lotacao, cargo, funcao, regime, rescisao e padrao.
- **Uso seguro:** relatorios funcionais.

### Consulta: `sql_query_cgmmovpad`

- **Objetivo:** cruzar servidor, movimentacao e padrao.

### Consulta: `sql_query_cargo`

- **Objetivo:** retornar o cargo atual do servidor na competencia da folha.

### Consulta: `sql_query_func_rhpessoal`

- **Objetivo:** base funcional ampla com variantes para ferias e contratos temporarios.
- **Casos especiais:**
  - `1`: periodos aquisitivos alteraveis
  - `2`: servidores com periodo a gozar
  - `3`: periodos de gozo agendados
  - `4`: servidores com periodos aquisitivos sem ferias cadastradas

### Consulta: `sql_query_baseRelatorios`

- **Objetivo:** gerar base padrao para relatorios da folha.
- **Tabelas:** `rhpessoal`, `rhpessoalmov`, tabela de calculo informada, `rhrubricas`, `rhrubelemento`, `rhrubretencao` e estrutura orcamentaria/funcional de apoio.
- **Uso seguro:** backbone de diversos relatorios de folha.

### Consulta: `sql_queryInsntituicoesServidoresVinculo`

- **Objetivo:** recuperar instituicoes por servidor/vinculo.

### Consulta: `sql_queryMargemEConsig`

- **Objetivo:** calcular margem e consignacao por competencia.

### Consulta: `sql_queryServidoresConsignar`

- **Objetivo:** listar servidores para consignacao/E-consig.
- **Uso seguro:** base de integracoes financeiras.

### Consulta: `sql_queryReajuste`

- **Objetivo:** selecionar aposentados conforme tipo de reajuste.

### Consulta: `sql_verificaSituacaoServidor`

- **Objetivo:** verificar situacao do servidor na competencia, incluindo rescisao.

### Consulta: `sql_query_com_temporarios`

- **Objetivo:** base de servidor com contratos temporarios e dados complementares de cadastro.

### Consulta: `sql_query_baseRelatoriosComplementar`

- **Objetivo:** base para relatorios quando a estrutura suplementar esta ativa.

### Consulta: `sqlServidorSemVinculoESocial`

- **Objetivo:** montar dados eSocial de servidor sem vinculo.

### Cuidados

- Nao confundir este cadastro com `rhpessoalmov`: aqui o foco e o servidor, nao a foto da competencia.
- Muitos metodos assumem a competencia corrente da folha via `DBPessoal::getAnoFolha()` e `DBPessoal::getMesFolha()`.
- Quase todos os relatorios relevantes dependem de `rhpessoalmov`; sem essa movimentacao o contexto funcional fica incompleto.
- Varios trechos sao legados e extensos; para alteracao de regra, vale verificar qual consulta a tela realmente usa antes de tocar no restante.

### Perguntas que ela responde bem

- Qual e o cadastro mestre do servidor?
- Qual e a matricula ligada ao CGM?
- O servidor tem rescisao, cedencia, ferias ou afastamento associado?
- Quais matriculas estao ativas para o mesmo CPF/CGM?
- Qual a base funcional usada pela folha e pelos relatorios de pessoal?
