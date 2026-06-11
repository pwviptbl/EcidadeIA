## cadastro.doi



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.doi`



### Resumo tecnico

- Descricao: Preencher.
- Chave primaria: j180_id
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j180_id, j180_id_registro_imoveis, j180_id_usuario
- Candidatas a coluna de tempo: j180_ano_registro, j180_data_importacao

### Relacionamentos

- `j180_id_registro_imoveis` -> `cadastro.setorregimovel` (j69_sequencial) [doi_j180_id_registro_imoveis_fk]
- `j180_id_usuario` -> `configuracoes.db_usuarios` (id_usuario) [doi_j180_id_usuario_fk]

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
