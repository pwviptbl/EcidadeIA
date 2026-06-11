## cadastro.loteloc



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.loteloc`



### Resumo tecnico

- Descricao: loteloc
- Chave primaria: j06_idbql
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j06_idbql
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j06_idbql` -> `cadastro.lote` (j34_idbql) [loteloc_idbql_fk]
- `j06_setorloc` -> `cadastro.setorloc` (j05_codigo) [loteloc_setorloc_fk]

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
