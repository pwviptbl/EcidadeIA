## cadastro.iptutabelasdepend



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptutabelasdepend`



### Resumo tecnico

- Descricao: iptutabelasdepend
- Chave primaria: j128_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j128_sequencial
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j128_iptutabelasdepend` -> `cadastro.iptutabelas` (j121_sequencial) [iptutabelasdepend_iptutabelasdepend_fk]
- `j128_iptutabelas` -> `cadastro.iptutabelas` (j121_sequencial) [iptutabelasdepend_iptutabelas_fk]

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
