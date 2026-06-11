## cadastro.carzonavalor



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.carzonavalor`



### Resumo tecnico

- Descricao: Valores das caracteristicas por zona
- Chave primaria: Nao informada.
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j72_caract, j72_quant, j72_quantfim, j72_quantini, j72_sequencial
- Candidatas a coluna de tempo: j72_anousu

### Relacionamentos

- `j72_caract` -> `cadastro.caracter` (j31_codigo) [carzonavalor_caract_fk]
- `j72_zona` -> `cadastro.zonas` (j50_zona) [carzonavalor_zona_fk]

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
