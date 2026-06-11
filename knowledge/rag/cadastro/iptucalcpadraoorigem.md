## cadastro.iptucalcpadraoorigem



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptucalcpadraoorigem`



### Resumo tecnico

- Descricao: dados da origem da importação
- Chave primaria: j27_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j27_matric, j27_sequencial
- Candidatas a coluna de tempo: j27_anousu

### Relacionamentos

- `j27_anousu, j27_anousu, j27_matric, j27_matric` -> `cadastro.iptucalc` (j23_matric, j23_anousu, j23_anousu, j23_matric) [iptucalcpadraoorigem_ae_matric_fk]
- `j27_iptucalcpadrao` -> `cadastro.iptucalcpadrao` (j10_sequencial) [iptucalcpadraoorigem_iptucalcpadrao_fk]

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
