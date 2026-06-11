## cadastro.carvalor



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.carvalor`



### Resumo tecnico

- Descricao: Valores das caracteristicas
- Chave primaria: j71_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j71_caract, j71_codigo, j71_quantfim, j71_quantini
- Candidatas a coluna de tempo: j71_anousu

### Relacionamentos

- `j71_caract` -> `cadastro.caracter` (j31_codigo) [carvalor_caract_fk]

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
