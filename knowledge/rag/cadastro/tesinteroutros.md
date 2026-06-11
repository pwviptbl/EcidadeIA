## cadastro.tesinteroutros



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.tesinteroutros`



### Resumo tecnico

- Descricao: tesinteroutros
- Chave primaria: Nao informada.
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j84_tesinter, j84_tesintertipo
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j84_tesinter` -> `cadastro.tesinter` (j39_sequencial) [tesinteroutros_tesinter_fk]
- `j84_tesintertipo` -> `cadastro.tesintertipo` (j92_sequencial) [tesinteroutros_tesintertipo_fk]

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
