# Roadmap do AgenteV2

## Fase 0 - Contrato

Status: iniciado.

Entregas:

- pasta `agenteV2`;
- documentacao de arquitetura;
- contratos JSON;
- estrategia de modelo;
- regras sobre fontes de conhecimento.
- guia de estrutura de conhecimento para enriquecimento.

## Fase 0.5 - Curadoria facil de enriquecer

Status: iniciado.

Objetivo: deixar claro onde o consultor deve enriquecer conceitos, tabelas e
relacionamentos.

Entregas:

- guia `docs/estrutura-conhecimento.md`;
- modelos em `knowledge/manual/_modelos`;
- regra explicita: regra de negocio sim, SQL pronto nao.

## Fase 1 - Esqueleto executavel

Status: iniciado.

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

Status: iniciado.

Objetivo: compilar `QueryPlan` validado.

Operacoes iniciais:

- `compare_periods`;
- `count_by_dimension`;
- `sum_by_dimension`;
- `detail_listing`.

Regra: sem SQL pronto hardcoded.

Entregas:

- `SqlCompiler`;
- `run_phase2.py`;
- artefato de SQL auditavel por operacao;
- primeira operacao funcional: `compare_periods`.

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
