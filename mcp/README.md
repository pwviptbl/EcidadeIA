# MCP e-Cidade read-only

Servidor MCP para expor catalogo, metadata e consulta PostgreSQL read-only do e-Cidade.

## Rodar

```bash
cd "/home/dbseller/Modelos/MVP/mcp"
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 server.py
```

Por padrao o transporte e `stdio`, ideal para Claude Desktop, Gemini CLI, Codex e outros agentes locais.

Para teste HTTP interno:

```bash
MCP_TRANSPORT=streamable-http MCP_HOST=127.0.0.1 MCP_PORT=8010 python3 server.py
```

Endpoint:

```text
http://127.0.0.1:8010/mcp
```

Para usar em ChatGPT Web ou Claude Web, esse endpoint precisa ser HTTPS acessivel pelo provedor e protegido por autenticacao/proxy. Nao exponha esse MCP sem autenticacao.

Com ngrok, adicione o host publico no `.env`:

```env
MCP_ALLOWED_HOSTS=127.0.0.1:*,localhost:*,SEU-SUBDOMINIO.ngrok-free.app
MCP_ALLOWED_ORIGINS=http://127.0.0.1:*,http://localhost:*,https://SEU-SUBDOMINIO.ngrok-free.app
```

Se for apenas uma demo local controlada, tambem e possivel desativar a protecao de Host header:

```env
MCP_DISABLE_DNS_REBINDING_PROTECTION=true
```

## Segurança aplicada

- Usa catalogo JSON como allowlist de tabelas.
- Permite somente SQL iniciado por `SELECT` ou `WITH`.
- Bloqueia multiplas statements.
- Bloqueia comandos como `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `COPY`, `DO`, `CALL`, `SET`.
- Exige referencias no formato `schema.tabela`.
- Restringe schemas por `MCP_ALLOWED_SCHEMAS`.
- Aplica `statement_timeout`.
- Executa com `SET TRANSACTION READ ONLY`.
- Forca limite maximo de linhas.
- Grava auditoria em `data/consultas.jsonl`.

## Caminhos configuraveis

O `.env` controla as fontes principais:

```env
MCP_CATALOG_DIR=/home/dbseller/Modelos/MVP/catalog
MCP_KNOWLEDGE_DIR=/home/dbseller/Modelos/MVP/knowledge
MCP_RAG_DOCUMENTS_PATH=/home/dbseller/Modelos/MVP/rag/catalog_documents.jsonl
MCP_DATA_DIR=/home/dbseller/Modelos/MVP/mcp/data
```

`catalog/` e `knowledge/` sao fontes editaveis. `rag/catalog_documents.jsonl` e gerado.

## Ferramentas MCP

- `ecidade_health`
- `ecidade_catalog_index`
- `ecidade_catalog_search`
- RAG do catálogo: gere/atualize `rag/catalog_documents.jsonl` com:
  ```bash
  python3 ../tools/build_rag_documents.py
  ```
- `ecidade_list_schemas`
- `ecidade_list_tables`
- `ecidade_describe_table`
- `ecidade_get_relationships`
- `ecidade_readonly_query`

## Exemplo de configuracao Gemini CLI

```json
{
  "mcpServers": {
    "ecidade": {
      "command": "/home/dbseller/Modelos/MVP/mcp/.venv/bin/python",
      "args": ["/home/dbseller/Modelos/MVP/mcp/server.py"]
    }
  }
}
```

## Exemplo de configuracao Claude Desktop

```json
{
  "mcpServers": {
    "ecidade": {
      "command": "/home/dbseller/Modelos/MVP/mcp/.venv/bin/python",
      "args": ["/home/dbseller/Modelos/MVP/mcp/server.py"]
    }
  }
}
```
