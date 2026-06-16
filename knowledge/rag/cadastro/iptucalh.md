## cadastro.iptucalh



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptucalh`



### Resumo tecnico

- Descricao: Históricos de cálculo e classificação dos lançamentos do IPTU e receitas correlatas.
- Chave primaria: j17_codhis
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- Nenhum relacionamento catalogado.

### Filtros padrao

- Nenhum filtro padrao catalogado.

### Semantica de filtros

- Regra catalogada `historico_iptu_local`:
  - `table: cadastro.iptucalh`
  - `column: j17_descr`
  - `operator: CONTAINS`
  - `value: iptu`
  - Observacao: a descricao do historico deve ser tratada como classificacao local, nao como nome fixo universal.
- Para perguntas de soma de IPTU, a classificacao do historico e obrigatoria; `j01_baixa` nao e filtro necessario se a pergunta nao pedir imoveis ativos.
- Para taxas, isencoes e descontos, usar a descricao do historico para separar o componente correto.

### Regra de negocio para enriquecer

- O que esta tabela representa no negocio?
- Quando ela deve ser preferida sobre outras tabelas parecidas?
- Que perguntas ela responde bem?
- Que filtros de negocio sao seguros?
- O que nao pode ser inferido a partir dela?

### Cuidados / riscos

- Preencher com ambiguidades, excecoes e limites conhecidos.
