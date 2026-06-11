## cadastro.caractercaracteristica



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.caractercaracteristica`



### Resumo tecnico

- Descricao: Vinculo entra caracteristica iptu e catacteristica
- Chave primaria: db143_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: db143_caracter, db143_sequencial
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `db143_caracter` -> `cadastro.caracter` (j31_codigo) [caractercaracteristica_caracter_fk]
- `db143_caracteristica` -> `configuracoes.caracteristica` (db140_sequencial) [caractercaracteristica_caracteristica_fk]

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
