## cadastro.lotenumero_proc



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.lotenumero_proc`



### Resumo tecnico

- Descricao: armazena o numero do processo
- Chave primaria: j11_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j11_codigo
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j11_codigo` -> `cadastro.lotenumero` (j12_codigo) [lotenumero_proc_codigo_fk]
- `j11_processo` -> `protocolo.protprocesso` (p58_codproc) [lotenumero_proc_processo_fk]

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
