## cadastro.ruas



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.ruas`



### Resumo tecnico

- Descricao: Cadastro de todas as ruas e avenidas do municipio
- Chave primaria: j14_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j14_codigo, j14_tipo
- Candidatas a coluna de tempo: j14_dtlei

### Relacionamentos

- `j14_tipo` -> `cadastro.ruastipo` (j88_codigo) [ruas_tipo_fk]

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
