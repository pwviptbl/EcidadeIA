## cadastro.iptuisen



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptuisen`



### Resumo tecnico

- Descricao: cadastro das matricula com suas isencoes
- Chave primaria: j46_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j46_codigo, j46_idusu, j46_matric
- Candidatas a coluna de tempo: j46_dtfim, j46_dtinc, j46_dtini

### Relacionamentos

- `j46_matric` -> `cadastro.iptubase` (j01_matric) [iptuisen_matric_fk]
- `j46_tipo` -> `cadastro.tipoisen` (j45_tipo) [iptuisen_tipo_fk]

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
