## cadastro.zonafatorarea



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.zonafatorarea`



### Resumo tecnico

- Descricao: Zona Fator Area
- Chave primaria: j113_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j113_sequencial
- Candidatas a coluna de tempo: j113_anousu

### Relacionamentos

- `j113_zona` -> `cadastro.zonas` (j50_zona) [zonafatorarea_zona_fk]

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
