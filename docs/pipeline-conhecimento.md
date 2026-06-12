# Pipeline de conhecimento

Este documento define a sequencia para transformar estrutura do banco e manuais humanos em conhecimento operacional usado pelo agente.

## Camadas

### 1. Banco e dicionario

Fonte tecnica inicial:

- banco real ou snapshot do cliente;
- `information_schema` para schemas, tabelas, colunas, PK e FK;
- dicionario e-Cidade em `configuracoes.db_sysarquivo`, `configuracoes.db_syscampo` e `configuracoes.db_sysarqcamp`.

Script:

```bash
cd /home/dbseller/Modelos/MVP
python3 tools/extract_catalog.py --schema cadastro --output catalog/cadastro_extraido.json
```

Saida:

- `catalog/cadastro_extraido.json`

Esse arquivo e fonte estruturada para o MCP. Ele deve conter relacionamento, colunas, chaves, descricoes tecnicas e metadados pequenos.

### 2. Manual humano

Fonte editavel por analista, consultor ou desenvolvedor:

- `knowledge/manual/ecidade.md`
- `knowledge/manual/<schema>.md`
- `knowledge/manual/<schema>/<tabela>.md`

Uso:

- explicar regra de negocio;
- registrar observacoes do consultor;
- guardar exemplos SQL maiores;
- documentar quando usar ou nao usar uma tabela;
- documentar cuidados e limites.

O manual completo nao deve ser enviado inteiro para o RAG. Ele e a base humana.

### 3. Conhecimento operacional

Fonte curta para IA:

- `knowledge/rag/<schema>.md`
- `knowledge/rag/<schema>/<tabela>.md`

Script:

```bash
cd /home/dbseller/Modelos/MVP
python3 tools/build_knowledge_rag.py
```

Saida:

- arquivos Markdown curtos em `knowledge/rag/`

Esses arquivos sao gerados a partir de `knowledge/manual/`. Nao edite `knowledge/rag/` como fonte principal; ajuste o manual e gere novamente.

### 4. JSONL de busca

Artefato final consumido pelo MCP/RAG:

- `rag/catalog_documents.jsonl`

Script:

```bash
cd /home/dbseller/Modelos/MVP
python3 tools/build_rag_documents.py
```

Entrada:

- `catalog/*.json`
- `knowledge/rag/**/*.md`

Saida:

- `rag/catalog_documents.jsonl`

Nao edite esse arquivo manualmente.

## Sequencia recomendada

### Quando mudou somente o manual

```bash
cd /home/dbseller/Modelos/MVP
python3 tools/run_knowledge_pipeline.py --schema cadastro
```

Equivale a:

```bash
python3 tools/build_knowledge_rag.py
python3 tools/build_rag_documents.py
```

### Quando mudou a estrutura do banco

```bash
cd /home/dbseller/Modelos/MVP
python3 tools/run_knowledge_pipeline.py --schema cadastro --from-db
```

Equivale a:

```bash
python3 tools/extract_catalog.py --schema cadastro --output catalog/cadastro_extraido.json
python3 tools/build_knowledge_rag.py
python3 tools/build_rag_documents.py
```

### Quando quiser gerar Markdown para revisao no Obsidian

```bash
cd /home/dbseller/Modelos/MVP
python3 tools/run_knowledge_pipeline.py --schema cadastro --export-obsidian --skip-knowledge-rag --skip-rag-documents
```

Saida:

- `docs/exemplos/obsidian/cadastro_extraido.catalogo.md` ou arquivo equivalente ao nome do JSON.

## Como repetir para outros schemas

Para outro schema:

```bash
python3 tools/run_knowledge_pipeline.py --schema arrecadacao --from-db
```

Depois crie ou edite:

```text
knowledge/manual/arrecadacao.md
knowledge/manual/arrecadacao/<tabela>.md
```

E gere novamente:

```bash
python3 tools/run_knowledge_pipeline.py --schema arrecadacao
```

Para todos os schemas:

```bash
python3 tools/run_knowledge_pipeline.py --schema all --from-db
```

Use `all` com cuidado, porque pode gerar muito catalogo e muito documento RAG.

## Regra de responsabilidade

- `catalog/`: fato estruturado, pequeno, usado pelo MCP e guardrails.
- `knowledge/manual/`: manual completo e explicacao humana.
- `knowledge/rag/`: recorte operacional gerado para IA.
- `rag/`: indice JSONL gerado para busca.
- `docs/`: documentacao do projeto e processo.

## Arquivos gerados

Arquivos gerados por script:

- `catalog/*_extraido.json`
- `docs/exemplos/obsidian/*.catalogo.md`
- `knowledge/rag/**/*.md`
- `rag/catalog_documents.jsonl`

Arquivos fonte para edicao humana:

- `knowledge/manual/**/*.md`
- `catalog/*.json`, quando for enriquecimento estruturado intencional
- `docs/**/*.md`

## Validacao depois do build

Depois de rodar o pipeline:

1. reinicie o MCP se ele estiver carregando catalogo/RAG em memoria;
2. reinicie o agente se alterou configuracao ou codigo;
3. teste uma pergunta simples de selecao de tabela;
4. teste uma pergunta que exige relacionamento;
5. confira no log se aparecem `route.llm_selection`, `context.done`, `sql.plan` e `execute.done`.
