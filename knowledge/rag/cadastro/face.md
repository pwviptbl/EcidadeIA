## cadastro.face



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.face`



### Resumo tecnico

- Descricao: Cadastro das faces de quadras do municipio. Cada face de quadra é a representação da "frente" ou "lado" de cada quadra. Normalmente uma quadra tem 4 faces, onde cada lado tem um logradouro.
- Chave primaria: j37_face
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j37_codigo, j37_face, j37_lado, j37_outros, j37_profr
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j37_codigo` -> `cadastro.ruas` (j14_codigo) [face_codigo_fk]
- `j37_setor` -> `cadastro.setor` (j30_codi) [face_setor_fk]

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
