## cadastro.iptucalcpadraolog



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptucalcpadraolog`



### Resumo tecnico

- Descricao: Log do calculo padrão
- Chave primaria: j19_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j19_iptucalcpadrao, j19_sequencial
- Candidatas a coluna de tempo: j19_data

### Relacionamentos

- `j19_iptucalcpadrao` -> `cadastro.iptucalcpadrao` (j10_sequencial) [iptucalcpadraolog_iptucalcpadrao_fk]
- `j19_usuario` -> `configuracoes.db_usuarios` (id_usuario) [iptucalcpadraolog_usuario_fk]

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
