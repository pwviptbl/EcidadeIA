## cadastro.testadanumero



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.testadanumero`



### Resumo tecnico

- Descricao: Numero do imovel
- Chave primaria: j15_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j15_codigo, j15_face, j15_idbql
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j15_idbql, j15_idbql, j15_face, j15_face` -> `cadastro.testada` (j36_face, j36_idbql, j36_face, j36_idbql) [testadanumero_idbql_face_fk]

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
