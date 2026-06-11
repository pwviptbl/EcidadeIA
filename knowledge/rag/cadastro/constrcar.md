## cadastro.constrcar



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.constrcar`



### Resumo tecnico

- Descricao: Cadastro das caracteristicas das construcoes escrituradas
- Chave primaria: j53_matric, j53_idcons, j53_caract
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j53_caract, j53_idcons, j53_matric
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j53_matric, j53_matric, j53_idcons, j53_idcons` -> `cadastro.constrescr` (j52_matric, j52_idcons, j52_matric, j52_idcons) [constrcar_matric_idcons_fk]

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
