## cadastro.tesinterlote



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.tesinterlote`



### Resumo tecnico

- Descricao: Ligacao da tabela lote com tesinter
- Chave primaria: j69_tesinter
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j69_idbql, j69_tesinter
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j69_idbql` -> `cadastro.lote` (j34_idbql) [tesinterlote_idbql_fk]
- `j69_tesinter` -> `cadastro.tesinter` (j39_sequencial) [tesinterlote_tesinter_fk]

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
