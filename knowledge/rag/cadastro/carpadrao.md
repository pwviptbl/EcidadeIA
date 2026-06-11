## cadastro.carpadrao



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.carpadrao`



### Resumo tecnico

- Descricao: Tabela que contém as caracteristicas padrões dos grupos
- Chave primaria: j33_codgrupo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j33_codcaracter, j33_codgrupo
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j33_codcaracter` -> `cadastro.caracter` (j31_codigo) [carpadrao_codcaracter_fk]
- `j33_codgrupo` -> `cadastro.cargrup` (j32_grupo) [carpadrao_codgrupo_fk]

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
