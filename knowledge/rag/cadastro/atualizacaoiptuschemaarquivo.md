## cadastro.atualizacaoiptuschemaarquivo



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.atualizacaoiptuschemaarquivo`



### Resumo tecnico

- Descricao: Arquivos importados para atualização de cadastros imobiliários.
- Chave primaria: j143_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j143_sequencial
- Candidatas a coluna de tempo: j143_dataimportacao

### Relacionamentos

- `j143_atualizacaoiptuschema` -> `cadastro.atualizacaoiptuschema` (j142_sequencial) [atualizacaoiptuschemaarquivo_ed143_atualizacaoiptuschema_fk]

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
