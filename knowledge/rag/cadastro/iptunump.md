## cadastro.iptunump



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptunump`



### Resumo tecnico

- Descricao: Contem dados referentes aos numpres (códigos de arrecadacao) gerados para os carnês
- Chave primaria: j20_anousu, j20_matric
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j20_matric, j20_numpre
- Candidatas a coluna de tempo: j20_anousu

### Relacionamentos

- `j20_matric` -> `cadastro.iptubase` (j01_matric) [iptunump_matric_fk]

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
