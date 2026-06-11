## cadastro.promitente



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.promitente`



### Resumo tecnico

- Descricao: Cadastro dos promitente compradores. Identificacao dos contribuintes que compram imoveis financiados e so averbam em seu nome apos o termino do pagamento.
- Chave primaria: j41_matric, j41_numcgm
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j41_matric, j41_numcgm
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j41_matric` -> `cadastro.iptubase` (j01_matric) [promitente_matric_fk]
- `j41_numcgm` -> `protocolo.cgm` (z01_numcgm) [promitente_numcgm_fk]

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
