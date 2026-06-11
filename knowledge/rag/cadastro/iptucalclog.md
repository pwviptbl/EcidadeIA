## cadastro.iptucalclog



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptucalclog`



### Resumo tecnico

- Descricao: Log do calculo do iptu
- Chave primaria: j27_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j27_codigo, j27_quantaproc, j27_usuario
- Candidatas a coluna de tempo: j27_anousu, j27_data

### Relacionamentos

- `j27_usuario` -> `configuracoes.db_usuarios` (id_usuario) [iptucalclog_usuario_fk]

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
