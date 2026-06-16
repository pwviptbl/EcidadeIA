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
Compare o valor total de movimentacoes de 2025 e 2026 e explique os principais fatores de variacao
```

Resultado esperado:

- plano completo;
- evidencias de negocio;
- zero SQL gerado nessa fase.

## Fase 1.5 - Normalizacao de contrato e regressao

Status: iniciado.

Objetivo: estabilizar o contrato entre `BusinessResolver`, `SchemaPlanner` e
`SqlCompiler` antes de ampliar executor e UI.

Entregas:

- metricas normalizadas com `table`, `column`, `aggregation`;
- filtros normalizados com `operator/value` ou `rule_code/rule_params`;
- joins normalizados com `source_columns[]` e `target_columns[]`;
- `grain` e `group_by` apontando para colunas reais, nao rotulos humanos;
- cenarios fixos de regressao para perguntas-base.

Regras:

- nao deixar SQL bruto em `condition`;
- nao deixar regra de negocio hardcoded no compilador/critic;
- fixture quebrada bloqueia evolucao do pipeline.

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

Status: iniciado.

Objetivo: revisar e corrigir antes/depois da execucao.

Entregas:

- `SqlCritic`;
- reparo por erro de coluna/tabela/sintaxe;
- limite de tentativas;
- log auditavel.

## Fase 4 - UI e auditoria

Status: planejado.

Objetivo: resposta humana com fonte recolhivel.

Entregas:

- SQL usado;
- tabelas e filtros;
- evidencias do manual;
- limitacoes.

## Fase 5 - Executor

Status: iniciado.

Objetivo: executar SQL read-only aprovada e registrar retorno auditavel.

Entregas:

- `Executor`;
- runner com `ecidade_readonly_query`;
- retorno com `row_count`, `duration_ms` e `rows`;
- erro exposto sem mascarar a SQL executada.

## Fase 6 - AnswerSynthesizer

Status: iniciado.

Objetivo: produzir resposta humana com a SQL recolhida por padrao.

Entregas:

- resposta curta e direta;
- fonte tecnica em bloco recolhivel;
- SQL completa preservada para validacao;
- saida estruturada para UI e debug.
