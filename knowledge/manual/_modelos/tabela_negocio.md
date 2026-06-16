# Modelo - Tabela de negocio

Use este modelo para enriquecer `knowledge/manual/<schema>/<tabela>.md`.
Arquivos dentro de `_modelos` nao devem entrar no RAG.

## Tabela: `schema.tabela`

- Nome humano:
- O que representa:
- Quando usar:
  -
- Quando evitar:
  -
- Grao:
- Entidade principal:
- Chave de negocio:
  -
- Coluna temporal:
- Metricas atomicas:
  - nome: coluna, agregacao recomendada, significado
- Dimensoes:
  - nome: coluna/tabela, significado
- Filtros de negocio:
  -
- Relacionamentos importantes:
  -
- Regra de contagem:
- Regra de agregacao:
- Riscos de duplicidade:
  -
- O que nao inferir:
  -
- Cuidados:
  -

## Como preencher

- O foco e ensinar uso correto da tabela.
- Nao escrever SQL pronto.
- Preferir colunas atomicas e significado de negocio.
- Se uma coluna for codigo/classificacao, indicar a tabela de descricao.
- Se a tabela for fato financeiro, deixar claro se representa calculado, pago,
  cancelado, isento ou outro estado.
