## cadastro.iptubaixa



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptubaixa`



### Resumo tecnico

- Descricao: Tabela das baixas de matricula
- Chave primaria: j02_matric
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j02_matric, j02_usuario
- Candidatas a coluna de tempo: j02_data, j02_dtbaixa

### Relacionamentos

- `j02_matric` -> `cadastro.iptubase` (j01_matric) [iptubaixa_matric_fk]
- `j02_usuario` -> `configuracoes.db_usuarios` (id_usuario) [iptubaixa_usuario_fk]

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
