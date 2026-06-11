## cadastro.setorfiscalvalor



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.setorfiscalvalor`



### Resumo tecnico

- Descricao: Valores por ano dos setores fiscais de m2 terreno
- Chave primaria: j82_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j82_codigo, j82_setorfiscal
- Candidatas a coluna de tempo: j82_anousu

### Relacionamentos

- `j82_setorfiscal` -> `cadastro.setorfiscal` (j90_codigo) [setorfiscalvalor_setorfiscal_fk]

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
