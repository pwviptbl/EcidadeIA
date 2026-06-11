## cadastro.testada



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.testada`



### Resumo tecnico

- Descricao: Cadastro para identificar a testada dos lotes
- Chave primaria: j36_idbql, j36_face
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j36_codigo, j36_face, j36_idbql, j36_testle
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j36_codigo` -> `cadastro.ruas` (j14_codigo) [testada_codigo_fk]
- `j36_idbql` -> `cadastro.lote` (j34_idbql) [testada_idbql_fk]

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
