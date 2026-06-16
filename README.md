# MVP Agente e-Cidade

Este repositorio junta runtime, conhecimento e ferramentas do MVP:

- `agenteV2/`: linha atual do agente e-Cidade, com pipeline catalogo + RAG + LLM.
- `mcp/`: servidor MCP read-only para expor catalogo, RAG, metadata e consultas SQL seguras no banco e-Cidade.
- `knowledge/manual/`: manual humano completo em Markdown.
- `knowledge/rag/`: snippets operacionais derivados do manual para indexacao.
- `catalog/`: catalogo estruturado em JSON.
- `rag/`: artefatos gerados para busca.
- `tools/`: utilitarios para extrair, converter e regenerar catalogos/RAG.

## Fonte de conhecimento

Use esta separacao:

- `catalog/`: catalogo estruturado em JSON. Bom para schema, chaves, grao, colunas, regras curtas e consultas validadas.
- `knowledge/manual/`: manual humano completo. Bom para regras de negocio, cuidados, exemplos SQL, contexto legado e explicacoes maiores.
- `knowledge/rag/`: versao curta e operacional do manual. Esta camada entra no RAG.
- `rag/catalog_documents.jsonl`: artefato gerado. Nao editar manualmente.

Quando alterar `knowledge/manual/`, gere os snippets:

```bash
python3 tools/build_knowledge_rag.py
```

Quando alterar `catalog/` ou `knowledge/rag/`, regenere o RAG:

```bash
python3 tools/build_rag_documents.py
```

## Fluxo rapido

1. O agente recebe a pergunta.
2. O agente chama `ecidade_catalog_search`.
3. O MCP busca candidatos no catalogo estruturado e no RAG.
4. O agente monta contexto com tabelas, regras, markdowns e relacionamentos.
5. Quando existir plano deterministico, ele usa esse plano sem depender da LLM para SQL.
6. Caso contrario, a LLM gera SQL read-only.
7. O MCP valida e executa a consulta.
8. A LLM apenas explica o resultado retornado.

## Documentacao

- [Arquitetura](docs/arquitetura.md)
- [Fluxo do agente](docs/fluxo-agente.md)
- [Guia de catalogo](docs/guia-catalogo.md)
- [Estrutura proposta](docs/estrutura-proposta.md)


cd /home/dbseller/Modelos/MVP/mcp
  MCP_TRANSPORT=streamable-http MCP_HOST=127.0.0.1 MCP_PORT=8010 .venv/bin/python server.py

  Em outro terminal:

  cd /home/dbseller/Modelos/MVP/agenteV2
  python3 run_phase6.py "sua pergunta"

  Antes de testar, se alterou knowledge/ ou catalog/, regenere:

  cd /home/dbseller/Modelos/MVP
   python3 tools/build_knowledge_rag.py
  python3 tools/build_rag_documents.py

# EcidadeIA
