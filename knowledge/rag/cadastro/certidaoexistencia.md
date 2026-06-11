## cadastro.certidaoexistencia



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.certidaoexistencia`



### Resumo tecnico

- Descricao: certidão de existência de construção
- Chave primaria: j133_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j133_areaconstruida, j133_arearealconstruida, j133_arquivo, j133_matric, j133_sequencial
- Candidatas a coluna de tempo: j133_data, j133_dathabite, j133_dtprocesso

### Relacionamentos

- `j133_matric, j133_matric, j133_iptuconstr, j133_iptuconstr` -> `cadastro.iptuconstr` (j39_matric, j39_idcons, j39_matric, j39_idcons) [certidaoexistencia_matric_iptuconstr_fk]
- `j133_db_usuarios` -> `configuracoes.db_usuarios` (id_usuario) [certidaoexistencia_usuarios_fk]

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
