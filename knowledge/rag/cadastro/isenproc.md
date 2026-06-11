## cadastro.isenproc



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.isenproc`



### Resumo tecnico

- Descricao: guarda o codigo de isenção da matricula e o codigo do processo
- Chave primaria: Nao informada.
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j61_codigo
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j61_codigo` -> `cadastro.iptuisen` (j46_codigo) [isenproc_codigo_fk]
- `j61_codproc` -> `protocolo.protprocesso` (p58_codproc) [isenproc_codproc_fk]

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
