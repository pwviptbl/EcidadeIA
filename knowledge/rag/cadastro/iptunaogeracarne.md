## cadastro.iptunaogeracarne



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptunaogeracarne`



### Resumo tecnico

- Descricao: Nao gera carne
- Chave primaria: j66_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j66_sequencial, j66_usuario
- Candidatas a coluna de tempo: j66_data

### Relacionamentos

- `j66_usuario` -> `configuracoes.db_usuarios` (id_usuario) [iptunaogeracarne_usuario_fk]

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
