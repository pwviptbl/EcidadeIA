## cadastro.doi_importacao



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.doi_importacao`



### Resumo tecnico

- Descricao: Preencher.
- Chave primaria: j181_id
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j181_id, j181_id_doi, j181_matricula, j181_numcgm
- Candidatas a coluna de tempo: j181_data, j181_data_processamento

### Relacionamentos

- `j181_id_doi` -> `cadastro.doi` (j180_id) [doi_importacao_j181_id_doi_fk]
- `j181_numcgm` -> `protocolo.cgm` (z01_numcgm) [doi_importacao_j181_numcgm_fk]

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
