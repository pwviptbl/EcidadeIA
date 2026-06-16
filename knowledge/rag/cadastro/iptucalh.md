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

- `j17_descr` e uma classificacao local do historico, nao um nome fixo universal.
- Pode representar IPTU, taxa de lixo, isencao, desconto ou outro componente tributario conforme o municipio.
- Para IPTU puro, usar a classificacao local equivalente a IPTU; quando nao houver codificacao valida, a descricao contendo IPTU e a regra padrao.
- Para perguntas de soma de IPTU, o historico e obrigatorio; `j01_baixa` nao entra se a pergunta nao pedir imoveis ativos.

### Regra de negocio para enriquecer

- O que esta tabela representa no negocio?
- Quando ela deve ser preferida sobre outras tabelas parecidas?
- Que perguntas ela responde bem?
- Que filtros de negocio sao seguros?
- O que nao pode ser inferido a partir dela?

### Cuidados / riscos

- `j17_descr` pode variar entre municipios e ate entre configuracoes do mesmo ambiente.
- `j01_baixa` nao e um filtro necessario para valor calculado, salvo quando a pergunta pedir ativos.
