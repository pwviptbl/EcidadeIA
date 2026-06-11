## cadastro.constrescr



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.constrescr`



### Resumo tecnico

- Descricao: cadastro das Construcoes escrituradas
- Chave primaria: j52_matric, j52_idcons
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j52_area, j52_codigo, j52_idaument, j52_idcons, j52_matric
- Candidatas a coluna de tempo: j52_ano, j52_dtdemo, j52_dtlan

### Relacionamentos

- `j52_codigo` -> `cadastro.ruas` (j14_codigo) [constrescr_codigo_fk]
- `j52_matric` -> `cadastro.iptubase` (j01_matric) [constrescr_matric_fk]

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
