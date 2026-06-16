# AgenteV2

Nova linha do agente e-Cidade, separada do `agent/` legado.

O objetivo desta versao e criar um agente que raciocina por etapas antes de gerar
SQL. O fluxo nao pode ser `pergunta -> SQL`. Toda resposta executavel precisa
passar por plano estruturado, validacao e critica.

## Principios

- Regra de negocio vem antes de SQL.
- `knowledge/manual/*` e a fonte humana de conceitos, cuidados e relacionamentos.
- SQL pronto nao deve ser colocado em Markdown, JSON de catalogo ou codigo.
- A LLM deve produzir planos estruturados em JSON, nao texto livre de pensamento.
- Todo plano deve ser validado contra catalogo, RAG e relacionamentos conhecidos.
- O compilador SQL deve operar por operacoes genericas, nao por pergunta pronta.
- Toda resposta com dados deve trazer fonte tecnica recolhivel/auditavel.

## Pipeline Obrigatorio

1. `IntentExtractor`
2. `BusinessResolver`
3. `SchemaPlanner`
4. `PlanValidator`
5. `SqlCompiler`
6. `SqlCritic`
7. `Executor`
8. `RepairLoop`
9. `AnswerSynthesizer`

Detalhes em [docs/arquitetura.md](docs/arquitetura.md).

## Enriquecimento

A V2 usa a mesma raiz `knowledge/manual/*`, mas com contrato mais claro de
preenchimento. O guia pratico esta em
[docs/estrutura-conhecimento.md](docs/estrutura-conhecimento.md).

Modelos editaveis para consultor:

- `knowledge/manual/_modelos/conceito_negocio.md`
- `knowledge/manual/_modelos/receita_relacionamento.md`
- `knowledge/manual/_modelos/tabela_negocio.md`

## Estrutura

```text
agenteV2/
  docs/                         documentacao e contratos do novo agente
  src/agente_v2/contracts/      schemas e objetos de plano
  src/agente_v2/infrastructure/ adaptadores para MCP, catalogo, LLM e storage
  src/agente_v2/prompts/        prompts versionados por etapa
  src/agente_v2/stages/         implementacao das etapas do pipeline
  tests/                        testes unitarios e cenarios de regressao
```

## Modelo

Padrao recomendado para a V2:

- `Gemini 2.5 Flash`: planner, resolver de negocio, critic e resposta final.
- `Gemini Flash Lite`: tarefas simples e baratas, como titulo ou resumo.
- temperatura baixa: `0.0` a `0.2`.
- JSON mode ou structured output sempre que a etapa retornar contrato.

Detalhes em [docs/modelos.md](docs/modelos.md).

## Fase 1

A primeira fase executavel monta plano e para antes de SQL.

```bash
cd /home/dbseller/Modelos/MVP
python3 agenteV2/run_phase1.py "Compare o IPTU 2025 e 2026 e explique os principais fatores de aumento"
```

Detalhes em [docs/fase1.md](docs/fase1.md).

## Fase 2

Compila o plano validado para SQL auditavel.

```bash
cd /home/dbseller/Modelos/MVP
python3 agenteV2/run_phase2.py "Compare o IPTU 2025 e 2026 e explique os principais fatores de aumento"
```

Detalhes em [docs/arquitetura.md](docs/arquitetura.md).
