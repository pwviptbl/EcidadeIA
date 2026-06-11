## cadastro.cadimobil



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.cadimobil`



### Resumo tecnico

- Descricao: cadastro de imobiliárias
- Chave primaria: j63_numcgm
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j63_numcgm
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j63_numcgm` -> `protocolo.cgm` (z01_numcgm) [cadimobil_numcgm_fk]

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
