## cadastro.mobimportacao



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.mobimportacao`



### Resumo tecnico

- Descricao: Dados Importados
- Chave primaria: j95_codimporta
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j95_idusuario
- Candidatas a coluna de tempo: j95_data

### Relacionamentos

- `j95_idusuario` -> `configuracoes.db_usuarios` (id_usuario) [mobimportacao_idusuario_fk]

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
