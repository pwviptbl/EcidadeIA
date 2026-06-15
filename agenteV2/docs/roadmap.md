# Roadmap do AgenteV2

## Fase 0 - Contrato

Status: iniciado.

Entregas:

- pasta `agenteV2`;
- documentacao de arquitetura;
- contratos JSON;
- estrategia de modelo;
- regras sobre fontes de conhecimento.

## Fase 1 - Esqueleto executavel

Objetivo: rodar o pipeline inteiro sem executar SQL.

Entregas:

- `IntentExtractor`;
- `BusinessResolver`;
- `SchemaPlanner`;
- `PlanValidator`;
- resposta de debug mostrando plano e bloqueios.

Pergunta alvo:

```text
Compare o IPTU 2025 e 2026 e explique os principais fatores de aumento
```

Resultado esperado:

- plano completo;
- evidencias de negocio;
- zero SQL gerado nessa fase.

## Fase 2 - Compilador generico

Objetivo: compilar `QueryPlan` validado.

Operacoes iniciais:

- `compare_periods`;
- `count_by_dimension`;
- `sum_by_dimension`;
- `detail_listing`.

Regra: sem SQL pronto hardcoded.

## Fase 3 - Critic e RepairLoop

Objetivo: revisar e corrigir antes/depois da execucao.

Entregas:

- `SqlCritic`;
- reparo por erro de coluna/tabela/sintaxe;
- limite de tentativas;
- log auditavel.

## Fase 4 - UI e auditoria

Objetivo: resposta humana com fonte recolhivel.

Entregas:

- SQL usado;
- tabelas e filtros;
- evidencias do manual;
- limitacoes.
