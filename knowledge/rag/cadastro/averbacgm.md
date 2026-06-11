## cadastro.averbacgm



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.averbacgm`



### Resumo tecnico

- Descricao: novos promitentes ou proprietarios
- Chave primaria: j76_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j76_averbacao, j76_codigo, j76_numcgm
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j76_averbacao` -> `cadastro.averbacao` (j75_codigo) [averbacgm_averbacao_fk]
- `j76_numcgm` -> `protocolo.cgm` (z01_numcgm) [averbacgm_numcgm_fk]
- `j76_tipo_contribuinte, j76_tipo_contribuinte, j76_tipo_contribuinte` -> `cadastro.tipocontribuinte` (j147_sequencial, j147_sequencial, j147_sequencial) [tipocontribuinte_sequencial_fk]

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
