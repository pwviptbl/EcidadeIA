## pessoal.rhempenhofolha

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_rhempenhofolha_classe.php`

Cadastro da folha que origina empenhos de pessoal. A classe concentra o cabecalho da folha, os vinculos com empenho e as consultas analiticas usadas pelo relatorio de empenho da folha.

### Resumo tecnico

- **Tipo de fonte:** classe DAO + consultas analiticas de folha
- **Tabela principal:** `pessoal.rhempenhofolha`
- **Chave operacional do cabecalho:** `rh72_sequencial`
- **Competencia:** `rh72_anousu`, `rh72_mesusu`
- **Tipo de empenho:** `rh72_tipoempenho`
- **Sigla do arquivo/ponto:** `rh72_siglaarq`
- **Organizacao orcamentaria:** `rh72_orgao`, `rh72_unidade`, `rh72_projativ`, `rh72_recurso`, `rh72_codele`
- **Grão base:** uma linha por folha
- **Grão analitico de rubricas:** uma linha por folha x rubrica associada

Interpretacao segura:

- A folha e o cabecalho de origem do processo de empenho do pessoal.
- O `numemp` nao esta gravado no cabecalho principal; ele surge pelo vinculo `rhempenhofolhaempenho`.
- O valor da folha aparece nas rubricas da tabela filha `rhempenhofolharubrica`, nao no cabecalho.

### Campos de negocio confirmados

- `rh72_sequencial`: identificador da folha.
- `rh72_coddot`: dotacao orcamentaria.
- `rh72_codele`: elemento orcamentario.
- `rh72_unidade`: unidade orcamentaria.
- `rh72_orgao`: orgao orcamentario.
- `rh72_projativ`: projeto/atividade.
- `rh72_anousu`: exercicio.
- `rh72_recurso`: recurso orcamentario.
- `rh72_mesusu`: mes de referencia.
- `rh72_siglaarq`: sigla do arquivo ou ponto.
- `rh72_tipoempenho`: tipo de empenho.
- `rh72_tabprev`: tabela de previdencia.
- `rh72_seqcompl`: sequencia da folha complementar.
- `rh72_concarpeculiar`: caracteristica peculiar.
- `rh72_funcao`, `rh72_subfuncao`, `rh72_programa`: classificacao funcional/programatica.
- `rh72_credor`: credor associado.
- `rh72_finalidadepagamentofundeb`: finalidade de pagamento do FUNDEB.

### Consulta: `sql_query`

#### Objetivo

Recuperar a folha com contexto orcamentario, estrutural e de configuracao institucional.

#### Tabelas

- `pessoal.rhempenhofolha`
- `orcamento.orctiporec`
- `orcamento.orcfuncao`
- `orcamento.orcsubfuncao`
- `orcamento.orcprograma`
- `orcamento.orcelemento`
- `orcamento.orcprojativ`
- `orcamento.orcunidade`
- `orcamento.orcdotacao`
- `orcamento.concarpeculiar`
- `orcamento.db_estruturavalor`
- `db_config`
- `orcamento.orcproduto`
- `orcamento.orcorgao`
- `orcamento.ppasubtitulolocalizadorgasto`
- `orcamento.concarpeculiarclassificacao`
- `empenho.finalidadepagamentofundeb`

#### Juncoes principais

- `orctiporec.o15_codigo = rhempenhofolha.rh72_recurso` `inner join`
- `orcfuncao.o52_funcao = rhempenhofolha.rh72_funcao` `left join`
- `orcsubfuncao.o53_subfuncao = rhempenhofolha.rh72_subfuncao` `left join`
- `orcprograma.o54_anousu = rhempenhofolha.rh72_anousu and o54_programa = rh72_programa` `left join`
- `orcelemento.o56_codele = rhempenhofolha.rh72_codele and o56_anousu = rh72_anousu` `inner join`
- `orcprojativ.o55_anousu = rhempenhofolha.rh72_anousu and o55_projativ = rh72_projativ` `inner join`
- `orcunidade.o41_anousu = rhempenhofolha.rh72_anousu and o41_orgao = rh72_orgao and o41_unidade = rh72_unidade` `inner join`
- `orcdotacao.o58_anousu = rhempenhofolha.rh72_coddot and o58_coddot = rh72_anousu` `left join`
- `concarpeculiar.c58_sequencial = rhempenhofolha.rh72_concarpeculiar` `inner join`
- `db_estruturavalor.db121_sequencial = orctiporec.o15_db_estruturavalor` `inner join`
- `db_config.codigo = orcprojativ.o55_instit` `inner join`
- `orcproduto.o22_codproduto = orcprojativ.o55_orcproduto` `inner join`
- `orcorgao.o40_anousu = orcunidade.o41_anousu and o40_orgao = o41_orgao` `inner join`
- `ppasubtitulolocalizadorgasto.o11_sequencial = orcdotacao.o58_localizadorgastos` `inner join`
- `concarpeculiarclassificacao.c09_sequencial = concarpeculiar.c58_tipo` `inner join`
- `finalidadepagamentofundeb.e151_sequencial = rhempenhofolha.rh72_finalidadepagamentofundeb` `inner join`

#### Uso seguro

- Use esta consulta para recuperar a folha com a classificacao orcamentaria completa.
- A combinacao de joins e ampla e pode eliminar registros se qualquer configuracao relacionada estiver ausente.
- A classe tambem expõe `sql_query_file()` para leitura bruta da folha.

### Consulta: `sql_query_rubricas`

- **Objetivo:** listar a folha com suas rubricas associadas.
- **Tabelas:** `rhempenhofolha`, `rhempenhofolharhemprubrica`, `rhempenhofolharubrica`
- **Juncoes:**
  - `rhempenhofolharhemprubrica.rh81_rhempenhofolha = rhempenhofolha.rh72_sequencial` `left join`
  - `rhempenhofolharubrica.rh73_sequencial = rhempenhofolharhemprubrica.rh81_rhempenhofolharubrica` `left join`
- **Grau do resultado:** uma linha por folha x rubrica.
- **Uso seguro:** base para entender a composição da folha antes de chegar ao empenho.

### Vínculo operacional

- O numero do empenho da folha é tratado na nota separada [`pessoal.rhempenhofolhaempenho`](/home/dbseller/Modelos/MVP/knowledge/rag/pessoal/rhempenhofolhaempenho.md).
- O relatório `pes2_rhempenhofolha002.php` usa esse vínculo para montar o PDF de empenho da folha.

### Bloco de retencao

#### Quando aparece

- O bloco de retencao e montado quando a configuracao `r11_geraretencaoempenho` da tabela `cfpess` esta habilitada.

#### Objetivo

Mostrar, para cada empenho da folha, as rubricas de retencao associadas.

#### Tabelas

- `pessoal.rhempenhofolha`
- `pessoal.rhempenhofolharhemprubrica`
- `pessoal.rhempenhofolharubrica`
- `pessoal.rhpessoalmov`
- `pessoal.rhempenhofolharubricaretencao`
- `pessoal.rhrubricas`

#### Filtros principais

- `rh72_sequencial = :rh72_sequencial_da_linha`
- `rh72_tipoempenho = :iTipo`
- `rh73_tiporubrica = 2`
- `rh73_pd = 2`
- `rh73_instit = DB_instit`

#### Grau do resultado

- Uma linha por rubrica de retencao dentro do empenho da folha.
- O valor da retencao e agregado por `rh73_rubric` e descricao da rubrica.

### Mapeamento de exibicao

- `r14` -> Salario
- `r48` -> Complementar
- `r35` -> 13o Salario
- `r20` -> Rescisao
- `r22` -> Adiantamento

Tipos de empenho:

- `1` -> Salario
- `2` -> Previdencia
- `3` -> FGTS

### Cuidados

- Nao confundir este cadastro com empenho geral nem com o relatorio `pes2_rhempenhofolha002.php`.
- O bloco principal e o bloco de retencao usam regras diferentes de `tiporubrica`.
- A classe depende fortemente de tabelas filhas; um registro ausente pode eliminar a linha final em consultas com `inner join`.
- Para o vínculo folha -> empenho, consulte a nota separada de `rhempenhofolhaempenho`.
- Se a pergunta for sobre empenho geral, usar a documentacao de `empenho.empenho`; se for sobre a folha e sua composicao, esta e a fonte correta.

### Perguntas que ela responde bem

- Quais empenhos foram gerados pela folha em uma competencia?
- Qual o valor total de rubrica principal por empenho da folha?
- Quais retencoes aparecem associadas ao empenho da folha?
- Qual ponto de folha gerou o empenho?
- Qual o empenho vinculado a um sequencial de folha?
