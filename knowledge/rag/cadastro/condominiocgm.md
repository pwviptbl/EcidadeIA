## cadastro.condominiocgm



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.condominiocgm`



### Resumo tecnico

- Descricao: CGM do Condomínio
- Chave primaria: j106_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j106_numcgm, j106_sequencial
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j106_condominio` -> `cadastro.condominio` (j107_sequencial) [condominiocgm_condominio_fk]
- `j106_numcgm` -> `protocolo.cgm` (z01_numcgm) [condominiocgm_j106_numcgm_fkey]

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
