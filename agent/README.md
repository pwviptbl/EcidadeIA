# Agent - MVP

Chat web simples para demonstrar um agente externo consultando o e-Cidade por uma API read-only.

## Rodar

```bash
cd "/home/dbseller/Modelos/MVP/agent"
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 app.py

```

Abra:

```text
http://127.0.0.1:5055
```

## Configuracao

Variaveis obrigatorias para o modo agente real:

```env
AGENTE_LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://172.19.1.230:11434
AGENTE_LLM_MODEL=qwen2.5-coder:14b
AGENTE_PLANNER_LLM_MODEL=qwen2.5-coder:14b
AGENTE_ANSWER_LLM_MODEL=qwen2.5-coder:14b
OLLAMA_TIMEOUT=900
OLLAMA_NUM_CTX=8192
MCP_SERVER_URL=http://127.0.0.1:8010/mcp
AGENTE_CATALOG_DIR=/home/dbseller/Modelos/MVP/catalog
```

Variaveis opcionais:

```env
AGENTE_HOST=127.0.0.1
AGENTE_PORT=5055
```

## Escopo do MVP

- Chat responsivo com historico local.
- Catalogo de dominios do e-Cidade em JSON.
- Agente orientado por IA:
  - recebe pergunta e historico;
  - IA identifica assunto e tabelas candidatas;
  - app busca catalogo/metadados/relacionamentos no e-Cidade;
  - IA monta SQL read-only;
  - e-Cidade executa;
  - IA valida o retorno e tenta corrigir ate 5 vezes;
  - IA gera a mensagem final.
- Consulta read-only na API do e-Cidade.
- Resposta com criterio, ressalvas e SQL usado.

O MCP fica reservado para evolucao posterior como adaptador sobre a API do e-Cidade.

## Documentacao relacionada

Na raiz do MVP:

- `docs/arquitetura.md`
- `docs/fluxo-agente.md`
- `docs/guia-catalogo.md`
- `docs/estrutura-proposta.md`
