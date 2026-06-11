## cadastro.moblevantamentoedi



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.moblevantamentoedi`



### Resumo tecnico

- Descricao: Constrições das Matrículas
- Chave primaria: j96_sequen
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j96_codigo, j96_idade, j96_matric, j96_sequen
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j96_codimporta` -> `cadastro.mobimportacao` (j95_codimporta) [moblevantamentoedi_codimporta_fk]

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
