## cadastro.histocorrenciaprocesso



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.histocorrenciaprocesso`



### Resumo tecnico

- Descricao: Guarda os processos vinculados a ocorrencia
- Chave primaria: ar26_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: ar26_sequencial
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `ar26_histocorrencia` -> `arrecadacao.histocorrencia` (ar23_sequencial) [histocorrenciaprocesso_histocorrencia_fk]

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
