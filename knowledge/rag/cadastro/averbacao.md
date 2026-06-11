## cadastro.averbacao



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.averbacao`



### Resumo tecnico

- Descricao: tabela principal do grupo de tabelas de averbação (troca de titularidade dos imóveis)
- Chave primaria: j75_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j75_codigo, j75_matric
- Candidatas a coluna de tempo: j75_data, j75_dttipo

### Colunas

| coluna | tipo | papel | metrica | descricao |
| --- | --- | --- | --- | --- |
| j75_codigo | integer |  |  | Codigo sequencial do registro. |
| j75_data | date |  |  | Data da Averbação do imovel |
| j75_dttipo | date |  |  | Data do Tipo de Averbação |
| j75_matric | integer |  |  | Codigo da matrícula do imovel para identificar o proprietário de um determinado lote. |
| j75_obs | text |  |  | Observação referente a averbação |
| j75_regra | integer |  |  | Regra usada para averbar conforme tipo |
| j75_situacao | integer |  |  | Situação da Averbação |
| j75_tipo | integer |  |  | Tipo de averbação |

### Relacionamentos

- `j75_matric` -> `cadastro.iptubase` (j01_matric) [averbacao_matric_fk]
- `j75_tipo` -> `cadastro.averbatipo` (j93_codigo) [averbacao_tipo_fk]

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
