## cadastro.doi_inconsistencias



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.doi_inconsistencias`



### Resumo tecnico

- Descricao: Preencher.
- Chave primaria: j182_id
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j182_id, j182_id_doi
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j182_id_doi` -> `cadastro.doi` (j180_id) [doi_inconsistencias_j182_id_doi_fk]

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
