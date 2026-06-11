## cadastro.carface



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.carface`



### Resumo tecnico

- Descricao: Cadastro das caracteristicas que identificam uma face de quadra.
- Chave primaria: j38_face, j38_caract
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j38_caract, j38_face
- Candidatas a coluna de tempo: j38_datalancamento

### Relacionamentos

- `j38_caract` -> `cadastro.caracter` (j31_codigo) [carface_caract_fk]
- `j38_face` -> `cadastro.face` (j37_face) [carface_face_fk]

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
