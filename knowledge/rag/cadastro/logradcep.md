## cadastro.logradcep



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.logradcep`



### Resumo tecnico

- Descricao: Cep por logradouro, utilizada para casos em que o municipio tem cep por logradouro e esta tabela interliga o cadastro imobiliario ao cadastro de ceps
- Chave primaria: Nao informada.
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j65_ceplog` -> `protocolo.db_ceplog` (db11_codlog) [logradcep_ceplog_fk]
- `j65_lograd` -> `cadastro.ruas` (j14_codigo) [logradcep_lograd_fk]

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
