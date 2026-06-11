## cadastro.zonasvalor



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.zonasvalor`



### Resumo tecnico

- Descricao: Valores por zona fiscal e por ano
- Chave primaria: j51_zona, j51_anousu
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna de tempo: j51_anousu

### Relacionamentos

- `j51_zona` -> `cadastro.zonas` (j50_zona) [zonasvalor_zona_fk]

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
