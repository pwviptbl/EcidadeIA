## cadastro.iptubasepredio



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptubasepredio`



### Resumo tecnico

- Descricao: IPTU Base Prédio
- Chave primaria: j109_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j109_matric, j109_sequencial
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j109_matric` -> `cadastro.iptubase` (j01_matric) [iptubasepredio_matric_fk]
- `j109_predio` -> `cadastro.predio` (j111_sequencial) [iptubasepredio_predio_fk]

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
