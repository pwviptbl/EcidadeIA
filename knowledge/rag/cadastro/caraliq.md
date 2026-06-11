## cadastro.caraliq



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.caraliq`



### Resumo tecnico

- Descricao: Aliquotas por caracteristica e ano
- Chave primaria: j73_anousu, j73_caract
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j73_caract
- Candidatas a coluna de tempo: j73_anousu

### Relacionamentos

- `j73_caract` -> `cadastro.caracter` (j31_codigo) [caraliq_caract_fk]

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
