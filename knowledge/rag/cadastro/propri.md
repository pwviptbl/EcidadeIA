## cadastro.propri



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.propri`



### Resumo tecnico

- Descricao: Cadastro dos outros proprietarios do imovel
- Chave primaria: j42_matric, j42_numcgm
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j42_matric, j42_numcgm
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j42_matric` -> `cadastro.iptubase` (j01_matric) [propri_matric_fk]
- `j42_numcgm` -> `protocolo.cgm` (z01_numcgm) [propri_numcgm_fk]
- `j42_tipo_contribuinte, j42_tipo_contribuinte, j42_tipo_contribuinte` -> `cadastro.tipocontribuinte` (j147_sequencial, j147_sequencial, j147_sequencial) [tipocontribuinte_sequencial_fk]

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
