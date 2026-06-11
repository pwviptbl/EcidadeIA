## cadastro.isenexe



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.isenexe`



### Resumo tecnico

- Descricao: Cadastro dos exercicios da isencao
- Chave primaria: j47_codigo, j47_anousu
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j47_codigo
- Candidatas a coluna de tempo: j47_anousu

### Relacionamentos

- `j47_codigo` -> `cadastro.iptuisen` (j46_codigo) [isenexe_codigo_fk]

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
