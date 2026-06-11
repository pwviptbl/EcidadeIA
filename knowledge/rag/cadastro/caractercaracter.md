## cadastro.caractercaracter



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.caractercaracter`



### Resumo tecnico

- Descricao: Vinculação das caracteristicas com as caracteristicas
- Chave primaria: j138_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j138_sequencial
- Candidatas a coluna de tempo: j138_anousu

### Relacionamentos

- `j138_caracterdestino` -> `cadastro.caracter` (j31_codigo) [caracterponto_caracterdestino_fk]
- `j138_caracterorigem` -> `cadastro.caracter` (j31_codigo) [caracterponto_caracterorigem_fk]

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
