## cadastro.averbaprocesso



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.averbaprocesso`



### Resumo tecnico

- Descricao: averbaprocesso
- Chave primaria: j77_averbacao
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j77_averbacao
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j77_averbacao` -> `cadastro.averbacao` (j75_codigo) [averbaprocesso_averbacao_fk]
- `j77_codproc` -> `protocolo.protprocesso` (p58_codproc) [averbaprocesso_codproc_fk]

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
