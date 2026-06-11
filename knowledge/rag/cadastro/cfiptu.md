## cadastro.cfiptu



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.cfiptu`



### Resumo tecnico

- Descricao: Controle dos dados para calculo do iptu
- Chave primaria: j18_anousu
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j18_dadoscertisen, j18_db_sysfuncoes, j18_formatlote, j18_formatquadra, j18_formatsetor
- Candidatas a coluna de tempo: j18_anousu, j18_dtoper, j18_permvenc

### Relacionamentos

- `j18_infla` -> `inflatores.inflan` (i01_codigo) [cfiptu_infla_fk]
- `j18_iptuhistisen` -> `cadastro.iptucalh` (j17_codhis) [cfiptu_j18_iptuhistisen_fk]
- `j18_templatecertidaoexitencia` -> `configuracoes.db_documentotemplate` (db82_sequencial) [cfiptu_j18_templatecertidaoexitencia_fk]
- `j18_receitacreditorecalculo` -> `caixa.tabrec` (k02_codigo) [cfiptu_receitacreditorecalculo_fk]
- `j18_tipodebitorecalculo` -> `caixa.arretipo` (k00_tipo) [cfiptu_tipodebitorecalculo_fk]
- `j18_tipoisen` -> `cadastro.tipoisen` (j45_tipo) [cfiptu_tipoisen_fk]

### Filtros padrao

- Nenhum filtro padrao catalogado.

### Semantica de filtros

- Nenhuma semantica de filtro catalogada.

### Regra de negocio para enriquecer

- O que esta tabela representa no negocio?
- Quando ela deve ser preferida sobre outras tabelas parecidas?
- Que perguntas ela responde bem?
- Que filtros de negocio sao seguros?
- O que nao pode ser inferido a partir dela?

### Cuidados / riscos

- Preencher com ambiguidades, excecoes e limites conhecidos.
