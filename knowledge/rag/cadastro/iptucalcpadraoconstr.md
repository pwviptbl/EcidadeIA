## cadastro.iptucalcpadraoconstr



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptucalcpadraoconstr`



### Resumo tecnico

- Descricao: Construções
- Chave primaria: j11_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j11_idcons, j11_matric, j11_sequencial
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j11_iptucalcpadrao` -> `cadastro.iptucalcpadrao` (j10_sequencial) [iptucalcpadraoconstr_iptucalcpadrao_fk]
- `j11_matric, j11_matric, j11_idcons, j11_idcons` -> `cadastro.iptuconstr` (j39_matric, j39_idcons, j39_idcons, j39_matric) [iptucalcpadraoconstr_matric_idcons_fk]

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
