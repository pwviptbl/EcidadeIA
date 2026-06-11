## cadastro.iptunaogeracarnecgm



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptunaogeracarnecgm`



### Resumo tecnico

- Descricao: Cgms que nao devem gerar carne na emissao geral do IPTU
- Chave primaria: j68_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j68_naogeracarne, j68_numcgm, j68_sequencial
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j68_naogeracarne` -> `cadastro.iptunaogeracarne` (j66_sequencial) [iptunaogeracarnecgm_naogeracarne_fk]
- `j68_numcgm` -> `protocolo.cgm` (z01_numcgm) [iptunaogeracarnecgm_numcgm_fk]

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
