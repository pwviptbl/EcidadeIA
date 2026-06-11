## cadastro.iptuconstrhabite



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptuconstrhabite`



### Resumo tecnico

- Descricao: Habite-se das construções
- Chave primaria: j131_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j131_idcons, j131_matric, j131_sequencial
- Candidatas a coluna de tempo: j131_data, j131_dthabite, j131_dtprot

### Relacionamentos

- `j131_matric, j131_matric, j131_idcons, j131_idcons` -> `cadastro.iptuconstr` (j39_idcons, j39_matric, j39_idcons, j39_matric) [iptuconstrhabite_matric_idcons_fk]

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
