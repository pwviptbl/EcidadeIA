## cadastro.zonafator



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.zonafator`



### Resumo tecnico

- Descricao: Zona Fator
- Chave primaria: j110_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j110_sequencial
- Candidatas a coluna de tempo: j110_anousu

### Relacionamentos

- `j110_zona` -> `cadastro.zonas` (j50_zona) [zonafator_zona_fk]

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
