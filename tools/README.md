# Extrator de Catalogos e-Cidade

Gera catalogos JSON para o MCP unindo a estrutura real do banco e o dicionario de dados do e-Cidade.

A estrutura real vem do banco de producao/snapshot: schemas, tabelas, campos, PK e FK.
Rotulos e descricoes vêm do dicionario: `configuracoes.db_sysarquivo`,
`configuracoes.db_syscampo` e `configuracoes.db_sysarqcamp`.

## Uso

```bash
cd /home/dbseller/Modelos/MVP/tools
cp .env.example .env
python3 extract_catalog.py --schema cadastro --output ../catalog/cadastro_extraido.json
```

Para gerar um arquivo por schema:

```bash
python3 extract_catalog.py --schema all --output-dir ../catalog
```

Para gerar os snippets operacionais a partir do manual humano:

```bash
python3 build_knowledge_rag.py
```

Para gerar os documentos de entrada do RAG a partir dos catalogos e snippets:

```bash
python3 build_rag_documents.py
```

## Saida

O JSON gerado segue o formato aceito pelo MCP:

- `domain`, `label`, `description`, `primary_schema`
- `tables`
- `tables.<schema.tabela>.columns`
- `primary_key`
- `foreign_keys`
- metadados minimos de coluna: `description` e `type`

O JSONL do RAG gera documentos a partir do catalogo estruturado e de
`knowledge/rag/`. O manual completo em `knowledge/manual/` nao e indexado
diretamente.

Depois da extracao automatica, os analistas podem enriquecer o mesmo JSON com:

- `intents`
- `metrics`
- `templates`
- `entity_key`
- `time_key`
- `foreign_keys`
- `blocked_columns`
