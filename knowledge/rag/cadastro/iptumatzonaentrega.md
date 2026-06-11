## cadastro.iptumatzonaentrega



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptumatzonaentrega`



### Resumo tecnico

- Descricao: Ligacao das matriculas com a zona de entrega
- Chave primaria: j86_sequencial
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j86_iptucadzonaentrega, j86_matric, j86_sequencial
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j86_iptucadzonaentrega` -> `cadastro.iptucadzonaentrega` (j85_codigo) [iptumatzonaentrega_iptucadzonaentrega_fk]
- `j86_matric` -> `cadastro.iptubase` (j01_matric) [iptumatzonaentrega_matric_fk]

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
