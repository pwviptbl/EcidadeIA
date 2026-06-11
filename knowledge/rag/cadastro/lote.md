## cadastro.lote



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.lote`



### Resumo tecnico

- Descricao: cadastro de Lotes do Municipio
- Chave primaria: j34_idbql
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j34_areal, j34_idbql, j34_lote, j34_quadra
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j34_bairro` -> `cadastro.bairro` (j13_codi) [lote_bairro_fk]
- `j34_setor` -> `cadastro.setor` (j30_codi) [lote_setor_fk]

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
