# Ferramentas de Catalogo e Conhecimento e-Cidade

Esta pasta guarda os scripts que transformam estrutura do banco, catalogo JSON e
manual humano em documentos operacionais para o agente.

## Sequencia curta

Quando mudou somente `knowledge/manual/`:

```bash
cd /home/dbseller/Modelos/MVP
python3 tools/run_knowledge_pipeline.py --schema cadastro
```

Quando mudou a estrutura do banco:

```bash
cd /home/dbseller/Modelos/MVP
python3 tools/run_knowledge_pipeline.py --schema cadastro --from-db
```

Quando quiser mandar material para curadoria no Obsidian:

```bash
cd /home/dbseller/Modelos/MVP
python3 tools/run_knowledge_pipeline.py --schema cadastro --export-obsidian --skip-knowledge-rag --skip-rag-documents
```

Guia completo:

- `docs/pipeline-conhecimento.md`

## Modo conhecimento primeiro

Durante a curadoria, deixe o agente sem SQL livre:

```bash
AGENTE_ALLOW_GENERIC_SQL=false
```

Assim perguntas sem plano deterministico viram diagnostico de conhecimento:
rota, tabelas, evidencias RAG e lacunas para preencher no manual. Use
`AGENTE_ALLOW_GENERIC_SQL=true` apenas quando quiser testar novamente a geracao
livre de SQL.

## Scripts

### `extract_catalog.py`

Gera catalogos JSON para o MCP unindo a estrutura real do banco e o dicionario
de dados do e-Cidade.

A estrutura real vem do banco de producao/snapshot: schemas, tabelas, campos,
PK e FK. Rotulos e descricoes vêm do dicionario:
`configuracoes.db_sysarquivo`, `configuracoes.db_syscampo` e
`configuracoes.db_sysarqcamp`.

```bash
cd /home/dbseller/Modelos/MVP
cp .env.example .env
python3 tools/extract_catalog.py --schema cadastro --output catalog/cadastro_extraido.json
```

Para gerar um arquivo por schema:

```bash
python3 tools/extract_catalog.py --schema all --output-dir catalog
```

### `export_catalog_markdown.py`

Exporta `catalog/*.json` para Markdown de revisao humana/Obsidian.
O formato exportado segue o padrao V2 de tabela de negocio, sem SQL pronto:
identidade, grao, chaves, colunas principais, metricas, dimensoes, filtros,
contagem, agregacao, relacionamentos, riscos e cuidados.

```bash
python3 tools/export_catalog_markdown.py --domain cadastro
```

Saida padrao:

- `docs/exemplos/obsidian/*.catalogo.md`

### `scaffold_business_knowledge.py`

Gera esqueletos de curadoria para o novo modelo de conhecimento de negocio:

```bash
python3 tools/scaffold_business_knowledge.py --domain cadastro
```

Saida padrao:

- `docs/exemplos/obsidian/*.conceitos.md`
- `docs/exemplos/obsidian/*.relacionamentos_negocio.md`

Esses arquivos sao rascunhos para consultor/analista. Depois de validar uma
secao, promova o conteudo para:

- `knowledge/manual/<schema>/conceitos.md`
- `knowledge/manual/<schema>/relacionamentos_negocio.md`

Os esqueletos seguem os modelos em:

- `knowledge/manual/_modelos/conceito_negocio.md`
- `knowledge/manual/_modelos/receita_relacionamento.md`
- `knowledge/manual/_modelos/tabela_negocio.md`

### `build_knowledge_rag.py`

Gera snippets operacionais a partir do manual humano:

```bash
python3 tools/build_knowledge_rag.py
```

Entrada:

- `knowledge/manual/**/*.md`

Saida:

- `knowledge/rag/**/*.md`

Observacao: `knowledge/rag/` e gerado. Edite preferencialmente o manual e gere
de novo.

### `build_rag_documents.py`

Gera os documentos de entrada do RAG a partir dos catalogos e snippets:

```bash
python3 tools/build_rag_documents.py
```

Entrada:

- `catalog/*.json`
- `knowledge/rag/**/*.md`

Saida:

- `rag/catalog_documents.jsonl`

### `validate_knowledge_manual.py`

Valida o padrao humano de conhecimento e impede regressao para SQL pronto:

```bash
python3 tools/validate_knowledge_manual.py --schema cadastro
```

Checagens principais:

- arquivos de tabela em `knowledge/manual/<schema>/` devem iniciar com
  `# Tabela de negocio: schema.tabela`;
- `knowledge/manual/` e `knowledge/rag/` nao podem conter SQL pronto, blocos
  `sql`, secoes legadas de consultas prontas ou `sql_exemplo`.

### `run_knowledge_pipeline.py`

Executa a sequencia padrao para reduzir erro operacional:

```bash
python3 tools/run_knowledge_pipeline.py --schema cadastro
python3 tools/run_knowledge_pipeline.py --schema cadastro --from-db
python3 tools/run_knowledge_pipeline.py --schema cadastro --export-obsidian --skip-knowledge-rag --skip-rag-documents
python3 tools/run_knowledge_pipeline.py --schema cadastro --export-business-scaffold --skip-knowledge-rag --skip-rag-documents
```

Por padrao, o pipeline tambem executa `validate_knowledge_manual.py`. Use
`--skip-validate` apenas para diagnostico temporario.

## Saidas

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

Os rascunhos em `docs/exemplos/obsidian/` tambem nao sao indexados diretamente.
Eles servem para curadoria antes da promocao para `knowledge/manual/`.

Depois da extracao automatica, os analistas podem enriquecer o mesmo JSON com:

- `intents`
- `metrics`
- `templates`
- `entity_key`
- `time_key`
- `foreign_keys`
- `blocked_columns`
