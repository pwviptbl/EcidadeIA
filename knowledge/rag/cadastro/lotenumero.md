## cadastro.lotenumero



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.lotenumero`



### Resumo tecnico

- Descricao: Armazena o numero do Lote
- Chave primaria: j12_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j12_codigo, j12_idbql, j12_lograd
- Candidatas a coluna de tempo: j12_data

### Relacionamentos

- `j12_idbql` -> `cadastro.lote` (j34_idbql) [lotenumero_idbql_fk]
- `j12_lograd` -> `cadastro.ruas` (j14_codigo) [lotenumero_lograd_fk]

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
