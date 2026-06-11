## cadastro.iptubaseregimovel



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptubaseregimovel`



### Resumo tecnico

- Descricao: dados do registro de imóveis
- Chave primaria: j04_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j04_matric, j04_matricregimo, j04_sequencial
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j04_matric` -> `cadastro.iptubase` (j01_matric) [iptubaseregimovel_matric_fk]
- `j04_setorregimovel` -> `cadastro.setorregimovel` (j69_sequencial) [iptubaseregimovel_setorregimovel_fk]

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
