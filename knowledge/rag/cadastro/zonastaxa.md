## cadastro.zonastaxa



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.zonastaxa`



### Resumo tecnico

- Descricao: Taxas por zona/ano
- Chave primaria: j57_zona, j57_receit, j57_anousu
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna de tempo: j57_anousu, j57_valor

### Relacionamentos

- `j57_receit` -> `caixa.tabrec` (k02_codigo) [zonastaxa_receit_fk]
- `j57_zona` -> `cadastro.zonas` (j50_zona) [zonastaxa_zona_fk]

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
