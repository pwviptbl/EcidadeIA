# Arquitetura

## Componentes

### MCP

Diretorio: `mcp/`

Responsabilidades:

- manter allowlist de schemas/tabelas;
- expor ferramentas MCP;
- carregar catalogo estruturado;
- carregar documentos RAG gerados;
- validar SQL read-only;
- executar consulta no PostgreSQL com limite e timeout;
- registrar auditoria em `mcp/data/consultas.jsonl`.

### Agente

Diretorio: `agent/`

Responsabilidades:

- receber a pergunta pelo chat;
- chamar ferramentas MCP;
- selecionar rota/tabelas;
- montar contexto para SQL;
- preferir planos deterministicos quando existirem;
- usar LLM para gerar SQL apenas quando nao houver regra deterministica;
- explicar o resultado sem inventar dado.

### Conhecimento

Diretorios:

- `catalog/`: JSON estruturado.
- `knowledge/manual/`: Markdown editavel para humano.
- `knowledge/rag/`: Markdown operacional indexado no RAG.
- `rag/`: JSONL gerado para busca.

## Configuracao central

O MCP le estes caminhos por variavel de ambiente:

```env
MCP_CATALOG_DIR=/home/dbseller/Modelos/MVP/catalog
MCP_KNOWLEDGE_DIR=/home/dbseller/Modelos/MVP/knowledge
MCP_RAG_DOCUMENTS_PATH=/home/dbseller/Modelos/MVP/rag/catalog_documents.jsonl
MCP_DATA_DIR=/home/dbseller/Modelos/MVP/mcp/data
```

O agente pode apontar para o mesmo catalogo com:

```env
AGENTE_CATALOG_DIR=/home/dbseller/Modelos/MVP/catalog
```

## Regra pratica

Nao misturar runtime com fonte de conhecimento:

- regra estruturada entra em `catalog/`;
- manual completo entra em `knowledge/manual/`;
- regra operacional para IA entra em `knowledge/rag/`;
- documento RAG e gerado;
- logs e auditoria ficam em `mcp/data/`;
- resposta final deve depender do SQL executado, nao do texto do catalogo.
