## cadastro.moblevatamento



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.moblevatamento`



### Resumo tecnico

- Descricao: Levantamento do cadastro PDA
- Chave primaria: j97_sequen
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j97_cidade, j97_matric, j97_profun, j97_sequen
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j97_codimporta` -> `cadastro.mobimportacao` (j95_codimporta) [moblevatamento_codimporta_fk]

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
