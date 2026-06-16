# Fase 1 - Plano sem SQL

Esta fase implementa o primeiro ciclo executavel do AgenteV2.

## Escopo

Entrada:

- pergunta em linguagem natural.

Saida:

- `IntentSpec`;
- `BusinessSpec`;
- `SchemaPlan`;
- resultado do `PlanValidator`.

Fora de escopo:

- gerar SQL;
- executar SQL;
- sintetizar resposta com dados reais;
- reparar erro de banco.

## Como executar

```bash
cd /home/dbseller/Modelos/MVP
python3 agenteV2/run_phase1.py "Compare o IPTU 2025 e 2026 e explique os principais fatores de aumento"
```

Para ver o payload completo:

```bash
python3 agenteV2/run_phase1.py --json "Compare o IPTU 2025 e 2026 e explique os principais fatores de aumento"
```

## Dependencias

- MCP ativo em `MCP_SERVER_URL` ou `AGENTEV2_MCP_SERVER_URL`;
- `GEMINI_API_KEY` configurada;
- modelo planner em `AGENTEV2_PLANNER_MODEL`, padrao `gemini-2.5-flash`.

## Garantia da fase

O orquestrador `AgentV2Phase1` nao possui chamada de execucao SQL e nao possui
compilador SQL. O ponto de parada e a validacao do plano.
