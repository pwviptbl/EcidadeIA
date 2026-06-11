## cadastro.averbaformalpartilhacgm



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.averbaformalpartilhacgm`



### Resumo tecnico

- Descricao: Averba formal partilha
- Chave primaria: j102_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j102_numcgm, j102_sequencial
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j102_averbaformalpartilha` -> `cadastro.averbaformalpartilha` (j100_sequencial) [averbaformalpartilhacgm_averbaformalpartilha_fk]
- `j102_numcgm` -> `protocolo.cgm` (z01_numcgm) [averbaformalpartilhacgm_numcgm_fk]

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
