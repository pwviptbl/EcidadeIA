## cadastro.iptunaogeracarnematric



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptunaogeracarnematric`



### Resumo tecnico

- Descricao: Preencher.
- Chave primaria: j131_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j131_matric, j131_sequencial
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j131_matric` -> `cadastro.iptubase` (j01_matric) [iptunaogeracarnematric_matric_fk]
- `j131_naogeracarne` -> `cadastro.iptunaogeracarne` (j66_sequencial) [iptunaogeracarnematric_naogeracarne_fk]

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
