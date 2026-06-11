## cadastro.averbatipo



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.averbatipo`



### Resumo tecnico

- Descricao: tipos de averbação
- Chave primaria: j93_codigo
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j93_codigo
- Candidatas a coluna de tempo: j93_datalimite

### Colunas

| coluna | tipo | papel | metrica | descricao |
| --- | --- | --- | --- | --- |
| j93_averbagrupo | integer |  |  | Grupo |
| j93_codigo | integer |  |  | Código sequencial do registro |
| j93_datalimite | date |  |  | Data limite |
| j93_descr | character varying |  |  | Descrição do tipo de averbação |
| j93_regra | integer |  |  | Regra do tipo de averbação 1- Proprietarios 2-Promitentes |

### Relacionamentos

- `j93_averbagrupo` -> `cadastro.averbagrupo` (j105_sequencial) [avertbatipo_averbagrupo_fk]

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
