# Estrutura Atual

## Estrutura adotada

```text
MVP/
  agenteV2/
  mcp/
  knowledge/
    manual/
      cadastro/
    rag/
      cadastro/
  catalog/
  rag/
  tools/
  docs/
```

Runtime fica separado de fonte de conhecimento e artefatos gerados.

## Responsabilidades

- `agenteV2/`: pipeline atual do agente e-Cidade.
- `mcp/`: servidor MCP, validacao SQL e acesso read-only ao banco.
- `knowledge/manual/`: Markdown completo editavel por humanos.
- `knowledge/rag/`: snippets curtos consumidos pelo RAG.
- `catalog/`: JSON estruturado consumido pelo MCP/RAG.
- `rag/`: JSONL gerado. Nao editar manualmente.
- `tools/`: scripts de extracao, conversao e build.
- `docs/`: documentacao do MVP.

## Criterio para proximas mudancas

Ao adicionar novo conhecimento:

- regra curta e estruturada entra em `catalog/`;
- explicacao longa, exemplo ou anotacao do consultor entra em `knowledge/manual/`;
- regra operacional curta para IA e gerada em `knowledge/rag/`;
- se editar o manual, rode `python3 tools/run_knowledge_pipeline.py --schema cadastro`;
- se extrair novamente do banco, rode `python3 tools/run_knowledge_pipeline.py --schema cadastro --from-db`;
- valide a pergunta no agente.

Sequencia detalhada: `docs/pipeline-conhecimento.md`.
