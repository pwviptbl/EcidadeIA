## pessoal.rhlota

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_rhlota_classe.php`

Cadastro de lotacao. A classe representa a unidade organizacional usada por pessoal, folha e relatorios funcionais, com amarracao para estrutura, orgao, caracteristica peculiar e usuarios vinculados.

### Resumo tecnico

- **Tipo de fonte:** classe DAO + consultas analiticas de pessoal
- **Tabela principal:** `pessoal.rhlota`
- **Chave operacional:** `r70_codigo`
- **Grau base:** uma linha por lotacao
- **Uso funcional:** base de lotacao para movimentacao, folha e relatorios cadastrais

Interpretacao segura:

- `rhlota` e a lotacao cadastral, nao a movimentacao do servidor.
- A classe e usada como ponto de amarracao para `rhpessoalmov`, `rhlotaexe`, `orcorgao` e relatorios de estrutura.
- A lotacao pode carregar caracteristica peculiar, estrutura, identificacao analitica e vinculo com usuarios.

### Campos de negocio confirmados

- `r70_codigo`: codigo da lotacao.
- `r70_codestrut`: codigo da estrutura.
- `r70_estrut`: codificacao estrutural da lotacao.
- `r70_descr`: descricao.
- `r70_analitica`: indica se e analitica.
- `r70_instit`: instituicao.
- `r70_ativo`: status ativo.
- `r70_numcgm`: numcgm vinculado.
- `r70_concarpeculiar`: caracteristica peculiar.

### Regras de manutencao

- `incluir()` exige estrutura, codificacao estrutural, descricao, flag analitica, instituicao, ativo, numcgm e caracteristica peculiar.
- A chave `r70_codigo` pode vir por parametro ou pela sequencia `rhlota_r70_codigo_seq`.
- `alterar()` e `excluir()` trabalham diretamente sobre `r70_codigo`.
- O cadastro registra auditoria em `db_acount*` quando a sessao nao desativa esse fluxo.

### Consulta: `sql_query`

#### Objetivo

Recuperar a lotacao com o contexto cadastral de estrutura e caracteristica peculiar.

#### Tabelas

- `pessoal.rhlota`
- `cgm`
- `db_estrutura`
- `pessoal.concarpeculiar`

#### Juncoes principais

- `cgm.z01_numcgm = rhlota.r70_numcgm` `inner join`
- `db_estrutura.db77_codestrut = rhlota.r70_codestrut` `inner join`
- `concarpeculiar.c58_sequencial = rhlota.r70_concarpeculiar` `inner join`

#### Grau do resultado

- Uma linha por lotacao cadastrada.
- Como ha `inner join`, a lotacao precisa ter cgm, estrutura e caracteristica peculiar validos para aparecer.

### Consulta: `sql_query_file`

- **Objetivo:** leitura bruta do cadastro de lotacao.
- **Uso seguro:** manutencao e consulta simples sem enriquecimento.

### Consulta: `sql_query_cgm`

- **Objetivo:** cruzar lotacao com servidor, regime e cargo principal.
- **Tabelas:** `rhlota`, `rhpessoalmov`, `rhpessoal`, `rhpesrescisao`, `rhregime`, `cgm`, `rhfuncao`.
- **Uso seguro:** saber quais servidores estao naquela lotacao.

### Consulta: `sql_query_leftorgao`

- **Objetivo:** trazer lotacao com orgao por ano.
- **Tabelas:** `rhlota`, `rhlotaexe`, `orcorgao`.

### Consulta: `sql_query_lota_cgm`

- **Objetivo:** ligar lotacao ao CGM cadastrado na propria lotacao.

### Consulta: `sql_query_orgao`

- **Objetivo:** recuperar o orgao associado a lotacao.

### Consulta: `sql_query_usuarios`

- **Objetivo:** listar usuarios vinculados a lotacao.
- **Tabelas:** `rhlota`, `cgm`, `db_estrutura`, `concarpeculiar`, `db_usuariosrhlota`, `db_usuarios`.

### Consulta: `sql_query_dadosElemento`

- **Objetivo:** gerar base de relatorio de lotacao com elementos orcamentarios e estrutura anual.
- **Tabelas:** `rhlota`, `rhlotaexe`, `orcorgao`, `orcunidade`, `rhlotavinc`, `orcprojativ`, `orctiporec`, `orcfuncao`, `orcsubfuncao`, `orcprograma`, `concarpeculiar`, `rhlotavincele`, `rhlotavincativ`, `orcelemento`, `rhlotavincrec`.
- **Uso seguro:** relatorio cadastral e analitico de lotacao.

### Cuidados

- Nao confundir lotacao com orgao: a lotacao e a unidade funcional, o orgao vem de `rhlotaexe` e `orcorgao`.
- Esta classe aparece como dependencia forte em `rhpessoalmov`, `rhpessoal` e varios relatorios de folha.
- O relatorio de elementos puxa muitas tabelas de apoio; uma configuracao incompleta derruba o resultado.

### Perguntas que ela responde bem

- Qual e a lotacao de um servidor?
- Qual estrutura e caracteristica peculiar a lotacao possui?
- Qual orgao esta associado a lotacao no ano?
- Quais usuarios estao vinculados a uma lotacao?
- Qual base estrutural/orcamentaria a lotacao usa nos relatorios?
