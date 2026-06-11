## cadastro.iptuant



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptuant`



### Resumo tecnico

- Descricao: cadastro para identificar as matricula quando troca oo nunmero nas conversoes de sistemas
- Chave primaria: j40_matric
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j40_matric, j40_refant
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j40_matric` -> `cadastro.iptubase` (j01_matric) [iptuant_matric_fk]

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
