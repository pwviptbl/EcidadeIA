## cadastro.ruasbairro



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.ruasbairro`



### Resumo tecnico

- Descricao: Bairro da rua
- Chave primaria: j16_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j16_codigo
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j16_bairro` -> `cadastro.bairro` (j13_codi) [ruasbairro_bairro_fk]
- `j16_lograd` -> `cadastro.ruas` (j14_codigo) [ruasbairro_lograd_fk]

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
