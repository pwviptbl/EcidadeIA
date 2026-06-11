## cadastro.iptuconstrobrasconstr



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptuconstrobrasconstr`



### Resumo tecnico

- Descricao: Tabela de ligação entre iptuconstr e obrasconstr
- Chave primaria: j132_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j132_idconstr, j132_matric, j132_sequencial
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j132_matric, j132_matric, j132_idconstr, j132_idconstr` -> `cadastro.iptuconstr` (j39_idcons, j39_matric, j39_matric, j39_idcons) [iptuconstrobrasconstr_matric_idconstr_fk]
- `j132_obrasconstr` -> `projetos.obrasconstr` (ob08_codconstr) [iptuconstrobrasconstr_obrasconstr_fk]

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
