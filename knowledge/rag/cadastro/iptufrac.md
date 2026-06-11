## cadastro.iptufrac



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptufrac`



### Resumo tecnico

- Descricao: Fracionamento dos lotes. É utilizado para calcular a area ou testada fracionada para uma matricula. É bastante comum utilizar em lote que tenham construcoes do tipo apartamento, onde devemos fracionar o valor vanel de um imovel
- Chave primaria: j25_anousu, j25_matric
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j25_fracao, j25_idbql, j25_matric
- Candidatas a coluna de tempo: j25_anousu

### Relacionamentos

- `j25_matric` -> `cadastro.iptubase` (j01_matric) [iptufrac_matric_fk]

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
