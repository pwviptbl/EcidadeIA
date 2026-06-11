## cadastro.zonassetorvalor



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.zonassetorvalor`



### Resumo tecnico

- Descricao: Estrutura criada para armazenar valor por zona e setor
- Chave primaria: j141_anousu, j141_zonas, j141_setor
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j141_sequencial
- Candidatas a coluna de tempo: j141_anousu

### Relacionamentos

- `j141_setor` -> `cadastro.setor` (j30_codi) [zonassetorvalor_setor_fk]
- `j141_zonas` -> `cadastro.zonas` (j50_zona) [zonassetorvalor_zonas_fk]

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
