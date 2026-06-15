# Fontes de Conhecimento

## Fonte humana

Editar e enriquecer:

- `knowledge/manual/<schema>/conceitos.md`;
- `knowledge/manual/<schema>/relacionamentos_negocio.md`;
- `knowledge/manual/<schema>/<tabela>.md`.

Esses arquivos devem conter:

- conceitos de negocio;
- filtros de negocio;
- cuidados e riscos;
- regras de contagem;
- caminhos entre entidades que FK nao explica;
- significado de metricas.

Nao devem conter:

- SQL pronto;
- relatorio pronto;
- resposta final pronta.

## Fonte gerada

Nao editar manualmente:

- `knowledge/rag/*`;
- `rag/catalog_documents.jsonl`.

Esses artefatos devem ser reconstruidos a partir de `knowledge/manual/*`.

## Catalogo estruturado

Usar para metadado tecnico e validavel:

- `catalog/*.json`.

Entram aqui:

- tabelas;
- colunas;
- chaves;
- tipos;
- chaves de negocio;
- grao;
- classificacoes estruturadas;
- metricas estruturadas quando forem atomicas.

Nao entram aqui:

- SQL pronto;
- texto longo de explicacao humana;
- exemplos que virem atalho de query.
