## pessoal.rhpessoalmov

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_rhpessoalmov_classe.php`

Cadastro de movimentacao de pessoal por competencia. A classe guarda a situacao funcional do servidor em um mes/ano da instituicao e serve como base para consultas de folha, rescisao, dados bancarios, duplo vinculo e extracoes gerenciais.

### Resumo tecnico

- **Tipo de fonte:** classe DAO + consultas analiticas de pessoal
- **Tabela principal:** `pessoal.rhpessoalmov`
- **Chave operacional:** `rh02_seqpes`
- **Contexto obrigatorio:** `rh02_instit`, `rh02_anousu`, `rh02_mesusu`, `rh02_regist`
- **Grau base:** uma linha por movimentacao de pessoal na competencia
- **Identidade pratica da linha:** matricula + instituicao + competencia + sequencia

Interpretacao segura:

- Nao e apenas um cadastro de servidor. E a foto da movimentacao do servidor em uma competencia.
- A classe carrega muitos campos de lotacao, cargo, regime, folha, previdencia e afastamentos para uso em rotinas de folha.
- `rh02_seqpes` e a chave usada em quase todas as rotinas de manutencao e leitura.

### Campos de negocio confirmados

- `rh02_instit`: instituicao.
- `rh02_seqpes`: sequencia da movimentacao.
- `rh02_anousu`, `rh02_mesusu`: competencia.
- `rh02_regist`: matricula.
- `rh02_codreg`: codigo do regime.
- `rh02_tipsal`: tipo de salario.
- `rh02_folha`: tipo de folha.
- `rh02_fpagto`: pagamento.
- `rh02_tbprev`: tabela de previdencia.
- `rh02_hrsmen`, `rh02_hrssem`: jornada mensal e semanal.
- `rh02_ocorre`: agentes nocivos.
- `rh02_equip`: equiparacao.
- `rh02_tpcont`: tipo de contrato.
- `rh02_vincrais`: vinculo.
- `rh02_salari`: salario.
- `rh02_lota`: lotacao.
- `rh02_funcao`: cargo.
- `rh02_rhtipoapos`: tipo de aposentadoria/pensao.
- `rh02_validadepensao`: validade da pensao.
- `rh02_deficientefisico`: deficiente fisico.
- `rh02_portadormolestia`: portador de molestia.
- `rh02_datalaudomolestia`: data do laudo.
- `rh02_tipodeficiencia`: tipo de deficiencia.
- `rh02_abonopermanencia`: abono permanencia.
- `rh02_diasgozoferias`: dias padrao a gozar.
- `rh02_horasdiarias`: horas diarias.
- `rh02_cedencia`, `rh02_onus`, `rh02_ressarcimento`: cedencia e onus.
- `rh02_datacedencia`: data da movimentacao de cedencia.
- `rh02_cnpjcedencia`: CNPJ de origem/destino.
- `rh02_regimejornadatrabalho`: regime da jornada.
- `rh02_dataabonopermanencia`: inicio do abono.
- `rh02_descinstrumento`: descricao do instrumento.
- `rh02_sitpagbeneficio`: pensao concedida judicial.

### Regras de manutencao

- `incluir()` exige, no minimo, ano, mes, registro, regime, tipo de salario, tipo de folha, pagamento, tabela de previdencia, horas, equiparacao, vinculo, lotacao, cargo e varios campos obrigatorios de status.
- A chave `rh02_seqpes` pode vir por parametro ou sequencia `rhpessoalmov_rh02_seqpes_seq`.
- O registro e gravado com auditoria em `db_acount*` quando a sessao nao desativa esse fluxo.
- `alterar()` e `excluir()` trabalham com `rh02_seqpes` e `rh02_instit` como identificacao operacional.
- `sql_record()` trata tabela vazia como erro de leitura.

### Consulta: `sql_query`

#### Objetivo

Recuperar a movimentacao de pessoal com contexto cadastral e estrutural para exibicao e analise.

#### Tabelas

- `pessoal.rhpessoalmov`
- `pessoal.rhpessoal`
- `db_config`
- `pessoal.rhlota`
- `pessoal.rhregime`
- `cgm`
- `db_estrutura`
- `pessoal.tipodeficiencia`

#### Juncoes principais

- `rhpessoal.rh01_regist = rhpessoalmov.rh02_regist` `inner join`
- `db_config.codigo = rhpessoalmov.rh02_instit` `inner join`
- `rhlota.r70_codigo = rhpessoalmov.rh02_lota and rhlota.r70_instit = rhpessoalmov.rh02_instit` `inner join`
- `rhregime.rh30_codreg = rhpessoalmov.rh02_codreg and rhregime.rh30_instit = rhpessoalmov.rh02_instit` `inner join`
- `cgm.z01_numcgm = db_config.numcgm` `inner join`
- `db_estrutura.db77_codestrut = rhlota.r70_codestrut` `inner join`
- `tipodeficiencia.rh150_sequencial = rhpessoalmov.rh02_tipodeficiencia` `left join`

#### Filtros

- `rh02_seqpes`
- `rh02_instit`
- ou `dbwhere` livre

#### Grau do resultado

- Uma linha por movimentacao filtrada.
- Como ha varios `inner join`, um cadastro incompleto em lotacao, regime ou configuracao institucional derruba o resultado.

### Consulta: `sql_query_file`

- **Objetivo:** leitura bruta da tabela de movimentacao.
- **Tabelas:** `rhpessoalmov` e, opcionalmente, `rhpessoal` quando `validaRhPessoal = true`.
- **Uso seguro:** base para manutencao e auditoria quando nao se quer o peso dos joins da consulta principal.

### Consulta: `sql_query_rescisao`

- **Objetivo:** localizar a movimentacao e a rescisao associada.
- **Tabelas:** `rhpessoalmov` e `rhpesrescisao`.
- **Join:** `rhpesrescisao.rh05_seqpes = rhpessoalmov.rh02_seqpes` `left join`
- **Uso seguro:** verificar se a movimentacao possui registro de rescisao amarrado.

### Consulta: `sql_query_parametros`

- **Objetivo:** buscar a movimentacao de uma matricula em uma competencia.
- **Tabelas:** `rhpessoalmov` e `rhregime`.
- **Filtros:** `rh02_regist`, `rh02_anousu`, `rh02_mesusu`.
- **Uso seguro:** ponto de entrada para rotinas que precisam do regime da competencia.

### Consulta: `sql_query_faixasSalariais`

- **Objetivo:** consolidar proventos por servidor e agrupar por regime, lotacao, cargo ou geral.
- **Tabelas de apoio:** `gerfsal`, `gerfcom`, `gerfres`, `gerfs13`, `rhpessoal`, `rhpessoalmov`.
- **Regras chave:**
  - filtra `pd = 1`
  - ignora rubricas a partir de `R950`
  - respeita selecao adicional via `sSelecao`
  - trata complementar com `r48_semest`
- **Grau do resultado:** um somatorio por servidor e agrupador.

### Consulta: `sql_query_dados_bancario`

- **Objetivo:** relacionar a movimentacao com os dados bancarios do servidor.
- **Tabelas:** `rhpessoalmov` e `rhpesbanco`.
- **Uso seguro:** extracao de folha/pagamento.

### Consulta: `sql_queryFinanceiroPeloCodigo`

- **Objetivo:** montar extracao financeira por rubrica, matricula, lotacao, cargo e recurso.
- **Tabelas:** tabela de calculo passada por parametro, `rhpessoalmov`, `rhpessoal`, `rhregime`, `rhlota`, `rhlotaexe`, `rhlotavinc`, `rhfuncao`, `rhpescargo`, `rhcargo`, `rhrubricas`, `orctiporec`, `cgm`, `orcorgao`.
- **Uso seguro:** analitico de folha para financeiro/orcamento.

### Consulta: `sql_query_baseServidores`

- **Objetivo:** montar base ampla de servidores com dados cadastrais, funcionais, previdenciarios, bancarios e de afastamento.
- **Estruturas auxiliares:** CTE `pensao` e CTE `rhipe`.
- **Uso seguro:** consultas gerenciais e exportacoes mais completas.

### Consulta: `sql_queryDadosServidor`

- **Objetivo:** retornar os dados do servidor em uma competencia.
- **Tabelas:** `rhpessoal` e `rhpessoalmov`.
- **Uso seguro:** leitura simples de um servidor com recorte temporal.

### Consulta: `sql_queryPaginacao`

- **Objetivo:** buscar matricula anterior e posterior com criterio de calculo e filtro opcional de lotacao.
- **Uso seguro:** navegacao entre servidores em telas de folha.

### Consultas auxiliares

- `sql_servidorCargoLotacaoSecretarias`: lista servidores por cargo, lotacao e secretarias.
- `sql_query_matricula_cgm`: relaciona movimentacao com `cgm`.
- `sql_query_file_regime`: cruza movimentacao com regime e cadastro de regime.
- `sql_query_movimentacao`: monta o detalhamento completo da movimentacao, com dados de cargo, lotacao, banco, padrao, cargo emergencial, instrucao, estado civil, etc.
- `sql_duplo_vinculo`, `sql_duplo_vinculo_matricula`, `sql_servidores_duplo_vinculo`, `sql_servidores_duplo_vinculo_rescindidos`: tratamento de duplo vinculo por competencia.
- `isRescindido`: valida se a matricula tem rescisao.

### Cuidados

- Nao confundir esta classe com o cadastro mestre `rhpessoal`; aqui o foco e a movimentacao por competencia.
- Muitas consultas usam `inner join` e vao eliminar linhas quando falta configuracao de lotacao, regime, orcamento ou pessoa.
- Varios metodos antigos usam `split()` e logica legada de PHP/SQL; mantenha compatibilidade ao ajustar.
- Para perguntas de folha, esta e uma fonte base de contexto, nao o calculo final.

### Perguntas que ela responde bem

- Qual e a movimentacao do servidor na competencia?
- Qual regime, lotacao, cargo e salario estavam vigentes?
- A matricula esta rescindida ou possui dupla vinculo?
- Quais dados bancarios estao amarrados a movimentacao?
- Qual a base funcional usada pelas rotinas de folha e financeiro?
