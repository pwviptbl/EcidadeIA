## cadastro.tesinter



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.tesinter`



### Resumo tecnico

- Descricao: Cadastro das testadas internas dos lotes
- Chave primaria: j39_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j39_idbql, j39_sequencial, j39_testle
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j39_idbql` -> `cadastro.lote` (j34_idbql) [tesinter_idbql_fk]
- `j39_orientacao` -> `cadastro.orientacao` (j64_sequencial) [tesinter_orientacao_fk]

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
