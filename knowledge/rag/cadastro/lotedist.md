## cadastro.lotedist



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.lotedist`



### Resumo tecnico

- Descricao: Identificacao da distancia do lote em relacao ao logradouro mais próximo
- Chave primaria: j54_idbql
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j54_codigo, j54_distan, j54_idbql, j54_orientacao
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j54_codigo` -> `cadastro.ruas` (j14_codigo) [lotedist_codigo_fk]
- `j54_idbql` -> `cadastro.lote` (j34_idbql) [lotedist_idbql_fk]
- `j54_orientacao` -> `cadastro.orientacao` (j64_sequencial) [lotedist_orientacao_fk]

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
