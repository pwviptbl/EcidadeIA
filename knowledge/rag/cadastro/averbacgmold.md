## cadastro.averbacgmold



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.averbacgmold`



### Resumo tecnico

- Descricao: guarda cgms de antigo proprietarios e promitentes
- Chave primaria: j79_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j79_averbacao, j79_codigo, j79_numcgm
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j79_averbacao` -> `cadastro.averbacao` (j75_codigo) [averbacgmold_averbacao_fk]
- `j79_numcgm` -> `protocolo.cgm` (z01_numcgm) [averbacgmold_numcgm_fk]

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
