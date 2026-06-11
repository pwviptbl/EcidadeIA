## cadastro.facevalor



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.facevalor`



### Resumo tecnico

- Descricao: Valores da face por ano
- Chave primaria: j81_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j81_codigo, j81_face
- Candidatas a coluna de tempo: j81_anousu

### Relacionamentos

- `j81_face` -> `cadastro.face` (j37_face) [facevalor_face_fk]

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
