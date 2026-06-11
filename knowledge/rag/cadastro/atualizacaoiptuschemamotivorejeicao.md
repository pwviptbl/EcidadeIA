## cadastro.atualizacaoiptuschemamotivorejeicao



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.atualizacaoiptuschemamotivorejeicao`



### Resumo tecnico

- Descricao: Tabela que guarda o motivo de rejeição.
- Chave primaria: j146_atualizacaoiptuschemamatricula
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j146_atualizacaoiptuschemamatricula
- Candidatas a coluna de tempo: j146_data

### Relacionamentos

- `j146_atualizacaoiptuschemamatricula` -> `cadastro.atualizacaoiptuschemamatricula` (j144_sequencial) [atualizacaoiptuschemamotivorejeicao_fk]

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

### Resumo tecnico

- Descricao: Cadastro das averbacoes das matriculas (TABELA NAO É MAIS UTILIZADA NO E-CIDADE)
- Chave primaria: j55_codave
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j55_cidade, j55_codave, j55_matric, j55_numcgm, j55_regimo
- Candidatas a coluna de tempo: j55_data

### Relacionamentos

- `j55_matric` -> `cadastro.iptubase` (j01_matric) [averba_matric_fk]
- `j55_numcgm` -> `protocolo.cgm` (z01_numcgm) [averba_numcgm_fk]
