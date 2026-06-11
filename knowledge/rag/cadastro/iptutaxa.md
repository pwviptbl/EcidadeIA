## cadastro.iptutaxa



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptutaxa`



### Resumo tecnico

- Descricao: Esta tabela contem as taxas que serao cobradas juntamente com o iptu
- Chave primaria: j19_anousu, j19_receit
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j19_receit, j19_valor
- Candidatas a coluna de tempo: j19_anousu

### Relacionamentos

- `j19_receit` -> `caixa.tabrec` (k02_codigo) [iptutaxa_receit_fk]

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
