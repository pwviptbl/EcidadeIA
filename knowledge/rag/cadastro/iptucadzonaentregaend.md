## cadastro.iptucadzonaentregaend



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptucadzonaentregaend`



### Resumo tecnico

- Descricao: Codigo do logradouro, numero do imovel e complemento do cadastro de zona de entrega
- Chave primaria: j87_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j87_iptucadzonaentrega, j87_sequencial
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j87_iptucadzonaentrega` -> `cadastro.iptucadzonaentrega` (j85_codigo) [iptucadzonaentregaend_iptucadzonaentrega_fk]
- `j87_lograd` -> `cadastro.ruas` (j14_codigo) [iptucadzonaentregaend_lograd_fk]

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
