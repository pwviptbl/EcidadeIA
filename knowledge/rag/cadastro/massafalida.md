## cadastro.massafalida



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.massafalida`



### Resumo tecnico

- Descricao: Tabela de massas falidas
- Chave primaria: j58_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j58_codigo, j58_data, j58_numcgm, j58_obs
- Candidatas a coluna de tempo: j58_data

### Relacionamentos

- `j58_numcgm` -> `protocolo.cgm` (z01_numcgm) [massafalida_numcgm_fk]

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
